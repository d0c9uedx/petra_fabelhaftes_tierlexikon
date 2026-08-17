"""'Sehen = Sammeln' (ADR 0003): einziger Ort, an dem user_seen_animals geschrieben wird."""
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.user_seen_animal import UserSeenAnimal


def mark_animal_seen(db: Session, user_id: int, animal_id: int) -> UserSeenAnimal:
    now = datetime.now(timezone.utc)
    entry = (
        db.query(UserSeenAnimal)
        .filter(UserSeenAnimal.user_id == user_id, UserSeenAnimal.animal_id == animal_id)
        .first()
    )
    if entry is None:
        entry = UserSeenAnimal(
            user_id=user_id,
            animal_id=animal_id,
            first_seen_at=now,
            last_seen_at=now,
            seen_count=1,
        )
        db.add(entry)
    else:
        entry.last_seen_at = now
        entry.seen_count += 1
    db.flush()
    return entry
