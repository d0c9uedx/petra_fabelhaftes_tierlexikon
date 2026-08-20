"""Befüllt die Datenbank mit den 300 Steckbriefen aus data/tierlexikon_steckbriefe.json.

Die Quelldatei liefert pro Tier größtenteils Freitext (siehe `tierlexikon-app-projektskizze.md`)
und kein festes Vokabular für `fortpflanzung`/`gesellschaftsleben`. Die Zuordnung auf die
strikten Modell-Enums (`ReproductionMode`, `SocialBehavior`) ist eine bewusste, dokumentierte
Entscheidung — siehe docs/adr/0005-tierdaten-mapping-heuristik.md für die Begründung und
Grenzfälle. Echte Bild-URLs kommen separat aus `data/animal_images.json`
(name_de -> Wikipedia-Foto, siehe `data/prepare_animal_images.py`); Tiere ohne Treffer dort
fallen auf das Kategorie-Platzhalter-SVG aus ADR 0005 zurück — siehe
docs/adr/0007-echte-tierfotos.md.

Die sechs neuen "Liebesleben"/Charakter-Zusatzfelder (`funfakt`, `superkraft`, `balzzeit`,
`nestbau`, `tanz_der_liebe`, `beziehungsstatus`) sind dagegen direkt mit dem passenden
Wert recherchiert/verfasst worden statt aus Freitext geparst — `beziehungsstatus` wird
deshalb 1:1 auf den `RelationshipStatus`-Enum abgebildet, ohne Heuristik. Fehlt eine
Information (auch nach Recherche), bleibt der JSON-Wert `null` — siehe
docs/adr/0006-neue-steckbrief-felder-nullable.md.

Ausführen mit: python -m app.seed.seed_data
"""
import json
from pathlib import Path

from app.database import Base, SessionLocal, engine
from app.models.animal import (
    Animal,
    AnimalCategory,
    RelationshipStatus,
    ReproductionMode,
    SocialBehavior,
)

DATA_FILE = Path(__file__).parent / "data" / "tierlexikon_steckbriefe.json"
IMAGE_MAPPING_FILE = Path(__file__).parent / "data" / "animal_images.json"

# JSON-`kategorie` -> AnimalCategory. "Nicht-Säugetier" entspricht der Projektskizze-
# Kategorie "sonstige Landtiere (Nicht-Säugetiere)", z. B. Reptilien, Amphibien, Wirbellose.
CATEGORY_MAP = {
    "Vogel": AnimalCategory.VOGEL,
    "Fisch": AnimalCategory.FISCH,
    "Insekt": AnimalCategory.INSEKT,
    "Säugetier": AnimalCategory.SAEUGETIER,
    "Nicht-Säugetier": AnimalCategory.SONSTIGES_LANDTIER,
}

# Manueller Sonderfall: der einzige Eintrag, dessen `fortpflanzung`-Text nicht eindeutig
# mit "Eier legend" oder "lebendgebärend" beginnt (Rochen: "je nach Art Eier legend oder
# lebendgebärend"). Siehe ADR 0005.
REPRODUCTION_OVERRIDES: dict[str, ReproductionMode] = {
    "Rochen": ReproductionMode.EGG_LAYING,
}

# Schlüsselwörter für die Gesellschaftsleben-Heuristik (ADR 0005). Reihenfolge ist Teil der
# Regel: "einzelgänger" hat Vorrang vor den Herdentier-Schlüsselwörtern, weil in allen
# beobachteten Grenzfällen ("überwiegend Einzelgänger, ... teils in Gruppen") die primäre
# Lebensweise solitär ist und die Gruppenbildung nur eine Ausnahme beschreibt.
SOLITARY_KEYWORDS = ("einzelgänger",)
HERD_KEYWORDS = (
    "gesellig", "schwärm", "kolonie", "sozial", "gruppen", "herde", "rudel",
    "völker", "volk", "rotten", "rotte", "paaren", "paare", "gemeinschaft",
)


def _map_category(kategorie: str) -> AnimalCategory:
    return CATEGORY_MAP[kategorie]


