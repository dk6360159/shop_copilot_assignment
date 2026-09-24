import time
import uuid

from app.agent.agent import ShopFloorAgent
from datetime import datetime, timezone

def build_audit_record(
    transaction_id: str,
    query: str,
    work_order_id: str | None,
    image_name: str | None,
    defect_category: str | None,
    ocr_text: str | None,
    configuration: dict,
    decision_trace: list,
    final_answer: str,
    latency_ms: float,
    proposed_action: dict | None,
) -> dict:
    return {
        "id": transaction_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "query": query,
        "work_order_id": work_order_id,
        "image_path": image_name,
        "defect_category": defect_category,
        "ocr_text": ocr_text,
        "configuration": configuration,
        "decision_trace": decision_trace,
        "final_answer": final_answer,
        "latency_ms": latency_ms,
        "proposed_action": proposed_action,
        "feedback_score": None,
        "reward": None,
    }
from app.core.config import get_settings
from app.rag.retriever import Retriever
from app.rag.generator import LocalLLM
from app.rl.bandit import bandit
from app.cv.classifier import DefectClassifier
from app.cv.ocr import OCRService
from app.modules.transactions.service import TransactionService

settings = get_settings()

class InspectionService:
    def __init__(self, transaction_service: TransactionService) -> None:
        self.classifier = DefectClassifier()
        self.ocr = OCRService()
        self.retriever = Retriever()
        self.llm = LocalLLM()
        self.agent = ShopFloorAgent(
            classifier=self.classifier,
            ocr=self.ocr,
            retriever=self.retriever,
            llm=self.llm,
        )
        self.transaction_service = transaction_service

    async def inspect(
        self,
        query: str,
        work_order_id: str | None,
        image_bytes: bytes | None,
        image_name: str | None,
    ) -> dict:
        started = time.perf_counter()
        transaction_id = str(uuid.uuid4())

        state = "no_image" if image_bytes is None else "unknown"
        rag_top_k = bandit.choose(state)

        result = self.agent.run(
            query=query,
            work_order_id=work_order_id,
            image_bytes=image_bytes,
            rag_top_k=rag_top_k,
        )

        if image_bytes is not None:
            state = result["defect_category"] or "no_defect"
            result["state"] = state

        latency_ms = round((time.perf_counter() - started) * 1000, 2)
        configuration = {
            "rag_top_k": rag_top_k,
            "llm_model": settings.ollama_model,
            "fallback_used": result["fallback_used"],
        }

        record = build_audit_record(
            transaction_id=transaction_id,
            query=query,
            work_order_id=work_order_id,
            image_name=image_name,
            defect_category=result["defect_category"],
            ocr_text=result["ocr_text"],
            configuration=configuration,
            decision_trace=result["trace"],
            final_answer=result["answer"],
            latency_ms=latency_ms,
            proposed_action=result["proposed_action"],
        )
        
        # Now async save
        await self.transaction_service.save_transaction(record)

        return {
            "transaction_id": transaction_id,
            "answer": result["answer"],
            "defect_category": result["defect_category"],
            "ocr_text": result["ocr_text"],
            "configuration": configuration,
            "decision_trace": result["trace"],
            "latency_ms": latency_ms,
            "proposed_action": result["proposed_action"],
        }
