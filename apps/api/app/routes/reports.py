from fastapi import APIRouter, HTTPException

from app.database import memory_store, persist_generated_report
from app.schemas import GenerateReportRequest, ReportResponse
from app.services.report_generator import generate_report

router = APIRouter(prefix="/api", tags=["reports"])


@router.post("/generate-report", response_model=ReportResponse)
async def generate(payload: GenerateReportRequest) -> ReportResponse:
    session = memory_store.sessions.get(payload.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    report = generate_report(session)
    memory_store.reports[report["report_id"]] = report
    persist_generated_report(report, session, payload.user_id)
    return ReportResponse(**report)


@router.get("/reports/{report_id}", response_model=ReportResponse)
async def get_report(report_id: str) -> ReportResponse:
    report = memory_store.reports.get(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found.")
    return ReportResponse(**report)
