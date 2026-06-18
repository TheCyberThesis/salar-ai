from dataclasses import dataclass

from app.services.language_detector import detect_language


@dataclass(frozen=True)
class Classification:
    detected_language: str
    domain: str
    subcategory: str | None
    confidence: float
    emergency_level: str


SUPPORTED_CATEGORIES = [
    "lost_phone",
    "stolen_phone",
    "lost_bike",
    "stolen_bike",
    "lost_car",
    "stolen_car",
    "electricity_bill_overcharging",
    "gas_bill_overcharging",
    "water_bill_overcharging",
    "workplace_harassment_women",
]


def _has_any(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def classify_complaint(message: str, language_hint: str | None = None) -> Classification:
    text = message.lower()
    language = detect_language(message, language_hint)

    lost_terms = ["lost", "kho", "gum", "missing", "گم", "کھو"]
    stolen_terms = ["stolen", "snatch", "snatched", "chori", "چوری", "چھین"]
    phone_terms = ["phone", "mobile", "device", "imei", "فون", "موبائل"]
    bike_terms = ["bike", "motorcycle", "motor bike", "موٹر سائیکل", "موٹرسائیکل"]
    car_terms = ["car", "vehicle", "گاڑی", "کار"]

    if _has_any(text, phone_terms) and (_has_any(text, lost_terms) or _has_any(text, stolen_terms)):
        stolen = _has_any(text, stolen_terms)
        return Classification(
            language,
            "lost_or_stolen_vehicle_device",
            "stolen_phone" if stolen else "lost_phone",
            0.91,
            "medium",
        )

    if _has_any(text, bike_terms) and (_has_any(text, lost_terms) or _has_any(text, stolen_terms)):
        stolen = _has_any(text, stolen_terms)
        return Classification(
            language,
            "lost_or_stolen_vehicle_device",
            "stolen_bike" if stolen else "lost_bike",
            0.9,
            "medium",
        )

    if _has_any(text, car_terms) and (_has_any(text, lost_terms) or _has_any(text, stolen_terms)):
        stolen = _has_any(text, stolen_terms)
        return Classification(
            language,
            "lost_or_stolen_vehicle_device",
            "stolen_car" if stolen else "lost_car",
            0.89,
            "medium",
        )

    if _has_any(text, ["electricity", "bijli", "lesco", "iesco", "k-electric", "ke ", "بجلی"]):
        return Classification(language, "utility_bill_overcharging", "electricity_bill_overcharging", 0.88, "low")

    if _has_any(text, ["gas", "sui", "sngpl", "ssgc", "گیس"]):
        return Classification(language, "utility_bill_overcharging", "gas_bill_overcharging", 0.86, "low")

    if _has_any(text, ["water", "wasa", "pani", "پانی"]):
        return Classification(language, "utility_bill_overcharging", "water_bill_overcharging", 0.82, "low")

    bill_terms = ["bill", "بل"]
    overcharge_terms = ["zyada", "ziada", "ziyada", "bohat", "overcharge", "mehnga", "zada", "zyada", "غلط", "زیادہ", "high", "extra"]
    if _has_any(text, bill_terms) and _has_any(text, overcharge_terms):
        return Classification(language, "utility_bill_overcharging", "electricity_bill_overcharging", 0.78, "low")

    if _has_any(text, ["harassment", "harass", "harras", "office", "workplace", "boss", "colleague", "ہراسانی"]):
        return Classification(language, "workplace_harassment_women", "workplace_harassment_women", 0.87, "high")

    return Classification(language, "unsupported", None, 0.42, "low")
