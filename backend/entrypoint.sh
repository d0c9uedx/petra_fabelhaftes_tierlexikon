#!/bin/sh
# Startet den Container: Schema migrieren, Tierdaten seeden (idempotent, siehe
# app/seed/seed_data.py), dann den API-Server starten, der bei vorhandenem
# Frontend-Build auch die SPA mit ausliefert (siehe app/main.py).
set -e

alembic upgrade head
python -m app.seed.seed_data
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
