from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.animal import Animal, AnimalCategory
from app.models.user import User
from app.models.user_seen_animal import UserSeenAnimal
from app.schemas.animal import AnimalListItem, AnimalOut
from app.services.seen import mark_animal_seen

router = APIRouter(prefix="/animals", tags=["animals"])


@router.get("", response_model=list[AnimalListItem])
def list_animals(
    category: AnimalCategory | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Animal)
    if category is not None:
        query = query.filter(Animal.category == category)
    animals = query.order_by(Animal.name_de).all()

    seen_ids = {
        row.animal_id
        for row in db.query(UserSeenAnimal.animal_id).filter(UserSeenAnimal.user_id == current_user.id)
    }
    return [
        AnimalListItem.model_validate(animal).model_copy(update={"seen": animal.id in seen_ids})
        for animal in animals
    ]


@router.get("/{animal_id}", response_model=AnimalOut)
def get_animal(animal_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    animal = db.get(Animal, animal_id)
    if animal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tier nicht gefunden")
    return animal


@router.post("/{animal_id}/seen", status_code=status.HTTP_204_NO_CONTENT)
def mark_seen(
    animal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    animal = db.get(Animal, animal_id)
    if animal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tier nicht gefunden")
    mark_animal_seen(db, current_user.id, animal_id)
    db.commit()
