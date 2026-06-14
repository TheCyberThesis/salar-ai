from typing import Any
from uuid import uuid4

from app.maps.maps_fallback import build_maps_search_link
from app.rag.retriever import retrieve_knowledge
from app.services.complaint_templates import generate_complaint_draft
from app.services.missing_fields import get_missing_fields
from app.services.privacy import mask_sensitive_data


DISCLAIMER = (
    "Salaar AI provides AI-powered public guidance for civic and social issues. "
    "It is not a substitute for professional legal advice. For serious legal matters, "
    "please consult a qualified lawyer or relevant authority."
)


REQUIRED_DOCUMENTS: dict[str, list[str]] = {
    "lost_phone": ["CNIC copy", "IMEI number if available", "phone box or purchase receipt if available", "SIM/operator details", "last known location and incident date/time"],
    "stolen_phone": ["CNIC copy", "IMEI number if available", "phone box or purchase receipt if available", "SIM/operator details", "last known location and incident date/time"],
    "lost_bike": ["CNIC copy", "vehicle registration book/card", "number plate", "model/color details", "last known location and incident date/time"],
    "stolen_bike": ["CNIC copy", "vehicle registration book/card", "number plate", "model/color details", "last known location and incident date/time"],
    "lost_car": ["CNIC copy", "vehicle registration book/card", "number plate", "chassis/engine number if available", "last known location and incident date/time"],
    "stolen_car": ["CNIC copy", "vehicle registration book/card", "number plate", "chassis/engine number if available", "last known location and incident date/time"],
    "electricity_bill_overcharging": ["Current bill copy", "previous bill copy", "reference/customer number", "current meter reading photo", "CNIC/contact details if provider requires"],
    "gas_bill_overcharging": ["Current bill copy", "previous bill copy", "consumer/customer number", "current meter reading photo", "CNIC/contact details if provider requires"],
    "water_bill_overcharging": ["Current bill copy", "previous bill copy", "consumer/account number", "current meter reading photo if applicable", "CNIC/contact details if authority requires"],
    "workplace_harassment_women": ["High-level incident summary", "dates/times", "workplace/organization details", "accused role/designation", "evidence or witnesses if available", "copies of relevant communications if safe to preserve"],
}


def _department(subcategory: str | None, data: dict[str, Any]) -> str:
    if not subcategory:
        return "Relevant department"
    if subcategory in {"lost_phone", "stolen_phone", "lost_bike", "stolen_bike", "lost_car", "stolen_car"}:
        return "Nearest police station or relevant police public-service center"
    if subcategory == "electricity_bill_overcharging":
        return f"{data.get('provider') or 'Electricity distribution company'} customer service center; regulator escalation where verified"
    if subcategory == "gas_bill_overcharging":
        return f"{data.get('provider') or 'Gas utility provider'} complaint/customer service center; regulator escalation where verified"
    if subcategory == "water_bill_overcharging":
        return f"{data.get('provider') or 'Local WASA/water authority'} complaint center"
    if subcategory == "workplace_harassment_women":
        return "Workplace inquiry committee, FOSPAH, or relevant provincial ombudsperson/authority"
    return "Relevant department"


def _procedure(subcategory: str | None) -> list[str]:
    if subcategory in {"lost_phone", "stolen_phone"}:
        return [
            "Visit or contact the nearest police station/public-service reporting point for a loss/theft report.",
            "Share CNIC details only with the relevant authority and provide IMEI, SIM/operator, last location, and incident date/time if available.",
            "Ask for a written diary number, report number, complaint number, FIR/reference number, or receiving copy as applicable.",
            "Block the SIM through the mobile operator and verify PTA/DIRBS-related steps from official PTA guidance if needed.",
            "Keep photos/copies of every submitted document and every reference number.",
        ]
    if subcategory in {"lost_bike", "stolen_bike", "lost_car", "stolen_car"}:
        return [
            "Report the lost/stolen vehicle to the nearest police station or relevant police service center.",
            "Provide registration book/card, number plate, vehicle model/color, and chassis/engine details if available.",
            "Request a written report/FIR/diary/complaint number according to the incident context.",
            "Keep a copy/photo of the submitted application and the issued reference.",
            "Follow up with the police station/service center using the issued reference number.",
        ]
    if subcategory in {"electricity_bill_overcharging", "gas_bill_overcharging", "water_bill_overcharging"}:
        return [
            "Contact the utility provider/customer service center first and submit a bill review/correction request.",
            "Attach the current bill, previous bill, meter photo, current reading, and customer/reference number.",
            "Ask for a complaint/reference/token number for tracking.",
            "Track the complaint through the provider’s official process.",
            "If unresolved, verify escalation options with the relevant regulator or authority in the knowledge base.",
        ]
    if subcategory == "workplace_harassment_women":
        return [
            "If there is immediate physical danger, contact emergency services, trusted support, or a relevant local authority immediately.",
            "Write a high-level factual timeline and preserve evidence safely without sharing it publicly.",
            "Submit the complaint to the workplace inquiry committee if available, or consult FOSPAH/relevant provincial authority guidance.",
            "Request confidentiality and a written receiving copy/complaint/reference number.",
            "For serious legal action, consult a qualified lawyer or relevant authority.",
        ]
    return ["This MVP supports only the three configured civic guidance domains."]


