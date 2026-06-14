from fastapi import APIRouter, Depends, Request

from app.schemas import ClassifyRequest, ClassifyResponse
from app.services.complaint_classifier import classify_complaint
from app.services.rate_limiter import rate_limiter

router = APIRouter(prefix="/api", tags=["classification"])


def enforce_rate_limit(request: Request) -> None:
    rate_limiter.check(request)


@router.post("/classify", response_model=ClassifyResponse, dependencies=[Depends(enforce_rate_limit)])
async def classify(payload: ClassifyRequest) -> ClassifyResponse:
    result = classify_complaint(payload.message, payload.language_hint)
    return ClassifyResponse(**result.__dict__)
