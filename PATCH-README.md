# PATCH: Poster chnt31-fdox (CHNT31, Digital Creative Award)

Stand: 2026-10-31, Runde 7 (enthält die Runden 2 bis 6, ältere ZIPs müssen nicht mehr eingespielt werden). Dieses Patch-ZIP aktualisiert das Poster `posters/chnt31-fdox/` (Titel, Autorenfolge, Hook-Bild,
Query 2 spatial, Logos, FDOx-Logo im Header, größere Fotos, Grafiken) und ändert im Kern **eine** Sache: `py/step_render.py` (neue Optionen
`valign: center` für Karten und `logos_valign: center`, `authors_pt`, `affil_pt`, `subtitle_pt`, `subtitle_bold` im Header, `center_last` für Karten) samt Hinweis in `GUIDE.md`. Die `PATCH-README.md` im Repo-Root wird durch diese Datei
überschrieben; wer die alte behalten will, kopiert sie vorher weg.

## Inhalt

| Pfad | Was |
|---|---|
| `posters/chnt31-fdox/brief.yaml` | Fakten: Titel, Autor:innen, Personen, Logos (Namenskästchen), Links/QR, Zahlen mit Quelle, Referenzen |
| `posters/chnt31-fdox/poster.yaml` | Struktur: Blöcke und Layout (A0 hoch, Theme research-squirrel) |
| `posters/chnt31-fdox/content/` | Texte als Markdown (englisch) |
| `posters/chnt31-fdox/data/sparql/` | die zwei echten SPARQL-Abfragen (`.rq`) und ihre Ergebnisse (`.csv`) |
| `posters/chnt31-fdox/img/` | Abbildungen (aus `fdox-visuals`, zugeschnitten), Vorschau CIIC 81, Fotos in `img/people/` |
| `posters/chnt31-fdox/PRIMER.md` | Poster-PRIMER (deutsch): Beschlüsse, Quellen, offene Punkte |
| `py/step_render.py`, `GUIDE.md` | Option `valign: center` für Karten und `logos_valign: center` im Header (Personen- und Logo-Karte zentriert) |
| `posters/chnt31-fdox/dist/` | gebautes `poster.pdf`, `poster-preview.png`, Berichte (werden im Repo getrackt) |

## Was ausführen

Vorher löschen (ein ZIP kann nichts löschen): `posters/chnt31-fdox/content/07_sparql_creator.md`,
`posters/chnt31-fdox/data/sparql/creator.rq`, `creator-result.csv` (siehe `BEFEHLE-chnt31-fdox.md`).

Windows-Befehle: siehe `BEFEHLE-chnt31-fdox.md`. Kurz:

```
python main.py --poster chnt31-fdox
python tools/build_all.py --poster chnt31-fdox --check-repro
```

## Woran man sieht, dass es stimmt

- Bau endet mit `== result: ok`; Seite A0 hoch, Grundschrift 28 pt, Titel 60 pt.
- `--check-repro` meldet „rebuild identical“ (Prüfsumme des PDFs gleich).
- Nur erwartete Warnungen: `event.place`, `event.dates`, `event.print_deadline` sind noch TODO, daher scheitert
  `--strict` bewusst, bis Florian sie ausfüllt und `status: final` setzt.
- Vorschau öffnen: sechs Stationen der Journey, zwei SPARQL-Tabellen, Personen- und Logo-Karte, Referenzen unten.

## Hier geprüft

Patch auf frischem Klon angewendet, zweimal gebaut, Ergebnis byte-gleich zur mitgelieferten `dist/`.
SPARQL-Ergebnisse gegen das Registry-Bundle (Commit 253aee9) am 2026-10-31 mit rdflib abgefragt.

## Commit-Vorschlag

```
chnt31-fdox: rounds 2 to 7 (title, author order, logos, spatial query, header logo, valign option)
```
