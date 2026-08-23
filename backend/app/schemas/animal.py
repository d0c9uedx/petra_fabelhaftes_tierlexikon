from pydantic import BaseModel, ConfigDict

from app.models.animal import (
    AnimalCategory,
    RelationshipStatus,
    ReproductionMode,
    SocialBehavior,
)


class AnimalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name_de: str
    name_scientific: str
    image_url: str
    category: AnimalCategory
    genus: str | None
    family: str | None
    home_turf: str
    conservation_status: str
    reproduction_mode: ReproductionMode
    offspring_brood: str
    baby_wait_time: str
    favorite_food: str
    arch_enemies: str
    social_life: SocialBehavior
    group_size: str | None
    personality: str
    fun_fact: str | None
    superpower: str | None
    mating_season: str | None
    nest_building: str | None
    courtship_dance: str | None
    relationship_status: RelationshipStatus | None


class AnimalListItem(BaseModel):
    """Schlankere Darstellung für Listen (Kategorie-Browsing, Weiterklick-Warteschlange)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name_de: str
    image_url: str
    category: AnimalCategory
    seen: bool = False


class CategoryOut(BaseModel):
    value: AnimalCategory
    label: str
