# PRIMER – poster-kit

Arbeitsplan für den Kern des Poster-Kits (Engine, Themes, Schriften, geteilte Logos). Einzelne Poster liegen als Ordner in `posters/<id>/` im selben Repository und haben je ein eigenes `PRIMER.md` (Vorlage: `posters/_template/PRIMER.md`); dieses hier gehört keinem Poster. Teil A gilt immer, Teil B ist die Übersicht, Teil C sind die Schritte, Teil D sind offene Punkte.

**Für ein Poster:** Beschlüsse zu Engine, Themes und Schriften gelten für alle Poster und stehen hier. Weicht ein Poster davon ab, steht das mit Datum in dessen PRIMER (Teil A4).

---

## Teil A – Immer gültig

### A1 Ausgangslage

| Was | Wo | Rolle |
|---|---|---|
| Poster | `posters/<id>/` | je Poster: `brief.yaml` (Fakten), `poster.yaml` (Struktur), `content/`, `img/`, `PRIMER.md`, `dist/` |
| Demo und Gerüst | `posters/demo/`, `posters/_template/` | Demo zeigt jede Option; `_template` ist das Gerüst für `--new-poster` |
| Geteilte Logos | `shared/logos/` | Institute, Förderer, Netzwerke; Nutzungsrechte je Datei in der README dort |
| Themes | `themes/<id>/theme.yaml` | Farben (Palette → Tokens), Rollen, Kartenstile, Schriften, Formen |
| Schriftbibliothek | `fonts/<familie>/` | geteilt von allen Themes, mit Lizenz und `SOURCES.md` |
| Engine | `main.py`, `py/` | `theme.py`, `poster_utils.py`, `step_validate.py`, `step_render.py`, `step_preview.py` |
| Erklärung | `GUIDE.md` | jede Option, Themes, Prüfungen, Fork-Ablauf (Englisch) |
| Ausgabe | `posters/<id>/dist/` | erzeugt, nicht von Hand ändern |
| Ablauf | `WORKFLOW.md`, `INTERVIEW.md` | Windows-cmd-Befehle (bauen, GitHub); Interview zum Start eines Posters |

**Befunde** (geprüft 2026-10-09, beim Bau):

- Aus dem CHNT31-Poster abgeleitet: Die erste Engine kannte `purple` und `gold` als feste Namen. Eine andere Palette ging nur durch Umbenennen der Werte. Jetzt kennt die Engine nur noch Tokens (`primary`, `card` …); Markennamen stehen nur in der Palette eines Themes.
- Der Kontrast-Check hat beim ersten Lauf einen echten Fehler gefunden: chublets-Gold als Pfeil- und Badge-Farbe auf der lila Karte kommt nur auf 2,9:1 (Grenze 3:1). Lösung: optionales Token `connector` (chublets: `primary`). Beim ersten CHNT-Entwurf war das unbemerkt geblieben.
- Gold auf Weiß liegt bei 3,2:1, chublets-Gold taugt also für Balken und Rahmen, nicht für Fließtext.
- Libre Franklin gibt es bei Google Fonts nur als Variable Font (`LibreFranklin[wght].ttf`); die statischen Dateien liefern 404. reportlab kann keine Gewichtsachse wählen. Darum vier statische Schnitte (400 und 700, je roman und italic) per `fontTools.varLib.instancer` erzeugt (`tools/make_static_librefranklin.py`). Das sind abgeleitete Schriften unter derselben OFL; Quelle und SHA-256 stehen in `fonts/libre-franklin/SOURCES.md`.
- Fira Sans und PT Sans gibt es als statische TTFs. PT Sans hat „PT Sans" und „ParaType" als Reserved Font Names; die Dateien sind unverändert, nur umbenannt.
- Das Repository `Research-Squirrel-Engineers/squirrel-colours` enthält (laut Seitenabruf am 2026-10-09) nur eine `README.md` mit neun Hex-Werten und eine PDF, keine maschinenlesbare Datei und keine sichtbare Lizenz. Der Abruf war eine Zusammenfassung der Seite, „View all files" ließ sich nicht öffnen. Die Hex-Werte im Theme sind aus der README übernommen, nicht gegen die PDF geprüft.
- Die beiden N4O-Blautöne stammen aus derselben README. Graue, `bright-blue` und `dark-blue` im Theme `nfdi4objects` sind squirrel-Begleitfarben, keine offiziellen N4O-Farben.
- Die Tailwind-Werte im Theme `neutral` sind aus der veröffentlichten Skala eingetippt, nicht gegen die Website geprüft.
- Eine Aufzählungszeile mit `` `<br>` `` im Code-Span wurde zunächst als Zeilenumbruch gesetzt. Behoben: `<br>` wirkt nur außerhalb von Backticks.
- reportlab trägt Helvetica und Times-Roman in die Schriftressourcen ein, zeichnet damit aber keinen Text. Die eingebetteten Schriften sind die Theme-Schriften.

