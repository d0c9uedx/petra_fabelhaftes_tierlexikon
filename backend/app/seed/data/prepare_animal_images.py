#!/usr/bin/env python3
"""
Verkleinert/konvertiert die von download_wikipedia_images.py heruntergeladenen
Rohbilder (backend/app/seed/data/images/, roh von Wikipedia, teils mehrere MB
und stark unterschiedliche Auflösungen) zu kompakten WebP-Dateien, passend für
die Steckbrief-/Tierkarten-/Quiz-Platzhalterboxen im Frontend.

Liest animal_images.json (name_de -> image_path), schreibt die verkleinerten
Bilder nach frontend/public/images/animals/<slug>.webp. Diese Dateien werden
regulär committet (im Gegensatz zu den *.jpg-Rohbildern, die per .gitignore
lokal bleiben) und von backend/app/seed/seed_data.py referenziert.

Ausführen mit: python -m app.seed.data.prepare_animal_images
(benötigt Pillow, das kein reguläres Backend-Dependency ist: pip install Pillow)
"""
import json
from pathlib import Path

from PIL import Image

SCRIPT_DIR = Path(__file__).parent
MAPPING_FILE = SCRIPT_DIR / "animal_images.json"
IMAGES_DIR = SCRIPT_DIR / "images"
OUT_DIR = SCRIPT_DIR.parents[3] / "frontend" / "public" / "images" / "animals"

MAX_EDGE = 640
WEBP_QUALITY = 78


def _flatten_to_rgb(img: Image.Image) -> Image.Image:
    """Bettet transparente/Palette-Bilder auf weißem Hintergrund ein, statt
    schwarze Ränder o.ä. beim WebP-Export zu riskieren."""
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        background = Image.new("RGB", img.size, (255, 255, 255))
        rgba = img.convert("RGBA")
        background.paste(rgba, mask=rgba.split()[-1])
        return background
    return img.convert("RGB")


def main() -> None:
    with MAPPING_FILE.open(encoding="utf-8") as f:
        mapping: dict[str, dict] = json.load(f)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    processed = 0
    skipped_no_match = 0
    failed = 0

    for name_de, entry in mapping.items():
        image_path = entry.get("image_path", "")
        if not image_path or image_path == "nicht gefunden":
            skipped_no_match += 1
            continue

        src = SCRIPT_DIR / image_path
        if not src.is_file():
            print(f"WARNUNG: Quelldatei fehlt für '{name_de}': {src}")
            failed += 1
            continue

        dest = OUT_DIR / f"{src.stem}.webp"
        try:
            with Image.open(src) as img:
                img = _flatten_to_rgb(img)
                img.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
                img.save(dest, "WEBP", quality=WEBP_QUALITY)
            processed += 1
        except Exception as exc:  # noqa: BLE001 - einmaliges Datenaufbereitungsskript
            print(f"FEHLER bei '{name_de}' ({src.name}): {exc}")
            failed += 1

    print("\nFertig!")
    print(f"Verarbeitet: {processed}")
    print(f"Ohne Treffer übersprungen (bleiben beim Platzhalter): {skipped_no_match}")
    print(f"Fehlgeschlagen: {failed}")
    print(f"Ausgabeordner: {OUT_DIR}")


if __name__ == "__main__":
    main()
