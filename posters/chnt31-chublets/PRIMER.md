# PRIMER: Poster chnt31-chublets

Arbeitsplan und Gedächtnis **dieses einen Posters**. Der Kern (Engine, Themes, Schriften) steht im
[PRIMER.md des Kits](../../PRIMER.md) und in [GUIDE.md](../../GUIDE.md); hier steht nur, was dieses Poster betrifft.
Ein Chat, ein Poster, ein Schritt: wer weiterarbeitet, liest zuerst Teil A und den Schritt in Teil B.

Stand: 31.10.2026 (Runde 2)

---

## Teil A: Rahmen und Beschlusslage

### A1 Anlass

| | |
|---|---|
| Veranstaltung | CHNT31, Beitrag zum Digital Creative Award (Poster); gleicher Track wie `chnt31-fdox` |
| Ort, Datum | offen (D1); auch im Brief von `chnt31-fdox` steht es noch nicht |
| Format | A0 hoch (siehe `poster.yaml`, `page:`); vom Autor bestätigt, Vorgabe der Tagung nicht geprüft (D7) |
| Abgabe / Druck bis | nicht nötig (Autor, 31.10.2026: „das ist egal“) |
| URL | https://www.chnt.at/ (wie bei `chnt31-fdox`) |
| Theme | `chublets` (siehe `poster.yaml`, `theme:`) |
| Fakten | `brief.yaml`; `poster.yaml` liest sie per `{{ brief.… }}` |
| Ansprechpartner | Florian Thiery (LEIZA) |

### A2 Zielbild

Das Poster ist fertig, wenn:

1. Titel, Kernaussage und die sechs Stationen aus zwei Metern lesbar sind. Kernaussage (Vorschlag von Claude, vom Autor
   übernommen): „Open research software for cultural heritage would become findable, citable and queryable as Linked Data
   in a chublets Wikibase.“
2. Jede Zahl und jedes SPARQL-Ergebnis eine Quelle und ein Abfragedatum hat (Teil C, `data/sparql/`).
3. `python main.py --poster chnt31-chublets --strict` ohne Warnung läuft (setzt voraus: `event.place` und `event.dates`
   ausgefüllt, `status: final`).
4. chublets.software als bestehender Hub erkennbar ist (Autor, Runde 2: „da existiert ja“).

### A3 Regeln für dieses Poster

- Sprache der Texte: britisches Englisch; `PRIMER.md` Deutsch; im Chat Deutsch (du).
- Formal wie `chnt31-fdox`: Titel eine Zeile, fetter Untertitel, Rückgrat als `flow`, danach Grafikstreifen (Runde 2
  statt Zoom-Karten und SPARQL-Karten), Karten People, Explore, Behind the work, References unten (Vorgabe des Autors).
- Ein Absatz höchstens 40 Wörter, ein Aufzählungspunkt höchstens 15.
- Zahlen: nur mit Quelle und Abfragedatum (`brief.numbers`); Texte verweisen darauf.
- Konzepte, die nicht laufen, im Konditional und `planned` (gestrichelt). Zurzeit gibt es keines: alle sechs Stationen sind durchgezogen.
- Nichts auf dem Poster, was nicht in Teil C begründet ist; Fakten aus dem Gedächtnis stehen in Teil D.

### A4 Beschlusslage

