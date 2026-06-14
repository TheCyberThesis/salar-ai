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
- `GOOGLE_MAPS_API_KEY` for Google Places report enrichment. Keep this backend-only in `apps/api/.env`.
- `AI_PROVIDER=gemini`
- `AI_ENABLE_GROK_FALLBACK=true`
- `GEMINI_API_KEY`
- `GEMINI_DEFAULT_MODEL=gemini-3.5-flash`
- `GEMINI_COMPLEX_MODEL=gemini-3.5-flash`
- `GEMINI_AUDIO_MODEL=gemini-3.5-flash`
- `GROK_API_KEY`
- `GROK_MODEL=grok-4.3`
- `RATE_LIMIT_PER_MINUTE`

Gemini is the primary provider. The backend uses Gemini for Roman Urdu/text response generation and voice-message transcription. Grok is used only when Gemini is unavailable or fails and `AI_ENABLE_GROK_FALLBACK=true`. If both keys are missing, the API stays in deterministic mock/fallback mode.

When `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are configured, generated reports can be persisted to `user_complaints` for authenticated users.

When `GOOGLE_MAPS_API_KEY` is configured, generated reports try to include the nearest relevant office from Google Places with address, coordinates, phone number if available, and a direct Google Maps link. If Places fails or the key is missing, the report falls back to a safe Google Maps search link.

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

For authenticated report history, configure Supabase Auth and set the frontend Supabase URL and anon key. Guest users still get browser-local report history.

## Voice Messages

Voice messages are recorded in the browser and sent to `POST /api/voice-message` as base64 audio. The backend transcribes them with `GEMINI_AUDIO_MODEL`, then continues the normal chat flow with the transcript.

This path requires a working `GEMINI_API_KEY`. Grok is intentionally not used for voice transcription.

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
