import logging

import httpx

from app.config import get_settings
from app.maps.maps_fallback import build_maps_search_link

logger = logging.getLogger(__name__)


def _query_for_department(*, subcategory: str | None, city: str | None = None, area: str | None = None, provider: str | None = None) -> str:
    location = " ".join(part for part in [city, "Pakistan"] if part)
    if subcategory in {"lost_phone", "stolen_phone", "lost_bike", "stolen_bike", "lost_car", "stolen_car"}:
        incident_location = " ".join(part for part in [area, city, "Pakistan"] if part)
        return f"nearest police station {incident_location}"
    if subcategory == "electricity_bill_overcharging":
        name = provider or "electricity"
        return f"{name} customer service complaint office {location}"
    if subcategory == "gas_bill_overcharging":
        name = provider or "gas"
        return f"{name} customer service complaint office {location}"
    if subcategory == "water_bill_overcharging":
        name = provider or "WASA"
        return f"{name} water complaint office {location}"
    if subcategory == "workplace_harassment_women":
        return f"FOSPAH harassment ombudsperson office {location}"
    return f"public service office {location}"


def _fallback_location(*, subcategory: str | None, city: str | None = None, area: str | None = None, notes: str | None = None) -> dict[str, str | float | None]:
    return {
        "place_name": None,
        "address": None,
        "phone_number": None,
        "latitude": None,
        "longitude": None,
        "google_maps_place_id": None,
        "maps_link": build_maps_search_link(subcategory=subcategory, city=city, area=area),
        "notes": notes or "Google Maps API key is not configured; returned a safe search link fallback.",
    }


async def find_relevant_department_location(*, subcategory: str | None, city: str | None = None, area: str | None = None, provider: str | None = None) -> dict[str, str | float | None]:
    settings = get_settings()
    if not settings.google_maps_api_key:
        return _fallback_location(subcategory=subcategory, city=city, area=area)

    query = _query_for_department(subcategory=subcategory, city=city, area=area, provider=provider)
    logger.info("Google Places query: %s", query)
    field_mask = ",".join(
        [
            "places.id",
            "places.displayName",
            "places.formattedAddress",
            "places.location",
            "places.googleMapsUri",
            "places.nationalPhoneNumber",
            "places.internationalPhoneNumber",
        ]
    )
    try:
        async with httpx.AsyncClient(timeout=12) as client:
            response = await client.post(
                "https://places.googleapis.com/v1/places:searchText",
                headers={
                    "Content-Type": "application/json",
                    "X-Goog-Api-Key": settings.google_maps_api_key,
                    "X-Goog-FieldMask": field_mask,
                },
                json={
                    "textQuery": query,
                    "languageCode": "en",
                    "regionCode": "PK",
                    "pageSize": 1,
                },
            )
            response.raise_for_status()
            payload = response.json()
    except Exception as exc:  # pragma: no cover - external Google Maps path
        logger.warning("Google Places lookup failed: %s", exc)
        return _fallback_location(
            subcategory=subcategory,
            city=city,
            area=area,
            notes="Google Places lookup failed; returned a safe search link fallback.",
        )

    places = payload.get("places") or []
    if not places:
        return _fallback_location(
            subcategory=subcategory,
            city=city,
            area=area,
            notes="Google Places returned no matching office; confirm the correct department before visiting.",
        )

    place = places[0]
    display_name = place.get("displayName") or {}
    location = place.get("location") or {}
    return {
        "place_name": display_name.get("text"),
        "address": place.get("formattedAddress"),
        "phone_number": place.get("nationalPhoneNumber") or place.get("internationalPhoneNumber"),
        "latitude": location.get("latitude"),
        "longitude": location.get("longitude"),
        "google_maps_place_id": place.get("id"),
        "maps_link": place.get("googleMapsUri") or build_maps_search_link(subcategory=subcategory, city=city, area=area),
        "notes": "Google Places Text Search result. Confirm office jurisdiction, phone number, and timings before visiting.",
    }
