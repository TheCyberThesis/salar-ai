import re


URDU_RE = re.compile(r"[\u0600-\u06ff]")
ROMAN_URDU_WORDS = {
    "mera",
    "meri",
    "mujhe",
    "kho",
    "gaya",
    "gayi",
    "chori",
    "bijli",
    "bill",
    "bohat",
    "zyada",
    "office",
    "mein",
    "karni",
    "par",
    "rahi",
}


def detect_language(message: str, language_hint: str | None = None) -> str:
    if language_hint:
        return language_hint
    if URDU_RE.search(message):
        return "urdu"
    tokens = {token.lower() for token in re.findall(r"[A-Za-z']+", message)}
    if tokens & ROMAN_URDU_WORDS:
        return "roman_urdu"
    return "english"
