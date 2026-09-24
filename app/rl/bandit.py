import json
import random
from pathlib import Path
from app.core.config import get_settings

settings=get_settings()

class EpsilonGreedyBandit:
    """
    Contextual bandit:
      state  = defect category / no_image
      action = RAG top-K
      reward = feedback*10 - latency_seconds
    """

    ACTIONS = (2, 3, 5)

    def __init__(self) -> None:
        self.path = Path("data/bandit_state.json")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.values = self._load()

    def _load(self) -> dict:
        if not self.path.exists():
            return {}
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _ensure(self, state: str) -> None:
        self.values.setdefault(
            state,
            {str(action): {"value": 0.0, "count": 0} for action in self.ACTIONS},
        )

    def choose(self, state: str) -> int:
        self._ensure(state) 
        if random.random() < settings.epsilon:
            return random.choice(self.ACTIONS)

        state_values = self.values[state]
        return max(
            self.ACTIONS,
            key=lambda action: state_values[str(action)]["value"],
        )

    def update(self, state: str, action: int, reward: float) -> None:
        self._ensure(state)
        item = self.values[state][str(action)]
        count = item["count"] + 1
        old_value = item["value"]
        item["count"] = count
        item["value"] = old_value + (reward - old_value) / count
        self.path.write_text(
            json.dumps(self.values, indent=2),
            encoding="utf-8",
        )

    def snapshot(self) -> dict:
        return self.values

bandit = EpsilonGreedyBandit()
