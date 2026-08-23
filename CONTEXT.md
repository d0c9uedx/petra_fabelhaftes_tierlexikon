# Petras fabelhaftes Tierlexikon

Ein digitales Tierlexikon: Nutzer:innen durchstöbern Tiere nach Kategorien, sehen kompakte Steckbriefe und sammeln bzw. üben sie über ein Quiz mit Spaced Repetition.

## Language

**Steckbrief**:
Die kompakte Profil-Darstellung eines Tiers mit allen Datenfeldern (Name, wissenschaftlicher Name, Kategorie, Gattung, Familie, Zuhause, Gefährdungsstatus, Fortpflanzung, Wartezeit aufs Baby, Kinderschar, Lieblingsspeise, Erzfeinde, Gesellschaftsleben, Persönlichkeit, Superkraft, Funfakt, Balzzeit, Nestbau, Tanz der Liebe, Beziehungsstatus). Gattung und Familie stehen als Taxonomie-Felder ganz oben im Steckbrief; sie sind nullable und zeigen bis zur Nachpflege der Bestandstiere "Noch unbekannt" (siehe [docs/adr/0009-taxonomie-felder-gattung-familie.md](./docs/adr/0009-taxonomie-felder-gattung-familie.md)).
_Avoid_: Profil, Karte, Datenblatt

**Beziehungsstatus**:
Ob ein Tier monogam, mit wechselnden Liebhabern oder im Harem lebt. Bleibt explizit leer (nicht "unbekannt" im Sinne einer Datenlücke), wenn die Art keine klassifizierbare Paarbindung hat — das betrifft z. B. viele Fische und Insekten ohne Balz-/Paarbindungsverhalten.
_Avoid_: Paarungssystem, Sozialstruktur (das ist Gesellschaftsleben)

**Superkraft**:
Die Verteidigungs- oder Überlebensstrategie eines Tiers, insbesondere gegen seine Erzfeinde (z. B. Tarnung, Gift, Geschwindigkeit). Abzugrenzen von Funfakt, der ein beliebiges interessantes Detail sein kann.
_Avoid_: Fähigkeit, Talent

**Kategorie**:
Eine von sechs festen Gruppen, nach denen Tiere eingeordnet und gefiltert werden: Vögel, Fische, Käfer/Insekten, Säugetiere, sonstige Landtiere, Fabelwesen. Die Kategorie bestimmt zugleich den Auswahlpool für Quiz-Distraktoren — falsche Antwortoptionen kommen ausschließlich aus derselben Kategorie wie das gefragte Tier.
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