def _map_reproduction(name_de: str, fortpflanzung: str) -> ReproductionMode:
    if name_de in REPRODUCTION_OVERRIDES:
        return REPRODUCTION_OVERRIDES[name_de]
    if fortpflanzung.startswith("lebendgebärend"):
        return ReproductionMode.LIVE_BEARING
    return ReproductionMode.EGG_LAYING


def _map_social_behavior(name_de: str, gesellschaftsleben: str) -> SocialBehavior:
    text = gesellschaftsleben.lower()
    if any(keyword in text for keyword in SOLITARY_KEYWORDS):
        return SocialBehavior.SOLITARY
    if any(keyword in text for keyword in HERD_KEYWORDS):
        return SocialBehavior.HERD
    # Bei allen bisherigen Einträgen greift eine der beiden Regeln oben. Für künftig
    # ergänzte Tiere, die durch beide Raster fallen, lieber konservativ SOLITARY annehmen
    # und sichtbar warnen, statt eine unbegründete Herdentier-Annahme zu treffen.
    print(f"WARNUNG: Gesellschaftsleben von '{name_de}' nicht eindeutig zuordenbar "
          f"('{gesellschaftsleben}') — falle zurück auf SOLITARY.")
    return SocialBehavior.SOLITARY


def _load_image_map() -> dict[str, str]:
    """name_de -> Dateiname unter frontend/public/images/animals/, für Tiere mit
    echtem Foto (siehe backend/app/seed/data/prepare_animal_images.py). Tiere ohne
    Treffer (image_path == "nicht gefunden") fehlen bewusst in der Map und fallen
    unten auf das Kategorie-Platzhalter-SVG zurück."""
    if not IMAGE_MAPPING_FILE.is_file():
        return {}
    with IMAGE_MAPPING_FILE.open(encoding="utf-8") as f:
        raw = json.load(f)
    return {
        name_de: f"{Path(entry['image_path']).stem}.webp"
        for name_de, entry in raw.items()
        if entry.get("image_path") and entry["image_path"] != "nicht gefunden"
    }


IMAGE_MAP: dict[str, str] = _load_image_map()


def _image_url(name_de: str, category: AnimalCategory) -> str:
    if name_de in IMAGE_MAP:
        return f"/images/animals/{IMAGE_MAP[name_de]}"
    return f"/images/placeholder-{category.value}.svg"


def _load_animals() -> list[dict]:
    with DATA_FILE.open(encoding="utf-8") as f:
        raw = json.load(f)

    animals = []
    for entry in raw:
        category = _map_category(entry["kategorie"])
        animals.append(dict(
            name_de=entry["name_de"],
            name_scientific=entry["name_wiss"],
            image_url=_image_url(entry["name_de"], category),
            category=category,
            home_turf=entry["zuhause"],
            conservation_status=entry["status"],
            reproduction_mode=_map_reproduction(entry["name_de"], entry["fortpflanzung"]),
            offspring_brood=entry["kinderschar"],
            baby_wait_time=entry["wartezeit_aufs_baby"],
            favorite_food=entry["lieblingsspeise"],
            arch_enemies=entry["erzfeinde"],
            social_life=_map_social_behavior(entry["name_de"], entry["gesellschaftsleben"]),
            group_size=None,
            personality=entry["persoenlichkeit"],
            fun_fact=entry.get("funfakt"),
            superpower=entry.get("superkraft"),
            mating_season=entry.get("balzzeit"),
            nest_building=entry.get("nestbau"),
            courtship_dance=entry.get("tanz_der_liebe"),
            relationship_status=(
                RelationshipStatus(entry["beziehungsstatus"]) if entry.get("beziehungsstatus") else None
            ),
        ))
    return animals


ANIMALS: list[dict] = _load_animals()


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Animal).count() > 0:
            print("Tiere bereits vorhanden, überspringe Seed.")
            return
        for data in ANIMALS:
            db.add(Animal(**data))
        db.commit()
        print(f"{len(ANIMALS)} Tiere eingefügt.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
