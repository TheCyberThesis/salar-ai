import re
from typing import Any


CNIC_RE = re.compile(r"\b\d{5}-?\d{7}-?\d\b")
PHONE_RE = re.compile(r"\b(?:\+92|0)?3\d{2}[- ]?\d{7}\b")


def mask_sensitive_text(value: str) -> str:
    value = CNIC_RE.sub("XXXXX-XXXXXXX-X", value)
    value = PHONE_RE.sub("03XX-XXXXXXX", value)
    return value


def mask_sensitive_data(data: dict[str, Any]) -> dict[str, Any]:
    masked: dict[str, Any] = {}
    for key, value in data.items():
        if isinstance(value, str):
            masked[key] = mask_sensitive_text(value)
        else:
            masked[key] = value
    return masked
