# PRIMER: Poster caa-uk-2026-ogham

Arbeitsplan und Gedächtnis **dieses einen Posters**. Der Kern (Engine, Themes, Schriften) steht im
[PRIMER.md des Kits](../../PRIMER.md) und in [GUIDE.md](../../GUIDE.md); hier steht nur, was dieses Poster betrifft.
Ein Chat, ein Poster, ein Schritt: wer weiterarbeitet, liest zuerst Teil A und den Schritt in Teil B.

Stand: 01.11.2026 (erste Runde)

---

## Teil A: Rahmen und Beschlusslage

### A1 Anlass

| | |
|---|---|
| Veranstaltung | CAA UK 2026, Poster; eingereichtes Abstract „Purported, Alleged, Undetermined: Four Degrees of Doubt in the Ogham Corpus“ |
| Ort, Datum | Glasgow; Datum offen (D1) |
| Format | A0 hoch; vom Autor am 01.11.2026 bestätigt, Vorgabe des Veranstalters noch nicht geprüft (D7) |
| Abgabe / Druck bis | offen (D1) |
| Theme | `caa-uk` (siehe `poster.yaml`, `theme:`); Palette und Schrift am 01.11.2026 vom Autor bestätigt |
| Fakten | `brief.yaml`; `poster.yaml` liest sie per `{{ brief.… }}` |
| Autor | Florian Thiery, Zugehörigkeit „Research Squirrel Engineers Network“ (D8) |

### A2 Zielbild

1. Die Karte und die Leiter aus drei Steinen (Garranes, Dyke, Blackwaterfoot 1) sind ohne Vorwissen lesbar und stehen oben.
2. Ein Stein (Gigha 1) läuft ganz durch: Lesungen, TEI, CRM-Graph, gewichtete Aussage, Axiome und Reasoning, Regel v1 gegen v2; der ehrliche Block „Where the method is blind“ gehört dazu.
3. Jede Zahl auf dem Poster hat eine Quelle (Teil C und `brief.yaml`, `numbers:`).
4. Was das Repository (noch) nicht kann, ist als „to do“ oder gestrichelt markiert, nie als erledigt.
5. `python main.py --poster caa-uk-2026-ogham --strict` läuft ohne Warnung.

### A3 Regeln für dieses Poster

- Sprache der Texte: britisches Englisch; dieses PRIMER ist Deutsch.
- Orange (`caa-uk`) steht nur für Zweifel: Rolle `problem`, der Block „limits“, Konzept-Boxen.
- Zahlen: nur mit Quelle und Datum der Abfrage. Gezählt wird in der **Transliterations-Edition** (`subtype="transliteration"`), weil die Ogham-Edition denselben Text noch einmal enthält und alles doppelt zählt.
- Nichts auf dem Poster, was nicht in Teil C begründet ist; was die Repositories nicht belegen, steht nicht als erledigt da.

### A4 Beschlusslage

