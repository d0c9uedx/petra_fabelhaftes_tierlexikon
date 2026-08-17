# Projektskizze: Tierlexikon-App

## Grundidee

Eine App (Web-App, umgesetzt mit Python/FastAPI im Backend) als digitales Tierlexikon. Nutzer können Tiere nach Kategorien durchstöbern, bekommen kompakte Steckbriefe mit Bild, und perspektivisch gibt es ein Sammel- und Quiz-System mit Spaced-Repetition-Logik.

## Kategorien

- Vögel
- Fische
- Käfer / Insekten
- Säugetiere
- sonstige Landtiere (Nicht-Säugetiere, z. B. Reptilien, Amphibien)

Nutzer sollen nach diesen Kategorien filtern können.

## Steckbrief pro Tier (Datenfelder)

| Feld | Beschreibung |
|---|---|
| Name (deutsch) | Alltagsname |
| Name (wissenschaftlich) | Gattungs-/Artname |
| Bild / Thumbnail | Bild-URL |
| Kategorie | Vogel / Fisch / Insekt / Säugetier / sonstiges Landtier |
| Lebensraum | Wo das Tier vorkommt |
| Häufigkeit / Gefährdungsstatus | z. B. IUCN-Status, häufig / selten / bedroht |
| Fortpflanzung | Eier legend oder lebendgebärend |
| Nachkommen | Anzahl pro Wurf/Gelege |
| Brutzeit / Tragzeit | Dauer |
| Ernährung | Lieblingsnahrung |
| Natürliche Feinde | Wer das Tier frisst |
| Sozialverhalten | Einzelgänger oder Herdentier; bei Herdentier ungefähre Gruppengröße |
| Charaktereigenschaften | 1–2 Sätze, z. B. gutmütig, vertrauensvoll, scheu |

### Beispiel: Kapibara

- Name: Kapibara (Hydrochoerus hydrochaeris)
- Kategorie: Säugetier
- Lebensraum: Ufernähe von Flüssen und Sümpfen, Süd- und Mittelamerika
- Gefährdungsstatus: nicht gefährdet, Bestand stabil
- Fortpflanzung: lebendgebärend, Tragzeit ca. 5 Monate
- Nachkommen: meist 3–5 Jungtiere pro Wurf
- Ernährung: Wasserpflanzen, Gräser, Rinde
- Natürliche Feinde: Jaguare, Kaimane, Anakondas, Greifvögel
- Sozialverhalten: Herdentier, typische Gruppengröße 10–20 Tiere
- Charakter: gesellig, friedlich, sehr entspannt und verträglich mit anderen Tieren

## Kern-Features

1. **Kategorie-Browsing**: Nutzer wählt Kategorie, sieht Liste der Tiere.
2. **Tages-Tier**: täglich wird ein Tier vorgeschlagen (Steckbrief + Bild).
3. **Weiterklick-Funktion**: durch Tiere klicken, zufällige Reihenfolge; bereits gesehene Tiere fallen für eine Weile aus dem Vorschlag heraus (Cooldown-Logik).
4. **Sammel-Fortschritt**: Speicherung, welche Tiere ein Nutzer bereits gesehen hat.
5. **Quiz mit Spaced Repetition** (perspektivisch):
   - Pro Nutzer und Tier wird gespeichert, wie oft richtig/falsch beantwortet wurde.
   - Falsch beantwortete Tiere werden häufiger erneut abgefragt, ähnlich einem Vokabeltrainer.
   - Datum der letzten Abfrage wird gespeichert, um das Timing für die nächste Abfrage zu berechnen.
6. **Mehrbenutzer-Unterstützung**: mehrere Nutzer-Accounts, jeweils eigener Sammel- und Quiz-Fortschritt.

## Technische Architektur

- **Frontend**: React oder Vue (Kategorie-Auswahl, Steckbrief-Ansicht, Quiz-UI)
- **Backend**: Python mit FastAPI
- **Datenbank**: relational (z. B. PostgreSQL oder SQLite zum Start)
- **Bilder**: extern gehostet oder als URL-Referenzen in der Datenbank, nicht fest in die App eingebaut (App bleibt schlank, lädt Daten/Bilder vom Backend nach)

