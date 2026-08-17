from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import animals, auth, categories, daily_animal, discover, progress, quiz

settings = get_settings()

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
