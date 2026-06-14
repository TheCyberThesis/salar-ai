# Architecture

```txt
User
  -> Next.js Web App
  -> FastAPI Backend
  -> Supabase DB + Auth + Storage
  -> LLM Provider + RAG + Google Maps
```

## Frontend

The Next.js app lives in `apps/web`.

- `/` is the civic-tech home page.
- `/chat` is the guest-ready guidance flow.
- `/report/[id]` renders generated reports.
- `/dashboard` shows previous browser-saved reports and a Supabase Auth magic-link entry point.

Reusable UI components live in `apps/web/components`. The chat UI calls only the FastAPI backend; it never calls Gemini, Grok, or Maps directly.

## Backend

The FastAPI app lives in `apps/api/app`.

- `routes/` exposes HTTP endpoints.
- `services/` owns classification, missing-field logic, privacy masking, rate limiting, templates, and report generation.
- `ai/` contains provider abstractions for Gemini, Grok, and mock fallback.
- `rag/` contains retrieval and embedding boundaries.
- `maps/` contains Google Maps integration boundaries and fallback search links.
- `safety/` contains validation and output-safety helpers.
- `seed/` contains Pakistan source metadata and seed knowledge chunks.

## Data Flow

1. User sends a message from `/chat`.
2. FastAPI validates and rate-limits the request.
3. The backend detects language and classifies the issue.
4. Category-specific missing fields are calculated.
5. RAG retrieves source metadata/chunks for the category.
6. The assistant asks follow-up questions or marks the session ready for report generation.
7. `/api/generate-report` builds a structured civic guidance report and maps fallback URL.
8. If Supabase service credentials and an authenticated user ID are present, the backend inserts the report into `user_complaints`.
9. The frontend displays the report and keeps a browser copy for demo resilience.

## Deployment Targets

- Frontend: Vercel
- Backend: Render, Railway, or Fly.io
- Database/Auth/Storage: Supabase
