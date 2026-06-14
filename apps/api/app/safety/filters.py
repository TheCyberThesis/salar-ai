from app.services.privacy import mask_sensitive_text


def apply_output_safety(text: str) -> str:
    return mask_sensitive_text(text)
