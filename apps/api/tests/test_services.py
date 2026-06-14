import asyncio
from unittest.mock import patch

from app.ai.base import LLMResponseError
from app.services.ai_assistant import enhance_report_with_ai, generate_guidance_reply
from app.services.complaint_classifier import classify_complaint
from app.services.missing_fields import get_missing_fields, infer_fields_from_message, questions_for_fields
from app.services.privacy import mask_sensitive_text
from app.services.report_generator import apply_department_location, generate_report


def _complete_phone_session() -> dict:
    return {
        "id": "11111111-1111-1111-1111-111111111111",
        "category": "lost_or_stolen_vehicle_device",
        "subcategory": "stolen_phone",
        "detected_language": "english",
        "location": {"city": "Islamabad", "area": "G-11/1"},
        "collected_data": {
            "incident_type": "stolen",
            "phone_model": "Redmi Note 14",
            "last_known_location": "Street 41, G-11/1, Islamabad",
            "incident_date_time": "today at 8:13 am",
            "incident_description": (
                "The phone was snatched from my hand while I was waiting for my ride. "
                "The rider wore a black helmet and jacket, came on a 125cc bike at high speed, "
                "had no number plate, escaped toward Street 42, and two CCTV cameras were nearby."
            ),
            "imei": "359621004856035",
            "sim_number_or_operator": "Jazz/Zong",
            "city": "Islamabad",
            "applicant_name": "Muhammad Haris",
            "applicant_contact": "03001234567",
            "draft_language": "english",
        },
    }


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


def test_workplace_harassment_multiline_answers_are_collected() -> None:
    collected = infer_fields_from_message(
        (
            "NO\n"
            "Alina Nawaz\n"
            "Jazz headquarters F8 markaz islamabad\n"
            "My boss tried to touch me inappropriately\n"
            "tomorrow at 3:30pm after launch\n"
            "Project lead"
        ),
        {"city": "Islamabad"},
        "workplace_harassment_women",
    )

    assert collected["immediate_safety_risk"] == "no"
    assert collected["complainant_name"] == "Alina Nawaz"
    assert collected["workplace_name"] == "Jazz headquarters F8 markaz islamabad"
    assert collected["nature_of_issue_high_level"] == "My boss tried to touch me inappropriately"
    assert collected["incident_dates"] == "tomorrow at 3:30pm after launch"
    assert collected["accused_role"] == "Project lead"
    assert get_missing_fields("workplace_harassment_women", collected) == [
        "evidence_or_witnesses",
        "internal_committee_available",
    ]

    collected = infer_fields_from_message("yes", collected, "workplace_harassment_women")
    assert collected["internal_committee_available"] == "yes"
    assert get_missing_fields("workplace_harassment_women", collected) == ["evidence_or_witnesses"]

    collected = infer_fields_from_message(
        "yes i have a video of him harrassing me\nno i haven't initiated a complain in internal committee",
        collected,
        "workplace_harassment_women",
    )
    assert collected["evidence_or_witnesses"] == "yes i have a video of him harrassing me"
    assert get_missing_fields("workplace_harassment_women", collected) == []


def test_workplace_single_no_answers_immediate_safety_first() -> None:
    collected = infer_fields_from_message("NO", {}, "workplace_harassment_women")

    assert collected["immediate_safety_risk"] == "no"
    assert "internal_committee_available" not in collected


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


def test_required_documents_include_rented_residence_proof() -> None:
    session = _complete_phone_session()
    session["collected_data"] = infer_fields_from_message(
        "I live in a rented house as a tenant.",
        session["collected_data"],
        "stolen_phone",
    )

    report = generate_report(session)

    assert "CNIC copy" in report["required_documents"]
    assert any("tenant/rented" in document for document in report["required_documents"])
    assert any("rent or tenancy agreement" in document for document in report["required_documents"])


def test_required_documents_include_owned_residence_proof() -> None:
    session = _complete_phone_session()
    session["subcategory"] = "electricity_bill_overcharging"
    session["category"] = "utility_bill_overcharging"
    session["collected_data"] = {
        "provider": "IESCO",
        "reference_or_customer_number": "123456789",
        "bill_month": "June 2026",
        "amount_charged": "12000",
        "current_meter_reading": "4567",
        "meter_photo_available": "yes",
        "city": "Islamabad",
        "consumer_name": "Muhammad Haris",
        "address": "G-11/1 Islamabad",
        "residence_status": "owned",
    }

    report = generate_report(session)

    assert "CNIC copy" in report["required_documents"]
    assert any("residency/residence and ownership" in document for document in report["required_documents"])
    assert any("registry" in document and "allotment" in document for document in report["required_documents"])


