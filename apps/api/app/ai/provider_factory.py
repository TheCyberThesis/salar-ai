import logging

from app.ai.base import AIMessage, LLMNetworkError, LLMResponseError, MockAIProvider
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
            logger.warning("Gemini failed (field extraction); trying Grok fallback: %s", exc)

    if settings.ai_enable_grok_fallback and settings.grok_api_key:
        logger.info("Using Grok fallback (field extraction)")
        try:
            result = await GrokProvider().generate(messages, complex_case=complex_case)
            logger.info("Grok fallback succeeded (field extraction)")
            return result
        except Exception as exc:  # pragma: no cover - external provider path
            logger.warning("Grok fallback failed (field extraction): %s", exc)

    if fallback_text is not None:
        return fallback_text
    return await mock.generate(messages, complex_case=complex_case)


async def generate_chat_reply(
    messages: list[AIMessage],
    *,
    complex_case: bool = False,
) -> str:
    """Generate a chat reply, raising LLMNetworkError or LLMResponseError when all providers fail.

    Unlike generate_text_with_fallback, this function does not swallow errors — callers
    are expected to catch and translate them into user-facing messages.
    """
    settings = get_settings()
    had_network_error = False
    had_response_error = False

    if settings.ai_provider == "mock":
        return await MockAIProvider().generate(messages, complex_case=complex_case)

    if settings.gemini_api_key:
        try:
            return await GeminiProvider().generate(messages, complex_case=complex_case)
        except LLMNetworkError as exc:
            had_network_error = True
            logger.warning("Gemini network error: %s", exc)
        except Exception as exc:
            had_response_error = True
            logger.warning("Gemini generation failed: %s", exc)

    if settings.ai_enable_grok_fallback and settings.grok_api_key:
        logger.info("Using Grok fallback (chat/report)")
        try:
            result = await GrokProvider().generate(messages, complex_case=complex_case)
            logger.info("Grok fallback succeeded (chat/report)")
            return result
        except LLMNetworkError as exc:
            had_network_error = True
            logger.warning("Grok network error: %s", exc)
        except Exception as exc:
            had_response_error = True
            logger.warning("Grok fallback failed: %s", exc)

    if had_response_error:
        raise LLMResponseError("All LLM providers returned an error or unexpected response.")
    raise LLMNetworkError("All LLM providers are unreachable.")


async def transcribe_audio_with_gemini(*, audio_base64: str, mime_type: str) -> str:
    """Transcribe voice messages with Gemini; Grok is intentionally not used for audio."""
    return await GeminiProvider().transcribe_audio(audio_base64=audio_base64, mime_type=mime_type)
