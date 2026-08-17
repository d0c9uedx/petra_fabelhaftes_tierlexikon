---
status: accepted
---

# SQLite als Start-Datenbank

Die App braucht zum Start keine produktionsreife Mehrbenutzer-Datenbank — SQLite senkt die Einstiegshürde, weil kein separater DB-Server aufgesetzt werden muss. Um eine spätere Migration auf PostgreSQL nicht zu erschweren, verzichten die SQLAlchemy-Modelle bewusst auf SQLite-spezifische Eigenheiten (generische `Enum`-Typen statt Text-Hacks, `DateTime(timezone=True)` konsequent, keine impliziten `AUTOINCREMENT`-Annahmen) und Alembic verwaltet das Schema von Anfang an. Der Wechsel bleibt damit eine reine Änderung der `DATABASE_URL`, kein Modell-Umbau.
