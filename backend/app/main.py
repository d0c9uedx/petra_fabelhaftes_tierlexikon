import mimetypes
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.routers import animals, auth, categories, daily_animal, discover, progress, quiz

settings = get_settings()

# Python's mimetypes module doesn't know .webp on all platforms (e.g. Debian slim).
# Register it explicitly so FileResponse / StaticFiles serve the correct Content-Type.
mimetypes.add_type("image/webp", ".webp")

app = FastAPI(title="Petras fabelhaftes Tierlexikon", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(animals.router)
app.include_router(discover.router)
app.include_router(daily_animal.router)
app.include_router(progress.router)
app.include_router(quiz.router)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}


# Im Single-Container-Deployment (siehe docs/adr/0004) kopiert das Docker-Image den
# gebauten Frontend-Build hierher; im lokalen Dev-Workflow (`uvicorn --reload` ohne
# Frontend-Build) existiert das Verzeichnis nicht, und dieser Block bleibt komplett inaktiv.
FRONTEND_DIST = Path(__file__).parent / "static_frontend"

if FRONTEND_DIST.is_dir():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="frontend-assets")
    app.mount("/images", StaticFiles(directory=FRONTEND_DIST / "images"), name="frontend-images")

    @app.get("/{full_path:path}", include_in_schema=False)
    def serve_frontend(full_path: str):
        """SPA-Fallback: liefert existierende Build-Dateien aus, sonst index.html
        (React-Router übernimmt clientseitig). Wird zuletzt registriert, damit die
        API-Router oben immer Vorrang behalten."""
        candidate = FRONTEND_DIST / full_path
        if full_path and candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(FRONTEND_DIST / "index.html")
