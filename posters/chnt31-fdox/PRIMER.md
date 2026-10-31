# PRIMER: Poster chnt31-fdox

Arbeitsplan und Gedächtnis **dieses einen Posters**. Der Kern (Engine, Themes, Schriften) steht im
[PRIMER.md des Kits](../../PRIMER.md) und in [GUIDE.md](../../GUIDE.md); hier steht nur, was dieses Poster betrifft.
Ein Chat, ein Poster, ein Schritt: wer weiterarbeitet, liest zuerst Teil A und den Schritt in Teil B.

Stand: 31.10.2026 (zweite Runde)

---

## Teil A: Rahmen und Beschlusslage

### A1 Anlass

| | |
|---|---|
| Veranstaltung | CHNT31, Beitrag zum Digital Creative Award (Poster) |
| Ort, Datum | offen (siehe D3) |
| Format | A0 hoch (siehe `poster.yaml`, `page:`); vom Autor im Interview bestätigt, die Vorgabe des Veranstalters wurde online nicht gefunden |
| Abgabe / Druck bis | offen (siehe D3); die Frist des Digital Creative Award lautet laut CIPA-Seite 16.10.2026 |
| Theme | `research-squirrel` (siehe `poster.yaml`, `theme:`) |
| Fakten | `brief.yaml` (Titel, Veranstaltung, Autoren, Personen, Logos, Links, Zahlen mit Quelle, Referenzen); `poster.yaml` liest sie per `{{ brief.… }}` |
| Ansprechpartner | Florian Thiery (LEIZA) |

### A2 Zielbild

Das Poster ist fertig, wenn:

1. Titel, Kernaussage und die sechs Stationen der Journey aus zwei Metern lesbar sind; der Rest trägt die Leserin, die
   dreißig Sekunden bleibt.
2. Jede Zahl und jedes SPARQL-Ergebnis eine Quelle hat (Teil C, `data/sparql/`).
3. `python main.py --poster chnt31-fdox --strict` ohne Warnung läuft (setzt voraus: `event.*` in `brief.yaml`
   ausgefüllt, `status: final`).
4. Der Hinweis „our own perspective, not an official FDO reference implementation“ auf dem Poster steht.

### A3 Regeln für dieses Poster

- Sprache der Texte: Englisch (British English); `PRIMER.md` Deutsch.
- Ein Absatz höchstens 40 Wörter, Aufzählungspunkt höchstens 15; Fließtext nur, wo kein Flow, keine Tabelle und keine
  Abbildung trägt.
- Zahlen: nur mit Quelle und Abfragedatum (`brief.numbers`, Teil C).
- SPARQL-Abfragen auf dem Poster sind die, die wirklich liefen (`data/sparql/*.rq`), die Ergebnisse stammen aus
  `data/sparql/*-result.csv`. Wird die Abfrage gekürzt, steht das auf dem Poster („prefixes omitted“).
- Begriffe: „FDO“ ist das allgemeine Konzept, „FDOx“ die eigene Umsetzung, Mehrzahl „FDOxs“ ohne Apostroph.
- Nichts im Präsens, was nicht läuft; Konzepte stehen im Konditional.
- Nichts auf dem Poster, was nicht in Teil C begründet ist.

### A4 Beschlusslage

