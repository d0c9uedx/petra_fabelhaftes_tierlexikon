"""Vereinfachter SM-2-Algorithmus für das Multiple-Choice-Quiz (binär: richtig/falsch).

Siehe Implementierungsplan für die Herleitung der Konstanten.
"""
from datetime import datetime, timedelta, timezone

from app.models.user_quiz_progress import UserQuizProgress

MIN_EASINESS_FACTOR = 1.3


def apply_answer(progress: UserQuizProgress, correct: bool) -> UserQuizProgress:
    now = datetime.now(timezone.utc)
    progress.last_answered_at = now

    if correct:
        progress.correct_count += 1
        progress.repetitions += 1

        if progress.repetitions == 1:
            progress.interval_days = 1
        elif progress.repetitions == 2:
            progress.interval_days = 6
        else:
            progress.interval_days = round(progress.interval_days * progress.easiness_factor)

        progress.easiness_factor = max(MIN_EASINESS_FACTOR, progress.easiness_factor + 0.1)
    else:
        progress.incorrect_count += 1
        progress.repetitions = 0
        progress.interval_days = 1
        progress.easiness_factor = max(MIN_EASINESS_FACTOR, progress.easiness_factor - 0.2)

    progress.next_due_at = now + timedelta(days=progress.interval_days)
    return progress
