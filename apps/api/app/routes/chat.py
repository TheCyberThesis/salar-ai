from datetime import UTC, datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, Request

from app.database import memory_store
from app.rag.retriever import retrieve_knowledge
from app.schemas import ChatRequest, ChatResponse
from app.services.complaint_classifier import classify_complaint
from app.services.missing_fields import get_missing_fields, infer_fields_from_message, questions_for_fields
from app.services.rate_limiter import rate_limiter

router = APIRouter(prefix="/api", tags=["chat"])


def enforce_rate_limit(request: Request) -> None:
    rate_limiter.check(request)


def _unsupported_reply() -> str:
    return (
        "Salaar AI’s MVP currently supports only lost/stolen phone, bike, or car; "
        "utility bill overcharging; and workplace harassment against women. "
        "I can help if your issue fits one of these categories."
    )


@router.post("/chat", response_model=ChatResponse, dependencies=[Depends(enforce_rate_limit)])
async def chat(payload: ChatRequest) -> ChatResponse:
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

    if payload.user_location:
        location = payload.user_location.model_dump()
        session["location"] = location
        if location.get("city"):
            session["collected_data"]["city"] = location["city"]

    session["messages"].append({"role": "user", "content": payload.message, "created_at": now})
    session["collected_data"] = infer_fields_from_message(
        payload.message,
        session.get("collected_data", {}),
        session.get("subcategory"),
    )

    if session["category"] == "unsupported":
        session["stage"] = "unsupported"
        reply = _unsupported_reply()
        missing_fields: list[str] = []
        questions: list[str] = []
        sources = []
    else:
        missing_fields = get_missing_fields(session.get("subcategory"), session["collected_data"])
        questions = questions_for_fields(missing_fields)
        sources = retrieve_knowledge(session["category"], session.get("subcategory"), city=session["collected_data"].get("city"))
        if missing_fields:
            session["stage"] = "collecting_missing_info"
            prefix = "I can help with this. "
            if session["subcategory"] == "workplace_harassment_women":
                prefix = "I’m sorry you’re dealing with this. Your safety and privacy come first. "
            reply = prefix + "Please answer these details so I can prepare more accurate guidance: " + " ".join(questions)
        else:
            session["stage"] = "ready_to_generate"
            reply = "I have enough information to generate a civic guidance report. You can now generate the report."

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
        detected_language=session.get("detected_language") or classification.detected_language,
        follow_up_questions=questions,
        sources=sources,
    )