### A2 Zielbild

```
poster.yaml ──┐
content/*.md ─┤
img/*, logos ─┼─► validate (Theme, Kontrast, Dateien) ─► render (Autofit) ─► dist/poster.pdf   (Vektor, Schrift eingebettet)
themes/<id> ──┤                                                              dist/layout_report.txt (Theme, Kontrast, why je Block)
fonts/*.ttf ──┘                                              preview ──────► dist/poster-preview.png
```

Eigenschaften, die das Ergebnis haben muss (jede ist prüfbar):

1. Seitenformat exakt wie `page.size` (A0 = 841 × 1189 mm), eine Seite.
2. Zweimal bauen ergibt byte-identische Dateien (`sha256sum dist/*`).
3. Keine gedruckte Schrift unter `min_pt` (24 pt); Basisschrift mindestens `autofit.min_pt` (28 pt), sonst bricht der Build ab.
4. Jeder Block hat eine `why:`-Notiz, die im Layout-Report erscheint.
5. `python main.py --strict` läuft nur durch, wenn kein `TODO` mehr im Poster steht, kein Platzhalterbild fehlt, das Theme `ready` ist und `meta.status: final` gilt.
6. Jedes mitgelieferte Theme baut das Demo-Poster ohne Fehler.
7. Kein Farbpaar der Engine liegt unter 3:1.

### A3 Querschnittsregeln

- Eingaben (`content/`, `img/`, `themes/`, `fonts/`) werden vom Build nie verändert; alles, was ein Skript schreibt, landet in `dist/`.
- **Keine Uhr in der Ausgabe.** `RELEASE` in `py/poster_utils.py`; reportlab läuft mit `invariant=1`.
- **Zweimal laufen lassen, `git status` bleibt beim zweiten Mal sauber.**
- Kein Netzwerkzugriff im Build; Schriften und Beispielbilder liegen im Repo.
- Die Engine kennt nur Tokens, nie Farbnamen. Neue Farben kommen in ein Theme, nicht in den Code.
- Ein Theme ist selbsttragend bis auf die Schriftbibliothek; jede Schriftfamilie trägt ihre Lizenz und `SOURCES.md`.
- Posterinhalt (Texte, Beschriftungen, `why:`) ist British English; `PRIMER.md` ist Deutsch.
- Konzepte, die nicht laufen, stehen im Konditional.
- Gold nie für Fließtext; Status nie nur über Farbe (durchgezogen = umgesetzt, gestrichelt = geplant oder Konzept).
- Engine-Änderungen (`py/`, `main.py`) werden im Template gemacht und in die Forks gemergt, nicht pro Poster verbogen.
- Befehle für Windows `cmd`, je Zeile ein Befehl.
- Ein Thema pro Chat, ein Repo pro Chat.

### A4 Beschlusslage

