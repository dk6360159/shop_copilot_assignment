from typing import Any
from pydantic import BaseModel, Field

class Configuration(BaseModel):
    rag_top_k: int = Field(ge=1)
    llm_model: str
    fallback_used: bool = False

class TraceStep(BaseModel):
    step: int
    tool: str
    reason: str
    result: Any

class ProposedAction(BaseModel):
    type: str
    description: str
    requires_human_approval: bool = True

class InspectResponse(BaseModel):
    transaction_id: str
    answer: str
    defect_category: str | None = None
    ocr_text: str | None = None
    configuration: Configuration
    decision_trace: list[TraceStep]
    latency_ms: float
    proposed_action: ProposedAction | None = None