| Beschluss | Begründung | Datum |
|---|---|---|
| Format A0 hoch | Standard des Kits; Vorgabe der CHNT31 online nicht gefunden, Autor bestätigt | 2026-10-31 |
| Theme `research-squirrel` | Fira Sans wie in den `fdox-visuals`-Grafiken; passt zu den kopierten Abbildungen. Weicht vom Vermerk „neutral“ im Kern-PRIMER (S5, D12) ab | 2026-10-31 |
| Roter Faden: der Ogham-Stein CIIC 81 aus Cork; Freshford (Heiliger Brunnen) nur klein als zweiter Fall | passt zum Titel; ein Objekt trägt die Erzählung | 2026-10-31 |
| Autorenfolge Thiery (1,2: LEIZA, Research Squirrel Engineers Network), Tharandt (3: HU Berlin) | vom Autor bestätigt, Florian Erstautor; Schreibweise Tharandt bestätigt | 2026-10-31 |
| Titel „From Pocket to SPARQL“ (90 pt, eine Zeile), Rest des Abstract-Titels als Untertitel (52 pt, fett) | vom Autor gewünscht; neben dem großen FDOx-Logo | 2026-10-31 |
| FDOx-Logo (Eichhörnchen) oben rechts im Header (`header.logos`, 140 mm, vertikal zentriert mit der neuen Option `logos_valign: center`); Hook-Karte heißt „1 · A scan in the pocket“ (Nummerierung wie die Stationen) | vom Autor gewünscht | 2026-10-31 |
| Karte „Behind the work“: oben LEIZA und Research Squirrel Engineers, unten DFG, NFDI, NFDI4Objects (Zeilen mit „Funded by“ / „In cooperation with“) | vom Autor gewünscht | 2026-10-31 |
| Package: keine Bildunterschrift; Hinweis auf b-unicycling (CC BY 4.0, via Sketchfab) steht als Satz im Text | vom Autor gewünscht; die Namensnennung der Lizenz bleibt erhalten | 2026-10-31 |
| Hook: Foto des Originals (ungeschnitten) neben dem 3D-Modell, ohne Bildunterschrift | vom Autor gewünscht; Lizenzangabe (CC BY-NC-SA 4.0) steht nicht mehr auf dem Poster, nur in der Lizenztabelle (Query 1) | 2026-10-31 |
| Station 6 „Query“: SPARQL im Browser; NFDI4Objects-Anbindung als geplant genannt | Registry-Stand S7, Anbindung S9 noch offen; vom Autor bestätigt („in Planung“) | 2026-10-31 |
| Query 2 ersetzt: Koordinaten der 3D-Modelle (`spatial.rq`) statt Urheber-Abfrage; Zusatz „prefixes omitted“ entfällt | mehr Ergebniszeilen, räumlicher Bezug; vom Autor gewünscht | 2026-10-31 |
| Logos (DFG, NFDI, NFDI4Objects, LEIZA, Research Squirrel Engineers) in `img/logos/`; Personenfotos größer; `valign: center` neu im Kit (Engine-Änderung in `py/step_render.py`, in GUIDE.md beschrieben) | vom Autor gewünscht | 2026-10-31 |
| Erzählbogen: sechs Stationen Capture, Package, Describe, Deposit, Register, Query | folgt dem Abstract; als nativer `flow` gesetzt, damit er in den Theme-Schriften und aus zwei Metern lesbar bleibt | 2026-10-31 |
| Zoom-Abbildungen aus `fdox-visuals` kopiert (zugeschnitten), nicht neu gezeichnet | „Wiederverwendung heißt Kopieren“; die Step-Nummernmarken der Folien sind abgeschnitten, damit sie nicht mit der Journey-Nummerierung kollidieren | 2026-10-31 |
| Vier-Schritt-Grafik (`fdox-four-step-pattern`) gestrichen | in der verfügbaren Spaltenbreite wäre die Schrift rund 14 pt, nicht lesbar; die Journey trägt die Idee | 2026-10-31 |
| Zahlenkacheln gestrichen | „8 sources · 7,793 triples“ steht bereits in Abbildung 4, die 6 Modelle in der Tabelle; `brief.numbers` bleibt als Beleg | 2026-10-31 |
| Zwei echte SPARQL-Abfragen gegen das Registry-Bundle (Lizenz, Urheber) | der Abstract verspricht echte Abfragen mit Ergebnissen | 2026-10-31 |
| Personen- und Logo-Karte mit den Modulen `people` und `supporters` | vom Autor gewünscht; Logos zunächst als Namenskästchen | 2026-10-31 |
| Referenzen als Karte in der untersten Bandreihe | vom Autor gewünscht; so kostet sie keine eigene Reihe | 2026-10-31 |
| Schreibweise „Louise Tharandt“, Zugehörigkeit HU Berlin | Projektnotiz; bestätigen (D1) | 2026-10-31 |

### A5 Befehle (Windows und Ablauf: [../../WORKFLOW.md](../../WORKFLOW.md))

```
python main.py --poster chnt31-fdox                   # bauen: posters/chnt31-fdox/dist/poster.pdf und poster-preview.png
python main.py --poster chnt31-fdox --theme chublets  # anderes Theme probieren
python main.py --poster chnt31-fdox --strict          # Release-Prüfung: Warnungen werden Fehler
python main.py --poster chnt31-fdox --blocks          # Blockliste als Markdown für Teil C
python tools/build_all.py --poster chnt31-fdox --check-repro   # zweimal bauen, PDFs müssen gleich sein
```

---

## Teil B: Schritte

| Schritt | Inhalt | Status |
|---|---|---|
| P0 | Gerüst aus `_template` angelegt; Interview geführt ([INTERVIEW.md](../../INTERVIEW.md)), `brief.yaml` ausgefüllt, Anlass und Format in A1 | fertig 2026-10-31 (Ort, Datum und Druckfrist offen, D3) |
| P1 | Kernaussage und Gliederung: welche Blöcke, in welcher Reihenfolge | fertig 2026-10-31 |
| P2 | Texte, Zahlen und Quellen in `content/`, Teil C ausfüllen | in Arbeit (Texte und Quellen stehen; Rückmeldung des Autors steht aus) |
| P3 | Abbildungen, Fotos der Personen, Logos der Förderer | in Arbeit (Fotos da, Logos fehlen D4, Foto des Ogham-Steins als Aufhänger gesetzt) |
| P4 | Theme und Layout feinjustieren, Vorschau prüfen | in Arbeit (Seite ist voll: Titel auf der Untergrenze 60 pt, Puffer 3 mm, D9) |
| P5 | `--strict` grün, `status: final`, Druckfreigabe, PDF in `dist/` committen | offen |