### Grobes Datenmodell

1. **animals** — alle Steckbrief-Felder aus der Tabelle oben
2. **users** — Nutzerkonten (für Mehrbenutzer-Unterstützung)
3. **user_seen_animals** — welcher Nutzer hat welches Tier wann gesehen (Basis für Tages-Vorschlag und Cooldown)
4. **user_quiz_progress** — pro Nutzer und Tier: Zähler richtig/falsch beantwortet, Datum letzte Abfrage (Basis für Spaced-Repetition-Timing)

## Startpunkt: Tierlisten pro Kategorie (je 30 bekannte Arten)

### Vögel

Hausrotschwanz, Amsel, Kohlmeise, Blaumeise, Rotkehlchen, Star, Haussperling, Elster, Rabenkrähe, Buchfink, Mauersegler, Rauchschwalbe, Mehlschwalbe, Kuckuck, Waldkauz, Steinadler, Weißkopfseeadler, Turmfalke, Mäusebussard, Graureiher, Weißstorch, Höckerschwan, Stockente, Graugans, Pfau, Flamingo, Kaiserpinguin, Strauß, Kolibri, Papagei (Ara)

### Fische

Karpfen, Forelle, Hecht, Zander, Barsch, Wels, Aal, Hering, Kabeljau, Thunfisch, Lachs, Seezunge, Makrele, Sardine, Goldfisch, Guppy, Zebrabärbling, Diskusfisch, Clownfisch, Kaiserfisch (Kaiserangelfisch), Rochen, Hammerhai, Weißer Hai, Seepferdchen, Fugu (Kugelfisch), Piranha, Karpfenlaus-Wirt Koi, Marlin, Schwertfisch, Anglerfisch

### Käfer / Insekten

Marienkäfer (Siebenpunkt), Maikäfer, Hirschkäfer, Rosenkäfer, Laufkäfer, Borkenkäfer, Kartoffelkäfer, Leuchtkäfer (Glühwürmchen), Mistkäfer, Nashornkäfer, Honigbiene, Hummel, Wespe, Hornisse, Ameise, Termite, Florfliege, Libelle, Heuschrecke, Grille, Gottesanbeterin, Stabheuschrecke, Stubenfliege, Stechmücke, Schmetterling (Admiral), Schwalbenschwanz, Kohlweißling, Monarchfalter, Seidenspinner, Wanderheuschrecke

### Säugetiere

Löwe, Tiger, Elefant, Giraffe, Zebra, Nashorn, Nilpferd, Gorilla, Schimpanse, Braunbär, Eisbär, Wolf, Fuchs, Reh, Hirsch, Wildschwein, Igel, Eichhörnchen, Maulwurf, Fledermaus, Delfin, Blauwal, Orca, Kapibara, Koala, Känguru, Panda, Waschbär, Otter, Luchs

### Sonstige Landtiere (Nicht-Säugetiere)

Chamäleon, Leguan, Bartagame, Gecko, Krokodil, Alligator, Schildkröte (Landschildkröte), Boa Constrictor, Klapperschlange, Kobra, Ringelnatter, Blindschleiche, Waran (Komodowaran), Frosch (Grasfrosch), Kröte, Feuersalamander, Axolotl, Molch, Spinne (Kreuzspinne), Vogelspinne, Skorpion, Tausendfüßer, Regenwurm, Schnecke (Weinbergschnecke), Nacktschnecke, Seestern, Qualle, Krake, Krabbe, Languste

## Offene Punkte für die Weiterentwicklung

- Genaue technische Wahl: PostgreSQL vs. SQLite
- Bildquellen klären (Lizenzfragen bei extern gehosteten Bildern)
- Detaillierte Steckbrief-Daten für die 150 Tiere oben recherchieren und befüllen
- Authentifizierung/Login-Konzept für Mehrbenutzer-Unterstützung
- Genaues Cooldown-Timing für "bereits gesehene Tiere" festlegen
- Quiz-UI-Konzept (Multiple Choice? Freitext? Bild-Erkennung?)
