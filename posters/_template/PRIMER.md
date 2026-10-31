# PRIMER: Poster {{id}}

Arbeitsplan und Gedächtnis **dieses einen Posters**. Der Kern (Engine, Themes, Schriften) steht im
[PRIMER.md des Kits](../../PRIMER.md) und in [GUIDE.md](../../GUIDE.md); hier steht nur, was dieses Poster betrifft.
Ein Chat, ein Poster, ein Schritt: wer weiterarbeitet, liest zuerst Teil A und den Schritt in Teil B.

Stand: TT.MM.JJJJ

---

## Teil A: Rahmen und Beschlusslage

### A1 Anlass

| | |
|---|---|
| Veranstaltung | TODO |
| Ort, Datum | TODO |
| Format | A0 hoch (siehe `poster.yaml`, `page:`) |
| Abgabe / Druck bis | TODO |
| Theme | `neutral` (siehe `poster.yaml`, `theme:`) |
| Fakten | `brief.yaml` (Titel, Veranstaltung, Autoren, Förderer, Zahlen mit Quelle); `poster.yaml` liest sie per `{{ brief.… }}` |
| Ansprechpartner | TODO |

### A2 Zielbild

Was gilt als fertig? Drei bis fünf Sätze, die sich am PDF prüfen lassen, zum Beispiel:

1. Die Kernaussage steht oben links und ist aus zwei Metern lesbar.
2. Jede Zahl auf dem Poster hat eine Quelle (Teil C).
3. `python main.py --poster {{id}} --strict` läuft ohne Warnung.

### A3 Regeln für dieses Poster

- Sprache der Texte: TODO (Englisch, britisches Englisch)
- Zeitform und Ton: TODO
- Zahlen: nur mit Quelle und Datum der Abfrage
- Nichts auf dem Poster, was nicht in Teil C begründet ist

### A4 Beschlusslage

| Beschluss | Begründung | Datum |
|---|---|---|
| TODO | TODO | TT.MM.JJJJ |

### A5 Befehle (Windows und Ablauf: [../../WORKFLOW.md](../../WORKFLOW.md))

```
python main.py --poster {{id}}                 # bauen: posters/{{id}}/dist/poster.pdf und poster-preview.png
python main.py --poster {{id}} --theme chublets  # anderes Theme probieren
python main.py --poster {{id}} --strict          # Release-Prüfung: Warnungen werden Fehler
python main.py --poster {{id}} --blocks          # Blockliste als Markdown für Teil C
```

---

## Teil B: Schritte

| Schritt | Inhalt | Status |
|---|---|---|
| P0 | Gerüst aus `_template` angelegt; Interview geführt ([INTERVIEW.md](../../INTERVIEW.md)), `brief.yaml` ausgefüllt, Anlass und Format in A1 | offen |
| P1 | Kernaussage und Gliederung: welche Blöcke, in welcher Reihenfolge | offen |
| P2 | Texte, Zahlen und Quellen in `content/`, Teil C ausfüllen | offen |
| P3 | Abbildungen, Fotos der Personen, Logos der Förderer | offen |
| P4 | Theme und Layout feinjustieren, Vorschau prüfen | offen |
| P5 | `--strict` grün, `status: final`, Druckfreigabe, PDF in `dist/` committen | offen |

Status: `offen`, `in Arbeit`, `fertig` (mit Datum).

---

## Teil C: Blöcke, Quellen, Warum

Pro Block: wofür er da ist, woher Text und Zahlen kommen. `python main.py --poster {{id}} --blocks` erzeugt die
Tabelle aus `poster.yaml` (Feld `why`); Quellen und Abfragedaten trägst du hier ein.

| Block | Rolle | Warum | Quelle / Stand |
|---|---|---|---|
| TODO | TODO | TODO | TODO |

---

## Teil D: Offene Punkte

| Nr. | Frage | Wer entscheidet | Stand |
|---|---|---|---|
| D1 | Ort, Datum und Druckfrist der Veranstaltung (`event.*` im Brief) | Autor | offen |
| D2 | Einwilligung für Fotos von Personen auf dem Poster | Autor, Abgebildete | offen |
| D3 | Nutzungsregeln der Logos (Förderer, Institute, Netzwerke), Vermerk in `shared/logos/README.md` oder `img/logos/README.md` | Autor | offen |
| D4 | Lizenzen der Bilder und Grafiken, Namensnennung als Satz im Text, Vermerk in `img/README.md` | Autor | offen |
| D5 | Sind Grafiken aus Folien oder Screenshots auf A0 lesbar (Schrift in der Grafik mindestens etwa 24 pt)? | Autor | offen |
| D6 | Lizenz des Posters und `CITATION.cff` (Zitierzeile, DOI) | Autor | offen |
| D7 | Formatvorgabe der Veranstaltung geprüft (Größe, Hoch-/Querformat) | Autor | offen |

---

## Änderungsprotokoll

| Datum | Änderung | Anlass |
|---|---|---|
| TT.MM.JJJJ | Gerüst angelegt | Start |
