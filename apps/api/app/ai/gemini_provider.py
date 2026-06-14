import httpx

from app.ai.base import AIMessage, AIProvider, MockAIProvider
from app.config import get_settings


class GeminiProvider(AIProvider):
    def __init__(self) -> None:
        self.settings = get_settings()
        self.mock = MockAIProvider()

    async def generate(self, messages: list[AIMessage], *, complex_case: bool = False) -> str:
        if not self.settings.gemini_api_key:
            return await self.mock.generate(messages, complex_case=complex_case)

        model = self.settings.gemini_complex_model if complex_case else self.settings.gemini_default_model
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        contents = [
            {"role": "user" if msg.role != "assistant" else "model", "parts": [{"text": msg.content}]}
            for msg in messages
        ]
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                url,
                params={"key": self.settings.gemini_api_key},
                json={"contents": contents},
            )
            response.raise_for_status()
            payload = response.json()
        candidates = payload.get("candidates") or []
        if not candidates:
            return await self.mock.generate(messages, complex_case=complex_case)
        return candidates[0]["content"]["parts"][0].get("text", "")
