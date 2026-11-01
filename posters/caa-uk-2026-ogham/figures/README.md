# Figure scripts

Python scripts that draw the figures of the poster `caa-uk-2026-ogham` into `../img/`. The poster build itself
(`python main.py --poster caa-uk-2026-ogham`) does not run them: it reads the PNG files that are checked in. Run them
only to redraw a figure after the data or the design changed.

## Inputs

| What | Where from | Set with |
|---|---|---|
| TEI/EpiDoc editions and weights | checkout of [`LinkedOpenOgham/tei--epidoc-amt`](https://github.com/LinkedOpenOgham/tei--epidoc-amt) (`data/*.xml`, `out/*.amt.ttl`) | environment variable `AMT` (default `/tmp/w/new/amt`) |
| Places of the corpus map | `out/places.geojson` of [`LinkedOpenOgham/tei--epidoc-crosswalk`](https://github.com/LinkedOpenOgham/tei--epidoc-crosswalk) | `CRWALK` |
| Land polygons | Natural Earth `ne_10m_land.geojson` (public domain) from [`nvkelso/natural-earth-vector`](https://github.com/nvkelso/natural-earth-vector) | `NE_LAND` |
| Photographs of the stones | folder `images/` of a checkout of [`lguariento/og-h-am`](https://github.com/lguariento/og-h-am) | `OGHAM_IMAGES` |

Python 3.11 or later with `matplotlib`, `lxml`, `rdflib`, `Pillow` and `playwright` (Chromium installed). Fonts come from
`../../../fonts/` (Barlow, Noto Sans Ogham); nothing is taken from the system.

## Order

```
python prepare_photos.py     # img/photos/*.jpg
python map_corpus.py         # img/map-corpus.png
python ladder_rows.py        # img/ladder-all.png (and the intermediate row-*.png, which are not checked in)
python gigha.py              # img/gigha-readings.png, gigha-graph.png, gigha-reasoning.png, gigha-photo.png
```

## Files

| File | Role |
|---|---|
| `common.py` | palette of the `caa-uk` theme, font registration, paths |
| `htmlfig.py` | renders a piece of HTML (sizes in millimetres) to a PNG with Chromium at 200 dpi |
| `markup.py` | turns an edition (`unclear`, `supplied`, `gap`, `choice`) into HTML and reads weights from the AMT graphs |
| `prepare_photos.py` | crops and downsizes the photographs |
| `map_corpus.py` | corpus map with record status (numbered, doubtful, lost) |
| `ladder_rows.py` | the three rows of the ladder: photograph, Ogham, transliteration, weight bar |
| `gigha.py` | the worked example: readings, model graph, axioms and derived weights, photograph |

Figures that contain text are drawn as PNG because SVG text is not outlined in the PDF.
