import logging

import httpx

from app.ai.base import AIMessage, AIProvider, AIProviderUnavailable, LLMNetworkError, LLMResponseError
from app.config import get_settings

logger = logging.getLogger(__name__)


class GrokProvider(AIProvider):
    def __init__(self) -> None:
        self.settings = get_settings()

    async def generate(self, messages: list[AIMessage], *, complex_case: bool = False) -> str:
        if not self.settings.grok_api_key:
            raise AIProviderUnavailable("Grok API key is not configured.")

        response_messages = [{"role": msg.role, "content": msg.content} for msg in messages]
        try:
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
        except (httpx.ConnectError, httpx.TimeoutException) as exc:
            raise LLMNetworkError(f"Grok unreachable: {exc}") from exc
        except httpx.HTTPStatusError as exc:
            logger.error("Grok API error %s: %s", exc.response.status_code, exc.response.text)
            raise LLMResponseError(
                f"Grok API error {exc.response.status_code}: {exc.response.text}"
            ) from exc
        except Exception as exc:
            raise LLMResponseError(f"Grok request failed: {exc}") from exc
        choices = payload.get("choices") or []
        if not choices:
            raise LLMResponseError("Grok returned no choices.")
        return choices[0].get("message", {}).get("content", "")
