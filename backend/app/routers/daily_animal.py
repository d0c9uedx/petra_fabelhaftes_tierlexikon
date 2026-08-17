from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.animal import AnimalOut
from app.services.daily_pick import get_or_assign_daily_animal

router = APIRouter(prefix="/daily-animal", tags=["daily-animal"])


@router.get("", response_model=AnimalOut)
def daily_animal(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    animal = get_or_assign_daily_animal(db, current_user.id)
    if animal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Keine Tiere in der Datenbank")
    return animal
