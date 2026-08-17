"""Persistierter Tages-Tier-Pick pro Nutzer und Datum (siehe app/services/daily_pick.py)."""
from datetime import date

from sqlalchemy import Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class UserDailyAnimal(Base):
    __tablename__ = "user_daily_animal"
    __table_args__ = (UniqueConstraint("user_id", "assigned_date", name="uq_user_daily_animal"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    animal_id: Mapped[int] = mapped_column(ForeignKey("animals.id"), nullable=False)
    assigned_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
