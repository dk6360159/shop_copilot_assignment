from pydantic import BaseModel, Field

class FeedbackRequest(BaseModel):
    transaction_id: str
    score: int = Field(ge=0, le=1)

class FeedbackResponse(BaseModel):
    transaction_id: str
    score: int
    reward: float
    updated: bool

