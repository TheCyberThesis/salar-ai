from fastapi import HTTPException


def validate_message_length(message: str, max_length: int = 4000) -> None:
    if not message.strip():
        raise HTTPException(status_code=422, detail="Message cannot be empty.")
    if len(message) > max_length:
        raise HTTPException(status_code=413, detail="Message is too long.")
