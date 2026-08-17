from pydantic import BaseModel

from app.models.animal import AnimalCategory


class CategoryProgress(BaseModel):
    category: AnimalCategory
    seen_count: int
    total_count: int


class ProgressOut(BaseModel):
    seen_count: int
    total_count: int
    by_category: list[CategoryProgress]


class SeenAnimalIds(BaseModel):
    seen_animal_ids: list[int]
