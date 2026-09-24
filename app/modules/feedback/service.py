from app.modules.transactions.repository import TransactionRepository
from app.rl.bandit import bandit

class FeedbackService:
    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    async def record_feedback(self, transaction_id: str, score: int) -> dict:
        tx = await self.repository.get_by_id(transaction_id)
        if tx is None:
            raise ValueError("Transaction not found")

        latency_seconds = tx.latency_ms / 1000.0
        reward = (score * 10) - latency_seconds

        state = tx.defect_category or "no_image"
        
        config = tx.configuration_json
        action = config["rag_top_k"]
        bandit.update(state, action, reward)

        updated = await self.repository.update_feedback(transaction_id, score, reward)
        return {
            "transaction_id": transaction_id,
            "score": score,
            "reward": reward,
            "updated": updated,
        }

