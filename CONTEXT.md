# Petras fabelhaftes Tierlexikon

Ein digitales Tierlexikon: Nutzer:innen durchstöbern Tiere nach Kategorien, sehen kompakte Steckbriefe und sammeln bzw. üben sie über ein Quiz mit Spaced Repetition.

## Language

**Steckbrief**:
Die kompakte Profil-Darstellung eines Tiers mit allen Datenfeldern (Name, wissenschaftlicher Name, Kategorie, Lebensraum, Gefährdungsstatus, Fortpflanzung, Ernährung, natürliche Feinde, Sozialverhalten, Charaktereigenschaften).
_Avoid_: Profil, Karte, Datenblatt

**Kategorie**:
Eine von fünf festen Gruppen, nach denen Tiere eingeordnet und gefiltert werden: Vögel, Fische, Käfer/Insekten, Säugetiere, sonstige Landtiere.
_Avoid_: Klasse, Typ, Gruppe

**Tages-Tier**:
Das pro Nutzer:in und Kalendertag automatisch bestimmte, vorgeschlagene Tier. Wird beim ersten Abruf des Tages persistiert (nicht bei jedem Request neu berechnet), damit es über den Tag stabil bleibt — unabhängig davon, ob der Abruf selbst den Cooldown-Pool verändert.
_Avoid_: Tier des Tages (als Code-Bezeichner), Vorschlag

**Weiterklick**:
Das zufällige Durchklicken von Tieren außerhalb des Cooldowns, initiiert durch Nutzer:innen-Aktion. Im Code als "Discover" bezeichnet.
_Avoid_: Zufallstier, Browse

**Cooldown**:
Der Zeitraum (Default 5 Tage, konfigurierbar über `ANIMAL_COOLDOWN_DAYS`), in dem ein kürzlich gesehenes Tier weder bei Weiterklick noch als Tages-Tier erneut vorgeschlagen wird. Ein gemeinsamer Pool/Mechanismus deckt beide Features ab — es gibt keinen separaten Cooldown pro Feature.
_Avoid_: Sperrzeit, Pause

**Gesehen** (= Sammel-Fortschritt):
Ein Tier gilt als gesehen, sobald sein Steckbrief angezeigt wurde. Sehen und Sammeln sind identisch — es gibt keine gesonderte Sammel-Aktion (kein "Merken"-Button). Der Sammel-Fortschritt einer Nutzerin ist die Menge ihrer gesehenen Tiere.
_Avoid_: Gesammelt (als eigenständiger Zustand), Favorisiert

**Quiz-Fortschritt**:
Der pro Nutzer:in und Tier gespeicherte Spaced-Repetition-Zustand: Zähler richtig/falsch beantworteter Quizfragen, aktuelles Wiederholungsintervall, Fälligkeitsdatum der nächsten Abfrage. Unabhängig vom Sammel-Fortschritt (ein gesehenes Tier muss nicht im Quiz abgefragt worden sein und umgekehrt).
_Avoid_: Lernfortschritt, Score
