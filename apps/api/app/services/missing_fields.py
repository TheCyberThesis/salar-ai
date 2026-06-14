import re
from typing import Any


REQUIRED_FIELDS: dict[str, list[str]] = {
    "lost_phone": [
        "incident_type",
        "phone_model",
        "last_known_location",
        "incident_date_time",
        "imei",
        "sim_number_or_operator",
        "city",
        "applicant_name",
        "draft_language",
    ],
    "stolen_phone": [
        "incident_type",
        "phone_model",
        "last_known_location",
        "incident_date_time",
        "imei",
        "sim_number_or_operator",
        "city",
        "applicant_name",
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
    "imei": "Do you have the IMEI number? If not, check the phone box, purchase receipt, Google/Apple device info, or telecom/PTA records if available.",
    "sim_number_or_operator": "Which SIM/mobile operator was in the phone?",
    "city": "Which city and area are relevant?",
    "applicant_name": "What name should appear on the complaint draft?",
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


def infer_fields_from_message(message: str, existing: dict[str, Any], subcategory: str | None) -> dict[str, Any]:
    text = message.strip()
    lower = text.lower()
    updated = dict(existing)

    if subcategory:
        updated.setdefault("subcategory", subcategory)

    if any(term in lower for term in ["lost", "kho", "gum", "گم"]):
        updated["incident_type"] = "lost"
    if any(term in lower for term in ["stolen", "chori", "snatch", "چوری"]):
        updated["incident_type"] = "stolen"

    imei_match = re.search(r"\b\d{15}\b", text)
    if imei_match:
        updated["imei"] = imei_match.group(0)

    money_match = re.search(r"(?:rs\.?|pkr)?\s?(\d{3,8})", lower)
    if money_match and "bill" in lower:
        updated["amount_charged"] = money_match.group(1)

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

    updated["latest_user_message"] = text
    return updated


def get_missing_fields(subcategory: str | None, collected_data: dict[str, Any]) -> list[str]:
    if not subcategory:
        return []
    required = REQUIRED_FIELDS.get(subcategory, [])
    return [field for field in required if not collected_data.get(field)]


def questions_for_fields(fields: list[str], limit: int = 4) -> list[str]:
    return [FIELD_QUESTIONS[field] for field in fields[:limit] if field in FIELD_QUESTIONS]
