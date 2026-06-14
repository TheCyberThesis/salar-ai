from hashlib import sha256


def mock_embedding(text: str, dimensions: int = 768) -> list[float]:
    """Deterministic local embedding placeholder for tests/dev without API keys."""
    digest = sha256(text.encode("utf-8")).digest()
    values: list[float] = []
    while len(values) < dimensions:
        for byte in digest:
            values.append((byte / 255.0) * 2 - 1)
            if len(values) == dimensions:
                break
        digest = sha256(digest).digest()
    return values
