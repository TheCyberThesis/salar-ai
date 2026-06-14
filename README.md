# Salaar AI

Salaar AI is an AI-powered civic guidance MVP for Pakistani citizens. It helps users understand where to report supported civic/social issues, what information and documents may be needed, what proof/token/report number to collect, and how to draft a complaint/application.

This is not a lawyer replacement. The frontend and generated reports include the required legal/public guidance disclaimer.

## MVP Domains

- Lost or stolen phone, bike, or car
- Utility bill overcharging
- Workplace harassment against women

## Stack

- Frontend: Next.js, React, TypeScript, Tailwind CSS
- Backend: FastAPI, typed service modules, mock-ready AI provider abstraction
- Database/Auth/Storage: Supabase PostgreSQL/Auth/Storage
- RAG: Supabase PostgreSQL with pgvector
- Maps: Google Maps API boundary with safe Google Maps search fallback
- AI: Gemini 3.5 Flash primary for Roman Urdu/text and voice-message processing, Grok as last-resort text fallback, mock fallback when keys are missing

## Run Locally

Backend:

```bash
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd apps/web
npm install
npm run dev
```

Open `http://localhost:3000`. The frontend expects the API at `http://localhost:8000` by default.

For real AI calls, set `GEMINI_API_KEY` in `apps/api/.env`. The default model is `gemini-3.5-flash` for chat/report text and voice-message transcription. Set `GROK_API_KEY` only as a backup; the backend calls Grok after Gemini is unavailable or fails.

## Edit These First

- API keys: `.env.example`, then create `.env` files for local use.
- Supabase configuration: `supabase/migrations/001_initial_schema.sql`, `supabase/seed.sql`, `apps/web/lib/supabase.ts`, `apps/api/app/database.py`
- Seed data: `supabase/seed.sql`
- Pakistan source list: `apps/api/app/seed/pakistan_sources.json`
- Knowledge chunks: `apps/api/app/seed/knowledge_seed.py`
- AI prompts: `apps/api/app/ai/prompts.py`
- Frontend branding: `apps/web/app/page.tsx`, `apps/web/components/AssistantHeader.tsx`, `apps/web/app/globals.css`, `apps/web/public/civic-guidance-hero.png`

## Demo Prompt

Try:

```txt
Mera phone kho gaya hai
```

Then generate a guidance report. The mock backend will classify the complaint, ask for missing details, create a report draft, include proof/token reminders, and display source notes.

## Documentation

- `docs/ARCHITECTURE.md`
- `docs/API.md`
- `docs/DATABASE_SCHEMA.md`
- `docs/SETUP.md`
- `docs/PROMPTS.md`
- `docs/KNOWLEDGE_BASE.md`
