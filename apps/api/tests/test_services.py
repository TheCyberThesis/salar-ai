from app.services.complaint_classifier import classify_complaint
from app.services.missing_fields import get_missing_fields, infer_fields_from_message, questions_for_fields
from app.services.privacy import mask_sensitive_text
from app.services.report_generator import apply_department_location, generate_report


def test_lost_phone_roman_urdu_classification() -> None:
    result = classify_complaint("Mera phone kho gaya hai")
    assert result.detected_language == "roman_urdu"
    assert result.domain == "lost_or_stolen_vehicle_device"
    assert result.subcategory == "lost_phone"


def test_stolen_bike_classification() -> None:
    result = classify_complaint("Meri bike chori ho gayi hai")
    assert result.subcategory == "stolen_bike"


def test_electricity_overbilling_classification() -> None:
    result = classify_complaint("Mera bijli ka bill bohat zyada aa gaya hai")
    assert result.domain == "utility_bill_overcharging"
    assert result.subcategory == "electricity_bill_overcharging"


def test_workplace_harassment_classification() -> None:
    result = classify_complaint("Mujhe office mein harassment face karni par rahi hai")
    assert result.domain == "workplace_harassment_women"
    assert result.emergency_level == "high"


def test_unsupported_domain() -> None:
    result = classify_complaint("Mujhe passport renew karwana hai")
    assert result.domain == "unsupported"


def test_missing_fields_for_phone() -> None:
    missing = get_missing_fields("lost_phone", {"incident_type": "lost"})
    assert "imei" in missing
    assert "city" in missing
    questions = questions_for_fields(missing, limit=len(missing))
    assert questions[0].startswith("Explain the full incident in detail")


def test_numbered_phone_answers_are_collected() -> None:
    collected = infer_fields_from_message(
        "1. redmi note 14\n2. G11/1, Islamabad\n3. today at 8:13 am\n4. 359621004856035",
        {"incident_type": "lost"},
        "lost_phone",
    )
    assert collected["phone_model"] == "redmi note 14"
    assert collected["last_known_location"] == "G11/1, Islamabad"
    assert collected["incident_date_time"] == "today at 8:13 am"
    assert collected["imei"] == "359621004856035"


def test_multiline_snatching_details_are_collected() -> None:
    collected = infer_fields_from_message(
        "redmi note 14\ng10/1 islamabad\na person on bike snatched it from me when i was waiting for my indrive ride\n359621004856035",
        {"incident_type": "lost"},
        "lost_phone",
    )
    assert collected["incident_type"] == "stolen"
    assert collected["phone_model"] == "redmi note 14"
    assert collected["last_known_location"] == "g10/1"
    assert collected["city"] == "Islamabad"
    assert "snatched" in collected["incident_description"]
    assert collected["imei"] == "359621004856035"


def test_vague_lost_phone_message_does_not_fill_report_narrative_or_name() -> None:
    collected = infer_fields_from_message("i have lost my phone", {}, "lost_phone")
    assert collected["incident_type"] == "lost"
    assert "incident_description" not in collected
    assert "applicant_name" not in collected

    missing = get_missing_fields("lost_phone", {**collected, "city": "Islamabad"})
    assert "incident_description" in missing
    assert "applicant_name" in missing


def test_privacy_masking() -> None:
    masked = mask_sensitive_text("CNIC 3520212345671 phone 03001234567")
    assert "XXXXX-XXXXXXX-X" in masked
    assert "03XX-XXXXXXX" in masked


def test_report_uses_resolved_police_station_and_sho() -> None:
    session = {
        "id": "11111111-1111-1111-1111-111111111111",
        "category": "lost_or_stolen_vehicle_device",
        "subcategory": "lost_phone",
        "location": {"city": "Islamabad", "area": "G-11/1"},
        "collected_data": {
            "incident_type": "lost",
            "phone_model": "Redmi Note 14",
            "last_known_location": "G-11/1, Islamabad",
            "incident_date_time": "today at 8:13 am",
            "incident_description": "A person on a bike snatched it while I was waiting for my ride.",
            "imei": "359621004856035",
            "sim_number_or_operator": "Jazz/Zong",
            "city": "Islamabad",
            "applicant_name": "Muhammad Haris",
            "applicant_contact": "03001234567",
            "draft_language": "english",
        },
    }
    report = generate_report(session)
    report = apply_department_location(
        report,
        {
            "place_name": "Model Police Station Ramna",
            "address": "G-11 Markaz, Islamabad",
            "phone_number": "(051) 9330189",
            "latitude": 33.6667193,
            "longitude": 72.9965259,
            "google_maps_place_id": "ChIJG97Wiv6V3zgR11k_bUFsq2c",
            "maps_link": "https://maps.google.com/?cid=7470183435185641943",
            "notes": "Google Places Text Search result.",
        },
        session,
    )

    assert report["issue_type"] == "Lost mobile phone report"
    assert report["reporting_office"] == "Model Police Station Ramna"
    assert report["report_recipient"] == "Station House Officer (SHO)"
    assert "The Station House Officer (SHO)" in report["complaint_draft"]
    assert "Model Police Station Ramna" in report["complaint_draft"]
    assert "Redmi Note 14" in report["complaint_draft"]
    assert "359621004856035" in report["complaint_draft"]
    assert "03001234567" in report["complaint_draft"]
    assert "A person on a bike snatched it" in report["complaint_draft"]
    assert "[not provided]" not in report["complaint_draft"]
    assert "[Insert" not in report["complaint_draft"]
