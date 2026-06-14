import json
import logging
from typing import Any

from app.ai.base import AIMessage, LLMNetworkError, LLMResponseError
from app.ai.prompts import REPORT_PROMPT, SYSTEM_PROMPT
from app.ai.provider_factory import generate_chat_reply, generate_text_with_fallback

logger = logging.getLogger(__name__)


_FIELD_DESCRIPTIONS: dict[str, str] = {
    "incident_type": "Type of incident: one of 'lost', 'stolen', or 'snatched'",
    "incident_description": (
        "A DETAILED narrative of the full incident — must include at least MOST of: "
        "what happened step by step, what the user was doing at the time, "
        "culprit description (face, height, clothing, number of attackers), "
        "vehicle or bike details (color, model, registration plate if visible), "
        "direction of escape, whether any CCTV cameras were nearby, any witnesses, "
        "any ride-hailing or delivery order context. "
        "A single vague sentence like 'my phone was stolen' is NOT sufficient — "
        "do NOT extract that as incident_description."
    ),
    "phone_model": "Make and model of the phone",
    "last_known_location": (
        "The EXACT LOCATION WHERE THE INCIDENT HAPPENED — "
        "not the user's destination, hostel, home, or any other mentioned place. "
        "E.g. if the user says 'I was going to E11 but the phone was snatched at Street 41 G11/1', "
        "extract 'Street 41, G11/1'."
    ),
    "incident_date_time": "Date and time when the incident occurred",
    "imei": "15-digit IMEI number of the phone",
    "sim_number_or_operator": "Mobile network operator(s) whose SIM(s) were in the phone (Jazz, Zong, Telenor, Ufone, etc.)",
    "city": "City where the incident occurred",
    "applicant_name": "Full name to appear on the complaint/application",
    "applicant_contact": "Active phone number for police follow-up",
    "draft_language": "Preferred language for complaint draft: 'english', 'urdu', or 'roman_urdu'",
    "vehicle_registration_number": "Vehicle registration plate/number",
    "vehicle_model_color": "Vehicle make, model, and color",
    "provider": "Utility provider name (e.g. IESCO, LESCO, SNGPL, WASA)",
    "reference_or_customer_number": "Bill reference or customer number",
    "consumer_or_account_number": "Water bill consumer/account number",
    "bill_month": "Month of the disputed bill",
    "amount_charged": "Amount charged on the bill",
    "current_meter_reading": "Current meter reading",
    "meter_photo_available": "Whether user has a current meter photo available",
    "consumer_name": "Name on the utility bill",
    "address": "Service address on the utility bill",
    "immediate_safety_risk": "Whether the user is in immediate physical danger right now",
    "complainant_name": "Name for the harassment complaint",
    "workplace_name": "Name of workplace or organization",
    "nature_of_issue_high_level": "High-level description of the harassment (avoid graphic details)",
    "incident_dates": "Date(s) when harassment occurred",
    "accused_role": "Role or designation of the accused person",
    "evidence_or_witnesses": "Available evidence or witnesses if any",
    "internal_committee_available": "Whether the workplace has an internal harassment inquiry committee",
}


async def extract_fields_with_llm(
    *,
    message: str,
    existing_data: dict[str, Any],
    subcategory: str | None,
    required_fields: list[str],
) -> dict[str, Any]:
    """Use LLM to extract structured complaint fields from a user message."""
    fields_to_extract = {
        f: _FIELD_DESCRIPTIONS.get(f, f)
        for f in required_fields
        if not existing_data.get(f)
    }
    if not fields_to_extract:
        return existing_data

    already_collected = {k: v for k, v in existing_data.items() if k in required_fields and v}

    prompt = f"""Extract structured information from a Pakistani civic complaint message.

Complaint type: {subcategory or "unknown"}

Already collected (do NOT re-extract unless user is explicitly correcting a value):
{json.dumps(already_collected, ensure_ascii=False, indent=2)}

Fields still needed — extract ONLY if clearly stated in the message below:
{json.dumps(fields_to_extract, ensure_ascii=False, indent=2)}

User message:
{message}

Rules:
- For 'last_known_location': extract WHERE THE INCIDENT ACTUALLY HAPPENED, never the user's destination or travel origin.
- For 'incident_description': ONLY extract if the message contains a genuine detailed account (at least 4 of: how it happened, culprit physical description, vehicle details, escape direction, witnesses, CCTV, specific time/context). A vague line like "my phone was stolen at G-11" is NOT a valid incident_description — omit it so the AI knows to ask for more detail.
- Only include fields with clear explicit values. Do not guess or infer.
- Return a flat JSON object mapping field names to their extracted string values.
- Return {{}} if no extractable new information is present.
- No commentary — JSON only."""

    generated = await generate_text_with_fallback(
        [AIMessage("system", SYSTEM_PROMPT), AIMessage("user", prompt)],
        complex_case=False,
        fallback_text="{}",
    )

    parsed = _extract_json_object(generated)
    if not parsed:
        logger.info("LLM field extraction returned no parseable JSON; keeping existing data.")
        return existing_data

    merged = dict(existing_data)
    for key, value in parsed.items():
        if isinstance(value, str) and value.strip():
            merged[key] = value.strip()
        elif value and not isinstance(value, str):
            merged[key] = value
    return merged


