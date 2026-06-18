import re
from typing import Any


REQUIRED_FIELDS: dict[str, list[str]] = {
    "lost_phone": [
        "incident_type",
        "incident_description",
        "phone_model",
        "last_known_location",
        "incident_date_time",
        "imei",
        "sim_number_or_operator",
        "city",
        "applicant_name",
        "applicant_contact",
        "draft_language",
    ],
    "stolen_phone": [
        "incident_type",
        "incident_description",
        "phone_model",
        "last_known_location",
        "incident_date_time",
        "imei",
        "sim_number_or_operator",
        "city",
        "applicant_name",
        "applicant_contact",
        "draft_language",
    ],
    "lost_bike": [
        "incident_type",
        "vehicle_registration_number",
        "vehicle_model_color",
        "last_known_location",
        "incident_date_time",
        "city",
        "applicant_name",
    ],
    "stolen_bike": [
        "incident_type",
        "vehicle_registration_number",
        "vehicle_model_color",
        "last_known_location",
        "incident_date_time",
        "city",
        "applicant_name",
    ],
    "lost_car": [
        "incident_type",
        "vehicle_registration_number",
        "vehicle_model_color",
        "last_known_location",
        "incident_date_time",
        "city",
        "applicant_name",
    ],
    "stolen_car": [
        "incident_type",
        "vehicle_registration_number",
        "vehicle_model_color",
        "last_known_location",
        "incident_date_time",
        "city",
        "applicant_name",
    ],
    "electricity_bill_overcharging": [
        "provider",
        "reference_or_customer_number",
        "bill_month",
        "amount_charged",
        "current_meter_reading",
        "meter_photo_available",
        "city",
        "consumer_name",
        "address",
        "applicant_contact",
    ],
    "gas_bill_overcharging": [
        "provider",
        "reference_or_customer_number",
        "bill_month",
        "amount_charged",
        "current_meter_reading",
        "meter_photo_available",
        "city",
        "consumer_name",
        "address",
        "applicant_contact",
    ],
    "water_bill_overcharging": [
        "provider",
        "consumer_or_account_number",
        "bill_month",
        "amount_charged",
        "current_meter_reading",
        "city",
        "consumer_name",
        "address",
        "applicant_contact",
    ],
    "workplace_harassment_women": [
        "immediate_safety_risk",
        "complainant_name",
        "workplace_name",
        "city",
        "nature_of_issue_high_level",
        "incident_dates",
        "accused_role",
        "evidence_or_witnesses",
        "internal_committee_available",
    ],
}


FIELD_QUESTIONS: dict[str, str] = {
    "incident_type": "Was it lost, stolen, or snatched?",
    "phone_model": "What is the phone model?",
    "last_known_location": "What was the last known location?",
    "incident_date_time": "When did it happen?",
    "incident_description": (
        "Please describe the full incident in as much detail as possible. Include: "
        "exactly what happened step by step, what you were doing at the time, "
        "culprit description (face, height, clothing, how many people), "
        "any vehicle or bike (color, model, registration plate if you saw it), "
        "which direction they escaped, any CCTV cameras you noticed nearby, "
        "any witnesses, and any other relevant context (e.g. ride-hailing order, delivery). "
        "The more detail you give, the stronger your complaint will be."
    ),
    "imei": "Do you have the IMEI number? If not, check the phone box, purchase receipt, Google/Apple device info, or telecom/PTA records if available.",
    "sim_number_or_operator": "Which SIM/mobile operator was in the phone?",
    "city": "Which city and area are relevant?",
    "applicant_name": "What name should appear on the complaint draft?",
    "applicant_contact": "What is your contact number for follow-up?",
    "draft_language": "Do you want the complaint draft in English, Urdu, or Roman Urdu?",
    "vehicle_registration_number": "What is the vehicle registration or number plate?",
    "vehicle_model_color": "What is the vehicle model and color?",
    "provider": "Which provider handles the bill, for example IESCO, LESCO, K-Electric, SNGPL, SSGC, or WASA?",
    "reference_or_customer_number": "What is the bill reference, customer, or consumer number?",
    "consumer_or_account_number": "What is the water bill consumer/account number?",
    "bill_month": "Which bill month is disputed?",
    "amount_charged": "What amount was charged?",
    "current_meter_reading": "What is the current meter reading?",
    "meter_photo_available": "Do you have a clear current meter photo?",
    "consumer_name": "What consumer name appears on the bill?",
    "address": "What service address appears on the bill?",
    "immediate_safety_risk": "Are you in immediate danger right now?",
    "complainant_name": "What name should appear on the complaint draft?",
    "workplace_name": "What is the workplace or organization name?",
    "nature_of_issue_high_level": "At a high level, what happened? Please avoid graphic detail.",
    "incident_dates": "When did the incident or pattern happen?",
    "accused_role": "What is the accused person’s role or designation?",
    "evidence_or_witnesses": "Do you have evidence or witnesses, if any?",
    "internal_committee_available": "Does your workplace have an internal harassment inquiry committee?",
}


