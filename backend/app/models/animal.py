"""Das Tier-Modell mit allen Steckbrief-Feldern aus der Projektskizze plus den
verspielteren Zusatzfeldern (Funfakt, Superkraft, Liebesleben), siehe CONTEXT.md."""
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


class RelationshipStatus(str, enum.Enum):
    MONOGAMOUS = "monogam"
    MULTIPLE_PARTNERS = "wechselnde_liebhaber"
    HAREM = "harem"


class Animal(Base):
    """Ein Steckbrief: alle Datenfelder aus der Projektskizze, siehe CONTEXT.md.

    Die sechs "Liebesleben"/Charakter-Zusatzfelder (fun_fact, superpower,
    mating_season, nest_building, courtship_dance, relationship_status) sind
    bewusst nullable — siehe docs/adr/0006-neue-steckbrief-felder-nullable.md.
    """

    __tablename__ = "animals"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_de: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    name_scientific: Mapped[str] = mapped_column(String(160), nullable=False)
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    category: Mapped[AnimalCategory] = mapped_column(Enum(AnimalCategory), nullable=False, index=True)

    home_turf: Mapped[str] = mapped_column(Text, nullable=False)
    conservation_status: Mapped[str] = mapped_column(String(120), nullable=False)

    reproduction_mode: Mapped[ReproductionMode] = mapped_column(Enum(ReproductionMode), nullable=False)
    offspring_brood: Mapped[str] = mapped_column(String(60), nullable=False)
    baby_wait_time: Mapped[str] = mapped_column(String(60), nullable=False)

    favorite_food: Mapped[str] = mapped_column(Text, nullable=False)
    arch_enemies: Mapped[str] = mapped_column(Text, nullable=False)

    social_life: Mapped[SocialBehavior] = mapped_column(Enum(SocialBehavior), nullable=False)
    group_size: Mapped[str | None] = mapped_column(String(60), nullable=True)

    personality: Mapped[str] = mapped_column(Text, nullable=False)

    fun_fact: Mapped[str | None] = mapped_column(Text, nullable=True)
    superpower: Mapped[str | None] = mapped_column(Text, nullable=True)
    mating_season: Mapped[str | None] = mapped_column(Text, nullable=True)
    nest_building: Mapped[str | None] = mapped_column(Text, nullable=True)
    courtship_dance: Mapped[str | None] = mapped_column(Text, nullable=True)
    relationship_status: Mapped[RelationshipStatus | None] = mapped_column(Enum(RelationshipStatus), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
