from fastapi import APIRouter

from app.schemas import DepartmentResponse

router = APIRouter(prefix="/api", tags=["departments"])


DEPARTMENTS = [
    {
        "name": "Nearest Police Station",
        "type": "police",
        "province": None,
        "city": None,
        "website": None,
        "helpline": None,
        "address": "Use the maps search link or local police service portal for your city.",
    },
    {
        "name": "National Electric Power Regulatory Authority",
        "type": "federal_regulator",
        "province": None,
        "city": None,
        "website": "https://nepra.org.pk/",
        "helpline": None,
        "address": "Verify complaint submission channels on the official NEPRA website.",
    },
    {
        "name": "Oil and Gas Regulatory Authority",
        "type": "federal_regulator",
        "province": None,
        "city": None,
        "website": "https://ogra.org.pk/",
        "helpline": None,
        "address": "Verify complaint submission channels on the official OGRA website.",
    },
    {
        "name": "Federal Ombudsperson Secretariat for Protection Against Harassment",
        "type": "federal_ombudsperson",
        "province": None,
        "city": None,
        "website": "https://www.fospah.gov.pk/",
        "helpline": None,
        "address": "Verify current offices and complaint procedure on the official FOSPAH website.",
    },
]


@router.get("/departments", response_model=list[DepartmentResponse])
async def departments(city: str | None = None, province: str | None = None, category: str | None = None) -> list[DepartmentResponse]:
    results = DEPARTMENTS
    if city:
        results = [dept for dept in results if dept.get("city") in {None, city}]
    if province:
        results = [dept for dept in results if dept.get("province") in {None, province}]
    if category == "utility_bill_overcharging":
        results = [dept for dept in results if dept["type"] in {"federal_regulator", "utility_provider"}]
    if category == "workplace_harassment_women":
        results = [dept for dept in results if dept["type"] == "federal_ombudsperson"]
    if category == "lost_or_stolen_vehicle_device":
        results = [dept for dept in results if dept["type"] == "police"]
    return [DepartmentResponse(**dept) for dept in results]
