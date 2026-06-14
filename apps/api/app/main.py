from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routes import chat, classify, departments, feedback, health, reports, voice

settings = get_settings()

app = FastAPI(
    title="Salar AI API",
    description="AI-powered civic guidance backend for Pakistani citizens.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+" if settings.environment == "development" else None,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(classify.router)
app.include_router(chat.router)
app.include_router(reports.router)
app.include_router(departments.router)
app.include_router(feedback.router)
app.include_router(voice.router)
