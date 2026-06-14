from app.config import get_settings
from app.maps.maps_fallback import build_maps_search_link


async def find_relevant_department_location(*, subcategory: str | None, city: str | None = None, area: str | None = None) -> dict[str, str | None]:
    settings = get_settings()
    if not settings.google_maps_api_key:
        return {
            "place_name": None,
            "address": None,
            "maps_link": build_maps_search_link(subcategory=subcategory, city=city, area=area),
            "notes": "Google Maps API key is not configured; returned a safe search link fallback.",
        }
    # Places API integration can be added here without changing route contracts.
    return {
        "place_name": None,
        "address": None,
        "maps_link": build_maps_search_link(subcategory=subcategory, city=city, area=area),
        "notes": "Google Maps Places lookup is ready to be implemented for configured deployments.",
    }
