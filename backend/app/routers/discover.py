from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.animal import AnimalOut
from app.services.cooldown_pool import pick_random_animal

router = APIRouter(prefix="/discover", tags=["discover"])


@router.get("/next", response_model=AnimalOut)
def next_animal(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Weiterklick: nächstes zufälliges Tier außerhalb des Cooldowns (siehe CONTEXT.md).

    Markiert das Tier hier bewusst NICHT als gesehen — das übernimmt einheitlich
    die AnimalProfile-Komponente im Frontend beim Anzeigen (POST /animals/{id}/seen),
    dieselbe Stelle wie bei AnimalDetailPage. So bleibt "Sehen=Sammeln" an einem
    einzigen Ort im Code verankert (Ausnahme: das Tages-Tier, siehe daily_pick.py,
    das aus Stabilitätsgründen beim Zuweisen serverseitig markiert wird).
    """
    animal = pick_random_animal(db, current_user.id)
    if animal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Keine Tiere in der Datenbank")
    return animal
