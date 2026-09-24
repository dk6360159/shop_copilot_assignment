from app.modules.transactions.repository import TransactionRepository
from app.modules.transactions.models import Transaction

class TransactionService:
    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    async def get_transaction(self, transaction_id: str) -> Transaction | None:
        return await self.repository.get_by_id(transaction_id)

    async def save_transaction(self, transaction_data: dict) -> Transaction:
        return await self.repository.create(transaction_data)