WORKPLACE_INTERVIEW_FIELDS = [
    "immediate_safety_risk",
    "complainant_name",
    "workplace_name",
    "nature_of_issue_high_level",
    "incident_dates",
    "accused_role",
    "evidence_or_witnesses",
    "internal_committee_available",
]


INCIDENT_TERMS = {
    "lost",
    "phone",
    "mobile",
    "stolen",
    "snatch",
    "snatched",
    "chori",
    "kho",
    "gum",
    "bill",
    "harassment",
}


YES_NO_VALUES = {
    "yes": "yes",
    "y": "yes",
    "yeah": "yes",
    "yep": "yes",
    "haan": "yes",
    "han": "yes",
    "no": "no",
    "n": "no",
    "nope": "no",
    "nah": "no",
    "nahi": "no",
    "nahin": "no",
}


def _line_with_date_time(lines: list[str]) -> str | None:
    for line in lines:
        if re.search(r"\b(today|yesterday|tomorrow|\d{1,2}:\d{2}\s?(?:am|pm)?)\b", line.lower()):
            return line
    return None


def _detailed_incident_line(lines: list[str]) -> str | None:
    for line in lines:
        lower = line.lower()
        word_count = len(re.findall(r"[A-Za-z0-9]+", line))
        if any(term in lower for term in ["snatch", "snatched", "stolen", "chori"]):
            if word_count >= 4:
                return line
        if any(term in lower for term in ["lost", "kho", "gum"]):
            has_context = any(marker in lower for marker in [" from ", " near ", " while ", " when ", " at ", " in ", " on ", "pocket", "misplaced"])
            if has_context and word_count >= 5:
                return line
    return None


def _looks_like_person_name(line: str) -> bool:
    lower = line.lower().strip()
    words = lower.split()
    if not 2 <= len(words) <= 4:
        return False
    if any(term in lower for term in INCIDENT_TERMS):
        return False
    if any(term in lower for term in ["english", "urdu", "roman", "jazz", "zong", "telenor", "ufone", "samsung", "redmi", "iphone"]):
        return False
    return bool(re.fullmatch(r"[A-Za-z][A-Za-z .'-]{2,70}", line.strip()))


def _normalize_yes_no(value: str) -> str:
    lower = value.lower().strip().rstrip(".")
    return YES_NO_VALUES.get(lower, value.strip())


