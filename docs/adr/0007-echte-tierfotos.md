---
status: accepted
---

# Echte Tierfotos statt reiner Kategorie-Platzhalter

ADR 0005 hat die Kategorie-Platzhalter-SVGs als bewusste Interimslösung eingeführt, weil die
Seed-Quelldatei keine Bild-URLs liefert. Inzwischen liegen echte Fotos pro Tier vor
(`backend/app/seed/data/download_wikipedia_images.py` lädt sie per Wikipedia-REST-API,
`animal_images.json` bildet `name_de` auf den Rohbild-Pfad ab). Die Rohbilder selbst sind
groß und in Auflösung/Format uneinheitlich (Originale von Wikipedia, insgesamt mehrere hundert
MB) und bleiben deshalb bewusst außerhalb von Git (bestehende `*.jpg`-Regel in `.gitignore`) —
sie sind über das Download-Skript jederzeit reproduzierbar, kein Repo-Content. Ein neues
Begleitskript (`backend/app/seed/data/prepare_animal_images.py`) verkleinert jedes gefundene
Rohbild proportional auf max. 640px Kantenlänge und konvertiert es nach WebP; die Ausgabe landet
unter `frontend/public/images/animals/<slug>.webp` — also am selben Ort und nach demselben Muster
wie die bestehenden Platzhalter-SVGs (`frontend/public/images/placeholder-*.svg`), regulär
committet, sowohl im lokalen Dev-Setup (Vite serviert `public/` direkt) als auch im
Docker-Single-Container-Deployment (ADR 0004: landet im Frontend-Build und wird vom
SPA-Fallback in `main.py` ausgeliefert) ohne Sonderfall. `seed_data.py` liest
`animal_images.json` zur Seed-Zeit erneut und setzt `image_url` pro Tier entweder auf das echte
Foto oder — falls kein Treffer gefunden wurde — weiterhin auf das Kategorie-Platzhalter-SVG aus
ADR 0005; dieser Fallback-Mechanismus bleibt also vollständig erhalten, nur ergänzt statt ersetzt.

Zwei bewusste Trade-offs: Erstens bekommen die Bilddateien Klartext-Namen aus dem Tiernamen
(z. B. `amsel.webp`) statt anonymisierter Namen. Das ist im Steckbrief unproblematisch, öffnet
im Quiz aber theoretisch eine Seitenkanal-Lücke — `QuizAnimalOut` verschweigt den Tiernamen im
Payload bewusst, damit die Antwort nicht direkt verraten wird, aber über die Bild-URL im
Netzwerk-Tab ließe sich der Name trotzdem erschließen. Klartext-Namen wurden trotzdem gewählt,
weil die bestehende Payload-Absicherung ohnehin nur ein weicher Schutz ist (kein Anti-Cheat-
Anspruch) und anonymisierte Dateinamen einen zweiten Pfad/zweite Kopie pro Bild erfordert
hätten. Zweitens wird die Wikipedia-Lizenz-/Attributionsinformation (`animal_images.json`s
`source`-Feld, ein Link auf die jeweilige Wikipedia-Seite) aktuell nirgends in der UI angezeigt
— falls das Projekt öffentlich betrieben wird, ist eine Bildquellen-/Lizenzseite ein offener
Folge-Punkt, kein Teil dieser Änderung.
