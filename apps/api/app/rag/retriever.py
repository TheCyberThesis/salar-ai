from app.seed.knowledge_seed import KNOWLEDGE_CHUNKS


def retrieve_knowledge(category: str, subcategory: str | None = None, *, city: str | None = None, limit: int = 4) -> list[dict[str, str | None]]:
    matches = []
    for chunk in KNOWLEDGE_CHUNKS:
        if chunk["category"] == category or chunk.get("subcategory") == subcategory:
            if chunk.get("city") and city and chunk["city"].lower() != city.lower():
                continue
            matches.append(chunk)
    if not matches:
        matches = [chunk for chunk in KNOWLEDGE_CHUNKS if chunk["category"] == category]
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