def _fill_workplace_harassment_fields(lines: list[str], lower: str, updated: dict[str, Any]) -> None:
    if not lines:
        return

    missing_interview_fields = [field for field in WORKPLACE_INTERVIEW_FIELDS if not updated.get(field)]
    if len(lines) >= 2:
        for field, answer in zip(missing_interview_fields, lines):
            if field in {"immediate_safety_risk", "internal_committee_available"}:
                updated[field] = _normalize_yes_no(answer)
            else:
                updated[field] = answer.strip()
    elif len(lines) == 1:
        answer = lines[0].strip()
        normalized = _normalize_yes_no(answer)
        if normalized in {"yes", "no"} and not updated.get("immediate_safety_risk"):
            updated["immediate_safety_risk"] = normalized
        elif normalized in {"yes", "no"} and not updated.get("internal_committee_available"):
            updated["internal_committee_available"] = normalized
        elif len(missing_interview_fields) == 1:
            field = missing_interview_fields[0]
            updated[field] = normalized if field in {"immediate_safety_risk", "internal_committee_available"} else answer

    if not updated.get("evidence_or_witnesses") and any(
        term in lower
        for term in ["video", "recording", "audio", "screenshot", "message", "email", "witness", "proof", "evidence"]
    ):
        updated["evidence_or_witnesses"] = lines[0].strip()

    if not updated.get("internal_committee_available"):
        committee_match = re.search(
            r"\b(yes|no|yeah|yep|nope|nah|haan|han|nahi|nahin)\b.*\binternal\b.*\bcommittee\b",
            lower,
        )
        if committee_match:
            updated["internal_committee_available"] = _normalize_yes_no(committee_match.group(1))


def _infer_residence_status(lower: str) -> str | None:
    if re.search(r"\b(rented|renting|tenant|tenancy|kiraye|kiraya)\b", lower):
        return "rented"
    if re.search(r"\b(my\s+own|owned|ownership)\b.*\b(home|house|flat|apartment|property|residence)\b", lower):
        return "owned"
    if re.search(r"\b(home|house|flat|apartment|property|residence)\b.*\b(my\s+own|owned|ownership)\b", lower):
        return "owned"
    return None