| Beschluss | Begründung | Datum |
|---|---|---|
| Wahrheit vor Glanz: Die Grenzen der Methode stehen als Tabelle „Where the method is blind“ (vier Zeilen) | Entscheidung des Autors | 01.11.2026 |
| Aufbau: Karte, Leiter aus Steinen mit wachsendem Zweifel, ein Stein (Gigha 1) ganz durch TEI, CRM, AMT und Reasoning, dann Grenzen, Ausblick, Links, Personen | Entscheidung des Autors im Dialog | 01.11.2026 |
| Bishop Loch ist aus Leiter und Karte gestrichen; vier Grade des Zweifels: Garranes, Dyke und Blackwaterfoot 1 in der Leiter (Grad 1 bis 3), Gigha 1 als Grad 4 im Beispielband | Entscheidung des Autors: mehr Platz für das Reasoning-Beispiel | 01.11.2026 |
| Das Reasoning wird gezeigt, mit den Axiomen im AMT-Stil (Subsumtion, Rollenkette mit Produktlogik, Disjunktion) und den abgeleiteten Gewichten je Herausgeber | `tei--epidoc-amt` hat seit 0.5.0 fünf Axiome; der frühere Beschluss „Reason als geplant“ entfällt | 01.11.2026 |
| Grafiken entstehen aus Skripten im Poster-Ordner (`figures/`), die PNGs sind eingecheckt | Entscheidung des Autors: Skripte gehören ins Poster-Repo | 01.11.2026 |
| Ogham-Schrift wird aus den Daten gesetzt (Noto Sans Ogham), Markup (`unclear`, `supplied`, `gap`, `choice`) bleibt sichtbar | Entscheidung des Autors | 01.11.2026 |
| Kopf: Logo ohne weißen Rahmen, ohne die Zeile „Computer Applications …“, dunkleres Blau als Kopfband | Entscheidung des Autors | 01.11.2026 |
| Explore: ein QR-Code auf `https://linkedopenogham.github.io/tei--epidoc-crosswalk/`; „Behind the work“: nur Research Squirrel Engineers und NFDI4Objects, nebeneinander, ohne Text | Entscheidung des Autors | 01.11.2026 |
| Referenz „SPARQLing Ogham“ ersetzt durch Thiery et al. (2026), JOHD 12(1), 10, doi:10.5334/johd.425 | Entscheidung des Autors; Angaben von der Artikelseite | 01.11.2026 |
| Kopf, People nach `chnt31-fdox`; Autor ist nur Florian Thiery, A0 hoch | Entscheidung des Autors | 01.11.2026 |
| Das CAA-UK-Logo liegt in `shared/logos/caa-uk.png`, der Kopf nutzt die Kopie `caa-uk-short.png` | Lizenz vom Autor bestätigt | 01.11.2026 |

### A5 Befehle (Windows und Ablauf: [../../WORKFLOW.md](../../WORKFLOW.md))

```
python main.py --poster caa-uk-2026-ogham                 # bauen: posters/caa-uk-2026-ogham/dist/poster.pdf und poster-preview.png
python main.py --poster caa-uk-2026-ogham --strict          # Release-Prüfung: Warnungen werden Fehler
python main.py --poster caa-uk-2026-ogham --blocks          # Blockliste als Markdown für Teil C
```

---

## Teil B: Schritte

| Schritt | Inhalt | Status |
|---|---|---|
| P0 | Gerüst, `brief.yaml`, Anlass und Format | fertig 01.11.2026 (Datum, URL, Druckfrist offen: D1) |
| P1 | Kernaussage und Gliederung: 16 Blöcke in 6 Bändern | fertig 01.11.2026, in Überarbeitung mit dem Autor |
| P2 | Texte, Zahlen und Quellen in `content/`, Teil C | fertig im Entwurf, Zahlen mit Quelle im Brief |
| P3 | Fotos der Steine, Ergebnisse aus den erweiterten Repositories | Fotos und Gewichte sind drin; Fotorechte offen (D2) |
| P4 | Layout feinjustieren, Vorschau prüfen | läuft (Runden mit dem Autor) |
| P5 | `--strict` grün, `status: final`, Druckfreigabe | offen |

---

## Teil C: Blöcke, Quellen, Warum

`python main.py --poster caa-uk-2026-ogham --blocks` erzeugt die Tabelle aus `poster.yaml`; hier die Quellen.

