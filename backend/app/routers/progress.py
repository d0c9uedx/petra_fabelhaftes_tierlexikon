from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.animal import Animal, AnimalCategory
from app.models.user import User
from app.models.user_seen_animal import UserSeenAnimal
from app.schemas.progress import CategoryProgress, ProgressOut, SeenAnimalIds

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("", response_model=ProgressOut)
def get_progress(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    seen_ids = {
        row.animal_id
        for row in db.query(UserSeenAnimal.animal_id).filter(UserSeenAnimal.user_id == current_user.id)
    }

    by_category: list[CategoryProgress] = []
    for category in AnimalCategory:
        animal_ids = [a.id for a in db.query(Animal.id).filter(Animal.category == category)]
        by_category.append(
            CategoryProgress(
                category=category,
                seen_count=len(seen_ids.intersection(animal_ids)),
                total_count=len(animal_ids),
            )
        )

    total_count = db.query(Animal).count()
    return ProgressOut(seen_count=len(seen_ids), total_count=total_count, by_category=by_category)


@router.get("/animals", response_model=SeenAnimalIds)
def get_seen_animal_ids(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    seen_ids = [
        row.animal_id
        for row in db.query(UserSeenAnimal.animal_id).filter(UserSeenAnimal.user_id == current_user.id)
    ]
    return SeenAnimalIds(seen_animal_ids=seen_ids)