Status: `offen`, `in Arbeit`, `fertig` (mit Datum).

---

## Teil C: Blöcke, Quellen, Warum

Quellen der Zahlen und Ergebnisse: Registry-Bundle `dist/fdo-registry.ttl` (Release 2026-09-03, Repository
`fdo-squirrel-registry`, Commit `253aee9`), per `rdflib` abgefragt am 2026-10-31; 7.793 Triples, 8 Einträge, davon 6
vom Typ `fdo:3DDataFDO`.

| Block | Rolle | Titel | Warum | Quelle / Stand |
|---|---|---|---|---|
| `hook` | problem | A scan in the pocket | Das Problem in einem Absatz, dazu das eine Objekt, dem das ganze Poster folgt | Text: Abstract. Bild: `ciic81-original-and-model.png`, zusammengesetzt aus dem Foto des Originals (vom Autor, `ciic81-original.jpg`) und der Vorschau des gepackten Modells (`ciic81-preview.png`) |
| `idea` | aim | The idea: FDOx | Was FDOx ist, der Hinweis „own perspective“ und der Reproduzierbarkeitsanspruch | Text: Abstract; Verweise De Smedt et al. 2020 und Thiery 2026 (Referenzen) |
| `links` | resources | Explore | Wohin die Leserin danach geht | URLs geprüft am 2026-10-31: Registry-Seite und GitHub-Organisation erreichbar; DOI `10.5281/zenodo.18724635` aus `registry/sources.json` (Concept-DOI CIIC 81) |
| `journey` | method | The life of one model | Das Rückgrat: sechs Stationen in Reihenfolge | Abstract; Stationen 1 bis 6 siehe A4 (Status von Station 6: D6) |
| `package` | method | 2 · Package | Zoom auf Station 2 | Abbildung aus `fdox-talk-step1-fdo-encapsulation.png` (zugeschnitten); Modell Freshford von b-unicycling, CC BY 4.0, über Sketchfab (Registry-Eintrag) |
| `describe` | method | 3 · Describe | Zoom auf Station 3 | Abbildung `fdox-fdo-squirrel-architecture.png`; Text: Abstract |
| `register` | context | 4–6 · Register and query | Zoom auf die Stationen 4 bis 6 | Abbildung aus `fdox-talk-step4-federated-kg.png` (zugeschnitten); Text: Abstract |
| `sparql_licence` | result | Query 1: licences | Echte Abfrage, echtes Ergebnis | `data/sparql/licence.rq`, `licence-result.csv` (Registry-Stand siehe oben) |
| `sparql_spatial` | result | Query 2: where are the 3D models? | Zweite Abfrage: Koordinaten (schema:latitude/longitude) der 3D-Modelle, 5 Zeilen; Freshford hat im Bundle keine Koordinaten | `data/sparql/spatial.rq`, `spatial-result.csv` (Bundle wie oben) |
| `team` | context | People | Gesichter zu den Namen im Kopf | Fotos vom Autor geliefert, `img/people/`; Einwilligung D2 |
| `supporters` | resources | Behind the work | Förderer, Infrastruktur, Institut, Netzwerk | Logos vom Autor geliefert (`img/logos/`); Nutzungsregeln D4 |
| `references` | references | References | Belege für das Konzept und die beiden Repositories | `brief.references`, vom Autor geliefert |

### Befunde beim Bau

- **CIIC 81 im Registry-Bundle:** Der Eintrag heißt dort „CO074-148----“ (Version-DOI `10.5281/zenodo.22675886`,
  Concept-DOI `10.5281/zenodo.18724635`, laut `registry/sources.json`). In der Lizenztabelle steht deshalb „CO074-148----
  (CIIC 81)“.
- **Leeres Ergebnis:** Die Urheber-Abfrage mit `foaf:name` lieferte nichts, das Bundle benutzt `schema:name`. Typisches
  Symptom einer falschen IRI (siehe Registry-PRIMER S7).
- **Doppelte Zeile:** Ohne `FILTER(STRSTARTS(... "https://spdx.org/licenses/"))` erscheint Freshford zweimal, weil das
  Paket eine zweite, nicht-SPDX-Lizenz-IRI trägt. Der Filter steht deshalb auch auf dem Poster.
- **Platz:** Die erste Fassung war 375 mm zu hoch für A0 bei 28 pt; der Kopf allein brauchte 291 mm. Gekürzt durch Streichen
  der Vier-Schritt-Grafik und der Zahlenkacheln, kürzere Texte und Umbau der Spalten.

