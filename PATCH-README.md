# Patch: LEIZA-Theme mit Varianten (poster-kit 0.4.0)

Stand: 2026-10-31. Gilt auf dem Repo-Stand, den du am 31.10. gepusht hast.

## Was drin ist

| Datei | Änderung |
|---|---|
| `themes/leiza/theme.yaml` | LEIZA fertig (`state: ready`): Palette mit allen 30 Stufen, drei Varianten `red` (allgemein), `blue` (Forschung), `yellow` (Transfer), Libre Franklin |
| `py/theme.py` | Theme-Varianten: `theme: leiza:blue`, `theme_variant:` in poster.yaml oder `--theme leiza:blue`; klare Fehler bei unbekannter Variante |
| `py/step_render.py` | Layout-Report nennt die Variante |
| `main.py` | `--list-themes` zeigt die Varianten |
| `tools/build_all.py` | `--all-themes` baut auch jede Variante (Dateiname `poster-leiza-blue.pdf`) |
| `posters/demo/poster.yaml`, `posters/_template/poster.yaml` | Kommentar zur Theme-Auswahl |
| `GUIDE.md`, `README.md`, `PRIMER.md`, `CITATION.cff` | Doku: Abschnitt „Variants“, LEIZA nicht mehr pending, Beschlüsse und S6 im PRIMER, Version 0.4.0 |

Nicht enthalten: CHNT31-Poster (kommt in eigenem Chat als `posters/<id>/`), der Skill (kommt als Vorschlagskarte im Chat).

## Einspielen (Windows cmd, im Repo-Ordner)

```cmd
powershell -NoProfile -Command "Expand-Archive -Path C:\Users\du\Downloads\patch.zip -DestinationPath . -Force"
```

```cmd
del PATCH-README.md
```

## Prüfen

```cmd
python main.py --list-themes
```

Erwartet: bei `leiza` Status `ready` und eine Zeile `variants: red (general), blue (research), yellow (transfer)`.

```cmd
python tools\build_all.py --all-themes
```

Erwartet: `== done` ohne `FAILED`; in `posters\demo\dist\themes\` liegen sieben PDFs und PNGs, darunter `poster-leiza-red`, `-blue` und `-yellow`. Das Demo bleibt am Ende im Theme `neutral`.

```cmd
python main.py --theme leiza:blue
```

Erwartet: `result: ok`; `posters\demo\dist\layout_report.txt` beginnt mit `theme: leiza, variant blue (research)`. Danach `python main.py`, damit `dist` wieder das Demo im Standard-Theme zeigt (SHA-256 von `poster.pdf` beginnt mit `43f8840c029e1353`).

```cmd
python main.py --theme leiza:green
```

Erwartet: `ERROR: theme 'leiza' has no variant 'green'; it has: red, blue, yellow`.

## Hinweise

- LEIZA-Hexwerte stammen aus den Farbflächen des Styleguides, nicht aus der Tabelle (Blau `#4E628B` statt `#223466`, Gelb `#FAB600` statt `#FDB21A`); PRIMER D2.
- Die Poster-Ordner `posters/<id>/` und `shared/` werden von diesem Patch nicht berührt.
