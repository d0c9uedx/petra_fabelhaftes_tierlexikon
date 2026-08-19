# Petras fabelhaftes Tierlexikon

Ein digitales Tierlexikon: Tiere nach Kategorien durchstöbern, Steckbriefe ansehen, sammeln und im Quiz mit Spaced Repetition üben.

Dies ist der **erste Entwurf** (Scaffold) — die Struktur trägt bereits alle geplanten Features. Die Tierdatenbank ist mit 300 Arten befüllt (60 je Kategorie).

Hintergrund und Domänenbegriffe: siehe [CONTEXT.md](./CONTEXT.md). Architekturentscheidungen: siehe [docs/adr/](./docs/adr/).

## Struktur

- `backend/` — Python/FastAPI-API, SQLite (via SQLAlchemy + Alembic)
- `frontend/` — React (Vite + TypeScript)

## Mit Docker starten

Baut Frontend und Backend in einem einzigen Container (siehe [docs/adr/0004-docker-single-container-deployment.md](./docs/adr/0004-docker-single-container-deployment.md)), migriert das Schema und seedet die 300 Tiere automatisch beim Start:

```powershell
docker compose up --build
```

App läuft dann unter http://localhost:8000 (Frontend + API zusammen). Die SQLite-Datei liegt in einem benannten Docker-Volume (`tierlexikon-data`) und bleibt über Neustarts/Rebuilds erhalten.

## Backend starten (lokal, ohne Docker)

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

## Frontend starten (lokal, ohne Docker)

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

- Echte Tierfotos statt der aktuellen Kategorie-Platzhalterbilder besorgen (Bildquellen/Lizenzfragen klären)
- Migration auf PostgreSQL, sobald Mehrbenutzerbetrieb produktiv wird

## Docker bauen

Image neu bauen und Container starten:

```powershell
docker compose down
docker compose up --build -d
```

Logs anzeigen:

```powershell
docker compose logs -f
```