| Block | Rolle | Warum | Quelle / Stand |
|---|---|---|---|
| `map` | context | Das ganze Corpus mit Status; wer ohne Vorwissen kommt, sieht, worum es geht | `out/places.geojson` von `tei--epidoc-crosswalk`, Corpus `og-h-am` 9a68afd: 486 Fundorte mit Koordinate (455 nummeriert, 24 zweifelhaft (X), 7 verloren (L)); Status aus dem Serienbuchstaben der Kennung. Grundkarte: Natural Earth (gemeinfrei). Skript `figures/map_corpus.py` |
| `hook` | problem | Problem in zwei Sätzen | Abstract CAA UK 2026 |
| `idea` | aim | Zwei Achsen, zwei offene Pipelines | READMEs von `tei--epidoc-crosswalk` und `tei--epidoc-amt`, Stand 01.11.2026 |
| `question` | result | Schlussfrage mit drei Zahlen | 34 X-Datensätze (13 I, 12 W, 5 E, 4 S), also 21 britische, an den Dateinamen gezählt, Commit 9a68afd; 20 Steine ohne Koordinate (10 zweifelhaft, 7 verloren, 3 nummeriert): 506 Editionen minus 486 Fundorte |
| `ladder` | result | Rückgrat: drei Steine, Zweifel je Edition, Ogham, Transliteration mit Markup, Gewichtsbalken | Zählung mit lxml in `lguariento/og-h-am`, Commit 9a68afd, nur Transliterations-Edition: Garranes (I-COR-030) 3 `supplied`; Dyke (S-MOR-001) 12 `unclear`, 9 `gap`, 3 `choice`, `cert="low"`; Blackwaterfoot 1 (S-BUT-001) 9 `app`, 6 `rdg`; Gewichte aus `out/*.amt.ttl` von `tei--epidoc-amt`. Skript `figures/ladder_rows.py` |
| `gigha_photo`, `gigha_readings` | method | Stein 4 (Gigha 1, CIIC 506): fünf Herausgeber, fünf Lesungen, Anteile | `out/gigha1.amt.ttl`: 0,2727 (Macalister 1902 und 1945), 0,1818 (OG(H)AM-Edition, Rhys 1899), 0,0909 (Rhys 1901), Regel v2 |
| `gigha_graph` | method | Eine Lesung durch Achse 1 (CRM, CRMtex) und Achse 2 (AMT) | Modell nach README von `tei--epidoc-crosswalk` (E22, TX1, TX7, E21) und `tei--epidoc-amt` |
| `gigha_reasoning` | method | Axiome im AMT-Stil und abgeleitete Gewichte je Herausgeber | `ontology/ogham-amt.ttl` von `tei--epidoc-amt` (fünf Axiome, davon drei gezeigt: Subsumtion, Rollenkette `hasReading` dann `attributedTo` mit Produktlogik, Disjunktion), `out/README.md` |
| `gigha_rules` | method | Regel v1 gegen v2 | `cert="low"` auf der Edition: 0,18 zu 0,13 (Edition), 0,27 zu 0,29 (je Macalister-Lesung); Zahlen aus den Graphen beider Regeln |
| `limits` | discussion | Ehrliche Grenzen in vier Zeilen | ein Gewicht 1,0 trotz Zweifel (Garranes, drei ergänzte Buchstaben); Gewichte sind Anteile, keine Wahrscheinlichkeiten (Formel `c·a / Σ c·a`); Zweifel in Prosa unsichtbar („purported“, „alleged“ am Bishop Loch, nur in Worten); anonyme Lesungen (Blackwaterfoot 1: drei Lesungen ohne Herausgeber) |
| `outlook` | outlook | Wohin es geht | drei Punkte: alle 34 zweifelhaften Datensätze, Herausgeber nach den anonymen Lesungen fragen, Zweifel in Prosa als Markup (Vorschlag) |
| `links` | resources | Wohin als Nächstes | ein QR-Code: `https://linkedopenogham.github.io/tei--epidoc-crosswalk/` |
| `team` | context | Gesicht zum Namen | Foto aus `chnt31-fdox` |
| `supporters` | resources | Partner | Research Squirrel Engineers und NFDI4Objects (D3) |
| `references` | references | Literatur | fünf Einträge, DOI als Kurzlink |

---

## Teil D: Offene Punkte

