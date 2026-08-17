from pydantic import BaseModel, ConfigDict

from app.models.animal import AnimalCategory


class QuizAnimalOut(BaseModel):
    """Absichtlich OHNE name_de — sonst würde die Frage die Antwort verraten."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    image_url: str
    category: AnimalCategory


class QuizOption(BaseModel):
    animal_id: int
    name_de: str


class QuizQuestionOut(BaseModel):
    """Multiple-Choice-Frage: Bild des gesuchten Tiers + Namens-Optionen (eine davon korrekt)."""

    animal: QuizAnimalOut
    options: list[QuizOption]


class QuizAnswerIn(BaseModel):
    animal_id: int
    selected_animal_id: int


class QuizAnswerOut(BaseModel):
    correct: bool
    correct_animal_id: int
    repetitions: int
    interval_days: int
    next_due_at: str
