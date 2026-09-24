from typing import Any
from pydantic import BaseModel, ConfigDict

class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    timestamp: str
    query: str
    work_order_id: str | None
    image_path: str | None
    defect_category: str | None
    ocr_text: str | None
    configuration: dict[str, Any]
    decision_trace: list[dict[str, Any]]
    final_answer: str
    latency_ms: float
    proposed_action: dict[str, Any] | None
    feedback_score: int | None
    reward: float | None