def infer_fields_from_message(message: str, existing: dict[str, Any], subcategory: str | None) -> dict[str, Any]:
    text = message.strip()
    lower = text.lower()
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    updated = dict(existing)

    if subcategory:
        updated.setdefault("subcategory", subcategory)

    if any(term in lower for term in ["lost", "kho", "gum", "گم"]):
        updated["incident_type"] = "lost"
    if any(term in lower for term in ["stolen", "chori", "snatch", "snatched", "چھین", "چوری"]):
        updated["incident_type"] = "stolen"
    detailed_incident = _detailed_incident_line(lines)
    if detailed_incident and any(term in detailed_incident.lower() for term in ["snatch", "snatched", "چھین"]):
        updated["incident_description"] = detailed_incident

    imei_match = re.search(r"\b\d{15}\b", text)
    if imei_match:
        updated["imei"] = imei_match.group(0)

    numbered_answers = {
        match.group("number"): match.group("answer").strip()
        for match in re.finditer(r"(?m)^\s*(?P<number>\d+)[.)]\s*(?P<answer>.+?)\s*$", text)
    }
    if subcategory in {"lost_phone", "stolen_phone"} and numbered_answers:
        if numbered_answers.get("1") and not updated.get("phone_model"):
            updated["phone_model"] = numbered_answers["1"]
        if numbered_answers.get("2") and not updated.get("last_known_location"):
            updated["last_known_location"] = numbered_answers["2"]
        if numbered_answers.get("3") and not updated.get("incident_date_time"):
            updated["incident_date_time"] = numbered_answers["3"]
        if numbered_answers.get("4") and not updated.get("imei"):
            imei_from_answer = re.search(r"\b\d{15}\b", numbered_answers["4"])
            if imei_from_answer:
                updated["imei"] = imei_from_answer.group(0)

    if subcategory in {"lost_phone", "stolen_phone"} and not updated.get("phone_model"):
        phone_model_match = re.search(
            r"\b(iphone|samsung|redmi|xiaomi|oppo|vivo|infinix|tecno|realme|huawei|nokia|pixel)[\w +-]{0,40}",
            lower,
        )
        if phone_model_match:
            updated["phone_model"] = phone_model_match.group(0).strip()

    if not updated.get("last_known_location"):
        location_match = re.search(
            r"\b(?:g|f|e|i)-?\s?\d{1,2}(?:/\d{1,2})?\b|(?:sector|area|near)\s+[\w\s/-]{2,60}",
            lower,
        )
        if location_match:
            updated["last_known_location"] = location_match.group(0).strip()

    date_time_line = _line_with_date_time(lines)
    if not updated.get("incident_date_time") and date_time_line:
        updated["incident_date_time"] = date_time_line

    if subcategory in {"lost_phone", "stolen_phone"} and not updated.get("incident_description"):
        if detailed_incident:
            updated["incident_description"] = detailed_incident

    if subcategory in {"lost_phone", "stolen_phone"} and not updated.get("applicant_name"):
        name_match = re.search(r"(?:my name is|name is|i am|i'm)\s+([a-z][a-z\s.'-]{2,60})", lower)
        if name_match:
            updated["applicant_name"] = name_match.group(1).strip().title()

    if not updated.get("applicant_contact"):
        contact_match = re.search(r"\b(?:\+92|0)?3\d{2}[- ]?\d{7}\b", text)
        if contact_match:
            updated["applicant_contact"] = contact_match.group(0)

    if subcategory in {"lost_phone", "stolen_phone"} and not updated.get("draft_language"):
        if "english" in lower:
            updated["draft_language"] = "english"
        elif "roman urdu" in lower:
            updated["draft_language"] = "roman_urdu"
        elif "urdu" in lower:
            updated["draft_language"] = "urdu"

    if not updated.get("amount_charged"):
        money_match = re.search(r"(?:rs\.?\s*|pkr\s*)(\d{3,8})|\b(\d{3,8})\b", lower)
        if money_match and "bill" in lower:
            updated["amount_charged"] = money_match.group(1) or money_match.group(2)

    if any(city in lower for city in ["karachi", "lahore", "islamabad", "rawalpindi", "peshawar", "quetta", "multan"]):
        for city in ["Karachi", "Lahore", "Islamabad", "Rawalpindi", "Peshawar", "Quetta", "Multan"]:
            if city.lower() in lower:
                updated["city"] = city
                break

    if any(provider in lower for provider in ["iesco", "lesco", "fesco", "k-electric", "ke", "sngpl", "ssgc", "wasa"]):
        for provider in ["IESCO", "LESCO", "FESCO", "K-Electric", "SNGPL", "SSGC", "WASA"]:
            if provider.lower() in lower:
                updated["provider"] = provider
                break

    residence_status = _infer_residence_status(lower)
    if residence_status:
        updated["residence_status"] = residence_status

    if subcategory in {"lost_phone", "stolen_phone"} and not updated.get("sim_number_or_operator"):
        operators = [operator for operator in ["Jazz", "Zong", "Telenor", "Ufone", "Onic", "SCO"] if operator.lower() in lower]
        if operators:
            updated["sim_number_or_operator"] = "/".join(operators)

    if subcategory in {"lost_phone", "stolen_phone"} and not updated.get("applicant_name"):
        for line in lines:
            if _looks_like_person_name(line):
                updated["applicant_name"] = line.strip()
                break

    if subcategory == "workplace_harassment_women":
        _fill_workplace_harassment_fields(lines, lower, updated)

    updated["latest_user_message"] = text
    return updated


_INCIDENT_DESCRIPTION_MIN_WORDS = 20


def get_missing_fields(subcategory: str | None, collected_data: dict[str, Any]) -> list[str]:
    if not subcategory:
        return []
    required = REQUIRED_FIELDS.get(subcategory, [])
    missing = []
    for field in required:
        value = collected_data.get(field)
        if not value:
            missing.append(field)
        elif field == "incident_description":
            word_count = len(str(value).split())
            if word_count < _INCIDENT_DESCRIPTION_MIN_WORDS:
                missing.append(field)
    return missing


def questions_for_fields(fields: list[str], limit: int = 4) -> list[str]:
    return [FIELD_QUESTIONS[field] for field in fields[:limit] if field in FIELD_QUESTIONS]
