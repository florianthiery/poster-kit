# INTERVIEW: ein Poster in einem Gespräch starten

Diese Datei beschreibt, wie ein neues Poster in einer Claude-Sitzung beginnt und wie aus dem Gespräch ein
strukturiertes Dokument wird, das danach laufend fortgeschrieben wird. Das Ergebnis ist
`posters/<id>/brief.yaml`: die **eine Quelle aller Fakten** des Posters. `poster.yaml` liest sie mit
`{{ brief.… }}`; Struktur und Aussehen bleiben in `poster.yaml` und im Theme.

Gilt für Claude und für dich: Wer mit einem Poster weiterarbeitet, liest zuerst `brief.yaml` und `PRIMER.md`
des Posters.

## Ablauf

1. **Anlegen.** `python main.py --new-poster <id> --theme <theme>` (oder Claude legt den Ordner im Patch an). Das
   Gerüst enthält `brief.yaml` mit `status: interview` und lauter `TODO`.
2. **Interview** in Runden von höchstens vier Fragen, als Formular mit freiem Kommentarfeld. Gefragt wird nur,
   was in `brief.yaml` noch `TODO` ist. Nichts wird geraten: unbekannt bleibt `TODO`.
3. **Zurückspiegeln.** Claude zeigt die ausgefüllte `brief.yaml` und die Blockliste und fragt: stimmt das?
   Dann `status: draft`.
4. **Gerüst füllen.** Claude legt die Blöcke in `poster.yaml` an (je Block `role` und `why`), trägt in
   `PRIMER.md` Teil A1 (Anlass), A2 (Zielbild), A4 (Beschlüsse mit Datum) und Teil C (Blöcke) ein.
5. **Fortschreiben.** Ab jetzt: ein Fakt ändert sich → zuerst `brief.yaml`, dann bauen. Eine Entscheidung → A4 mit
   Datum. Eine Frage, die offen bleibt → Teil D. Wenn alles bestätigt ist: `status: confirmed`.

## Die Runden

| Runde | Fragen | Landet in |
|---|---|---|
| A Anlass | Veranstaltung, Ort, Datum, Format (A0 hoch/quer, A1), Abgabe- und Druckfrist, Sprache | `event`, `poster.language` |
| B Kern | Arbeitstitel, Untertitel, Kernaussage in einem Satz, Zielgruppe, was die Lesenden danach tun sollen | `poster` |
| C Menschen | Autorinnen und Autoren in Reihenfolge, Zugehörigkeiten, wer präsentiert, Fotos ja/nein (Einwilligung) | `authors`, `affiliations`, `people` |
| D Förderer | Förderer mit Kennzeichen, Kooperationen, Netzwerke, Gastgeber; liegen Logos vor, dürfen sie verwendet werden | `supporters`, `shared/logos/` |
| E Inhalt | Welche Bausteine (Problem, Methode/Ablauf, Zahlen, Tabelle, Abbildung, Ausblick, Einladung); vorhandene Abbildungen; Zahlen mit Quelle und Abfragedatum; Links für QR-Codes | Blöcke in `poster.yaml`, `numbers`, `links` |
| F Aussehen | Theme, Titelband oder schlichter Titel, Titel in ein, zwei oder drei Zeilen | `theme`, `header` |

Nach Runde E weiß Claude, welche Blöcke das Poster braucht; nach F, wie es aussieht. Danach folgt das
Zurückspiegeln.

## Regeln

- Ein Chat, ein Poster, ein Schritt.
- Zahlen stehen nur in `brief.numbers`, mit `source` und `queried`; Texte verweisen darauf.
- Fotos von Personen nur mit deren Einverständnis; Logos nur, wenn die Nutzungsregeln des Eigentümers es erlauben
  (Vermerk in `shared/logos/README.md`).
- Offene Entscheidungen, die den Inhalt ändern, kommen als Formular mit Kommentarfeld, nicht als Fließtextfrage.
- Antwortet jemand „weiß ich noch nicht“, bleibt `TODO` stehen und der Punkt kommt in Teil D des Posters.
