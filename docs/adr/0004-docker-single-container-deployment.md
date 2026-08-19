---
status: accepted
---

# Ein Container liefert Frontend und Backend gemeinsam aus

Für das Deployment baut ein einziges Multi-Stage-`Dockerfile` das React/Vite-Frontend und kopiert den Build-Output in das FastAPI-Image; `uvicorn` liefert dort neben der API auch die SPA aus (Static-Mount + Catch-all-Fallback-Route für clientseitiges Routing). Dadurch reicht ein `docker run`/`docker compose up` für die gesamte App, es gibt keine zweite Origin und damit kein CORS-Handling in Produktion — das Frontend ruft die API über relative Pfade auf (`VITE_API_BASE_URL` wird beim Build bewusst leer gelassen, siehe `Dockerfile`). Der Trade-off: das verwischt die in `CLAUDE.md` beschriebene bewusste Trennung "zwei unabhängig laufende Hälften" zugunsten eines einzelnen deploybaren Artefakts, und beide Teile lassen sich in diesem Setup nicht mehr unabhängig skalieren oder neu ausrollen. Der lokale Dev-Workflow (Backend via `uvicorn --reload`, Frontend via `npm run dev` auf Port 5173) bleibt davon unberührt — die Static-Mount-Logik in `app/main.py` aktiviert sich nur, wenn ein Frontend-Build-Verzeichnis im Image vorhanden ist. Sollte später eine unabhängige Skalierung/Auslieferung nötig werden, bleibt der Wechsel auf zwei Container (z. B. Backend + Nginx-Container fürs Frontend) ein reiner Packaging-Umbau, da Frontend- und Backend-Build im Dockerfile bereits als getrennte Stages existieren.
