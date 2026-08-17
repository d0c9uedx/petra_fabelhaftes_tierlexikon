# Petras fabelhaftes Tierlexikon

Ein digitales Tierlexikon: Tiere nach Kategorien durchstöbern, Steckbriefe ansehen, sammeln und im Quiz mit Spaced Repetition üben.

Dies ist der **erste Entwurf** (Scaffold) — die Struktur trägt bereits alle geplanten Features, die eigentliche Tierdatenbank (150 Arten) wird im nächsten Schritt befüllt. Aktuell sind 10 Beispieltiere über alle Kategorien geseedet.

Hintergrund und Domänenbegriffe: siehe [CONTEXT.md](./CONTEXT.md). Architekturentscheidungen: siehe [docs/adr/](./docs/adr/).

## Struktur

- `backend/` — Python/FastAPI-API, SQLite (via SQLAlchemy + Alembic)
- `frontend/` — React (Vite + TypeScript)

## Backend starten

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
copy .env.example .env
alembic upgrade head
python -m app.seed.seed_data
uvicorn app.main:app --reload
```

API läuft dann unter http://localhost:8000, interaktive Doku unter http://localhost:8000/docs.

Tests: `python -m pytest tests/ -v`

## Frontend starten

```powershell
cd frontend
npm install
copy .env.example .env
npm run dev
```

App läuft dann unter http://localhost:5173 (Backend muss parallel laufen).

## Kern-Features in diesem Entwurf

1. Kategorie-Browsing
2. Tages-Tier (pro Nutzer, stabil über den Tag)
3. Weiterklick mit Cooldown-Logik
4. Sammel-Fortschritt (= gesehene Tiere)
5. Quiz mit vereinfachtem Spaced-Repetition-Algorithmus (SM-2-artig)
6. Mehrbenutzer-Login (Benutzername/Passwort, JWT)

## Offene Punkte (nächste Schritte)

- Tierdatenbank auf die vollen 150 Arten aus der Projektskizze erweitern
- Bildquellen/Lizenzfragen für die finalen Tierbilder klären
- Migration auf PostgreSQL, sobald Mehrbenutzerbetrieb produktiv wird