| Beschluss | Begründung | Datum |
|---|---|---|
| Poster-Ordner `chnt31-chublets`, Theme `chublets`, A0 hoch | Standard; Autor bestätigt Theme `chublets` im Interview (Runde F) | 2026-10-31 |
| Das Poster folgt formal `chnt31-fdox` | Autor: „nimm dir generell ein Beispiel an chnt31-fdox“ | 2026-10-31 |
| Track „Digital Creative Award“ | Autor bestätigt, gleicher Track | 2026-10-31 |
| Arbeitstitel „Code is Data, Too“, eine Zeile, Untertitel fett | Autor (Runde F, „wie fdox“); der eingereichte Titel folgt | 2026-10-31 |
| Titel = eingereichter Titel „From open-archaeo to chublets.software: A Wikidata Pipeline for Archaeological Research Software“, unverändert, zwei Zeilen (Umbruch nach dem Doppelpunkt, `title_lines: 2`, Titel 70 pt); ersetzt den Arbeitstitel „Code is Data, Too“ | Autor nennt den Titel 2026-11-02; der Titel deckt nur Wikidata ab, das Poster zeigt auch statische Demo, Federation Wikibase und Hub; Vorschlag von Claude, den Titel nicht zu ändern (Programm und Poster bleiben gleich) | 2026-11-02 |
| Untertitel (eine Zeile, fett): „Chublets: from a curated list to a FAIR software marketplace, with Wikibase“ | Vorschlag von Claude: trägt, was der Titel nicht nennt (Chublets, Marktplatz, Wikibase); eine Zeile statt zwei spart rund 22 mm Kopfhöhe, dadurch bleibt der Titel bei 70 pt statt am Minimum von 60 pt | 2026-11-02 |
| Grafikstreifen `max_height_mm` 259 / 189 / 139 (vorher 260 / 190 / 140) | Die zweite Titelzeile kostet Höhe; die Streifen geben je 1 mm ab, Basisschrift bleibt bei 30 pt | 2026-11-02 |
| Rückgrat als `flow` mit sechs Stationen: open-archaeo, Prepare, Wikidata, Static demo, Federation Wikibase, chublets.software | Beschluss der Übergabe; Station „Prepare“ trägt OpenRefine und Python (Abbildung `open-archaeo-two-routes` aus chublets-visuals) | 2026-10-31 |
| Federation Wikibase (`chublets-wikibase.de`) als **Prototyp, durchgezogen** (Übergabe sagte `planned`) | Autor entscheidet nach Hinweis: PRIMER von wikibase-static führt sie als befüllt (980 Einträge, Push 2026-10-25). Live nicht geprüft; keine Zahl aus dem Push auf dem Poster | 2026-10-31 |
| chublets.software als Marktplatz: **existiert**, Station 6 durchgezogen, kein Konditional (ersetzt `planned`) | Autor, Runde 2: „da existiert ja!!!“ | 2026-10-31 |
| Beispiel-Chublet: SPARQLing Unicorn QGIS Plugin (Demo-Item Q360, Wikidata Q74005133) | Wunsch des Autors | 2026-10-31 |
| Sechs Grafiken aus `chublets-software/chublets-visuals` (Commit f408631, CC BY 4.0, Florian Thiery) in drei Streifen: Modell (`chublet-item`, `class-tree`), Crosswalk (`chublets-wikibase-datamodel`, `model-evidence-base`), Architektur (`static-vs-federation`, `chublets-four-step-pattern`) | Autor, Runde 2: Auswahl 1, 3, 4, 8, 10, 15; ersetzt die Entscheidung der Runde 1 (keine Bilder). Die neuen Grafiken tragen die Zahl 168 (Stand 2026-10-25), nicht mehr die veralteten | 2026-10-31 |
| Die drei Grafikstreifen sind **eine** Karte (`figures`, drei `image_row`-Teile), ohne Bildunterschriften; Legende „Solid boxes…“ im Journey-Streifen entfernt; Autofit-Deckel 30 pt (`theme_overrides`), damit der Platz den Grafiken bleibt | Autor, Runde 3 | 2026-10-31 |
| Explore: nur zwei QR-Codes (Browse the chublets, chublets Wikibase); Foto von Florian Thiery aus `chnt31-fdox` übernommen, die anderen drei bleiben Initialen | Autor, Runde 3 | 2026-10-31 |
| Behind the work: zwei Logos, zwei Logos, dann die drei (LEIZA, RSE / CAA, Wikimedia / DFG, NFDI, NFDI4Objects); die Zeile „Graphics: chublets-visuals“ aus den References entfernt (Grafiken sind vom Autor selbst, CC BY 4.0; Herkunft steht in `img/README.md`) | Autor, Runde 5 | 2026-10-31 |
| Zwei SPARQL-Karten vom Poster genommen; Dateien bleiben in `data/sparql/` | Autor, Runde 2: mehr Bilder, Abfragen raus | 2026-10-31 |
| Kopfzeile: vier Zugehörigkeitszeilen, Einrichtungen mit Komma getrennt, je Autor eine Zeile (1 bis 4) | Autor, Runde 2 | 2026-10-31 |
| Autorenfolge: Thiery (1), Gey (2), Lobinsky (3), Schubert (4); Zeilen siehe Brief | Autor: „genau so“; danach ergänzt: Thiery zusätzlich de-RSE e.V., Schubert zusätzlich CAA e.V. | 2026-10-31 |
| Wikimedia Deutschland, Berlin, Germany | Autor wählt diese Form | 2026-10-31 |
| Kopf-Logo: chublets-Rabe | Autor; Nutzungsbedingungen offen (D4) | 2026-10-31 |
| Personen-Karte mit Initialen, Fotos liefert der Autor nach | Autor | 2026-10-31 |
| QR-Ziele: Demo-Seite, wikibase-static, chublets-wikibase.de, open-archaeo | Autor | 2026-10-31 |
| SPARQL (Runde 1): Abfrage 1 gegen Wikidata, Abfrage 2 gegen die RDF-Datei der Demo | überholt durch Runde 2 (Abfragen nicht mehr auf dem Poster) | 2026-10-31 |
| Zahlenkacheln gestrichen | Platz; 416 steht in Station 1, 168 in den Grafiken; `brief.numbers` bleibt Beleg | 2026-10-31 |

