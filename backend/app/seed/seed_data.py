"""Befüllt die Datenbank mit einer Handvoll Beispieltieren.

Dies ist NICHT die vollständige Tierdatenbank (siehe Projektskizze, geplante
150 Arten) — das folgt im nächsten Schritt. Hier reichen ~10 Tiere über alle
Kategorien, damit Weiterklick, Tages-Tier, Cooldown und die Quiz-Distraktoren
im Erstentwurf sinnvoll durchgespielt werden können.

Ausführen mit: python -m app.seed.seed_data
"""
from app.database import Base, SessionLocal, engine
from app.models.animal import Animal, AnimalCategory, ReproductionMode, SocialBehavior

ANIMALS: list[dict] = [
    dict(
        name_de="Kapibara",
        name_scientific="Hydrochoerus hydrochaeris",
        image_url="https://upload.wikimedia.org/wikipedia/commons/2/29/Capybara_%28Hydrochoerus_hydrochaeris%29.JPG",
        category=AnimalCategory.SAEUGETIER,
        habitat="Ufernähe von Flüssen und Sümpfen, Süd- und Mittelamerika",
        conservation_status="nicht gefährdet, Bestand stabil",
        reproduction_mode=ReproductionMode.LIVE_BEARING,
        offspring_count="meist 3–5 Jungtiere pro Wurf",
        gestation_period="ca. 5 Monate",
        diet="Wasserpflanzen, Gräser, Rinde",
        natural_enemies="Jaguare, Kaimane, Anakondas, Greifvögel",
        social_behavior=SocialBehavior.HERD,
        group_size="10–20 Tiere",
        character_traits="Gesellig, friedlich, sehr entspannt und verträglich mit anderen Tieren.",
    ),
    dict(
        name_de="Igel",
        name_scientific="Erinaceus europaeus",
        image_url="https://upload.wikimedia.org/wikipedia/commons/4/4e/Erinaceus_europaeus_LC0119.jpg",
        category=AnimalCategory.SAEUGETIER,
        habitat="Gärten, Hecken, Waldränder in Europa",
        conservation_status="gefährdet (Bestand rückläufig)",
        reproduction_mode=ReproductionMode.LIVE_BEARING,
        offspring_count="4–5 Jungtiere pro Wurf",
        gestation_period="ca. 35 Tage",
        diet="Insekten, Schnecken, Würmer, gelegentlich Fallobst",
        natural_enemies="Uhu, Dachs, Fuchs",
        social_behavior=SocialBehavior.SOLITARY,
        group_size=None,
        character_traits="Nachtaktiv, scheu, rollt sich bei Gefahr zur Stachelkugel zusammen.",
    ),
    dict(
        name_de="Rotkehlchen",
        name_scientific="Erithacus rubecula",
        image_url="https://upload.wikimedia.org/wikipedia/commons/8/8d/Erithacus_rubecula_with_worm.jpg",
        category=AnimalCategory.VOGEL,
        habitat="Wälder, Gärten und Parks in Europa",
        conservation_status="nicht gefährdet",
        reproduction_mode=ReproductionMode.EGG_LAYING,
        offspring_count="5–7 Eier pro Gelege",
        gestation_period="Brutzeit ca. 13–14 Tage",
        diet="Insekten, Spinnen, Beeren",
        natural_enemies="Sperber, Katzen, Marder",
        social_behavior=SocialBehavior.SOLITARY,
        group_size=None,
        character_traits="Zutraulich, revierbewusst, singt ganzjährig.",
    ),
    dict(
        name_de="Weißstorch",
        name_scientific="Ciconia ciconia",
        image_url="https://upload.wikimedia.org/wikipedia/commons/3/3a/White_Stork_%28Ciconia_ciconia%29.jpg",
        category=AnimalCategory.VOGEL,
        habitat="Feuchtwiesen und offene Landschaften in Europa, überwintert in Afrika",
        conservation_status="nicht gefährdet, lokal geschützt",
        reproduction_mode=ReproductionMode.EGG_LAYING,
        offspring_count="3–5 Eier pro Gelege",
        gestation_period="Brutzeit ca. 33 Tage",
        diet="Frösche, Insekten, kleine Nagetiere",
        natural_enemies="Adler, Uhu (v. a. für Jungvögel)",
        social_behavior=SocialBehavior.HERD,
        group_size="lockere Kolonien, wenige bis mehrere Paare",
        character_traits="Ruhig, standorttreu, klappert mit dem Schnabel zur Kommunikation.",
    ),
    dict(
        name_de="Clownfisch",
        name_scientific="Amphiprion ocellaris",
        image_url="https://upload.wikimedia.org/wikipedia/commons/5/58/Common_clownfish.jpg",
        category=AnimalCategory.FISCH,
        habitat="Korallenriffe im Indopazifik, lebt in Symbiose mit Seeanemonen",
        conservation_status="nicht gefährdet",
        reproduction_mode=ReproductionMode.EGG_LAYING,
        offspring_count="100–1000 Eier pro Gelege",
        gestation_period="Eier schlüpfen nach ca. 6–10 Tagen",
        diet="Plankton, Algen, kleine Krebstiere",
        natural_enemies="größere Raubfische",
        social_behavior=SocialBehavior.HERD,
        group_size="kleine Gruppen an einer Wirtsanemone",
        character_traits="Territorial rund um die eigene Anemone, wechselt bei Bedarf das Geschlecht.",
    ),
    dict(
        name_de="Hecht",
        name_scientific="Esox lucius",
        image_url="https://upload.wikimedia.org/wikipedia/commons/0/09/Esox_lucius1.jpg",
        category=AnimalCategory.FISCH,
        habitat="Seen und langsam fließende Flüsse in Europa, Nordasien und Nordamerika",
        conservation_status="nicht gefährdet",
        reproduction_mode=ReproductionMode.EGG_LAYING,
        offspring_count="mehrere Tausend Eier pro Laichzeit",
        gestation_period="Eier schlüpfen nach ca. 2 Wochen",
        diet="Fische, gelegentlich Frösche und Wasservögel",
        natural_enemies="größere Hechte, Fischotter (v. a. für Jungfische)",
        social_behavior=SocialBehavior.SOLITARY,
        group_size=None,
        character_traits="Lauerjäger, territorial, gefräßig.",
    ),
    dict(
        name_de="Siebenpunkt-Marienkäfer",
        name_scientific="Coccinella septempunctata",
        image_url="https://upload.wikimedia.org/wikipedia/commons/4/4a/Coccinella_septempunctata.jpg",
        category=AnimalCategory.INSEKT,
        habitat="Wiesen, Gärten und Felder in Europa",
        conservation_status="nicht gefährdet",
        reproduction_mode=ReproductionMode.EGG_LAYING,
        offspring_count="bis zu mehreren Hundert Eiern über die Saison",
        gestation_period="Larvenentwicklung ca. 3–4 Wochen",
        diet="Blattläuse und andere kleine Insekten",
        natural_enemies="Vögel, Spinnen, parasitische Wespen",
        social_behavior=SocialBehavior.SOLITARY,
        group_size=None,
        character_traits="Nützlich für den Garten, wehrt Fressfeinde mit bitterem Sekret ab.",
    ),
    dict(
        name_de="Honigbiene",
        name_scientific="Apis mellifera",
        image_url="https://upload.wikimedia.org/wikipedia/commons/4/4a/Honeybee-27527-1.jpg",
        category=AnimalCategory.INSEKT,
        habitat="Weltweit in Kulturlandschaften, lebt in Völkern in Bienenstöcken",
        conservation_status="nicht akut gefährdet, aber unter Druck (Pestizide, Parasiten)",
        reproduction_mode=ReproductionMode.EGG_LAYING,
        offspring_count="die Königin legt bis zu 2000 Eier pro Tag",
        gestation_period="Entwicklung Ei bis Biene ca. 21 Tage",
        diet="Nektar und Pollen",
        natural_enemies="Varroamilbe, Hornissen, Bienenfresser",
        social_behavior=SocialBehavior.HERD,
        group_size="Völker von mehreren Zehntausend Tieren",
        character_traits="Hochorganisiert, fleißig, kommuniziert über den Schwänzeltanz.",
    ),
    dict(
        name_de="Feuersalamander",
        name_scientific="Salamandra salamandra",
        image_url="https://upload.wikimedia.org/wikipedia/commons/4/4a/Feuersalamander.JPG",
        category=AnimalCategory.SONSTIGES_LANDTIER,
        habitat="Feuchte Laubwälder in Mittel- und Südeuropa",
        conservation_status="nicht gefährdet, lokal durch Pilzerkrankung bedroht",
        reproduction_mode=ReproductionMode.LIVE_BEARING,
        offspring_count="20–40 Larven pro Wurf",
        gestation_period="Trächtigkeit ca. 8–10 Monate",
        diet="Insekten, Spinnen, Regenwürmer, Schnecken",
        natural_enemies="Ringelnatter, manche Vögel (Warnfarbe schützt vor vielen Fressfeinden)",
        social_behavior=SocialBehavior.SOLITARY,
        group_size=None,
        character_traits="Nachtaktiv, dämmerungsliebend, auffällig gelb-schwarz gefärbt als Warnsignal.",
    ),
    dict(
        name_de="Ringelnatter",
        name_scientific="Natrix natrix",
        image_url="https://upload.wikimedia.org/wikipedia/commons/9/95/Natrix_natrix_top.jpg",
        category=AnimalCategory.SONSTIGES_LANDTIER,
        habitat="Gewässernähe in Europa, oft in Teichen und Feuchtgebieten",
        conservation_status="gefährdet (regional unterschiedlich)",
        reproduction_mode=ReproductionMode.EGG_LAYING,
        offspring_count="10–30 Eier pro Gelege",
        gestation_period="Eier schlüpfen nach ca. 6–10 Wochen",
        diet="Frösche, Kröten, kleine Fische",
        natural_enemies="Greifvögel, Störche, Füchse",
        social_behavior=SocialBehavior.SOLITARY,
        group_size=None,
        character_traits="Ungiftig, scheu, stellt sich bei Gefahr tot oder gibt Sekret ab.",
    ),
]


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
        print(f"{len(ANIMALS)} Beispieltiere eingefügt.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
