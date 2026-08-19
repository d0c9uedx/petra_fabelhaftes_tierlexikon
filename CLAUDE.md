# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

"Petras fabelhaftes Tierlexikon" — a German-language digital animal encyclopedia. Users browse animals by category, view compact profiles ("Steckbriefe"), and (in later iterations) collect and quiz themselves on them with spaced repetition. This is an early scaffold: the structure supports all planned features end-to-end. The animal database is seeded with 300 species (`backend/app/seed/data/tierlexikon_steckbriefe.json`, 60 per category — the original 150 from the project sketch plus 150 more added later) — real photos are still an open item, animals currently render with one static placeholder image per category (see `tierlexikon-app-projektskizze.md` for the original project sketch).

Read [CONTEXT.md](CONTEXT.md) first for the domain glossary (Steckbrief, Tages-Tier, Weiterklick, Cooldown, Gesehen, Quiz-Fortschritt, Beziehungsstatus, Superkraft) — the code follows this ubiquitous language, in German, throughout models, routes, and UI copy. Architectural decisions with trade-offs are recorded in [docs/adr/](docs/adr/) — check there before revisiting SQLite-vs-Postgres, JWT-vs-session-cookie, the "Sehen = Sammeln" data model, single-container Docker deployment (ADR 0004), the seed data's free-text→enum mapping heuristic (ADR 0005), or why the "Liebesleben" Steckbrief fields are nullable (ADR 0006).

## Commands

### Docker (whole app, one container)

```powershell
docker compose up --build   # http://localhost:8000 — frontend + API together, migrates + seeds on start
```

See ADR 0004 for why it's one container. `Dockerfile` builds the frontend and copies it into the backend image; `backend/app/main.py` only mounts it if the build directory exists, so the plain `uvicorn --reload` dev workflow below is unaffected.

