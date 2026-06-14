from urllib.parse import quote_plus


def _query_for_subcategory(subcategory: str | None) -> str:
    if subcategory in {"lost_phone", "stolen_phone", "lost_bike", "stolen_bike", "lost_car", "stolen_car"}:
        return "nearest police station"
    if subcategory == "electricity_bill_overcharging":
        return "electricity customer service center"
    if subcategory == "gas_bill_overcharging":
        return "gas customer service center"
    if subcategory == "water_bill_overcharging":
        return "WASA water complaint office"
    if subcategory == "workplace_harassment_women":
        return "FOSPAH office harassment ombudsperson"
    return "relevant public service office"


def build_maps_search_link(*, subcategory: str | None, city: str | None = None, area: str | None = None) -> str:
    location = " ".join(part for part in [area, city, "Pakistan"] if part)
    query = f"{_query_for_subcategory(subcategory)} in {location or 'Pakistan'}"
    return f"https://www.google.com/maps/search/{quote_plus(query)}"