| Nr. | Frage | Wer entscheidet | Stand |
|---|---|---|---|
| D1 | Ort ist Glasgow; Datum, Adresse der Tagung und Druckfrist fehlen (`event.*` im Brief) | Autor | offen |
| D2 | Fotos der Steine: Urheber stehen in den TEI-`<desc>` (Garranes: Nora White; Dyke, Blackwaterfoot 1, Gigha 1: Megan Kasten), Lizenzen nicht. Mit den Herausgebern klären und als Satz auf das Poster setzen (zurzeit keine Zeile, kein Platz). Das Foto von Blackwaterfoot 1 hat nur 480 x 319 px und wirkt im Druck weich. Das Foto des Bishop Loch (NMS) ist nicht mehr im Poster | Autor | offen |
| D3 | Logos: auf dem Poster nur Research Squirrel Engineers und NFDI4Objects (Beschluss des Autors); Nutzungsregeln der beiden Logos prüfen | Autor | Logoauswahl entschieden, Regeln offen |
| D4 | Sind Tabellen und Bildunterschriften auf A0 lesbar? Basisgröße 29,5 pt; die Schrift in den Grafiken (Axiom-Schema, Ergebnistabelle) ist klein | Autor | offen |
| D5 | Lizenz des Posters und `CITATION.cff` (Zitierzeile, DOI) | Autor | offen |
| D6 | Einwilligung für das Porträt von Florian Thiery: Foto aus `chnt31-fdox`, eigene Person | Autor | erledigt, da eigenes Foto |
| D7 | Formatvorgabe der CAA UK (A0 hoch?) geprüft | Autor | offen |
| D8 | Zugehörigkeit im Kopf: nur „Research Squirrel Engineers Network“ wie vom Autor genannt; im DHd-Abstract stehen zusätzlich LEIZA und CAA e.V. Soll LEIZA in den Kopf? | Autor | offen |
| D9 | `tei--epidoc-crosswalk`: Der Abschnitt „Resolved modelling decisions“ der README nennt noch `TX6_Transcription` für Lesungen, der Abschnitt zur Validierung sagt, dass diese Klasse nicht existiert und `ogham:Reading` unter `TX7_Written_Text_Segment` liegt. Das Poster nutzt `TX7`. In der Repository-Erweiterung klären und die README bereinigen | Autor, Chat zur Repository-Erweiterung | offen |
| D10 | Welche Adresse hat die Engine heute: `n4o-rse/amt-engine` (Abstract, Poster) oder `alpaca-fair-framework/amt-engine` (README von `tei--epidoc-amt`)? | Autor | offen |
| D11 | Bishop Loch: Gewicht 1,0, Typ Vagueness, Statuszweifel nur in Prosa, bestätigt am Repository; der Stein steht nicht mehr als Beispiel auf dem Poster, nur als Aussage in „Where the method is blind“ | Autor | erledigt |
| D12 | Beispielstein: Gigha 1 gewählt (Stein 4), Blackwaterfoot 1 steht in der Leiter | Autor | erledigt |
| D13 | Tabelle „Where the text lands“: Die Zeile „a reading“ und die Abbildung auf `TX7` ist eine Modellierungsentscheidung der Crosswalk-Autoren, sie soll vor dem Druck nochmals gegen die Ontologie geprüft werden | Autor | offen |

| D14 | „Four Degrees“ im Titel: die Leiter heißt „Four degrees of doubt“, Garranes, Dyke und Blackwaterfoot 1 sind Grad 1 bis 3, Gigha 1 ist Grad 4 (Zweifel an der Edition selbst, `cert="low"`, Regel v2 verschiebt die Gewichte). Der Statuszweifel des Abstracts (Bishop Loch, „purported“) steht nur noch in „Where the method is blind“ | Autor | erledigt (Option A, 01.11.2026) |
| D15 | `--strict` ist rot, solange Datum, Adresse und Druckfrist (D1) fehlen | Autor | offen |

---

## Änderungsprotokoll

| Datum | Änderung | Anlass |
|---|---|---|
| 01.11.2026 | Gerüst angelegt, Brief, 13 Blöcke, Texte, erste Vorschau; Zahlen aus der OG(H)AM-Edition gezählt (nur Transliteration, nicht doppelt) | Start, Entscheidungen des Autors vom 01.11.2026 |
| 01.11.2026 | Überarbeitung mit dem Autor in mehreren Runden: Karte, Leiter, Gigha 1 durch TEI, CRM, AMT und Reasoning, Axiome im AMT-Stil; Grafikskripte in `figures/`; Bishop Loch gestrichen; Kopf mit dunklem Band und Logo ohne Platte; ein QR-Code; Referenz JOHD; kleine Engine-Erweiterungen (S16 im PRIMER des Kerns) | Wünsche des Autors vom 01.11.2026 |
| 01.11.2026 | Titelfrage gelöst: Leiter „Four degrees of doubt“, Zeilenmarken „Degree 1“ bis „Degree 3“, Gigha-Band „Degree 4“ | Wunsch des Autors, Option A |
