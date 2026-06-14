import re


URDU_RE = re.compile(r"[\u0600-\u06ff]")

# Words that are distinctly Roman Urdu and not common standalone English words
ROMAN_URDU_WORDS = {
    # possessives / pronouns
    "mera", "meri", "mere", "mujhe", "mujko",
    "aap", "apna", "apni", "apne",
    "unka", "unki", "unke",
    "hamara", "hamari", "hamare",
    "tumhara", "tumhari", "tumhare",
    "yeh", "woh",
    # verbs & auxiliaries
    "hai", "hain", "tha", "thi",
    "karo", "karna", "karta", "karti", "karte",
    "karni", "karunga", "karoungi",
    "raha", "rahi", "rahe",
    "hoga", "hogi", "honge",
    "aaya", "aayi", "aana",
    "gaya", "gayi", "jana", "jata", "jati",
    "lena", "dena",
    "chahiye", "chahta", "chahte", "chahti",
    # negation
    "nahi", "nahin", "nhi",
    # connectors / question words
    "aur", "lekin", "magar", "kyunke", "warna",
    "kya", "kyun", "kab", "kaun", "kahan", "kitna", "kitni",
    "jahan", "wahan", "yahan", "jab", "tab",
    "phir",
    # common adjectives / adverbs
    "mein", "bohat", "bahut", "zyada", "thoda", "zara",
    "theek", "thik", "sahi",
    "zaroor", "bilkul",
    "jaldi",
    "sirf", "bhi",
    "abhi", "aaj", "kal",
    "pehle", "baad",
    "poora", "puri",
    "kuch", "sab",
    # common nouns
    "ghar", "kaam", "raat", "subah", "sham",
    "paisa", "paise",
    "mushkil",
    "matlab",
    "darkhwast", "shukriya",
    "achha", "acha",
    "wala", "wali", "wale",
    "liya", "diya",
    "banda", "bande",
    "pata", "maloom",
    # civic-specific Roman Urdu
    "bijli", "chori", "kho",
}

# Minimum unique Roman Urdu token matches to confidently classify as Roman Urdu
_MIN_ROMAN_URDU_TOKENS = 1


def detect_language(message: str, language_hint: str | None = None) -> str:
    if language_hint:
        return language_hint
    if URDU_RE.search(message):
        return "urdu"
    tokens = {token.lower() for token in re.findall(r"[A-Za-z']+", message)}
    if len(tokens & ROMAN_URDU_WORDS) >= _MIN_ROMAN_URDU_TOKENS:
        return "roman_urdu"
    return "english"
