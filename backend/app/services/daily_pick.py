"""Bestimmt/lädt das Tages-Tier: pro Nutzer und Kalendertag, persistiert und stabil.

Siehe CONTEXT.md ("Tages-Tier") und den Implementierungsplan für die Begründung,
warum das Ergebnis in user_daily_animal gespeichert statt live berechnet wird.
"""
from datetime import date

from sqlalchemy.orm import Session

from app.models.animal import Animal
from app.models.user_daily_animal import UserDailyAnimal
from app.services.cooldown_pool import pick_random_animal
from app.services.seen import mark_animal_seen


def get_or_assign_daily_animal(db: Session, user_id: int, today: date | None = None) -> Animal | None:
    today = today or date.today()

    existing = (
        db.query(UserDailyAnimal)
        .filter(UserDailyAnimal.user_id == user_id, UserDailyAnimal.assigned_date == today)
        .first()
    )
    if existing is not None:
        return db.get(Animal, existing.animal_id)

    animal = pick_random_animal(db, user_id)
    if animal is None:
        return None

    db.add(UserDailyAnimal(user_id=user_id, animal_id=animal.id, assigned_date=today))
    mark_animal_seen(db, user_id, animal.id)
    db.commit()
    return animal
