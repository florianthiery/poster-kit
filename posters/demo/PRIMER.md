# PRIMER: Poster demo

Das Demo-Poster zeigt jede Option des Kits (Textarten, Flow, Tabelle, Bilder, Personen, Förderer, QR-Codes,
Rollen und Akzente) und erklärt sich selbst. Es ist kein echtes Poster: nichts hier ist Inhalt, alles ist Beispiel.

- Neues Poster anlegen: `python main.py --new-poster <id>` (leeres Gerüst) oder
  `python main.py --new-poster <id> --from-poster demo` (Kopie dieses Posters zum Abändern).
- Alle Optionen erklärt: [GUIDE.md](../../GUIDE.md).
- Das Demo baut absichtlich mit einer Warnung (fehlendes Platzhalterbild), damit `--strict` hier scheitert und
  du siehst, wie die Release-Prüfung antwortet.

Die Vorlage für den PRIMER eines echten Posters steht in [../_template/PRIMER.md](../_template/PRIMER.md).

## Änderungsprotokoll

| Datum | Änderung |
|---|---|
| 2026-10-31 | Demo um die Module `people` und `supporters` erweitert; Poster-Ordner `posters/<id>/` eingeführt |
