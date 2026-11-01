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

1. Die Leiter aus vier Steinen (Garranes, Dyke, Blackwaterfoot 1, Bishop Loch) ist aus zwei Metern lesbar und steht oben.
2. Der Weg des Zweifels (Auszeichnen, Crosswalk, Gewichten, Schließen) steht in vier Stationen; der ehrliche Block „Where the method does not see the doubt“ gehört dazu.
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
| Wahrheit vor Glanz: Bishop Loch zeigt die Grenze der Methode ehrlich | Entscheidung des Autors; für mehr ist kein Platz | 01.11.2026 |
| Fotos erst, wenn die Repositories erweitert sind und feststeht, was aufs Poster kommt | Entscheidung des Autors | 01.11.2026 |
| Kopf, People und Förderer/Partner nach `chnt31-fdox` | Entscheidung des Autors | 01.11.2026 |
| Autor ist nur Florian Thiery, A0 hoch | Entscheidung des Autors | 01.11.2026 |
| Das CAA-UK-Logo liegt in `shared/logos/caa-uk.png` und steht im Kopf | Lizenz vom Autor bestätigt | 01.11.2026 |
| „Reason“ (Schließen mit der AMT-Engine) ist als geplant gestrichelt | Die AMT-Graphen enthalten keine Axiome; die Engine validiert und exportiert nur (PRIMER von `tei--epidoc-amt`, A1) | 01.11.2026 |
| Die Beispieltabelle der Gewichte zeigt vorerst Gigha 1 (CIIC 506) | Das Repository enthält Dyke, Blackwaterfoot und Bishop Loch noch nicht; Vorschlag, später durch Blackwaterfoot 1 zu ersetzen | 01.11.2026 |

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
| P1 | Kernaussage und Gliederung: 13 Blöcke in 6 Bändern | fertig 01.11.2026, Vorschlag zur Durchsicht |
| P2 | Texte, Zahlen und Quellen in `content/`, Teil C | in Arbeit: Zahlen für Dyke, Blackwaterfoot und Bishop Loch stehen, Ergebnisse aus den Repositories fehlen noch |
| P3 | Fotos der Steine, Ergebnistabelle aus den erweiterten Repositories | offen, wartet auf die Erweiterung von `tei--epidoc-crosswalk` und `tei--epidoc-amt` |
| P4 | Layout feinjustieren, Vorschau prüfen | offen |
| P5 | `--strict` grün, `status: final`, Druckfreigabe | offen |

---

## Teil C: Blöcke, Quellen, Warum

`python main.py --poster caa-uk-2026-ogham --blocks` erzeugt die Tabelle aus `poster.yaml`; hier die Quellen.

| Block | Rolle | Warum | Quelle / Stand |
|---|---|---|---|
| `hook` | problem | Problem in zwei Sätzen | Abstract CAA UK 2026 |
| `idea` | aim | Zwei Achsen, zwei offene Pipelines | READMEs von `tei--epidoc-crosswalk` (cff6341) und `tei--epidoc-amt` (ae78c69), Stand 01.11.2026 |
| `ladder` | result | Rückgrat: vier Steine, Zweifel je Edition | Zählung mit lxml in `lguariento/og-h-am`, Commit 9a68afd (29.10.2026), nur Transliterations-Edition: Garranes (I-COR-030) 3 `supplied`; Dyke (S-MOR-001) 12 `unclear`, 9 `gap`, 3 `choice`, `cert="low"` auf Edition und Datierung; Blackwaterfoot 1 (S-BUT-001) 9 `app`, 6 `rdg`, Datierung `precision="low"`; Bishop Loch (S-LKS-X01) 2 `gap`, sonst keine Zweifelsmarkierung. Abstract-Aussage „absent from CIIC and CISP“: im XML ist `idno type="CIIC"` leer und `idno type="CISP"` gleich „x“. |
| `journey` | method | Vier Stationen | Die vierte (Reason) ist geplant: keine Axiome in den AMT-Graphen |
| `markup` | method | Signale und Sicherheitswerte | `out/README.md` von `tei--epidoc-amt`: unclear 0,5, supplied 0,3, gap 0,0; `choice` und `cert` liest der Konverter noch nicht |
| `crosswalk` | method | Abbildung auf CIDOC CRM | README von `tei--epidoc-crosswalk`; „a reading“ als `TX7`-Segment gemäß Abschnitt zur Ontologie-Korrektur (D9). Koordinatenstatus: asserted 475, qualified 6, textual_only 3, missing 20 (README, 504 Editionen) |
| `weigh` | method | Gewichtsformel und Beispiel | `tei--epidoc-amt`: `weight = c·a / Σ c·a`; Beispiel Gigha 1 (CIIC 506) |
| `limits` | discussion | Ehrliche Grenzen | Garranes: ein Gewicht 1,0 trotz c = 0,92 (PRIMER von `tei--epidoc-amt`, A1 und A4); Bishop Loch: 2 `gap`, sonst keine Markup-Zweifel; das Gewicht wäre 1,0 mit dem Typ Vagueness (aus den `gap`), der Statuszweifel steht nur in Prosa („purported“, „alleged“, „ogham-like“) |
| `question` | result | Schlussfrage und zwei Zahlen | 34 X-Datensätze (13 I, 12 W, 5 E, 4 S), also 21 britische; gezählt an den Dateinamen, Stand 01.11.2026, Commit 9a68afd |
| `links` | resources | Wohin als Nächstes | vier GitHub-Repositories; Adresse der Engine wie im DHd-Abstract (D10) |
| `team` | context | Gesicht zum Namen | Foto aus `chnt31-fdox` |
| `supporters` | resources | Förderer und Partner | Entwurf: Logosatz von `chnt31-fdox` (D3) |
| `references` | references | Literatur | Literaturverzeichnis des DHd-Abstracts, gekürzt |