def _proof_to_collect(subcategory: str | None) -> list[str]:
    if subcategory in {"lost_phone", "stolen_phone", "lost_bike", "stolen_bike", "lost_car", "stolen_car"}:
        return ["diary number", "complaint/report number", "FIR/reference number if applicable", "receiving/stamped copy", "photo/copy of submitted application"]
    if subcategory in {"electricity_bill_overcharging", "gas_bill_overcharging", "water_bill_overcharging"}:
        return ["complaint/reference number", "token number", "dated receiving copy", "screenshots of online complaint tracking"]
    if subcategory == "workplace_harassment_women":
        return ["receiving copy", "complaint/reference number", "acknowledgement email/letter", "copy of submitted complaint"]
    return []


def _timeline(subcategory: str | None) -> str:
    if subcategory in {"workplace_harassment_women"}:
        return "Timelines can depend on the applicable workplace policy, FOSPAH/provincial process, and urgency. Verify current timelines with the receiving authority."
    if subcategory in {"electricity_bill_overcharging", "gas_bill_overcharging", "water_bill_overcharging"}:
        return "Provider response timelines vary by provider and city. Ask the provider for the official tracking timeline when you submit the complaint."
    return "Police/public-service timelines vary by incident, city, and report type. Ask the receiving official when to follow up and keep the issued reference number."


def _escalation(subcategory: str | None) -> list[str]:
    if subcategory in {"lost_phone", "stolen_phone", "lost_bike", "stolen_bike", "lost_car", "stolen_car"}:
        return [
            "Return with the issued reference number if no update is received in the stated time.",
            "Ask the station/service center duty officer for the next follow-up step.",
            "Use official police complaint/public-service escalation channels where available for your province/city.",
        ]
    if subcategory == "electricity_bill_overcharging":
        return [
            "Escalate within the utility provider using the complaint/reference number.",
            "If unresolved, verify NEPRA Consumer Affairs complaint guidance from official NEPRA sources before escalating.",
        ]
    if subcategory == "gas_bill_overcharging":
        return [
            "Escalate within the gas utility provider using the complaint/reference number.",
            "If unresolved, verify OGRA complaint guidance from official OGRA sources before escalating.",
        ]
    if subcategory == "water_bill_overcharging":
        return [
            "Escalate within the local water authority/WASA using the complaint/reference number.",
            "Confirm local escalation forums because water authority processes differ by city/province.",
        ]
    if subcategory == "workplace_harassment_women":
        return [
            "If the workplace process is unsafe or unavailable, verify FOSPAH or relevant provincial authority complaint options.",
            "For urgent safety risks, prioritize emergency/trusted support before paperwork.",
            "For serious legal action, consult a qualified lawyer or competent authority.",
        ]
    return []


def generate_report(session: dict[str, Any]) -> dict[str, Any]:
    data = mask_sensitive_data(session.get("collected_data", {}))
    subcategory = session.get("subcategory")
    category = session.get("category", "unsupported")
    city = data.get("city") or session.get("location", {}).get("city")
    area = session.get("location", {}).get("area")
    knowledge = retrieve_knowledge(category, subcategory, city=city)
    maps_link = build_maps_search_link(subcategory=subcategory, city=city, area=area)
    missing = get_missing_fields(subcategory, data)
    department = _department(subcategory, data)

    return {
        "report_id": str(uuid4()),
        "session_id": session["id"],
        "summary": f"Guidance for {subcategory or category}.",
        "category": category,
        "subcategory": subcategory,
        "department": department,
        "user_provided_details": data,
        "missing_information": missing,
        "required_documents": REQUIRED_DOCUMENTS.get(subcategory or "", []),
        "step_by_step_procedure": _procedure(subcategory),
        "complaint_draft": generate_complaint_draft(subcategory, data),
        "where_to_submit": department,
        "maps_link": maps_link,
        "proof_to_collect": _proof_to_collect(subcategory),
        "timeline": _timeline(subcategory),
        "escalation_steps": _escalation(subcategory),
        "safety_privacy_notes": [
            "Avoid sharing CNIC, phone number, address, IMEI, or evidence publicly.",
            "Share sensitive information only with the relevant authority/provider when required.",
            "This guidance is based on available official Pakistani public sources in Salaar AI’s knowledge base. Please verify requirements with the relevant department before submitting your complaint.",
        ],
        "sources_used": knowledge,
        "disclaimer": DISCLAIMER,
    }
