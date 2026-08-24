---
status: accepted
---

# Taxonomie-Felder Gattung/Familie sind bewusst nullable, Fabelwesen bekommen eine eigene Kategorie

Der Steckbrief bekommt zwei neue Felder, `genus`/Gattung und `family`/Familie, die ganz oben im
Steckbrief stehen — noch vor "Zuhause". Wie schon bei den sechs "Liebesleben"-Feldern
(siehe [0006](0006-neue-steckbrief-felder-nullable.md)) gilt: beide sind `nullable=True`, weil das
Befüllen aller 300 Bestandstiere mit recherchierten, korrekten Gattungs-/Familiennamen ein eigener,
größerer Folgeschritt ist und nicht Teil der Feld-Einführung selbst. Bis dahin liefert die Datenbank
für jedes Bestandstier `NULL`, und `AnimalProfile.tsx` zeigt dafür — wie bei den anderen nullable
Feldern — den Platzhaltertext "Noch unbekannt" statt eines erfundenen Werts.

Eine Besonderheit gegenüber den bisherigen nullable Feldern: die Kategorie `AnimalCategory.FABELWESEN`
existiert im Modell, wird aber aktuell nirgends beim Seeden vergeben (die 300 Bestandstiere bleiben in
ihren fünf ursprünglichen Kategorien). Sie ist vorbereitet für künftige fiktive Tiere, deren Gattung/
Familie dann bewusst fiktiv (Pseudo-Latein) statt real wäre — ein Grund mehr, warum `genus`/`family`
nicht pauschal als "noch zu recherchierende Datenlücke" missverstanden werden dürfen: bei Fabelwesen
gibt es schlicht keine echte Taxonomie nachzutragen.

## Update: Folgeschritt umgesetzt

Der oben angekündigte Folgeschritt ist inzwischen erledigt: `backend/app/seed/data/tierlexikon_taxonomie.json`
liefert für alle 300 Bestandstiere recherchierte Gattungs-/Familiennamen sowie für die neu befüllte
Kategorie `Fabelwesen` (Troll, Zwerg, Gnom, Kobold, Werwolf, Vampir, Elf, Drache, Riese, Fee) bewusst
fiktive, pseudo-lateinische Taxonomie. `seed_data.py` liest diese Datei separat ein (analog zu
`animal_images.json`) und befüllt `genus`/`family` daraus. Bei uneindeutigen Sammelbegriffen im
Ausgangsdatensatz (z. B. "Skorpione", "Tausendfüßer", "Libellen" ohne festgelegte Art) bleibt der
Wert weiterhin bewusst `null` statt geraten — die nullable-Eigenschaft der Felder bleibt also auch
nach dem Befüllen bestehen und ist kein reiner Übergangszustand.
