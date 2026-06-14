# Setup

## Backend

```bash
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Create `apps/api/.env` or export environment variables based on root `.env.example`.

Important variables:

- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `GOOGLE_MAPS_API_KEY`
- `AI_PROVIDER`
- `GEMINI_API_KEY`
- `GROK_API_KEY`
- `RATE_LIMIT_PER_MINUTE`

If keys are missing, the API stays in mock/fallback mode.

When `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are configured, generated reports can be persisted to `user_complaints` for authenticated users.

## Frontend

```bash
cd apps/web
npm install
npm run dev
```

Create `apps/web/.env.local`:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
```

## Supabase

Apply:

```bash
supabase db push
supabase db reset
```

Or run the SQL files manually in this order:

1. `supabase/migrations/001_initial_schema.sql`
2. `supabase/seed.sql`

## Knowledge Ingestion

```bash
cd apps/api
python -m app.seed.knowledge_ingestion
```

The script currently prints a prepared payload with deterministic mock embeddings. Wire Supabase insertion and real embeddings when API credentials are configured.
