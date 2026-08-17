"""Das Tier-Modell mit allen Steckbrief-Feldern aus der Projektskizze."""
import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AnimalCategory(str, enum.Enum):
    VOGEL = "vogel"
    FISCH = "fisch"
    INSEKT = "insekt"
    SAEUGETIER = "saeugetier"
    SONSTIGES_LANDTIER = "sonstiges_landtier"


class ReproductionMode(str, enum.Enum):
    EGG_LAYING = "egg_laying"
    LIVE_BEARING = "live_bearing"


class SocialBehavior(str, enum.Enum):
    SOLITARY = "solitary"
    HERD = "herd"


class Animal(Base):
    """Ein Steckbrief: alle Datenfelder aus der Projektskizze, siehe CONTEXT.md."""

    __tablename__ = "animals"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_de: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    name_scientific: Mapped[str] = mapped_column(String(160), nullable=False)
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    category: Mapped[AnimalCategory] = mapped_column(Enum(AnimalCategory), nullable=False, index=True)

    habitat: Mapped[str] = mapped_column(Text, nullable=False)
    conservation_status: Mapped[str] = mapped_column(String(120), nullable=False)

    reproduction_mode: Mapped[ReproductionMode] = mapped_column(Enum(ReproductionMode), nullable=False)
    offspring_count: Mapped[str] = mapped_column(String(60), nullable=False)
    gestation_period: Mapped[str] = mapped_column(String(60), nullable=False)

    diet: Mapped[str] = mapped_column(Text, nullable=False)
    natural_enemies: Mapped[str] = mapped_column(Text, nullable=False)

    social_behavior: Mapped[SocialBehavior] = mapped_column(Enum(SocialBehavior), nullable=False)
    group_size: Mapped[str | None] = mapped_column(String(60), nullable=True)

    character_traits: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
