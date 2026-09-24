from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database.session import get_db
from app.modules.feedback.schemas import FeedbackRequest, FeedbackResponse
from app.modules.feedback.service import FeedbackService
from app.modules.transactions.repository import TransactionRepository

router = APIRouter(tags=["feedback"])

def get_feedback_service(db: AsyncSession = Depends(get_db)) -> FeedbackService:
    repo = TransactionRepository(db)
    return FeedbackService(repo)

@router.post("/feedback", response_model=FeedbackResponse)
async def feedback(
    request: FeedbackRequest,
    service: FeedbackService = Depends(get_feedback_service)
):
    try:
        return await service.record_feedback(request.transaction_id, request.score)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

