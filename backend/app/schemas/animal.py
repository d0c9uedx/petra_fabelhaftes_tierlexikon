from pydantic import BaseModel, ConfigDict

from app.models.animal import AnimalCategory, ReproductionMode, SocialBehavior


class AnimalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name_de: str
    name_scientific: str
    image_url: str
    category: AnimalCategory
    habitat: str
    conservation_status: str
    reproduction_mode: ReproductionMode
    offspring_count: str
    gestation_period: str
    diet: str
    natural_enemies: str
    social_behavior: SocialBehavior
    group_size: str | None
    character_traits: str


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
