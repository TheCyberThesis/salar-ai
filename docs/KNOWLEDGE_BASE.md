# Knowledge Base

Salaar AI is Pakistan-specific. The knowledge base must use authentic, verifiable Pakistani public sources and avoid random blogs, unofficial legal-advice pages, social media posts, or generic international guidance as authority.

## Source Priority

1. Official Government of Pakistan websites
2. Official federal/provincial department websites
3. Official regulator websites
4. Official police/public-service portals
5. Official utility provider websites
6. Official laws, rules, gazettes, PDFs, complaint manuals, and public notices
7. Reputable background sources only when clearly marked as non-authoritative context

## Current Source Registry

The curated source list is `apps/api/app/seed/pakistan_sources.json`.

Initial official-source categories include:

- Pakistan Telecommunication Authority: `https://www.pta.gov.pk/`
- Islamabad Capital Police: `https://islamabadpolice.gov.pk/`
- Punjab Police: `https://punjabpolice.gov.pk/`
- Police Khidmat Markaz Punjab: `https://pkm.punjab.gov.pk/`
- CPLC: `https://www.cplc.org.pk/`
- NEPRA: `https://nepra.org.pk/`
- OGRA: `https://ogra.org.pk/`
- K-Electric: `https://www.ke.com.pk/`
- SNGPL: `https://www.sngpl.com.pk/`
- SSGC: `https://www.ssgc.com.pk/`
- FOSPAH: `https://www.fospah.gov.pk/`

## Knowledge Chunks

Seed chunks live in `apps/api/app/seed/knowledge_seed.py` and `supabase/seed.sql`.

Each chunk includes:

- source name
- source type
- source URL
- issuing authority
- jurisdiction
- province/city if applicable
- category/subcategory
- content and summary
- language
- verified date
- last checked date
- confidence level

## Adding a Source

1. Add the official source to `pakistan_sources.json`.
2. Verify the domain belongs to the relevant authority.
3. Add or update chunks in `knowledge_seed.py`.
4. Set `verified_at` and `last_checked_at` to the verification date.
5. Run `python -m app.seed.knowledge_ingestion`.
6. Insert or upsert the generated chunks into Supabase.
7. Confirm final reports display the source in “Sources Used / Verification Notes.”

## Updating Embeddings

The MVP uses deterministic mock embeddings. Replace `mock_embedding` in `apps/api/app/rag/embeddings.py` with a real embedding provider and store vectors in `knowledge_chunks.embedding`.

## Anti-Hallucination Rules

- Prefer retrieved knowledge chunks over LLM general knowledge.
- Do not invent official phone numbers, addresses, deadlines, forms, legal sections, or complaint procedures.
- If the source is not in the knowledge base, say it could not be verified from the current official Pakistani source set.
- If requirements differ by city/province, ask for city/province before final guidance.
- Always show source name, jurisdiction, source URL if available, and last verified date.
