# AGENTS.md — Quick reference for agents

## Commands

### Backend (`backend/`, Python/FastAPI)

- Run all tests: `python -m pytest tests/ -v`
- Run single test: `python -m pytest tests/test_api.py::test_quiz_flow_updates_spaced_repetition -v`
- Dev server: `uvicorn app.main:app --reload` (from `backend/`, port 8000)
- New migration: `alembic revision --autogenerate -m "message" && alembic upgrade head`
- Seed 300 animals: `python -m app.seed.seed_data`
- No linter or formatter is configured

### Frontend (`frontend/`, React/Vite/TypeScript)

- Typecheck + build: `npm run build` (this is `tsc -b && vite build`)
- Dev server: `npm run dev` (port 5173, expects backend on 8000)
- No frontend test suite exists

## Key gotchas

- **No linter/formatter** — don't look for one or run lint commands
- **Frontend typecheck = `npm run build`** — no separate `typecheck` script
- **German everywhere** — domain terms (Steckbrief, Tages-Tier, Weiterklick), seed JSON keys, UI copy, many code identifiers. Don't "translate" identifiers.
- **Three-layer field naming** — German seed JSON key → English snake_case DB column/Python attr → German `<dt>` label. All three must be renamed together. See `backend/app/seed/seed_data.py` mapping dict.
- **Seen = Collected** — marking an animal "seen" IS the collection mechanic. No separate favorite/bookmark. Written from exactly one place per flow.
- **Cooldown is shared** — one pool (`ANIMAL_COOLDOWN_DAYS`, default 5) covers both Weiterklick and Tages-Tier. No per-feature cooldown.
- **Tages-Tier is persisted** at first request, not recalculated. Recalculating would shift the cooldown pool.
- **Six fields are nullable** — `fun_fact`, `superpower`, `mating_season`, `nest_building`, `courtship_dance`, `relationship_status`. See ADR 0006.

## Architecture (read these for depth)

- `CLAUDE.md` — full architecture, layer conventions, cross-cutting rules
- `CONTEXT.md` — domain glossary (Steckbrief, Tages-Tier, Weiterklick, Cooldown, Gesehen, etc.)
- `docs/adr/` — 6 ADRs covering SQLite, JWT, "Sehen = Sammeln", Docker single-container, seed mapping, nullable fields
- `tierlexikon-app-projektskizze.md` — original project sketch
