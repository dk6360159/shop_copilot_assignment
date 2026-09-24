from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database.session import get_db
from app.modules.transactions.schemas import TransactionResponse
from app.modules.transactions.repository import TransactionRepository
from app.modules.transactions.service import TransactionService

router = APIRouter(tags=["audit"])

def get_transaction_service(db: AsyncSession = Depends(get_db)) -> TransactionService:
    repo = TransactionRepository(db)
    return TransactionService(repo)

@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: str,
    service: TransactionService = Depends(get_transaction_service)
):
    result = await service.get_transaction(transaction_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return result

