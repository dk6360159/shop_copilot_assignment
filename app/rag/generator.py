import time
import os
import google.generativeai as genai
from app.core.config import get_settings

settings = get_settings()

class LocalLLM:
    def __init__(self) -> None:
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-3.8-flash')

    def generate(self, query: str, context: list[dict]) -> tuple[str, bool, float]:
        prompt = self._prompt(query, context)
        started = time.perf_counter()

        try:
            response = self.model.generate_content(prompt)
            answer = response.text.strip()
            elapsed = time.perf_counter() - started

            if answer and elapsed <= settings.llm_latency_ceiling_seconds:
                return answer, False, elapsed

            # Governance requirement:.
            return self._fallback(query, context), True, elapsed
        except Exception as e:
            print(f"LLM Exception: {e}")
            
            elapsed = time.perf_counter() - started
            return self._fallback(query, context), True, elapsed

    @staticmethod
    def _prompt(query: str, context: list[dict]) -> str:
        evidence = "\n\n".join(
            f"[{d['source']}] {d['text']}" for d in context
        )
        return f"""
You are ShopFloor Copilot, a manufacturing SOP assistant.
Answer ONLY from the supplied evidence. If evidence is insufficient,
say that a human review is required. Do not invent measurements,
contacts, or procedures.

Question:
{query}

Evidence:
{evidence}

Give a concise answer and mention the applicable rule.
""".strip()

    @staticmethod
    def _fallback(query: str, context: list[dict]) -> str:
        if not context:
            return "The available SOP evidence is insufficient; human review is required."
        best = context[0]["text"]
        return f"Based on the available SOP evidence: {best}"