| Frage | Beschluss | seit |
|---|---|---|
| Werkzeug | Python + reportlab, Vektor-PDF; kein Browser, kein LaTeX | 2026-10-09 |
| Eingabeformat | `poster.yaml` + `content/*.md` + `img/` + `themes/` | 2026-10-09 |
| Themes | Ordner `themes/<id>/theme.yaml`, Ablage im Repo, Basis-Themes im Template | 2026-10-09 |
| Mitgelieferte Themes | `neutral`, `chublets`, `research-squirrel`, `nfdi4objects`, `leiza`, `caa-uk`; weitere über `--new-theme` | 2026-10-09 (`caa-uk` ergänzt 2026-11-01) |
| Farbschichten | `palette` (Rohfarben wie in der Quelle) → `tokens` (Rollen) → `accents` (Kartenstile) → `roles` (Tag pro Block) | 2026-10-09 |
| Block-Tags | `role:` je Block; das Theme bildet Rollen auf Akzente ab; `accent:` erzwingt einen Stil | 2026-10-09 |
| Schriftbibliothek | `fonts/<familie>/` im Repo-Wurzelverzeichnis statt Schriften im Theme-Ordner (Fira Sans wird von zwei Themes genutzt, DejaVu Mono als Rückfall) | 2026-10-09 |
| Schriften je Theme | squirrel: Fira Sans; N4O: PT Sans; LEIZA: Libre Franklin; chublets: Fira Sans; neutral: DejaVu | 2026-10-09 (chublets: Vorschlag, passt zu chublets-visuals) |
| LEIZA-Farben | Styleguide „Basiselemente 4. Farben“: Rot `#E84248` (allgemein), Blau `#4E628B` (Forschung), Gelb `#FAB600` (Transfer), jeweils mit Abstufungen D1–D4 und 90–10 %; Hex-Werte aus den Farbflächen gemessen (Tabelle weicht bei Blau und Gelb ab) | 2026-10-31 (Blau bestätigt) |
| Theme-Varianten | Ein Theme kann `variants:` haben; `theme: leiza:blue`, `theme_variant:` oder `--theme leiza:blue`; LEIZA: Rot, Blau, Gelb als je eigene Leitfarbe, nicht gemischt; Gelb mit schlichtem Titel und schwarzen Balken, weil Weiß auf Gelb nicht lesbar ist | 2026-10-31 |
| CAA-UK-Farben | Logoblau `#1998D8` (aus der Logodatei gemessen, Weiß darauf nur 3,2:1: nur für Balken, Linien, Pfeile); abgeleitet: Tiefblau `#0B4F7A` (Kopfband, Weiß 8,7:1), Tinte `#12324A`, Himmel `#8FD0F2` (Ereigniszeile), Kartenfläche `#E8F4FB`; Orange `#C2410C` ist die einzige Warmfarbe und steht für Zweifel (Rolle `problem`, `invitation`, Status `concept`); Schrift Barlow, Überschriften Barlow Semi Condensed Bold, Mono DejaVu | 2026-11-01 (Palette und Schrift von Florian bestätigt) |
| N4O-Farben | `#043358`, `#005f8e` aus squirrel-colours | 2026-10-09 |
| squirrel-colours | Repository gehört Florian; Lizenz CC BY oder CC0, noch nicht festgelegt | Vorschlag 2026-10-09 |
| Kontrast | unter 3:1 Fehler; Text unter 4,5:1 Warnung; große Überschriften zwischen 3 und 4,5 Hinweis; Formen ab 3:1 in Ordnung | 2026-10-09 |
| Schriftgröße | Autofit 28–46 pt; Untergrenze 24 pt für alles Gedruckte | 2026-10-09 |
| Statuskodierung | durchgezogen/gestrichelt plus Nummernmarke; weitere Stati im Theme möglich | 2026-10-09 |
| Release-Prüfung | `--strict`: Warnungen werden Fehler, auch `status: draft` und `state: pending` | 2026-10-09 |
| Lieferung | Neues Repo als ZIP inklusive `dist/`; Änderungen an einem hochgeladenen Repo als Patch-ZIP | 2026-10-09 |
| Poster als Ordner | Poster entstehen in `posters/<id>/` im Kern-Repository statt als Fork; Pfade werden erst im Poster-Ordner, dann im Repo-Wurzelverzeichnis gesucht; poster-eigene Themes unter `posters/<id>/themes/` | 2026-10-31 |
| Poster-PRIMER | Jedes Poster hat ein eigenes deutsches `PRIMER.md` (Teil A Anlass/Zielbild/Beschlüsse, B Schritte P0–P5, C Blöcke mit Quellen, D offen, Änderungsprotokoll); `--blocks` erzeugt die Blocktabelle | 2026-10-31 |
| Brief | `posters/<id>/brief.yaml` ist die eine Quelle aller Fakten; `poster.yaml` und `content/*.md` lesen sie per `{{ brief.… }}`; Start per Interview (`INTERVIEW.md`), Status `interview` → `draft` → `confirmed` | 2026-10-31 |
| Header-Logos | Logos im Titelbereich sind optional und im Demo und Gerüst entfernt (doppelt zu Zugehörigkeiten und Förderer-Block) | 2026-10-31 |
| Module | `people` (runde Fotos, Namen, optional Rolle, keine Institution) und `supporters` (beschriftete Logo-Gruppen); `logos` bleibt für Altbestand | 2026-10-31 |
| Titel | `title_lines` ist Präferenz, keine Grenze; Titel schrumpft erst, wenn die Seite voll ist (bis `title_pt_min`) | 2026-10-31 |
| Lernen aus dem ersten Poster | `chnt31-fdox` (2026-10-31, sieben Rückmelderunden) liefert: Kartenoptionen `valign`, `center_last`; Header-Größen `authors_pt`, `affil_pt`, `subtitle_pt`, `subtitle_bold`, `logos_valign`; kleine Hochzahlen; Teil `image_row`; `matte: false` für Galerien; `per_row` für `supporters`; `tools/measure.py`; Fehlerbericht mit Bandhöhen; Autofit-Hinweis im Bericht; Warnung bei Dateien, die aus dem Kit-Root statt aus dem Poster-Ordner kommen | 2026-10-31 |
| CI | GitHub Action `build.yml`: Demo in allen Themes, Reproduzierbarkeit (`--check-repro`), `--strict` nur für Poster mit `status: final`; `.gitattributes` für Zeilenenden. Noch nicht auf GitHub gelaufen | 2026-10-31 |
| Bausteine | `gallery` (Bildraster mit Beschriftung), `timeline` (senkrecht/waagerecht, Status-Stile), `cite` (Zitierzeile aus `CITATION.cff`), `footer` (optionale Leiste: QR, Text, Lizenz-Badge); Linter, Provenienz, Varianten, Daten aus Dateien warten auf konkrete Anwendungsfälle | 2026-10-31 |
| Fußzeile | Keine DRAFT-Zeile mehr auf dem Poster; `status` ist nur Buchführung | 2026-10-31 |
| Sprache der Doku | `GUIDE.md`, `README.md`, Poster: British English; `PRIMER.md`: Deutsch | 2026-10-09 |

