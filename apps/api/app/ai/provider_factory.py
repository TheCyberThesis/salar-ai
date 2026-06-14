import logging

from app.ai.base import AIMessage, MockAIProvider
from app.ai.gemini_provider import GeminiProvider
from app.ai.grok_provider import GrokProvider
from app.config import get_settings

logger = logging.getLogger(__name__)


async def generate_text_with_fallback(
    messages: list[AIMessage],
    *,
    complex_case: bool = False,
    fallback_text: str | None = None,
) -> str:
    """Generate text with Gemini first, Grok only as a last-resort backup."""
    settings = get_settings()
    mock = MockAIProvider()

    if settings.ai_provider == "mock":
        return await mock.generate(messages, complex_case=complex_case)

    if settings.gemini_api_key:
        try:
            return await GeminiProvider().generate(messages, complex_case=complex_case)
        except Exception as exc:  # pragma: no cover - external provider path
            logger.warning("Gemini generation failed; considering fallback: %s", exc)

    if settings.ai_enable_grok_fallback and settings.grok_api_key:
        try:
            return await GrokProvider().generate(messages, complex_case=complex_case)
        except Exception as exc:  # pragma: no cover - external provider path
            logger.warning("Grok fallback failed; using mock response: %s", exc)

    if fallback_text is not None:
        return fallback_text
    return await mock.generate(messages, complex_case=complex_case)


async def transcribe_audio_with_gemini(*, audio_base64: str, mime_type: str) -> str:
    """Transcribe voice messages with Gemini; Grok is intentionally not used for audio."""
    return await GeminiProvider().transcribe_audio(audio_base64=audio_base64, mime_type=mime_type)
