import json
from pathlib import Path

from app.rag.embeddings import mock_embedding
from app.seed.knowledge_seed import KNOWLEDGE_CHUNKS


BASE_DIR = Path(__file__).resolve().parent


def load_sources() -> list[dict]:
    with (BASE_DIR / "pakistan_sources.json").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_seed_payload() -> list[dict]:
    """Prepare source-grounded chunks for Supabase insertion.

    MVP mode manually seeds verified official-source metadata and cautious summaries.
    Replace mock_embedding with a real embedding provider when API keys and outbound
    network access are configured.
    """
    payload = []
    seen = set()
    for chunk in KNOWLEDGE_CHUNKS:
        key = (chunk["source_name"], chunk["title"], chunk["category"], chunk.get("subcategory"))
        if key in seen:
            continue
        seen.add(key)
        payload.append({**chunk, "embedding": mock_embedding(chunk["content"])})
    return payload


def main() -> None:
    sources = load_sources()
    chunks = build_seed_payload()
    print(f"Loaded {len(sources)} official source records.")
    print(f"Prepared {len(chunks)} knowledge chunks with deterministic mock embeddings.")
    for chunk in chunks:
        print(f"- {chunk['source_name']}: {chunk['title']}")


if __name__ == "__main__":
    main()