def _language_instruction(detected_language: str | None) -> str:
    if detected_language == "roman_urdu":
        return (
            "IMPORTANT: Reply entirely in Roman Urdu (Urdu written in English letters, Pakistani casual style). "
            "Do NOT switch to English sentences. Civic/official terms like 'FIR', 'IMEI', 'CCTV', 'police station', "
            "'complaint', 'application' may stay in English as Pakistani speakers use them natively."
        )
    if detected_language == "urdu":
        return (
            "IMPORTANT: Reply entirely in Urdu script. "
            "Official names like 'FIR', 'IMEI', 'CCTV' may stay in English as they are used in Pakistani Urdu."
        )
    return "Reply in clear, simple English."


async def generate_guidance_reply(
    *,
    user_message: str,
    detected_language: str | None,
    category: str,
    subcategory: str | None,
    stage: str,
    missing_fields: list[str],
    follow_up_questions: list[str],
    sources: list[dict[str, Any]],
    fallback_reply: str,
) -> str:
    if category == "unsupported":
        return fallback_reply
    if stage == "ready_to_generate":
        return fallback_reply
    if missing_fields:
        return fallback_reply

    language_instruction = _language_instruction(detected_language)
    source_notes = [
        {
            "title": source.get("title"),
            "source_name": source.get("source_name"),
            "jurisdiction": source.get("jurisdiction"),
            "confidence_level": source.get("confidence_level"),
        }
        for source in sources[:4]
    ]

    prompt = f"""
Write the next Salar AI chat reply.

{language_instruction}

Hard constraints:
- Do not invent phone numbers, office addresses, forms, deadlines, laws, or legal claims.
- Stay inside the supported category and subcategory.
- Ask only the provided follow-up questions when information is missing.
- Never write a complaint/application/report draft in chat. Chat is only for collecting details.
- If enough information has been collected, tell the user to generate the final report instead of drafting it here.
- Mention safety/privacy briefly for harassment or sensitive personal data.
- Keep the reply concise and practical.

Incident detail collection (IMPORTANT):
- When 'incident_description' is in missing fields, explicitly ask the user to narrate the full incident in their own words: exactly what happened step by step, what they were doing, culprit appearance and clothing, vehicle/bike (color, model, plate), how many attackers, direction of escape, any CCTV cameras nearby, any witnesses. Tell the user that every detail strengthens the complaint.
- Do not accept "my phone was stolen" or similar one-liners as enough — probe for the story behind it.

Current state:
Category: {category}
Subcategory: {subcategory}
Stage: {stage}
Missing fields: {missing_fields}
Follow-up questions: {follow_up_questions}
Retrieved source notes: {json.dumps(source_notes, ensure_ascii=False)}
Fallback reply to improve: {fallback_reply}

User message:
{user_message}

Return only the user-facing reply.
""".strip()

    try:
        generated = await generate_chat_reply(
            [AIMessage("system", SYSTEM_PROMPT), AIMessage("user", prompt)],
            complex_case=category == "workplace_harassment_women",
        )
    except LLMNetworkError:
        return "Salar AI is unable to reach the AI service right now. Please try again in a moment."
    except Exception:
        return "The AI is currently busy. Please try again shortly."
    return generated.strip() or fallback_reply


def _extract_json_object(text: str) -> dict[str, Any] | None:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = stripped.strip("`")
        if stripped.lower().startswith("json"):
            stripped = stripped[4:].strip()
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        parsed = json.loads(stripped[start : end + 1])
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else None


async def enhance_report_with_ai(report: dict[str, Any], session: dict[str, Any]) -> dict[str, Any]:
    language_instruction = _language_instruction(session.get("detected_language"))
    draft_language = (
        report.get("user_provided_details", {}).get("draft_language")
        or session.get("detected_language")
        or "english"
    )
    report_context = dict(report)
    report_context.pop("complaint_draft", None)
    report_context["user_provided_details_for_draft"] = session.get("collected_data", {})
    prompt = f"""
{REPORT_PROMPT}

{language_instruction}

Rewrite the final report's summary and complaint/application draft using the report JSON.

The complaint_draft MUST be a polished official application, not a copy of the user's raw words.
Use a respectful Pakistani civic/police application tone.
Preserve all user-provided facts exactly: locations, route, dates/times, vehicle/bike details, CCTV details, phone/device details, applicant details, and reference numbers.
If a fact is not provided, do not invent it and do not add placeholders.
Keep the already resolved office/recipient/department from the report JSON.
Keep the draft language as: {draft_language}.

Do not change procedures, departments, recipient, office, source notes, proof reminders, maps links, or legal/public guidance disclaimers.
Do not invent facts. Use only the report JSON.
Return strict JSON with exactly these string keys: "summary", "complaint_draft".

Report JSON:
{json.dumps(report_context, ensure_ascii=False)}
""".strip()

    generated = await generate_chat_reply(
        [AIMessage("system", SYSTEM_PROMPT), AIMessage("user", prompt)],
        complex_case=report.get("category") == "workplace_harassment_women",
    )
    parsed = _extract_json_object(generated)
    if not parsed:
        logger.warning("AI report enhancement did not return parseable JSON.")
        raise LLMResponseError("AI report generation returned invalid JSON.")

    summary = parsed.get("summary")
    complaint_draft = parsed.get("complaint_draft")
    if not isinstance(summary, str) or not summary.strip():
        raise LLMResponseError("AI report generation returned an empty summary.")
    if not isinstance(complaint_draft, str) or not complaint_draft.strip():
        raise LLMResponseError("AI report generation returned an empty complaint draft.")

    report["summary"] = summary.strip()
    report["complaint_draft"] = complaint_draft.strip()
    return report
