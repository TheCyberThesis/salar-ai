# Database Schema

The Supabase schema is in `supabase/migrations/001_initial_schema.sql`.

## Core Tables

- `profiles`: Supabase Auth profile extension.
- `departments`: police, regulators, utilities, ombudspersons, and public-service offices.
- `complaint_categories`: the 10 MVP subcategories.
- `department_locations`: future location/place records.
- `required_documents`: required/optional documents by category.
- `complaint_templates`: reusable draft templates.
- `official_links`: official URLs by category.
- `user_complaints`: generated user guidance reports.
- `chat_sessions`: conversation state and collected data.
- `chat_messages`: user/assistant transcript.
- `feedback`: user feedback.
- `knowledge_sources`: official Pakistani source registry.
- `knowledge_chunks`: pgvector-backed civic knowledge chunks.

## pgvector

The migration enables:

```sql
create extension if not exists "vector";
```

`knowledge_chunks.embedding` uses `vector(768)` for MVP embeddings. The local ingestion script currently produces deterministic mock embeddings; replace it with a real embedding provider when API keys and outbound access are configured.

## Row Level Security

RLS is enabled for user-owned profile, complaint, session, message, and feedback data. Backend service-role operations can bypass RLS where appropriate; browser clients should use Supabase Auth and anon-key policies.

## Seed Data

`supabase/seed.sql` inserts:

- departments
- complaint categories
- required documents
- official links
- knowledge sources
- knowledge chunks
