from app.services.complaint_classifier import classify_complaint
from app.services.missing_fields import get_missing_fields
from app.services.privacy import mask_sensitive_text


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


def test_privacy_masking() -> None:
    masked = mask_sensitive_text("CNIC 3520212345671 phone 03001234567")
    assert "XXXXX-XXXXXXX-X" in masked
    assert "03XX-XXXXXXX" in masked
