#!/usr/bin/env python3
"""
Download Wikipedia images for animals from tierlexikon_steckbriefe.json.
Uses name_de as search term and filename.
"""

import json
import os
import re
import time
import requests
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
STECKBRIEFE_FILE = SCRIPT_DIR / "tierlexikon_steckbriefe.json"
IMAGES_DIR = SCRIPT_DIR / "images"
MAPPING_FILE = SCRIPT_DIR / "animal_images.json"

IMAGES_DIR.mkdir(exist_ok=True)

WIKI_API_BASE = "https://en.wikipedia.org/api/rest_v1/page/summary"
WIKI_DE_API_BASE = "https://de.wikipedia.org/api/rest_v1/page/summary"
USER_AGENT = "PetrasTierlexikonBot/1.0 (https://github.com/petras-fabelhaftes-tierlexikon)"


def clean_filename(name: str) -> str:
    """Convert name to safe filename: lowercase, spaces to underscores."""
    name = name.lower().strip()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s]+", "_", name)
    return name


def search_wikipedia(title: str, lang: str = "en") -> dict | None:
    """Search Wikipedia for a page and return its summary with image info."""
    base = WIKI_API_BASE if lang == "en" else WIKI_DE_API_BASE
    url = f"{base}/{requests.utils.quote(title)}"
    headers = {"User-Agent": USER_AGENT}

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("thumbnail") or data.get("originalimage"):
                return data
    except Exception:
        pass
    return None


def download_image(url: str, filepath: Path) -> bool:
    """Download an image from URL and save it."""
    headers = {"User-Agent": USER_AGENT}
    try:
        resp = requests.get(url, headers=headers, timeout=15, stream=True)
        if resp.status_code == 200:
            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
            return True
    except Exception:
        pass
    return False


def get_plural_variants(name_de: str) -> list[str]:
    """Generate German plural variants for a name."""
    name = name_de.strip()
    lower = name.lower()
    variants = []

    # Common German plural rules
    if lower.endswith("e") or lower.endswith("a") or lower.endswith("u"):
        # Biene → Bienen, Kuh → Kühe
        variants.append(name + "n")
        variants.append(name[:-1] + "üe")  # Kuh → Kühe
    elif lower.endswith("el") or lower.endswith("er"):
        # Vogel → Vögel, Kind → Kinder
        umlaut_map = {"a": "ä", "o": "ö", "u": "ü"}
        if len(name) > 2 and name[-3].lower() in umlaut_map:
            umlaut = umlaut_map[name[-3].lower()]
            variants.append(name[:-2] + umlaut + name[-2:])
        variants.append(name + "e")
    elif lower.endswith("s"):
        # Auto → Autos (already plural)
        pass
    elif lower.endswith("chen") or lower.endswith("lein"):
        # Diminutives are usually unchanged
        pass
    elif lower.endswith("ling") or lower.endswith("ing"):
        # Fink → Finke, Ring → Ringe
        variants.append(name + "e")
    elif lower.endswith("fish") or lower.endswith("fisch"):
        # Fisch → Fische
        variants.append(name + "e")
    else:
        # Default: add -e
        variants.append(name + "e")

    # Special cases with Umlaut
    umlaut_map = {"a": "ä", "o": "ö", "u": "ü"}
    special_endings = [("uchs", "üchse"), ("ock", "öcke"), ("opf", "öpfe")]
    for ending, plural_ending in special_endings:
        if lower.endswith(ending):
            pos = len(name) - len(ending)
            umlaut_char = name[pos].lower()
            if umlaut_char in umlaut_map:
                new_name = name[:pos] + umlaut_map[umlaut_char] + name[pos+1:]
                variants.append(new_name + plural_ending[1:])

    return variants


def clean_scientific_name(name_wiss: str) -> str:
    """Strip taxon annotations like (Familie), (Ordnung), spec. etc."""
    cleaned = re.sub(r"\s*\(.*?\)", "", name_wiss)
    cleaned = re.sub(r"\s*spec\.?", "", cleaned)
    return cleaned.strip()


def find_image(name_de: str, name_wiss: str = "") -> tuple[bool, str, str]:
    """
    Try to find a Wikipedia image for the given name_de.
    Search order: singular → plural variants → scientific name (EN only).
    Returns (success, image_url, wikipedia_url).
    """
    # Try singular first
    wiki_title = name_de.replace(" ", "_")
    summary = search_wikipedia(wiki_title, "en")
    if summary is None:
        summary = search_wikipedia(wiki_title, "de")

    if summary and (summary.get("originalimage") or summary.get("thumbnail")):
        img_url = summary.get("originalimage", {}).get("source") or summary.get("thumbnail", {}).get("source")
        wiki_url = summary.get("content_urls", {}).get("desktop", {}).get("page", "")
        return True, img_url, wiki_url

    # Try plural variants
    for variant in get_plural_variants(name_de):
        wiki_title = variant.replace(" ", "_")
        summary = search_wikipedia(wiki_title, "en")
        if summary is None:
            summary = search_wikipedia(wiki_title, "de")

        if summary and (summary.get("originalimage") or summary.get("thumbnail")):
            img_url = summary.get("originalimage", {}).get("source") or summary.get("thumbnail", {}).get("source")
            wiki_url = summary.get("content_urls", {}).get("desktop", {}).get("page", "")
            return True, img_url, wiki_url

    # Try scientific name (EN Wikipedia only)
    if name_wiss:
        latin = clean_scientific_name(name_wiss)
        if latin:
            summary = search_wikipedia(latin, "en")
            if summary and (summary.get("originalimage") or summary.get("thumbnail")):
                img_url = summary.get("originalimage", {}).get("source") or summary.get("thumbnail", {}).get("source")
                wiki_url = summary.get("content_urls", {}).get("desktop", {}).get("page", "")
                return True, img_url, wiki_url

    return False, "", ""


def main():
    with open(STECKBRIEFE_FILE, "r", encoding="utf-8") as f:
        animals = json.load(f)

    mapping = {}
    found = 0
    not_found = 0

    print(f"Processing {len(animals)} animals...")

    for i, animal in enumerate(animals):
        name_de = animal["name_de"]
        name_wiss = animal["name_wiss"]
        filename = clean_filename(name_de) + ".jpg"
        filepath = IMAGES_DIR / filename

        success, img_url, wiki_url = find_image(name_de, name_wiss)

        if success:
            if download_image(img_url, filepath):
                mapping[name_de] = {
                    "image_path": f"images/{filename}",
                    "source": wiki_url
                }
                found += 1
                status = "OK"
            else:
                mapping[name_de] = {
                    "image_path": "nicht gefunden",
                    "source": ""
                }
                not_found += 1
                status = "DOWNLOAD FAILED"
        else:
            mapping[name_de] = {
                "image_path": "nicht gefunden",
                "source": ""
            }
            not_found += 1
            status = "NOT FOUND"

        print(f"[{i+1}/{len(animals)}] {name_de}: {status}")

        # Rate limiting: 1 second between requests
        if i < len(animals) - 1:
            time.sleep(1)

    # Save mapping
    with open(MAPPING_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    print(f"\nDone!")
    print(f"Found: {found}")
    print(f"Not found: {not_found}")
    print(f"Total: {len(animals)}")
    print(f"Mapping saved to: {MAPPING_FILE}")


if __name__ == "__main__":
    main()
