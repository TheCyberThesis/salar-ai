from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routes import chat, classify, departments, feedback, health, reports

settings = get_settings()

app = FastAPI(
    title="Salaar AI API",
    description="AI-powered civic guidance backend for Pakistani citizens.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
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