### A5 Was in welchem Chat hochgeladen wird

`PRIMER.md` plus ein Bundle der Quellen, ohne erzeugte Dateien und ohne ungenutzte Schriftfamilien:

```cmd
powershell -NoProfile -Command "Compress-Archive -Path py,posters,shared,themes,fonts,tools,main.py,PRIMER.md,GUIDE.md,WORKFLOW.md,INTERVIEW.md,requirements.txt -DestinationPath bundle.zip -Force"
```

Nicht hochladen: `.venv/`, `.git/`, `dist/`, `bundle.zip`. Die Schriftbibliothek ist rund 8 MB; wer nur ein Theme nutzt, löscht die anderen Ordner vorher.

### A6 IRI-Landkarte

Entfällt: das Repo veröffentlicht kein RDF.

---

## Teil B – Schrittübersicht

| ID | Schritt | Repo | hängt ab von | Status |
|---|---|---|---|---|
| S0 | Festlegungen: Format, Werkzeug, Eingabeformat, Palette | poster-kit | – | erledigt 2026-10-09 |
| S1 | Skeleton: `main.py`, `poster_utils.py`, Lizenz, Pins (aus `chnt31-poster`) | poster-kit | S0 | erledigt 2026-10-09 |
| S2 | Layout-Engine: Karten, Autofit, Flow, Tabelle, Stats, QR, Logos | poster-kit | S1 | erledigt 2026-10-09 |
| S3 | Theme-System: Ordner, Palette/Tokens/Rollen, Schriftbibliothek, Kontrast-Check, `--theme`, `--new-theme` | poster-kit | S2 | erledigt 2026-10-09 |
| S4 | Fünf Themes und Demo-Poster mit allen Möglichkeiten, `GUIDE.md` | poster-kit | S3 | erledigt 2026-10-09 |
| S5 | CHNT31-Poster: fdox (Standard-Theme `neutral`) und chublets (`chublets`) als `posters/<id>/` | poster-kit | S11 | in eigenem Chat |
| S11 | Module `people` und `supporters`; Poster-Ordner, `--new-poster`, `--blocks`, Poster-PRIMER; `brief.yaml` mit `{{ brief.… }}`; `WORKFLOW.md`, `INTERVIEW.md`, `tools/build_all.py`; Titel dynamisch; Header ohne Logos; Fußzeile entfernt | poster-kit | S4 | erledigt 2026-10-31 |
| S6 | LEIZA-Farben eintragen, Theme auf `ready`; Theme-Varianten | poster-kit | – | erledigt 2026-10-31 |
| S12 | CI (Action, `.gitattributes`, `--check-repro`) und Bausteine `gallery`, `timeline`, `cite`, `footer` | poster-kit | S11 | erledigt 2026-10-31 |
| S13 | Lernen aus chnt31-fdox in den Core: `image_row`, `measure.py`, Fehlerbericht, Autofit-Hinweis, Doku, Interview, Standard-Punkte in Teil D; Aufräumen (Reste im Root, `PATCH-README.md`, `pipeline_report.txt`) | poster-kit | S12 | erledigt 2026-10-31 |
| S14 | Theme `caa-uk` (Logoblau, Orange für Zweifel, Barlow) und `fonts/barlow/` | poster-kit | S6 | erledigt 2026-11-01 |
| S15 | Poster `caa-uk-2026-ogham` (A0, Theme `caa-uk`): erste Blockstruktur, Brief, Texte; Logo `shared/logos/caa-uk.png` | poster-kit | S14, S11 | Entwurf 2026-11-01, Fotos offen |
| S7 | Zahlen und Autoren: der Brief ist da (S11); offen: Daten aus Dateien (CSV/JSON), Autoren aus `CITATION.cff` | poster-kit | S11 | teilweise |
| S8 | Provenienz je Block (`source`, `verified`) und weitere Linter (Bild-DPI, Wortbudget, überlaufender Block) | poster-kit | S4 | offen |
| S9 | Varianten: A4-Handout, Querformat, A1 aus einer Quelle | poster-kit | S4 | offen |
| S10 | Raster und Layout-Presets, Block-Plugins, Mehrsprachigkeit | poster-kit | S4 | offen |

