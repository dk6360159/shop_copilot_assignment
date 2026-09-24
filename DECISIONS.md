# FDE Decision Rationale

## 1. Why vector RAG?

The SOP corpus contains rules that should be retrieved selectively as the knowledge base grows. A small vector index lets the system retrieve only the evidence relevant to a particular defect or question and keeps the generation prompt focused. If the plant had a fixed 20-page SOP that rarely changed, a simpler long-context or deterministic document lookup approach could be reasonable because the operational complexity of a vector index may not be justified.

## 2. Why an agent loop?

The request can require different tools depending on whether an image, work order, defect, or SOP question is present, so a fixed pipeline would perform unnecessary work on some requests. A lightweight ReAct-style loop makes the selected tool path explicit and auditable. I would not make the final safety/governance decision agentic: irreversible actions such as scrap or external escalation should remain deterministic proposed actions followed by human approval.

## 3. Why classical CV?

The assignment is time-boxed and explicitly allows classical OpenCV. For synthetic demonstration images, preprocessing, edges, contours, and line detection provide a reproducible implementation without a training pipeline. I would move to a pretrained detector when defect appearance becomes more varied and robust localization is needed. I would fine-tune a custom model only after collecting representative, labeled plant images and establishing that domain-specific accuracy justifies the labeling and maintenance cost.

## 4. Scaling from one plant to ten

I would apply model tiering first: route simple questions and low-risk cases to a smaller local model while reserving a larger model for complex SOP reasoning. This directly reduces inference cost and latency without requiring a large data-collection or retraining program. Caching can then be added for repeated SOP queries.

## 5. Shop-floor governance risk

A key risk is that a visually ambiguous defect could lead a worker to treat an AI recommendation as an authoritative quality disposition. The current pilot mitigates this by recording an audit trail and requiring human approval for irreversible outcomes, but a real deployment should add calibrated confidence thresholds, mandatory quality sign-off for defined defect classes, and periodic review against labeled inspection outcomes.
