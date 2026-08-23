import random
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.animal import Animal
from app.models.user import User
from app.models.user_quiz_progress import UserQuizProgress
from app.schemas.quiz import QuizAnimalOut, QuizAnswerIn, QuizAnswerOut, QuizOption, QuizQuestionOut
from app.services.spaced_repetition import apply_answer

router = APIRouter(prefix="/quiz", tags=["quiz"])

MAX_OPTIONS = 4


def _pick_question_animal(db: Session, user_id: int) -> Animal | None:
    now = datetime.now(timezone.utc)

    due_progress = (
        db.query(UserQuizProgress)
        .filter(UserQuizProgress.user_id == user_id, UserQuizProgress.next_due_at <= now)
        .order_by(UserQuizProgress.next_due_at.asc())
        .first()
    )
    if due_progress is not None:
        return db.get(Animal, due_progress.animal_id)

    introduced_ids = {
        row.animal_id for row in db.query(UserQuizProgress.animal_id).filter(UserQuizProgress.user_id == user_id)
    }
    new_candidate = db.query(Animal).filter(Animal.id.notin_(introduced_ids)).order_by(Animal.id).first()
    return new_candidate


@router.get("/next", response_model=QuizQuestionOut)
def next_question(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    target = _pick_question_animal(db, current_user.id)
    if target is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aktuell ist keine Quizfrage fällig",
        )

    others = (
        db.query(Animal)
        .filter(Animal.id != target.id, Animal.category == target.category)
        .order_by(Animal.id)
        .all()
    )
    distractor_count = min(MAX_OPTIONS - 1, len(others))
    distractors = random.sample(others, distractor_count)

    options = [QuizOption(animal_id=target.id, name_de=target.name_de)]
    options += [QuizOption(animal_id=a.id, name_de=a.name_de) for a in distractors]
    random.shuffle(options)

    return QuizQuestionOut(animal=QuizAnimalOut.model_validate(target), options=options)


@router.post("/answer", response_model=QuizAnswerOut)
def submit_answer(
    payload: QuizAnswerIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    animal = db.get(Animal, payload.animal_id)
    if animal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tier nicht gefunden")

    progress = (
        db.query(UserQuizProgress)
        .filter(UserQuizProgress.user_id == current_user.id, UserQuizProgress.animal_id == payload.animal_id)
        .first()
    )
    if progress is None:
        # Explizite Werte statt auf die Spalten-Defaults zu vertrauen: die greifen erst
        # beim INSERT-Flush, apply_answer() rechnet aber sofort im Python-Objekt weiter.
        progress = UserQuizProgress(
            user_id=current_user.id,
            animal_id=payload.animal_id,
            correct_count=0,
            incorrect_count=0,
            repetitions=0,
            interval_days=0,
            easiness_factor=2.5,
        )
        db.add(progress)

    correct = payload.selected_animal_id == payload.animal_id
    apply_answer(progress, correct)
    db.commit()
    db.refresh(progress)

    return QuizAnswerOut(
        correct=correct,
        correct_animal_id=payload.animal_id,
        repetitions=progress.repetitions,
        interval_days=progress.interval_days,
        next_due_at=progress.next_due_at.isoformat() if progress.next_due_at else "",
    )