---

## Teil D: Offene Punkte

| Nr. | Frage | Wer entscheidet | Stand |
|---|---|---|---|
| D1 | Autorenfolge, Schreibweise, Zugehörigkeiten | Florian | erledigt 2026-10-31 |
| D2 | Einwilligung von Louise Tharandt für ihr Foto; Foto von Florian ist ein freigestelltes Rundbild | Florian, Louise | offen |
| D3 | CHNT31: Ort, Datum, Druckfrist, Postergröße und Regeln des Digital Creative Award (online nicht gefunden; Kontakt laut Seite: info@chnt.at) | Florian | offen |
| D4 | Logos: Dateien geliefert; Nutzungsregeln der Logos (DFG, NFDI, NFDI4Objects, LEIZA, RSE) prüfen, bevor das Repo öffentlich so bleibt; FDOx-Squirrel hat kein Logo; Förderhinweis (DFG) inhaltlich bestätigen | Florian | offen |
| D5 | Lizenz des Originalfotos: auf dem Poster steht keine Bildunterschrift mehr; Fotograf:in und Lizenz in `img/README.md` ergänzen | Florian | offen |
| D6 | Station 6: NFDI4Objects-Anbindung ist geplant, nicht umgesetzt; Poster sagt „planned“ | Florian | erledigt 2026-10-31 |
| D7 | Zoom-Abbildungen sind klein (Schrift in der Grafik etwa 10 pt): größer auf Kosten anderer Blöcke oder als native `flow`-Blöcke neu zeichnen | Florian | offen |
| D8 | Lizenz des Posters, `CITATION.cff` für das Poster und ggf. Zenodo-Deposit; der Baustein `cite` ist nicht benutzt | Florian | offen |
| D9 | Seite ist voll: Titel auf 60 pt, Puffer 3 mm; jede Textverlängerung braucht eine Kürzung an anderer Stelle | Florian | offen |
| D10 | SPARQL-Ergebnisse vor dem Druck neu abfragen, falls die Registry seit Release 2026-09-03 gewachsen ist | Florian | offen |
| D11 | Referenzen: Format Autor-Jahr, Eintrag „Squirrel Papers, 8(2), §4“ wie geliefert; Verweise im Text („De Smedt et al., 2020“, „Thiery, 2026“) prüfen | Florian | offen |

---

## Änderungsprotokoll

| Datum | Änderung | Anlass |
|---|---|---|
| 2026-10-31 | Gerüst angelegt, Interview (Format, Theme, Objekt, Autoren), `brief.yaml`, Texte, zwei SPARQL-Abfragen mit Ergebnissen, Abbildungen aus `fdox-visuals`, erster Bau | Start |
| 2026-10-31 | Personen-Karte mit Fotos, Logo-Karte (Namenskästchen), Referenzen; Layout auf drei Spalten in der untersten Reihe | Rückmeldung des Autors |
| 2026-10-31 | Titel zweizeilig, Florian Erstautor, RSE als Zugehörigkeit, Hook-Bilder, Query 2 spatial, Logos, größere Fotos, Station 6 „planned“, `valign` im Kit | zweite Rückmeldung des Autors |
| 2026-10-31 | Runde 3: Nummer 1 an der Hook-Karte, FDOx-Logo im Header, Logo-Karte neu gruppiert, Package ohne Bildunterschrift | dritte Rückmeldung des Autors |
| 2026-10-31 | Runde 4: Untertitel entfernt, Titelumbruch nach „Stone“, FDOx-Logo größer und zentriert, mehr Abstand zwischen den Hook-Bildern, „Next“-Satz in 4–6 entfernt, Zoom-Grafiken größer | vierte Rückmeldung des Autors |
| 2026-10-31 | Runde 5: Titel 57 pt, Autoren 44 pt, Zugehörigkeiten 32 pt mit kleinen Hochzahlen (neue Header-Optionen `authors_pt`, `affil_pt`), Explore mit vier QR-Codes (neu: FDOx-Paper, Zenodo 10.5281/zenodo.18441544) und einzeiligen Beschriftungen, Describe-Grafik größer | fünfte Rückmeldung des Autors |
| 2026-10-31 | Runde 6: Titel „From Pocket to SPARQL“ groß, Rest als Untertitel; Namen 36 pt, Zugehörigkeiten 26 pt; Karten-Option `center_last` (Grafik vertikal zentriert unter dem Text) bei Package, Describe, Register; Header-Option `subtitle_pt` | sechste Rückmeldung des Autors |
| 2026-10-31 | Runde 7: Titel 90 pt, Untertitel 52 pt fett (neue Header-Option `subtitle_bold`) | siebte Rückmeldung des Autors |
