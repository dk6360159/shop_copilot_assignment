from app.agent.tools import WorkOrderTool

class ShopFloorAgent:
    """
    ReAct-style operational loop.

    The planner is intentionally lightweight for a 4–5 hour assignment:
    tool selection is explicit and deterministic for safety-critical inputs,
    while Ollama is used for grounded natural-language generation.
    """

    def __init__(self, classifier, ocr, retriever, llm):
        self.classifier = classifier
        self.ocr = ocr
        self.retriever = retriever
        self.llm = llm
        self.work_order = WorkOrderTool()

    def run(self, query, work_order_id, image_bytes, rag_top_k):
        trace = []
        defect = None
        ocr_text = None

        step = 1

        if image_bytes is not None:
            defect = self.classifier.classify(image_bytes)
            trace.append({
                "step": step,
                "tool": "cv_inspection",
                "reason": "An image was supplied, so the visual defect state must be established.",
                "result": defect,
            })
            step += 1

            ocr_text = self.ocr.extract(image_bytes)
            trace.append({
                "step": step,
                "tool": "ocr",
                "reason": "The image may contain a stamped work-order or part identifier.",
                "result": ocr_text or "No text extracted",
            })
            step += 1

        query_for_retrieval = f"{query} defect={defect or 'no_image'} OcrTextOnImage={ocr_text or "No Image" }"
        context = self.retriever.search(query_for_retrieval, rag_top_k)

        trace.append({
            "step": step,
            "tool": "rag_search",
            "reason": "The query requires SOP, tolerance, rework, or escalation evidence.",
            "result": f"Retrieved {len(context)} chunks",
        })
        step += 1

        if work_order_id and (
            "work order" in query.lower()
            or "status" in query.lower()
            or "order" in query.lower()
        ):
            status = self.work_order.check(work_order_id)
            trace.append({
                "step": step,
                "tool": "check_work_order_status",
                "reason": "The query explicitly requires work-order information.",
                "result": status,
            })
            step += 1

        answer, fallback_used, llm_seconds = self.llm.generate(query, context)
        trace.append({
            "step": step,
            "tool": "local_llm",
            "reason": "Generate a concise answer grounded in retrieved SOP evidence.",
            "result": "fallback_template" if fallback_used else "ollama",
        })

        proposed_action = None
        q = query.lower()
        if defect in {"crack", "dimensional_deviation"} or "scrap" in q or "escalate" in q:
            proposed_action = {
                "type": "human_review",
                "description": "Potentially irreversible quality action requires human approval.",
                "requires_human_approval": True,
            }

        return {
            "answer": answer,
            "defect_category": defect,
            "ocr_text": ocr_text,
            "trace": trace,
            "fallback_used": fallback_used,
            "proposed_action": proposed_action,
        }
