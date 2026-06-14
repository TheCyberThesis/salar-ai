import logging
from functools import lru_cache
from typing import Any

import httpx
from supabase import Client, create_client
from supabase._sync.client import SupabaseException

from app.config import get_settings


@lru_cache
def get_supabase_client() -> Client | None:
    settings = get_settings()
    if not settings.supabase_url or not settings.supabase_service_role_key:
        return None
    try:
        return create_client(settings.supabase_url, settings.supabase_service_role_key)
    except SupabaseException as exc:
        logger.warning("Supabase client is not available: %s", exc)
        return None


class MemoryStore:
    """Small local store for hackathon/demo mode when Supabase is not configured."""

    def __init__(self) -> None:
        self.sessions: dict[str, dict[str, Any]] = {}
        self.reports: dict[str, dict[str, Any]] = {}
        self.feedback: list[dict[str, Any]] = []


memory_store = MemoryStore()

logger = logging.getLogger(__name__)


def _supabase_headers() -> dict[str, str] | None:
    settings = get_settings()
    key = settings.supabase_service_role_key
    if not settings.supabase_url or not key:
        return None
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }


def _rest_url(path: str) -> str:
    settings = get_settings()
    return f"{settings.supabase_url.rstrip('/')}/rest/v1/{path.lstrip('/')}"


def _resolve_category_id(subcategory: str | None) -> str | None:
    if not subcategory:
        return None
    headers = _supabase_headers()
    if not headers:
        return None
    try:
        response = httpx.get(
            _rest_url("complaint_categories"),
            headers=headers,
            params={"select": "id", "slug": f"eq.{subcategory}", "limit": "1"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        return data[0]["id"] if data else None
    except Exception as exc:  # pragma: no cover - depends on external Supabase
        logger.warning("Could not resolve category for Supabase persistence: %s", exc)
        return None


def persist_generated_report(report: dict[str, Any], session: dict[str, Any], user_id: str | None = None) -> None:
    """Persist report to Supabase when service credentials are configured.

    The MVP intentionally keeps a memory fallback so demos do not fail when
    Supabase is not configured.
    """
    if not user_id:
        return

    headers = _supabase_headers()
    if not headers:
        return

    category_id = _resolve_category_id(report.get("subcategory"))
    try:
        response = httpx.post(
            _rest_url("user_complaints"),
            headers={**headers, "Prefer": "return=minimal"},
            json={
                "id": report["report_id"],
                "user_id": user_id,
                "session_id": report["session_id"],
                "category_id": category_id,
                "title": report["summary"],
                "description": session.get("collected_data", {}).get("latest_user_message"),
                "collected_data": report["user_provided_details"],
                "generated_report": report,
                "status": "guidance_generated",
            },
            timeout=15,
        )
        response.raise_for_status()
    except Exception as exc:  # pragma: no cover - depends on external Supabase
        logger.warning("Could not persist generated report to Supabase: %s", exc)
