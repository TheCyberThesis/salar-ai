from fastapi import APIRouter, HTTPException

from app.database import memory_store, persist_generated_report
from app.maps.google_maps import find_relevant_department_location
from app.schemas import GenerateReportRequest, ReportResponse
from app.services.ai_assistant import enhance_report_with_ai
from app.services.missing_fields import get_missing_fields
from app.services.report_generator import apply_department_location, generate_report

router = APIRouter(prefix="/api", tags=["reports"])


@router.post("/generate-report", response_model=ReportResponse)
async def generate(payload: GenerateReportRequest) -> ReportResponse:
    session = memory_store.sessions.get(payload.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    missing_fields = get_missing_fields(session.get("subcategory"), session.get("collected_data", {}))
    if missing_fields:
        raise HTTPException(
            status_code=409,
            detail={
                "message": "More information is required before generating the final report.",
                "missing_fields": missing_fields,
            },
        )

    report = generate_report(session)
    data = session.get("collected_data", {})
    location = session.get("location", {})
    department_location = await find_relevant_department_location(
        subcategory=session.get("subcategory"),
        city=data.get("city") or location.get("city"),
        area=data.get("last_known_location") or location.get("area"),
    )
    report = apply_department_location(report, department_location, session)
    report = await enhance_report_with_ai(report, session)
    memory_store.reports[report["report_id"]] = report
    persist_generated_report(report, session, payload.user_id)
    return ReportResponse(**report)


@router.get("/reports/{report_id}", response_model=ReportResponse)
async def get_report(report_id: str) -> ReportResponse:
    report = memory_store.reports.get(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found.")
    return ReportResponse(**report)
