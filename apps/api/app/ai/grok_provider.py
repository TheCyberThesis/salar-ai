import httpx

from app.ai.base import AIMessage, AIProvider, AIProviderUnavailable
from app.config import get_settings


class GrokProvider(AIProvider):
    def __init__(self) -> None:
        self.settings = get_settings()

    async def generate(self, messages: list[AIMessage], *, complex_case: bool = False) -> str:
        if not self.settings.grok_api_key:
            raise AIProviderUnavailable("Grok API key is not configured.")

        response_messages = [{"role": msg.role, "content": msg.content} for msg in messages]
        async with httpx.AsyncClient(timeout=45) as client:
            response = await client.post(
                "https://api.x.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.settings.grok_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.settings.grok_model,
                    "messages": response_messages,
                    "temperature": 0.2,
                },
            )
            response.raise_for_status()
            payload = response.json()
        choices = payload.get("choices") or []
        if not choices:
            raise AIProviderUnavailable("Grok returned no choices.")
        return choices[0].get("message", {}).get("content", "")
