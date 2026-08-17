---
status: accepted
---

# "Sehen" und "Sammeln" sind ein gemeinsames Datenmodell

Statt eines eigenständigen Sammel-Akts (z. B. ein "Merken"-Button) zählt jeder Steckbrief-Aufruf automatisch zur Sammlung. Das spart im Erstentwurf ein komplettes Datenmodell samt UI-Interaktion, da eine einzige Tabelle (`user_seen_animals`) sowohl für den Cooldown-Pool (Weiterklick/Tages-Tier) als auch für den Sammel-Fortschritt genutzt wird. Der Trade-off: sollte später ein eigenständiges Favorisieren/Merken gewünscht sein (unabhängig vom bloßen Ansehen), müsste diese Tabelle in zwei Konzepte aufgespalten werden — das berührt dann auch die Cooldown-Logik, die aktuell direkt auf `last_seen_at` aufsetzt.
