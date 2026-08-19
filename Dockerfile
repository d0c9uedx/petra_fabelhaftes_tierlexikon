# Single-Container-Deployment: Backend (FastAPI) liefert das gebaute Frontend
# (React/Vite-SPA) mit aus. Siehe docs/adr/0004-docker-single-container-deployment.md
# für die Begründung und den Trade-off gegenüber getrennten Containern.

# --- Stage 1: Frontend bauen ------------------------------------------------
FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ ./

# Leer lassen (same-origin/relative API-Pfade): die SPA und die API laufen im selben
# Container auf demselben Origin, unabhängig davon, auf welchen Host/Port er gemappt
# wird. Siehe frontend/src/api/client.ts (apiFetch nutzt VITE_API_BASE_URL + Pfad).
ARG VITE_API_BASE_URL=""
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
RUN npm run build

# --- Stage 2: Backend + gebautes Frontend -----------------------------------
FROM python:3.11-slim AS backend
WORKDIR /app

COPY backend/ ./
RUN pip install --no-cache-dir . \
    && chmod +x entrypoint.sh

COPY --from=frontend-build /app/frontend/dist ./app/static_frontend

EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
