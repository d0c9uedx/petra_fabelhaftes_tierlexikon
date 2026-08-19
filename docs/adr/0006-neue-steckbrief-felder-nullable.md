---
status: accepted
---

# Neue Steckbrief-Felder sind bewusst nullable

Die sechs neuen Steckbrief-Felder (`fun_fact`/Funfakt, `superpower`/Superkraft, `mating_season`/Balzzeit,
`nest_building`/Nestbau, `courtship_dance`/Tanz der Liebe, `relationship_status`/Beziehungsstatus) sind —
anders als der Rest des `Animal`-Modells — als `nullable=True` modelliert. Das durchbricht die bisher
faktisch geltende Erwartung, jeder Steckbrief sei vollständig ausgefüllt: alle 150 Bestandstiere hatten
bislang für jedes Feld einen Wert, und selbst `group_size`, das einzige zuvor nullable Feld, wird vom
Seed-Skript durchgehend als `None` befüllt statt tatsächlich genutzt. Grund für die neue Nullability: die
sechs Felder verlangen Internet-Recherche pro Tierart, und nicht jede der 300 Arten hat für jedes Feld eine
seriös belegbare Antwort — `relationship_status` etwa ist für viele Fische und Insekten ohne Paarbindung
schlicht nicht klassifizierbar. Statt erfundener Platzhaltertexte bleibt das Feld dann explizit `NULL`, und
sowohl Seed-Skript als auch Frontend (`AnimalProfile.tsx`) behandeln `NULL` als regulären, darstellbaren
Zustand — die betroffene Zeile bleibt sichtbar und zeigt den Platzhaltertext "Noch unbekannt" statt eines
erfundenen Werts. Der Trade-off: künftige Contributor:innen dürfen `NULL` bei diesen sechs Feldern nicht als
Datenlücke missverstehen und blind nachpflegen wollen, solange die Recherche vorher ehrlich versucht wurde;
sollte ein Feld später verpflichtend werden, ist das eine bewusste künftige Entscheidung mit eigener
Migration (`nullable=False` + Backfill), kein Automatismus.
