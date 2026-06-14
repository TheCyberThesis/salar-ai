from typing import Any, Literal

from pydantic import BaseModel, Field


SupportedDomain = Literal[
    "lost_or_stolen_vehicle_device",
    "utility_bill_overcharging",
    "workplace_harassment_women",
    "unsupported",
]


class UserLocation(BaseModel):
    city: str | None = Field(default=None, max_length=80)
    area: str | None = Field(default=None, max_length=120)
    province: str | None = Field(default=None, max_length=80)


class ClassifyRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    language_hint: str | None = Field(default=None, max_length=40)


class ClassifyResponse(BaseModel):
    detected_language: str
    domain: SupportedDomain
    subcategory: str | None
    confidence: float
    emergency_level: Literal["low", "medium", "high"]


class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str = Field(min_length=1, max_length=4000)
    user_location: UserLocation | None = None
    user_id: str | None = None


class SourceNote(BaseModel):
    title: str
    source_name: str
    authority_type: str | None = None
    jurisdiction: str
    source_url: str | None = None
    verified_at: str | None = None
    confidence_level: str = "official_source_metadata"


class DepartmentLocation(BaseModel):
    place_name: str | None = None
    address: str | None = None
    phone_number: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    google_maps_place_id: str | None = None
    maps_link: str
    notes: str | None = None


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    stage: Literal["unsupported", "collecting_missing_info", "ready_to_generate"]
    missing_fields: list[str]
    category: SupportedDomain
    subcategory: str | None = None
    detected_language: str
    follow_up_questions: list[str] = Field(default_factory=list)
    sources: list[SourceNote] = Field(default_factory=list)


class VoiceChatRequest(BaseModel):
    session_id: str | None = None
    audio_base64: str = Field(min_length=1, max_length=18_000_000)
    mime_type: str = Field(default="audio/webm", max_length=80)
    user_location: UserLocation | None = None
    user_id: str | None = None


class VoiceChatResponse(BaseModel):
    transcript: str
    chat: ChatResponse


class GenerateReportRequest(BaseModel):
    session_id: str
    user_id: str | None = None


class ReportResponse(BaseModel):
    report_id: str
    session_id: str
    summary: str
    category: SupportedDomain
    subcategory: str | None
    issue_type: str
    department: str
    reporting_office: str
    report_recipient: str
    user_provided_details: dict[str, Any]
    missing_information: list[str]
    required_documents: list[str]
    step_by_step_procedure: list[str]
    complaint_draft: str
    where_to_submit: str
    maps_link: str
    department_location: DepartmentLocation | None = None
    proof_to_collect: list[str]
    timeline: str
    escalation_steps: list[str]
    safety_privacy_notes: list[str]
    sources_used: list[SourceNote]
    disclaimer: str


class DepartmentResponse(BaseModel):
    name: str
    type: str
    province: str | None = None
    city: str | None = None
    website: str | None = None
    helpline: str | None = None
    address: str | None = None


class FeedbackRequest(BaseModel):
    user_id: str | None = None
    complaint_id: str | None = None
    rating: int = Field(ge=1, le=5)
    helpful: bool
    comments: str | None = Field(default=None, max_length=2000)


class FeedbackResponse(BaseModel):
    ok: bool
    message: str
