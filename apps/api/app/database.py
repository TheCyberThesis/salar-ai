import logging
from functools import lru_cache
from typing import Any

from supabase import Client, create_client

from app.config import get_settings


@lru_cache
def get_supabase_client() -> Client | None:
    settings = get_settings()
    if not settings.supabase_url or not settings.supabase_service_role_key:
        return None
    return create_client(settings.supabase_url, settings.supabase_service_role_key)


class MemoryStore:
    """Small local store for hackathon/demo mode when Supabase is not configured."""

    def __init__(self) -> None:
        self.sessions: dict[str, dict[str, Any]] = {}
        self.reports: dict[str, dict[str, Any]] = {}
        self.feedback: list[dict[str, Any]] = []


memory_store = MemoryStore()

logger = logging.getLogger(__name__)


def persist_generated_report(report: dict[str, Any], session: dict[str, Any], user_id: str | None = None) -> None:
    """Persist report to Supabase when service credentials are configured.

    The MVP intentionally keeps a memory fallback so demos do not fail when
    Supabase is not configured.
    """
    client = get_supabase_client()
    if client is None or not user_id:
        return

    category_id = None
    subcategory = report.get("subcategory")
    if subcategory:
        try:
            category_response = (
                client.table("complaint_categories")
                .select("id")
                .eq("slug", subcategory)
                .limit(1)
                .execute()
            )
            if category_response.data:
                category_id = category_response.data[0]["id"]
        except Exception as exc:  # pragma: no cover - depends on external Supabase
            logger.warning("Could not resolve category for Supabase persistence: %s", exc)

    try:
        client.table("user_complaints").insert(
            {
                "id": report["report_id"],
                "user_id": user_id,
                "session_id": report["session_id"],
                "category_id": category_id,
                "title": report["summary"],
                "description": session.get("collected_data", {}).get("latest_user_message"),
                "collected_data": report["user_provided_details"],
                "generated_report": report,
                "status": "guidance_generated",
            }
        ).execute()
    except Exception as exc:  # pragma: no cover - depends on external Supabase
        logger.warning("Could not persist generated report to Supabase: %s", exc)
