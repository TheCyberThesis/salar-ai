from datetime import UTC, datetime

from fastapi import APIRouter

from app.database import memory_store
from app.schemas import FeedbackRequest, FeedbackResponse

router = APIRouter(prefix="/api", tags=["feedback"])


@router.post("/feedback", response_model=FeedbackResponse)
async def feedback(payload: FeedbackRequest) -> FeedbackResponse:
    memory_store.feedback.append({**payload.model_dump(), "created_at": datetime.now(UTC).isoformat()})
    return FeedbackResponse(ok=True, message="Feedback recorded. Thank you.")