### A5 Befehle (Windows und Ablauf: [../../WORKFLOW.md](../../WORKFLOW.md))

```
python main.py --poster chnt31-chublets                 # bauen: dist/poster.pdf und poster-preview.png
python main.py --poster chnt31-chublets --strict          # Release-Prüfung
python main.py --poster chnt31-chublets --blocks          # Blockliste als Markdown für Teil C
python tools/build_all.py --poster chnt31-chublets --check-repro   # zweimal bauen, PDFs müssen gleich sein
```

---

## Teil B: Schritte

| Schritt | Inhalt | Status |
|---|---|---|
| P0 | Gerüst, Interview Runden A, B, E, F, Autorenfolge zurückgespiegelt, `brief.yaml` | fertig 2026-10-31 (Ort und Datum offen, D1) |
| P1 | Kernaussage und Gliederung; Runde 2: neun Blöcke, vier Bänder plus Streifen | fertig 2026-10-31 |
| P2 | Texte, Zahlen, Quellen; SPARQL Abfrage 2 gelaufen (nicht mehr auf dem Poster) | fertig bis auf D6, D13 |
| P3 | Abbildungen (sechs gewählt, eingebaut), Fotos der Personen, Logos | in Arbeit (Fotos, Logos CAA und Wikimedia, D3, D4; Lesbarkeit D5) |
| P4 | Layout feinjustieren, Vorschau prüfen | Runde 2 gebaut, Puffer 1 mm; Lesbarkeit der Grafiken noch zu entscheiden (D5) |
| P5 | `--strict` grün, `status: final`, Druckfreigabe | offen |

---

## Teil C: Blöcke, Quellen, Warum

| Block | Rolle | Titel | Warum | Quelle / Stand |
|---|---|---|---|---|
| `hook` | problem | 1 · Software hides in plain sight | Problem in zwei Sätzen | Abstract der Einreichung nicht gefunden; Formulierung vom Autor zu bestätigen (D6) |
| `idea` | aim | The idea: chublets | Definition; chublets.software als Hub | README `chublets-wikibase-demo`; Autor, Runde 2 |
| `journey` | method | The life of one chublet | Rückgrat, sechs Stationen, alle durchgezogen | Beschlüsse A4 |
| `figures` | method | (Karte ohne Titel, drei Streifen) | Modell (`chublet-item`, `class-tree`), Crosswalk (`chublets-wikibase-datamodel`, `model-evidence-base`), Architektur (`static-vs-federation`, `chublets-four-step-pattern`) | chublets-visuals, Commit f408631, CC BY 4.0; Item Q360 der Demo; 168 Properties |
| `team` | context | People | Namen, später Fotos | `brief.people`; Einwilligung D3 |
| `links` | resources | Explore | QR-Ziele | `brief.links`; Erreichbarkeit nicht geprüft (D8) |
| `supporters` | resources | Behind the work | Förderer, Netzwerke | `brief.supporters`; Logo-Regeln D4 |
| `references` | references | References | Quellen der Repos, Crosswalk, Grafiken (CC BY 4.0) | `brief.references` |

---

## Teil D: Offene Punkte

