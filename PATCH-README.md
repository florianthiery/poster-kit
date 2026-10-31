# Patch: CI, `.gitattributes` und vier neue Bausteine

Enthält nur geänderte Dateien. Basis: der Stand nach dem LEIZA-Patch.

## Inhalt

| Datei | Änderung |
|---|---|
| `.github/workflows/build.yml` | neu: GitHub Action (Demo in allen Themes, Reproduzierbarkeit, strikter Check für `status: final`) |
| `.gitattributes` | neu: stabile Zeilenenden (LF), Binärdateien markiert |
| `py/step_render.py` | neue Bausteine `gallery`, `timeline`, `cite` und optionale Fußleiste `footer` |
| `py/step_validate.py` | Prüfungen für die neuen Bausteine und `footer:` |
| `tools/build_all.py` | `--check-repro`; `--strict` nur für Poster mit `status: final` |
| `posters/demo/poster.yaml` | zeigt alle neuen Bausteine (Galerie, Zeitleiste, Zitat, Fußleiste) |
| `posters/_template/poster.yaml` | Hinweis auf die neuen Teiltypen |
| `posters/demo/dist/…` | neu gebautes PDF, Vorschau, Layout-Bericht |
| `GUIDE.md`, `README.md`, `PRIMER.md`, `WORKFLOW.md`, `CITATION.cff` | Doku (S12, Beschlüsse, CI) |

## Was ausführen (Windows cmd, im Ordner `poster-kit`, venv aktiv)

```cmd
python main.py --poster demo
```

```cmd
python tools\build_all.py --poster demo --all-themes
```

```cmd
python tools\build_all.py --check-repro
```

Einmalig, damit `.gitattributes` greift:

```cmd
git add --renormalize .
```

Dann wie gewohnt `git add .`, `git commit`, `git push`.

## Prüfen

- Erster Lauf endet mit `result: ok`, `base 28.0 pt`, Warnung nur zu `not-there-yet.png` (gewollter Platzhalter).
- `--all-themes`: sieben Zeilen `… : ok` (chublets, leiza:red/blue/yellow, neutral, nfdi4objects, research-squirrel).
- `--check-repro`: `demo: rebuild identical`.
- In `posters\demo\dist\poster-preview.png`: Galerie oben rechts, Zeitleiste unten links, „How to cite“ unter den QR-Codes, Fußleiste mit QR und Badge „CC BY 4.0“.
- Nach dem Push: Tab *Actions* auf GitHub, grüner Haken (die Action ist bisher nur lokal auf YAML-Syntax geprüft).