### Backend (`backend/`, Python/FastAPI)

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
copy .env.example .env
alembic upgrade head
python -m app.seed.seed_data      # seeds the 300 animals from app/seed/data/tierlexikon_steckbriefe.json
uvicorn app.main:app --reload     # http://localhost:8000, docs at /docs
```

- Run all tests: `python -m pytest tests/ -v`
- Run a single test: `python -m pytest tests/test_api.py::test_quiz_flow_updates_spaced_repetition -v`
- New migration after model changes: `alembic revision --autogenerate -m "message"`, then `alembic upgrade head`
- No linter/formatter is configured yet.

### Frontend (`frontend/`, React + Vite + TypeScript)

```powershell
cd frontend
npm install
copy .env.example .env
npm run dev        # http://localhost:5173, expects backend running
npm run build       # tsc -b && vite build — use this to typecheck
```

There is no frontend test suite yet.

## Architecture

Monorepo with two independently-run halves talking over HTTP; there is no shared code between them, only a shared API contract. This dev-time separation stays true even though the Docker production build co-locates both halves in one container for deployment convenience (ADR 0004) — the frontend build is copied into the backend image, not merged into its source.

### Backend: layered FastAPI app

`app/main.py` wires everything together (CORS + router includes). Requests flow through distinct layers, each with one job:

- **`routers/`** — one router per feature (`auth`, `categories`, `animals`, `discover`, `daily_animal`, `progress`, `quiz`). Routers own HTTP concerns (status codes, auth dependency) and call into `services/`; they don't contain business logic themselves.
- **`services/`** — the actual domain logic, framework-agnostic:
  - `cooldown_pool.py` — computes the shared "eligible" animal pool (not seen recently) used by *both* Weiterklick and Tages-Tier; falls back to least-recently-seen if the pool is empty.
  - `daily_pick.py` — picks/persists the Tages-Tier. Deliberately **persists** the pick in `user_daily_animal` rather than recomputing it live, because marking an animal "seen" would otherwise shift the cooldown pool mid-day and change the answer on a second request.
  - `seen.py` — the single upsert for `user_seen_animals` ("Sehen = Sammeln", ADR 0003). Any code that wants to mark an animal seen calls this, not the ORM directly.
  - `spaced_repetition.py` — simplified binary SM-2 (no external library); pushes `interval_days`/`easiness_factor`/`next_due_at` on `UserQuizProgress`.
- **`models/`** (SQLAlchemy 2.0) — `Animal`, `User`, `UserSeenAnimal`, `UserQuizProgress`, `UserDailyAnimal`. Kept deliberately Postgres-portable (generic `Enum`, `DateTime(timezone=True)`) even though SQLite is the current store (ADR 0001) — don't introduce SQLite-only types.
- **`schemas/`** — Pydantic I/O models, kept separate from ORM models (e.g. `QuizAnimalOut` intentionally omits `name_de` so the multiple-choice quiz doesn't leak the answer in the question payload).
- **`auth/`** — `security.py` (password hashing via passlib/bcrypt, JWT encode/decode) and `dependencies.py` (`get_current_user`). Auth is JWT bearer tokens, not sessions (ADR 0002); the whole API except `/auth/*` requires a token.

Cross-cutting rule to preserve: **"seen" is written from exactly one place per flow** — the frontend's `AnimalProfile` component calls `POST /animals/{id}/seen` on mount (shared by animal-detail, daily-animal, and discover views), except the Tages-Tier assignment itself, which marks seen server-side at pick time for the stability reason above. Don't add a second seen-marking call for the same flow.

### Frontend: React/Vite SPA

- `router.tsx` defines all routes; everything except `/login` and `/registrieren` sits behind `ProtectedRoute` (redirects to login if `AuthContext` has no user).
- `context/AuthContext.tsx` is the only global state — holds the JWT (via `api/client.ts`'s `localStorage` helpers) and current user. Everything else is local `useState`/`useEffect` per page; there's no Redux/TanStack Query by design (see project history — kept intentionally minimal for this scaffold).
- `api/client.ts` is the single fetch wrapper (`apiFetch`) — attaches the bearer token, serializes JSON or form bodies, throws `ApiError` on non-2xx. All other `api/*.ts` files are thin typed wrappers around it; add new endpoints there rather than calling `fetch` directly in components.
- `components/AnimalProfile.tsx` is the shared Steckbrief renderer and the frontend half of "Sehen = Sammeln" (see cross-cutting rule above) — reuse it rather than duplicating profile markup when adding a new page that shows an animal.
- `types/index.ts` mirrors the backend Pydantic schemas by hand (no codegen) — keep both sides in sync manually when changing an endpoint's shape.

### Data model notes worth knowing before changing it

- Categories are a fixed 5-value enum end-to-end (backend `AnimalCategory`, frontend `AnimalCategory` union type, German labels in `routers/categories.py`): Vögel, Fische, Käfer/Insekten, Säugetiere, sonstige Landtiere. Keep both sides' value strings identical if you touch this.
- The cooldown window is one setting (`ANIMAL_COOLDOWN_DAYS`, default 5) shared by Weiterklick and Tages-Tier — there is intentionally no per-feature cooldown.
- `user_seen_animals` doubles as both "seen" and "collected" state (ADR 0003) — there's no separate favoriting/collection table. If a standalone "favorite" feature is ever added, it needs a new table; don't overload this one further.
- `Animal` Steckbrief fields follow one naming convention throughout: English `snake_case` for the DB column/Python attribute (e.g. `favorite_food`, `arch_enemies`, `home_turf`), a German key in the seed JSON (`lieblingsspeise`, `erzfeinde`, `zuhause`), and a German label in the frontend `<dt>` — all three renamed together if you rename a field, per `backend/app/seed/seed_data.py`'s mapping dict. The six newer "Liebesleben"/character fields (`fun_fact`, `superpower`, `mating_season`, `nest_building`, `courtship_dance`, `relationship_status`) are the only ones that are `nullable` — every other field is `NOT NULL` by convention; see ADR 0006 before adding another nullable field or before treating a `NULL` there as a data gap to backfill.
