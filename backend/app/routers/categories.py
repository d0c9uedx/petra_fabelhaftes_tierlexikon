from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user
from app.models.animal import AnimalCategory
from app.schemas.animal import CategoryOut

router = APIRouter(prefix="/categories", tags=["categories"])

CATEGORY_LABELS: dict[AnimalCategory, str] = {
    AnimalCategory.VOGEL: "Vögel",
    AnimalCategory.FISCH: "Fische",
    AnimalCategory.INSEKT: "Käfer / Insekten",
    AnimalCategory.SAEUGETIER: "Säugetiere",
    AnimalCategory.SONSTIGES_LANDTIER: "Sonstige Landtiere",
}


@router.get("", response_model=list[CategoryOut])
def list_categories(_=Depends(get_current_user)):
    return [CategoryOut(value=category, label=label) for category, label in CATEGORY_LABELS.items()]
