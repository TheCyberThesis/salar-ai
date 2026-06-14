from typing import Any
from datetime import date


def _value(data: dict[str, Any], key: str, fallback: str = "[not provided]") -> str:
    value = data.get(key)
    return str(value) if value else fallback


def _line(label: str, value: str) -> str:
    return f"- {label}: {value}"


def generate_complaint_draft(
    subcategory: str | None,
    data: dict[str, Any],
    *,
    reporting_office: str | None = None,
    report_recipient: str | None = None,
    office_address: str | None = None,
) -> str:
    if subcategory in {"lost_phone", "stolen_phone", "lost_bike", "stolen_bike", "lost_car", "stolen_car"}:
        item = "mobile phone" if "phone" in subcategory else "vehicle"
        incident_word = "snatched/stolen" if data.get("incident_type") == "stolen" or "stolen" in subcategory else "lost"
        subject = f"Application for report of {incident_word} {item}"
        office = reporting_office or "Relevant Police Station"
        recipient = report_recipient or "Station House Officer"
        provided_details = [
            _line("Applicant name", _value(data, "applicant_name")),
            _line("Applicant contact", _value(data, "applicant_contact")),
            _line("Incident type", incident_word),
            _line("Incident location", _value(data, "last_known_location")),
            _line("Incident date/time", _value(data, "incident_date_time")),
            _line("Incident description", _value(data, "incident_description")),
            _line("City", _value(data, "city")),
            _line("Phone/vehicle model", _value(data, "phone_model", _value(data, "vehicle_model_color"))),
            _line("IMEI/registration number", _value(data, "imei", _value(data, "vehicle_registration_number"))),
            _line("SIM/operator", _value(data, "sim_number_or_operator")),
        ]
        action_request = (
            "register my complaint/FIR or other applicable police report, take action according to law, and issue me a diary number, "
            "complaint number, FIR/reference number, or stamped receiving copy"
            if incident_word == "snatched/stolen"
            else "record my loss report and issue me a diary number, complaint/report number, or stamped receiving copy"
        )
        return f"""To,
The {recipient},
{office},
{_value(data, "city")}
{office_address or ""}

Subject: {subject}

Respected Sir/Madam,

I, {_value(data, "applicant_name")}, respectfully submit that my {item} was {incident_word} near {_value(data, "last_known_location")} on/around {_value(data, "incident_date_time")}.

Incident narrative:
{_value(data, "incident_description")}

Details already collected:
{chr(10).join(provided_details)}

I request you to kindly {action_request}. I also need the official report/reference for blocking the SIM(s), blocking the IMEI/device through the relevant channels, and protecting my personal data.

Applicant signature: __________________
Contact number: {_value(data, "applicant_contact")}
Date: {date.today().isoformat()}
"""

    if subcategory in {"electricity_bill_overcharging", "gas_bill_overcharging", "water_bill_overcharging"}:
        utility = "utility provider/customer service center"
        return f"""To,
The Customer Service / Complaint Officer,
{_value(data, "provider", utility)}

Subject: Request for review/correction of overcharged utility bill

Respected Sir/Madam,

I, {_value(data, "consumer_name")}, request review of my utility bill for {_value(data, "bill_month")}. My reference/customer number is {_value(data, "reference_or_customer_number", _value(data, "consumer_or_account_number"))}. The charged amount is {_value(data, "amount_charged")}, which appears incorrect based on my current meter reading and previous usage.

Please review the bill, inspect/correct the meter reading where required, and issue a complaint/reference number for tracking.

Attached/available documents:
- Current bill copy
- Previous bill copy
- Current meter reading photo
- CNIC/contact details if required by the provider

Applicant signature: __________________
Contact number: __________________
Date: __________________
"""

    if subcategory == "workplace_harassment_women":
        return f"""To,
The Inquiry Committee / Competent Authority,
{_value(data, "workplace_name")}

Subject: Complaint regarding workplace harassment

Respected Sir/Madam,

I, {_value(data, "complainant_name")}, request confidential handling of my complaint regarding workplace harassment at {_value(data, "workplace_name")} in {_value(data, "city")}. At a high level, the issue is: {_value(data, "nature_of_issue_high_level")}.

The incident/pattern occurred on/around {_value(data, "incident_dates")}. The accused person’s role/designation is {_value(data, "accused_role")}. Evidence or witnesses available: {_value(data, "evidence_or_witnesses")}.

I request that this complaint be formally received, kept confidential, and processed through the relevant workplace inquiry procedure or competent authority. Please issue a receiving copy, complaint number, or reference number.

Applicant signature: __________________
Date: __________________

Note: For serious legal action or urgent safety concerns, please contact the relevant authority or a qualified lawyer.
"""

    return "A complaint draft can be generated after the complaint category is identified."
