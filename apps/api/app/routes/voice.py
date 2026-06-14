import base64
import binascii

from fastapi import APIRouter, Depends, HTTPException

from app.ai.provider_factory import transcribe_audio_with_gemini
from app.routes.chat import enforce_rate_limit, process_chat_message
from app.schemas import ChatRequest, VoiceChatRequest, VoiceChatResponse

router = APIRouter(prefix="/api", tags=["voice"])


@router.post("/voice-message", response_model=VoiceChatResponse, dependencies=[Depends(enforce_rate_limit)])
async def voice_message(payload: VoiceChatRequest) -> VoiceChatResponse:
    try:
        base64.b64decode(payload.audio_base64, validate=True)
    except binascii.Error as exc:
        raise HTTPException(status_code=400, detail="Invalid base64 audio payload.") from exc

    try:
        transcript = await transcribe_audio_with_gemini(audio_base64=payload.audio_base64, mime_type=payload.mime_type)
    except Exception as exc:  # pragma: no cover - external provider path
        raise HTTPException(
            status_code=503,
            detail="Voice processing requires a working GEMINI_API_KEY. Please type the message or check Gemini configuration.",
        ) from exc

    chat_response = await process_chat_message(
        ChatRequest(
            session_id=payload.session_id,
            message=transcript,
            user_location=payload.user_location,
            user_id=payload.user_id,
        )
    )
    return VoiceChatResponse(transcript=transcript, chat=chat_response)
