import logging

import httpx

from app.ai.base import AIMessage, AIProvider, AIProviderUnavailable, LLMNetworkError, LLMResponseError
from app.config import get_settings

logger = logging.getLogger(__name__)


class GeminiProvider(AIProvider):
    def __init__(self) -> None:
        self.settings = get_settings()

    async def generate(self, messages: list[AIMessage], *, complex_case: bool = False) -> str:
        if not self.settings.gemini_api_key:
            raise AIProviderUnavailable("Gemini API key is not configured.")

        model = self.settings.gemini_complex_model if complex_case else self.settings.gemini_default_model
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        system_instruction = "\n\n".join(msg.content for msg in messages if msg.role == "system")
        contents = [
            {"role": "user" if msg.role != "assistant" else "model", "parts": [{"text": msg.content}]}
            for msg in messages
            if msg.role != "system"
        ]
        body: dict[str, object] = {"contents": contents}
        if system_instruction:
            body["system_instruction"] = {"parts": [{"text": system_instruction}]}

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    url,
                    headers={"x-goog-api-key": self.settings.gemini_api_key},
                    json=body,
                )
                response.raise_for_status()
                payload = response.json()
        except (httpx.ConnectError, httpx.TimeoutException) as exc:
            raise LLMNetworkError(f"Gemini unreachable: {exc}") from exc
        except httpx.HTTPStatusError as exc:
            raise LLMResponseError(
                f"Gemini API error {exc.response.status_code}"
            ) from exc
        except Exception as exc:
            raise LLMResponseError(f"Gemini request failed: {exc}") from exc
        candidates = payload.get("candidates") or []
        if not candidates:
            raise LLMResponseError("Gemini returned no candidates.")
        return candidates[0]["content"]["parts"][0].get("text", "")

    async def transcribe_audio(self, *, audio_base64: str, mime_type: str, prompt: str | None = None) -> str:
        if not self.settings.gemini_api_key:
            raise AIProviderUnavailable("Gemini API key is not configured.")

        instruction = prompt or (
            "Transcribe this Pakistani civic complaint voice message. "
            "Preserve Roman Urdu when the speaker uses Roman Urdu. "
            "Return only the transcript text, without commentary."
        )
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.settings.gemini_audio_model}:generateContent"
        body = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": instruction},
                        {"inline_data": {"mime_type": mime_type, "data": audio_base64}},
                    ],
                }
            ]
        }
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                url,
                headers={"x-goog-api-key": self.settings.gemini_api_key},
                json=body,
            )
            response.raise_for_status()
            payload = response.json()
        candidates = payload.get("candidates") or []
        if not candidates:
            raise AIProviderUnavailable("Gemini returned no audio transcript candidates.")
        parts = candidates[0].get("content", {}).get("parts", [])
        transcript = " ".join(part.get("text", "") for part in parts).strip()
        if not transcript:
            raise AIProviderUnavailable("Gemini returned an empty audio transcript.")
        return transcript
