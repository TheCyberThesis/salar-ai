import json
import logging

from app.ai.base import AIMessage
from app.ai.provider_factory import generate_text_with_fallback
from app.seed.verified_sources import VERIFIED_SOURCES

logger = logging.getLogger(__name__)

_SOURCE_BY_ID: dict[str, dict] = {s["id"]: s for s in VERIFIED_SOURCES}

_COMPACT_INDEX = [
    {
        "id": s["id"],
        "name": s["source_name"],
        "category": s["category"],
        "subcategory": s.get("subcategory"),
        "source_type": s["source_type"],
        "provider": s.get("provider"),
        "jurisdiction": s["jurisdiction"],
        "province": s.get("province"),
        "city": s.get("city"),
    }
    for s in VERIFIED_SOURCES
]

_CITY_PROVINCE: dict[str, str] = {
    "karachi": "Sindh",
    "hyderabad": "Sindh",
    "sukkur": "Sindh",
    "lahore": "Punjab",
    "faisalabad": "Punjab",
    "multan": "Punjab",
    "rawalpindi": "Punjab",
    "gujranwala": "Punjab",
    "sialkot": "Punjab",
    "islamabad": "Islamabad Capital Territory",
    "peshawar": "Khyber Pakhtunkhwa",
    "abbottabad": "Khyber Pakhtunkhwa",
    "mardan": "Khyber Pakhtunkhwa",
    "quetta": "Balochistan",
}


def _infer_province(city: str | None) -> str | None:
    if not city:
        return None
    return _CITY_PROVINCE.get(city.lower())


async def select_sources(
    *,
    category: str,
    subcategory: str | None,
    city: str | None,
    provider: str | None,
) -> list[dict]:
    province = _infer_province(city)

    # Match by subcategory when known; fall back to category-only when subcategory is None
    if subcategory:
        pool = [
            s for s in _COMPACT_INDEX
            if s["category"] == category
            and (s.get("subcategory") == subcategory or s.get("subcategory") is None)
        ]
    else:
        pool = [s for s in _COMPACT_INDEX if s["category"] == category]

    # When provider is known, exclude competing providers from the pool entirely
    if provider:
        provider_lower = provider.lower()
        pool = [
            s for s in pool
            if not s.get("provider") or s["provider"].lower() == provider_lower
        ]

    if not pool:
        return []

    prompt = f"""Select the most relevant official Pakistani sources for this civic complaint from the verified list below.

Complaint context:
- Category: {category}
- Subcategory: {subcategory or "not specified"}
- City: {city or "not specified"}
- Province: {province or "not specified"}
- Utility/service provider: {provider or "not specified"}

Verified sources available (JSON):
{json.dumps(pool, ensure_ascii=False)}

Rules:
- Always include the national regulator (NEPRA / OGRA / FOSPAH / PTA) when present in the list.
- If the provider matches a source in the list, include that source.
- For police complaints: include the provincial police matching the city or province; for Karachi also include CPLC.
- For harassment: include FOSPAH plus the provincial ombudsperson that matches city or province.
- If city/province is unknown, include only national-level sources (no province/city field).
- Never include sources from a different category.
- Return max 4 IDs.
- Return ONLY a JSON array of ID strings, e.g. ["id1", "id2"]. No explanation."""

    try:
        raw = await generate_text_with_fallback(
            [AIMessage("user", prompt)],
            fallback_text="[]",
        )
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.strip("`").lstrip("json").strip()
        ids = json.loads(raw)
        if not isinstance(ids, list):
            raise ValueError("not a list")
    except Exception as exc:
        logger.warning("LLM source selection failed, using national-level fallback: %s", exc)
        ids = [s["id"] for s in pool if not s.get("province") and not s.get("city")][:4]

    sources = []
    seen: set[str] = set()
    for source_id in ids:
        if not isinstance(source_id, str) or source_id in seen or source_id not in _SOURCE_BY_ID:
            continue
        seen.add(source_id)
        s = _SOURCE_BY_ID[source_id]
        sources.append({
            "title": s["title"],
            "source_name": s["source_name"],
            "authority_type": s["source_type"],
            "jurisdiction": s["jurisdiction"],
            "source_url": s.get("source_url"),
            "verified_at": s.get("verified_at"),
            "confidence_level": s.get("confidence_level", "official_source_metadata"),
        })
    return sources
