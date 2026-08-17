---
status: accepted
---

# JWT Bearer Token statt Session-Cookie für Auth

Frontend (Vite-Dev-Server) und Backend (FastAPI) laufen als getrennte Prozesse auf unterschiedlichen Ports, auch in Produktion potenziell auf unterschiedlichen Origins. Ein JWT Bearer Token im `Authorization`-Header ist stateless und vermeidet Cookie-/CORS-Komplexität (SameSite, Credentials-Handling). Der Trade-off: ein ausgestelltes Token lässt sich ohne zusätzliche Blacklist-Infrastruktur nicht vorzeitig widerrufen, und die Aufbewahrung im Frontend (localStorage) ist anfälliger für XSS als ein httpOnly-Cookie. Für den Erstentwurf wird das akzeptiert (kurze Token-Lebensdauer statt Widerruf-Mechanismus); ein Wechsel zu Session-Cookies wäre später ein echter Umbau der Auth-Flows.