| Nr. | Frage | Wer entscheidet | Stand |
|---|---|---|---|
| D1 | CHNT31: Ort und Datum (`event.place`, `event.dates`); auch bei fdox offen | Autor | offen |
| D2 | Wikidata-Abfrage nicht mehr auf dem Poster (Runde 2); `data/sparql/wikidata-chublets.rq` bleibt ungelaufen, nur falls sie später wieder gebraucht wird | Autor | erledigt für dieses Poster |
| D3 | Fotos aller vier Personen sind drin (vom Autor geliefert, Zuordnung vom Autor bestätigt 2026-10-31); Einwilligung von Gey, Lobinsky, Schubert noch zu bestätigen | Autor, Abgebildete | Einwilligung offen |
| D4 | Logos: Nutzungsregeln (DFG, NFDI, NFDI4Objects, LEIZA, RSE, chublets-Rabe, CAA Germany, Wikimedia Deutschland; die beiden letzten vom Autor am 2026-10-31 geliefert, Wikimedia-Logo schwarz, Beschnitt auf den Inhalt); Förderhinweis DFG bestätigen | Autor | offen |
| D5 | Schriftgröße der Grafiken auf A0 (Runde 3: Streifen höher, Basisschrift 28 pt): `class-tree`, `model-evidence-base`, `chublets-wikibase-datamodel`, `chublet-item` haben kleine Schrift (Näherung 9 bis 11 pt, kleinste Beschriftungen darunter); Entscheidung: eine Grafik streichen, `class-tree` auf volle Breite, oder so lassen | Autor | offen |
| D6 | Eingereichter Titel steht seit 2026-11-02 im Poster (siehe A4); Abstract liegt weiter nicht vor: `hook` und `idea` gegen den Abstract prüfen | Autor | Titel erledigt, Abstract offen |
| D7 | Formatvorgabe der Tagung (A0 hoch) | Autor | offen |
| D8 | Live-Seiten: Demo (GitHub Pages), chublets-wikibase.de, Repos prüfen; aus der Sandbox kein Zugriff (HTTP 403 des Proxys). Auch die Frage, ob `chublets-wikibase.de` öffentlich lesbar ist | Autor | offen |
| D9 | Grafik `chublets-four-step-pattern` und `model-evidence-base` nennen 826 Items und 6873 Aussagen; Abgleich mit dem Demo-Stand (6 852 Zeilen in `statements.csv`, 2026-10-31) offen. Zahlen des Wikibase-Pushs (980 Einträge, 7 012 Aussagen, Lauf 2026-10-25) stehen nur im PRIMER von wikibase-static; nicht auf dem Poster, solange kein Livewert mit Datum vorliegt | Autor | offen |
| D10 | Das README der Demo nennt noch „five“ Wikidata-Seeds, die CSV hat sechs; Poster nutzt sechs. Hinweis an das Demo-Repo | Autor | offen |
| D11 | 153 (Starter Pack), 158 (Demo-CSV) und 168 (chublets-visuals, 10 Kern + 149 + 9): das Poster nutzt 168 wie die Grafiken (`brief.numbers.1`) | Autor | erledigt 2026-10-31 |
| D12 | 442 (RDF, Merges einmal gezählt) gegenüber 444 (CSV-Zeilen mit „instance of chublet“); Poster nutzt 442 im Brief, im Text nur 416 | Autor | erledigt 2026-10-31 |
| D13 | OpenRefine-Seite mit find.software: im Poster nur als „OpenRefine and Python“ in Station 2 (Beleg: Abbildung `open-archaeo-two-routes`); die Rolle von find.software bitte ergänzen oder bestätigen | Autor | offen |
| D14 | Lizenz des Posters und `CITATION.cff` (DOI, Zitierzeile) | Autor | offen |
| D15 | Zugehörigkeiten: Städte für CAA e.V. und de-RSE e.V. wurden nicht genannt, also nicht gedruckt; Schreibweise „de-RSE e.V.“ wie geliefert | Autor | offen |
| D16 | ORCID und DOI fehlen in `CITATION.cff` von wikibase-static (TODO dort); Zitierung des Werkzeugs steht ohne DOI | Autor | offen |

---

## Änderungsprotokoll

| Datum | Änderung | Anlass |
|---|---|---|
| 31.10.2026 | Gerüst übernommen, Interview A, B, E, F, erster Bau, Abfrage 2 gelaufen | Übergabe und Chat |
| 31.10.2026 | Runde 2: chublets.software als bestehend, sechs Grafiken aus chublets-visuals in drei Streifen, SPARQL-Karten und Zoom-Karten entfernt, Kopf mit vier Zugehörigkeitszeilen | Rückmeldung des Autors |
| 31.10.2026 | Runde 3: Grafiken in eine Karte, ohne Unterschriften; Legende weg; zwei QR-Codes; Foto Thiery | Rückmeldung des Autors |
| 31.10.2026 | Runde 4: Fotos der vier Personen, Logos CAA Germany und Wikimedia Deutschland, Explore vertikal zentriert | Rückmeldung des Autors |
| 31.10.2026 | Runde 5: Logos in Zeilen 2 + 2 + 3, Grafik-Zeile aus den References | Rückmeldung des Autors |
| 31.10.2026 | Runde 6: Reference find.software (https://find-software.org/) ergänzt | Rückmeldung des Autors |
| 02.11.2026 | Runde 7: eingereichter Titel auf zwei Zeilen (70 pt), neuer einzeiliger Untertitel, Grafikstreifen je 1 mm niedriger | Rückmeldung des Autors |
