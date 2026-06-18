from datetime import UTC, datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, Request

from app.database import memory_store
from app.rag.source_selector import select_sources
from app.schemas import ChatRequest, ChatResponse
from app.services.ai_assistant import extract_fields_with_llm, generate_guidance_reply
from app.services.complaint_classifier import classify_complaint
from app.services.missing_fields import REQUIRED_FIELDS, get_missing_fields, infer_fields_from_message, questions_for_fields
from app.services.rate_limiter import rate_limiter

router = APIRouter(prefix="/api", tags=["chat"])


def enforce_rate_limit(request: Request) -> None:
    rate_limiter.check(request)


def _unsupported_reply(language: str | None = None) -> str:
    if language == "roman_urdu":
        return (
            "Salar AI abhi sirf teen categories support karta hai: "
            "lost/stolen phone, bike, ya car; utility bill overcharging; "
            "aur workplace harassment against women. "
            "Agar aapka masla in mein se hai toh batayein, main help karunga."
        )
    if language == "urdu":
        return (
            "Salar AI ابھی صرف تین categories support karta hai: "
            "lost/stolen phone، bike، ya car؛ utility bill overcharging؛ "
            "aur workplace harassment against women. "
            "Agar aapka masla in mein se hai toh batayein۔"
        )
    return (
        "Salar AI’s MVP currently supports only lost/stolen phone, bike, or car; "
        "utility bill overcharging; and workplace harassment against women. "
        "I can help if your issue fits one of these categories."
    )


def _normalize_phone_subcategory(session: dict) -> None:
    subcategory = session.get("subcategory")
    incident_type = session.get("collected_data", {}).get("incident_type")
    if subcategory == "lost_phone" and incident_type == "stolen":
        session["subcategory"] = "stolen_phone"
        session["collected_data"]["subcategory"] = "stolen_phone"


async def process_chat_message(payload: ChatRequest) -> ChatResponse:
    now = datetime.now(UTC).isoformat()
    session_id = payload.session_id or str(uuid4())
    session = memory_store.sessions.get(
        session_id,
        {
            "id": session_id,
            "user_id": payload.user_id,
            "category": None,
            "subcategory": None,
            "detected_language": None,
            "stage": "collecting_missing_info",
            "collected_data": {},
            "location": payload.user_location.model_dump() if payload.user_location else {},
            "messages": [],
            "created_at": now,
        },
    )

    classification = classify_complaint(payload.message)
    if not session.get("category") or session.get("category") == "unsupported":
        session["category"] = classification.domain
        session["subcategory"] = classification.subcategory
        session["detected_language"] = classification.detected_language
    else:
        if classification.domain == session.get("category") and classification.subcategory:
            if session.get("subcategory") in {None, "lost_phone"} and classification.subcategory == "stolen_phone":
                session["subcategory"] = classification.subcategory
        # Re-detect language every message so the reply language follows the user.
        # Non-English always wins. English only overwrites when the message is long
        # enough to be unambiguously English (avoids "ok"/"yes" resetting Roman Urdu).
        new_lang = classification.detected_language
        existing_lang = session.get("detected_language")
        if new_lang != "english":
            session["detected_language"] = new_lang
        elif not existing_lang or len(payload.message.split()) >= 6:
            session["detected_language"] = "english"

    if payload.user_location:
        location = payload.user_location.model_dump()
        session["location"] = location
        if location.get("city"):
            session["collected_data"]["city"] = location["city"]

    session["messages"].append({"role": "user", "content": payload.message, "created_at": now})
    session["collected_data"] = infer_fields_from_message(
        payload.message, session.get("collected_data", {}), session.get("subcategory")
    )
    session["collected_data"] = await extract_fields_with_llm(
        message=payload.message,
        existing_data=session.get("collected_data", {}),
        subcategory=session.get("subcategory"),
        required_fields=REQUIRED_FIELDS.get(session.get("subcategory") or "", []),
    )
    _normalize_phone_subcategory(session)

    current_language = session.get("detected_language") or classification.detected_language

    if session["category"] == "unsupported":
        session["stage"] = "unsupported"
        reply = _unsupported_reply(current_language)
        missing_fields: list[str] = []
        questions: list[str] = []
        sources = []
    else:
        missing_fields = get_missing_fields(session.get("subcategory"), session["collected_data"])
        question_limit = len(missing_fields) if session.get("subcategory") in {"lost_phone", "stolen_phone"} else 6
        questions = questions_for_fields(missing_fields, limit=question_limit)
        source_cache_key = (
            session.get("category"),
            session.get("subcategory"),
            session["collected_data"].get("city"),
            session["collected_data"].get("provider"),
        )
        if session.get("_source_cache_key") != source_cache_key:
            sources = await select_sources(
                category=session["category"],
                subcategory=session.get("subcategory"),
                city=session["collected_data"].get("city"),
                provider=session["collected_data"].get("provider"),
            )
            session["verified_sources"] = sources
            session["_source_cache_key"] = source_cache_key
        else:
            sources = session.get("verified_sources", [])
        if missing_fields:
            session["stage"] = "collecting_missing_info"
            prefix = "I can help with this. "
            if session["subcategory"] == "workplace_harassment_women":
                prefix = "I’m sorry you’re dealing with this. Your safety and privacy come first. "
            reply = prefix + "Please answer these details so I can prepare a complete filled report:\n" + "\n".join(f"- {question}" for question in questions)
        else:
            session["stage"] = "ready_to_generate"
            reply = "I have enough information to generate the final filled civic guidance report. Use the Generate guidance report button now."

    reply = await generate_guidance_reply(
        user_message=payload.message,
        detected_language=current_language,
        category=session["category"],
        subcategory=session.get("subcategory"),
        stage=session["stage"],
        missing_fields=missing_fields,
        follow_up_questions=questions,
        sources=sources,
        fallback_reply=reply,
    )

    session["updated_at"] = now
    session["messages"].append({"role": "assistant", "content": reply, "created_at": now})
    memory_store.sessions[session_id] = session

    return ChatResponse(
        session_id=session_id,
        reply=reply,
        stage=session["stage"],
        missing_fields=missing_fields,
        category=session["category"],
        subcategory=session.get("subcategory"),
        detected_language=current_language,
        follow_up_questions=questions,
        sources=sources,
    )


@router.post("/chat", response_model=ChatResponse, dependencies=[Depends(enforce_rate_limit)])
async def chat(payload: ChatRequest) -> ChatResponse:
    return await process_chat_message(payload)
