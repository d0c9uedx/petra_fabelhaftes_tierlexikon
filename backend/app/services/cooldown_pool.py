"""Gemeinsame Cooldown-Pool-Logik für Weiterklick (Discover) und Tages-Tier.

Ein Tier ist "eligible", wenn es noch nie gesehen wurde oder zuletzt vor mehr
als ANIMAL_COOLDOWN_DAYS gesehen wurde. Ist der Pool leer (z. B. bei einer
kleinen Seed-Datenbank), fällt die Auswahl auf das am längsten nicht mehr
gesehene Tier zurück (least-recently-seen), damit die App auch mit wenigen
Tieren nutzbar bleibt.
"""
import random
from datetime import datetime, timedelta, timezone

from sqlalchemy import nullsfirst, select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.animal import Animal
from app.models.user_seen_animal import UserSeenAnimal

settings = get_settings()


def get_eligible_pool(db: Session, user_id: int) -> list[Animal]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=settings.animal_cooldown_days)

    seen_subquery = (
        select(UserSeenAnimal.animal_id)
        .where(UserSeenAnimal.user_id == user_id, UserSeenAnimal.last_seen_at >= cutoff)
    )
    stmt = select(Animal).where(Animal.id.notin_(seen_subquery))
    return list(db.execute(stmt).scalars().all())


def pick_random_animal(db: Session, user_id: int) -> Animal | None:
    pool = get_eligible_pool(db, user_id)
    if pool:
        return random.choice(pool)
    return _least_recently_seen_fallback(db, user_id)


def _least_recently_seen_fallback(db: Session, user_id: int) -> Animal | None:
    stmt = (
        select(Animal)
        .outerjoin(
            UserSeenAnimal,
            (UserSeenAnimal.animal_id == Animal.id) & (UserSeenAnimal.user_id == user_id),
        )
        .order_by(nullsfirst(UserSeenAnimal.last_seen_at.asc()))
        .limit(1)
    )
    return db.execute(stmt).scalars().first()