---

## Teil D: Offene Punkte

| Nr. | Frage | Wer entscheidet | Stand |
|---|---|---|---|
| D1 | Ort ist Glasgow; Datum, Adresse der Tagung und Druckfrist fehlen (`event.*` im Brief) | Autor | offen |
| D2 | Fotos der Steine: Dateien, Lizenzen (Abbildung 4 des DHd-Abstracts nennt CC BY-NC-SA 4.0 für CIIC 81, CC BY 4.0 für CIIC 153, CC BY-SA 4.0 für CIIC 506), Vermerk in `img/README.md` und als Satz im Text; für Dyke, Blackwaterfoot und Bishop Loch (Foto der NMS im XML verlinkt, Rechte dort prüfen) noch nichts | Autor | offen |
| D3 | Welche Logos gehören auf dieses Poster? Entwurf: LEIZA, Research Squirrel Engineers, DFG, NFDI, NFDI4Objects wie bei `chnt31-fdox`; Nutzungsregeln der Logos prüfen | Autor | offen |
| D4 | Sind die Tabellen und Bildunterschriften auf A0 lesbar (28 pt, Basisgröße im Entwurf 29 pt, Puffer 7 mm)? | Autor | offen |
| D5 | Lizenz des Posters und `CITATION.cff` (Zitierzeile, DOI) | Autor | offen |
| D6 | Einwilligung für das Porträt von Florian Thiery: Foto aus `chnt31-fdox`, eigene Person | Autor | erledigt, da eigenes Foto |
| D7 | Formatvorgabe der CAA UK (A0 hoch?) geprüft | Autor | offen |
| D8 | Zugehörigkeit im Kopf: nur „Research Squirrel Engineers Network“ wie vom Autor genannt; im DHd-Abstract stehen zusätzlich LEIZA und CAA e.V. Soll LEIZA in den Kopf? | Autor | offen |
| D9 | `tei--epidoc-crosswalk`: Der Abschnitt „Resolved modelling decisions“ der README nennt noch `TX6_Transcription` für Lesungen, der Abschnitt zur Validierung sagt, dass diese Klasse nicht existiert und `ogham:Reading` unter `TX7_Written_Text_Segment` liegt. Das Poster nutzt `TX7`. In der Repository-Erweiterung klären und die README bereinigen | Autor, Chat zur Repository-Erweiterung | offen |
| D10 | Welche Adresse hat die Engine heute: `n4o-rse/amt-engine` (Abstract, Poster) oder `alpaca-fair-framework/amt-engine` (README von `tei--epidoc-amt`)? | Autor | offen |
| D11 | Bishop Loch: Das Poster sagt, das Gewicht sei 1,0 und der Statuszweifel stehe nur in Prosa. Sobald das Repository den Stein enthält, mit dem echten Ergebnis abgleichen | Autor | offen |
| D12 | Abbildung 6 des DHd-Abstracts zeigt Gigha 1; für das CAA-Poster Blackwaterfoot 1 als Beispiel einsetzen, sobald berechnet | Autor | offen |
| D13 | Tabelle „Where the text lands“: Die Zeile „a reading“ und die Abbildung auf `TX7` ist eine Modellierungsentscheidung der Crosswalk-Autoren, sie soll vor dem Druck nochmals gegen die Ontologie geprüft werden | Autor | offen |

---

## Änderungsprotokoll

| Datum | Änderung | Anlass |
|---|---|---|
| 01.11.2026 | Gerüst angelegt, Brief, 13 Blöcke, Texte, erste Vorschau; Zahlen aus der OG(H)AM-Edition gezählt (nur Transliteration, nicht doppelt) | Start, Entscheidungen des Autors vom 01.11.2026 |