S6 ist unabhängig von allem anderen. S7 und S8 hängen nur an S4 und können in beliebiger Reihenfolge laufen. S9 braucht ein eigenes Layout je Variante und kommt deshalb nach S7 und S8.

---

## Teil C – Die Schritte

## S3 – Theme-System

**Ziel:** Farben, Schriften und Formen stehen in `themes/<id>/theme.yaml`; die Engine kennt nur Tokens; ein neues Theme entsteht ohne Codeänderung.

### Erledigt 2026-10-09

`py/theme.py` löst Theme, `extends`, `theme_overrides` und Aliase auf und liefert den Kontrastbericht. Pflicht-Tokens, -Akzente und -Stati werden mit klaren Fehlermeldungen geprüft. `main.py` hat `--theme`, `--list-themes`, `--new-theme ID --base ID`. Gefunden: siehe Befunde zu Kontrast und Variable Fonts in A1.

## S4 – Themes und Demo-Poster

**Ziel:** Jedes Theme baut das Demo-Poster; `GUIDE.md` erklärt alles.

**Abnahme:** Alle fünf Themes bauen ohne Fehler (`leiza` mit der Warnung „pending"); zweimal bauen, `sha256sum dist/*` identisch; `--strict` schlägt fehl (Platzhalterbild, Entwurfsstatus) und der Fehler nennt den Grund; Vorschau jedes Themes angesehen.

### Erledigt 2026-10-09

Alle fünf Themes bauen. Basisgröße 28,5 pt bei `neutral`, `chublets`, `research-squirrel`, `leiza`; 29,5 pt bei `nfdi4objects` (PT Sans setzt schmaler). Zahlen im Layout-Report des jeweiligen Builds.

## S6 – LEIZA-Farben

**Ziel:** `themes/leiza/theme.yaml` hat eigene Palette und Tokens, `state: ready`.

**Abnahme:** Alle drei Varianten bauen das Demo ohne Fehler; Kontrastbericht ohne Fehler und ohne Warnung (Hinweise für große Überschriften sind in Ordnung); zweimal bauen ergibt identische Bytes.

### Erledigt 2026-10-31

Palette mit allen 30 Stufen (Rot, Blau, Gelb je D4–D1, Basis, 90–10 %) aus den Farbflächen des Styleguides, dazu ein abgeleitetes Grau für Bildunterschriften. Varianten `red`, `blue`, `yellow` (siehe A4). Rot: Balken `#C53A3D` (Weiß 5,2:1), Akzent die Markenfarbe; Blau: Balken die Markenfarbe `#4E628B` (Weiß 6,1:1); Gelb: schwarze Balken, gelbe Akzente, schlichter Titel. Hinweise (keine Warnungen): Weiß auf Markenrot 3,96:1 und die Ereigniszeile im Kopf 3,66:1, beides große Schrift.

## S11 – Module, Poster-Ordner, Brief

**Ziel:** Mehrere Poster im selben Repository; Fakten an einer Stelle; Personen und Förderer als Bausteine.

**Abnahme:** `--list-posters`, `--new-poster`, `--blocks`; alle Themes bauen `demo` ohne Fehler; zwei Läufe identisch; frisch entpackt im venv baut es; `--poster` fehlt bei mehreren Postern → Fehler mit Liste; `{{ brief.x }}` auf fehlenden Schlüssel → Fehler mit Namen.

### Erledigt 2026-10-31

`PeopleItem` (Zuschnitt mit `focus`/`zoom`, Initialen als Rückfall) und `SupportersItem` (Seitenverhältnis, Umbruch, Namenskästchen ohne Logo, `columns`). Demo auf den Brief umgestellt, Header-Logos entfernt. Beim Bau mussten Zahlenkacheln (`stats`) einzeilig werden: die Größe richtet sich jetzt nach dem breitesten Wert.

### Ideen für weitere Bausteine (nicht gebaut)

Gebaut in S12: Bildraster, Zeitleiste, Fußzeile mit Lizenz-Badge/QR, Zitierblock aus `CITATION.cff`; in S13 `image_row`. Offen: Zitat-/Aussagebox mit Hervorhebung, Vorher/Nachher-Bildpaar, Legende/Glossar.

## S14 – Theme `caa-uk`

**Ziel:** Ein Theme für Poster der CAA United Kingdom, abgeleitet vom Logo, mit Barlow als Schrift.

**Abnahme:** Demo baut mit `--theme caa-uk` ohne Fehler; alle Themes bauen weiter; zweimal bauen ergibt identische Bytes; Vorschau angesehen.

### Erledigt 2026-11-01

`themes/caa-uk/theme.yaml` und `fonts/barlow/` (Barlow Regular, Bold, Italic, BoldItalic, Barlow Semi Condensed Bold für Überschriften; statische TTFs aus dem Google-Fonts-Repository, OFL, SHA-256 in `SOURCES.md`). Basisgröße im Demo 29,0 pt, Puffer 6 mm. Kontrast: Tinte auf Logoblau 4,13:1 (Hinweis, große Schrift), Weiß auf Tiefblau 8,7:1, Weiß auf Orange 5,2:1. Das Logo-Blau trägt nie Fließtext. Fira Sans als Rückfall war nicht nötig, der Download ging durch.

Das CAA-UK-Logo liegt seit 2026-11-01 in `shared/logos/caa-uk.png` (Lizenz vom Autor bestätigt, Vermerk in der README dort); der Poster-Kopf zeichnet es auf einer weißen Platte.

## S7 bis S10

Ideen aus dem Konzept vom 2026-10-09, noch nicht ausgearbeitet. Jeder Schritt bekommt beim Start Ziel, Uploads und Abnahme.

---

## Teil D – Offene Punkte

- **D1** Lizenz von squirrel-colours festlegen (CC BY oder CC0) und als `LICENSE` ins Repository legen; danach `source.licence` in den Themes `research-squirrel` und `nfdi4objects` anpassen.
- **D2** LEIZA: Logo-Vorgaben (Schutzraum, Mindestgröße) fehlen noch; die Farben stehen (S6). Blau und Gelb: Styleguide-Tabelle und Farbflächen weichen ab, die Flächenwerte sind gewählt (Blau bestätigt, Gelb nach demselben Prinzip).
- **D3** Wird chublets mit Fira Sans bestätigt? Bisher Vorschlag.
- **D12** Das CHNT31-Poster (zwei Poster: fdox mit dem Standard-Theme `neutral`, chublets mit `chublets`) entsteht in einem eigenen Chat als `posters/<id>/`; die Migration der alten Engine ist damit dort, nicht hier.
- **D4** Formatvorgabe der jeweiligen Veranstaltung prüfen (A0 hoch? quer? Maximalgröße?) – pro Fork.
- **D5** Lizenz der Posterinhalte (Texte, Grafiken); Code steht unter MIT.
- **D6** Kein PDF/X-Export und keine Beschnittzugabe; falls eine Druckerei beides verlangt, wäre das ein eigener Schritt.
- **D7** `header_style: plain` ist implementiert und mit einem Override getestet, aber in keinem mitgelieferten Theme aktiv.
- **D13** Standard-Punkte je Poster (stehen im Gerüst `posters/_template/PRIMER.md`, Teil D): Ort/Datum/Druckfrist, Foto-Einwilligung, Logo-Nutzungsregeln, Bildlizenzen, Lesbarkeit von Folien-Grafiken, Poster-Lizenz und `CITATION.cff`, Formatvorgabe.
- **D14** Der Autofit füllt jeden freien Millimeter; eine Obergrenze je Poster geht über `theme_overrides: typography: autofit: max_pt` (im GUIDE beschrieben). Ob es einen eigenen Schalter braucht, zeigt sich am nächsten Poster.
- **D15** Patch-ZIPs können nichts löschen; entfernte Dateien stehen in der `PATCH-README.md` mit `del`-Befehlen. Ein Werkzeug, das aus einem ZIP-Manifest löscht, wäre denkbar, bisher nicht nötig.
- **D9** Fotos von Personen: Einwilligung klären, bevor ein Poster mit Porträts veröffentlicht wird.
- **D10** Logos von Förderern und Instituten: Nutzungsregeln prüfen; Vermerk in `shared/logos/README.md`.
- **D11** Soll es zusätzlich eine Kommandozeilen-Version des Interviews geben (`--interview`), falls ohne Claude gearbeitet wird?
- **D16** erledigt 2026-11-01: CAA-UK-Logo liegt in `shared/logos/caa-uk.png`, Lizenz vom Autor bestätigt.
- **D8** Die squirrel-Palette gegen die PDF `Squirrles Colors.pdf` abgleichen; bisher nur die README-Werte.
