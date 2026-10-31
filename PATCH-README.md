# PATCH: Poster chnt31-fdox (CHNT31, Digital Creative Award)

Stand: 2026-10-31. Dieses Patch-ZIP legt **ein neues Poster** an: `posters/chnt31-fdox/`.
Es ändert nichts am Kern (Engine, Themes, Schriften). Die `PATCH-README.md` im Repo-Root wird durch diese Datei
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
| `posters/chnt31-fdox/dist/` | gebautes `poster.pdf`, `poster-preview.png`, Berichte (werden im Repo getrackt) |

## Was ausführen

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
chnt31-fdox: poster for CHNT31 (Digital Creative Award), A0 portrait, research-squirrel theme
```
