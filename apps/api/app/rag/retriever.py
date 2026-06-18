from app.seed.knowledge_seed import KNOWLEDGE_CHUNKS


def retrieve_knowledge(category: str, subcategory: str | None = None, *, city: str | None = None, provider: str | None = None, limit: int = 4) -> list[dict[str, str | None]]:
    provider_lower = provider.lower() if provider else None
    matches = []
    for chunk in KNOWLEDGE_CHUNKS:
        if chunk["category"] == category or chunk.get("subcategory") == subcategory:
            if chunk.get("city") and city and chunk["city"].lower() != city.lower():
                continue
            # Skip provider-specific chunks that don't match the user's provider
            if chunk.get("provider") and provider_lower and chunk["provider"].lower() != provider_lower:
                continue
            matches.append(chunk)
    if not matches:
        matches = [chunk for chunk in KNOWLEDGE_CHUNKS if chunk["category"] == category]
    # Sort: provider-specific chunks first, then generic
    if provider_lower:
        matches.sort(key=lambda c: 0 if c.get("provider", "").lower() == provider_lower else 1)
    return [
        {
            "title": chunk["title"],
            "source_name": chunk["source_name"],
            "authority_type": chunk.get("source_type"),
            "jurisdiction": chunk["jurisdiction"],
            "source_url": chunk.get("source_url"),
            "verified_at": chunk.get("verified_at"),
            "confidence_level": chunk.get("confidence_level", "official_source_metadata"),
        }
        for chunk in matches[:limit]
    ]
