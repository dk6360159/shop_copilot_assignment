from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from app.modules.transactions.models import Transaction

class TransactionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, transaction_id: str) -> Transaction | None:
        result = await self.session.execute(select(Transaction).where(Transaction.id == transaction_id))
        return result.scalars().first()

    async def create(self, transaction_data: dict) -> Transaction:
        data = transaction_data.copy()
        if "configuration" in data:
            data["configuration_json"] = data.pop("configuration")
        if "decision_trace" in data:
            data["decision_trace_json"] = data.pop("decision_trace")
        if "proposed_action" in data:
            data["proposed_action_json"] = data.pop("proposed_action")

        transaction = Transaction(**data)
        self.session.add(transaction)
        await self.session.commit()
        await self.session.refresh(transaction)
        return transaction

    async def update_feedback(self, transaction_id: str, score: int, reward: float) -> bool:
        stmt = (
            update(Transaction)
            .where(Transaction.id == transaction_id)
            .values(feedback_score=score, reward=reward)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount == 1

