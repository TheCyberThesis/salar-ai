from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Salar AI API"
    environment: str = "development"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])

    supabase_url: str | None = None
    supabase_service_role_key: str | None = None
    supabase_anon_key: str | None = None
    database_url: str | None = None

    google_maps_api_key: str | None = None

    ai_provider: Literal["gemini", "grok", "mock"] = "gemini"
    ai_enable_grok_fallback: bool = True
    gemini_api_key: str | None = None
    gemini_default_model: str = "gemini-2.0-flash"
    gemini_complex_model: str = "gemini-2.0-flash"
    gemini_audio_model: str = "gemini-2.0-flash"
    grok_api_key: str | None = None
    grok_model: str = "grok-3-mini"

    rate_limit_per_minute: int = 20

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