def test_required_documents_include_residency_proof_for_workplace_complaint() -> None:
    session = {
        "id": "22222222-2222-2222-2222-222222222222",
        "category": "workplace_harassment_women",
        "subcategory": "workplace_harassment_women",
        "location": {"city": "Islamabad"},
        "collected_data": {
            "immediate_safety_risk": "no",
            "complainant_name": "Alina Nawaz",
            "workplace_name": "Jazz headquarters F8 markaz islamabad",
            "city": "Islamabad",
            "nature_of_issue_high_level": "My boss tried to touch me inappropriately",
            "incident_dates": "tomorrow at 3:30pm after lunch",
            "accused_role": "Project lead",
            "evidence_or_witnesses": "video evidence",
            "internal_committee_available": "yes",
        },
    }

    report = generate_report(session)

    assert "CNIC copy" in report["required_documents"]
    assert any("Proof of residency/residence" in document for document in report["required_documents"])


def test_report_uses_resolved_police_station_and_sho() -> None:
    session = _complete_phone_session()
    session["subcategory"] = "lost_phone"
    session["collected_data"]["incident_type"] = "lost"
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
    assert "The phone was snatched" in report["complaint_draft"]
    assert "[not provided]" not in report["complaint_draft"]
    assert "[Insert" not in report["complaint_draft"]


def test_ai_report_enhancement_rewrites_summary_and_complaint_draft() -> None:
    session = _complete_phone_session()
    report = generate_report(session)

    async def fake_generate(*args, **kwargs) -> str:
        return (
            "{"
            '"summary": "AI-polished summary for a phone snatching at Street 41, G-11/1, Islamabad.",'
            '"complaint_draft": "To,\\nThe Station House Officer (SHO),\\n\\n'
            'Subject: Application regarding mobile phone snatching\\n\\nRespected Sir/Madam,\\n'
            'I respectfully submit that my mobile phone was snatched at Street 41, G-11/1, Islamabad while I was waiting for my ride. '
            'The offender was wearing a black helmet and jacket, used a 125cc motorcycle without a number plate, and escaped towards Street 42. '
            'Two CCTV cameras are present near the place of occurrence.\\n\\n'
            'I request that my complaint be registered and that a diary number, complaint number, FIR/reference number, or stamped receiving copy be issued."'
            "}"
        )

    with patch("app.services.ai_assistant.generate_chat_reply", side_effect=fake_generate) as generated:
        updated = asyncio.run(enhance_report_with_ai(report, session))

    assert generated.called
    assert updated["summary"].startswith("AI-polished summary")
    assert "The offender was wearing a black helmet and jacket" in updated["complaint_draft"]
    assert session["collected_data"]["incident_description"] != updated["complaint_draft"]


def test_ai_report_enhancement_rejects_invalid_llm_response() -> None:
    session = _complete_phone_session()
    report = generate_report(session)

    async def fake_generate(*args, **kwargs) -> str:
        return "not json"

    with patch("app.services.ai_assistant.generate_chat_reply", side_effect=fake_generate):
        try:
            asyncio.run(enhance_report_with_ai(report, session))
        except LLMResponseError:
            return

    assert False, "Invalid LLM report output should fail instead of returning a template report."


def test_guidance_reply_uses_fallback_when_fields_are_missing() -> None:
    fallback = "Please answer the remaining evidence question."

    async def fake_generate(*args, **kwargs) -> str:
        return "You can generate your report now."

    with patch("app.services.ai_assistant.generate_chat_reply", side_effect=fake_generate) as generated:
        reply = asyncio.run(
            generate_guidance_reply(
                user_message="yes",
                detected_language="english",
                category="workplace_harassment_women",
                subcategory="workplace_harassment_women",
                stage="collecting_missing_info",
                missing_fields=["evidence_or_witnesses"],
                follow_up_questions=["Do you have evidence or witnesses, if any?"],
                sources=[],
                fallback_reply=fallback,
            )
        )

    assert reply == fallback
    assert not generated.called
