"""Modelle importieren, damit Alembic-Autogenerate und Base.metadata sie kennen."""
from app.models.animal import Animal, ReproductionMode, SocialBehavior, AnimalCategory
from app.models.user import User
from app.models.user_seen_animal import UserSeenAnimal
from app.models.user_quiz_progress import UserQuizProgress
from app.models.user_daily_animal import UserDailyAnimal

__all__ = [
    "Animal",
    "AnimalCategory",
    "ReproductionMode",
    "SocialBehavior",
    "User",
    "UserSeenAnimal",
    "UserQuizProgress",
    "UserDailyAnimal",
]
