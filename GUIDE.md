# Guide

Everything this repository can do, in one place. Read the quick start, then use the rest as a reference.

- [Quick start](#quick-start)
- [Forking for a new poster](#forking-for-a-new-poster)
- [How the pieces fit](#how-the-pieces-fit)
- [poster.yaml](#posteryaml)
- [Writing text: the Markdown subset](#writing-text-the-markdown-subset)
- [Themes](#themes)
- [Fonts](#fonts)
- [The checks](#the-checks)
- [Commands](#commands)
- [Printing](#printing)
- [When something looks wrong](#when-something-looks-wrong)
- [Extending the engine](#extending-the-engine)
- [Not built yet](#not-built-yet)

## Quick start

```cmd
pip install -r requirements.txt
```

```cmd
python main.py
```

You get three files in `dist/`:

| File | What it is |
|---|---|
| `poster.pdf` | The poster: one page, vector graphics, fonts embedded |
| `poster-preview.png` | A small raster preview for a quick look |
| `layout_report.txt` | Base text size, size of every block, the `why:` note of every block, the theme and its contrast result |

The demo poster explains itself: every block shows one feature, and `poster.yaml` and `content/` are the source of everything you see.

## Forking for a new poster

(Prefer to keep the poster in a repository that already exists? See *Drop-in use inside an existing repository* in `README.md`: the kit is one self-contained folder.)


1. Fork or copy this repository. Name it after the poster (`chnt31-poster`, `deRSE27-workshop-poster`).
2. In `poster.yaml` set `theme:`, `meta`, `page` and `header` (title, authors, affiliations, logos).
3. Delete the demo blocks you do not need, rewrite the rest, and write your texts in `content/*.md`. Keep the `why:` notes honest; they are the memory of the layout.
4. Put figures into `img/` and logos into `img/logos/`. Delete `img/sample-*` when you are done.
5. Run `python main.py` and open `dist/poster-preview.png`. Repeat.
6. Before printing: set `meta.status: final`, resolve every `TODO`, run `python main.py --strict`.
7. Replace `PRIMER.md` (see [below](#primer)), `CITATION.cff` and the project name in `README.md`.

To keep the fork mergeable with this template, change only `poster.yaml`, `content/`, `img/`, `PRIMER.md`, `CITATION.cff`, `README.md` and any theme you add. Everything in `py/` and `main.py` is the engine and should stay as it is.

### PRIMER

`PRIMER.md` is the German work plan of the repository: standing rules, the table of decisions with dates, the steps and the open points. In a fork it records why *this* poster looks the way it does. Keep the structure, replace the content.

## How the pieces fit

| Layer | Files | Answers | Changes |
|---|---|---|---|
| Content | `content/*.md`, `img/` | What is written and shown? | every revision |
| Structure | `poster.yaml` | Which blocks, in which order and columns? | per poster |
| Look | `themes/<id>/theme.yaml`, `fonts/` | Colours, typefaces, shapes, card styles | per brand or event |
| Engine | `main.py`, `py/` | Draws the PDF | rarely |

The build runs three steps: `validate` (checks the files and the theme), `render` (draws the PDF) and `preview` (makes the PNG).

## poster.yaml

Top-level keys: `meta`, `theme`, `theme_overrides`, `page`, `header`, `blocks`, `layout`.

### meta

| Key | Meaning |
|---|---|
| `title`, `author`, `subject`, `keywords` | Written into the PDF metadata |
| `short_title` | Used in the layout report |
| `status` | Bookkeeping only, nothing is printed on the poster. `--strict` refuses `draft`, so set `final` for the release build. |

### theme and theme_overrides

`theme: neutral` picks `themes/neutral/theme.yaml`. `python main.py --theme chublets` overrides it for one build, which is the quickest way to try a look.

`theme_overrides` is merged over the chosen theme for this poster only. Use it for one-off changes without writing a new theme:

```yaml
theme_overrides:
  shape: {header_style: plain}          # dark title on the page instead of a coloured band
  typography:
    autofit: {max_pt: 40}               # never set the body text larger than 40 pt
```

### page

| Key | Values |
|---|---|
| `size` | `A0`, `A1`, `A2`, `A3`, `A4` |
| `orientation` | `portrait` or `landscape` |
| `margin_mm`, `gap_mm` | Outer margin and the gap between cards |

The theme's sizes are meant for A0. On a smaller sheet the engine still fits the body text, but heading and title sizes are fixed points, so reduce them with `theme_overrides.typography.sizes`.

### header

```yaml
header:
  event: "EVENT 2026 · Poster"
  title: "Line one<br>line two"          # <br> forces a break; the size is fitted to title_lines
  # optional, per poster, override the theme:
  # title_lines: 3                       # preferred number of lines (a preference, not a limit)
  # title_pt_max: 130
  # title_pt_min: 70
  subtitle: "One line saying what the poster shows"
  authors:
    - {name: "Ada Example", affil: "1"}  # affil: the number(s) of the affiliation(s) below
  affiliations:
    - "Example Institute, Example City"
  logos_w_mm: 120
  logo_h_mm: 26
  logos:
    - {name: "Example logo", src: img/logos/example-logo.svg}   # with src: the file (SVG, PNG, JPG)
    - {name: "Institute name"}                                  # without src: the name in a pill
```

The title takes the largest size between `title_pt_min` and `title_pt_max` that fits in `title_lines` lines. `title_lines` is a preference: if the title still needs more lines at the minimum size, it simply wraps further, the header grows, the body text gets less room and the build warns. If the page is full even with the smallest body size, the title is reduced in steps (down to `title_pt_min`) and the body sizes are tried again; the build says so. The three keys can be set under `header:` in `poster.yaml` for one poster, without touching the theme. Logos are stacked on the right, each in a pill with the theme's secondary colour as outline.

### blocks

A block is a card. Common keys:

| Key | Meaning |
|---|---|
| `title` | Heading in the card's title bar. Optional. |
| `role` | Tag that the theme turns into a card style, for example `problem`, `method`, `outlook`. See [Themes](#roles-and-accents). |
| `accent` | Forces a card style by name and wins over `role`. |
| `why` | One sentence: why this block exists and looks like this. Copied into `layout_report.txt`. Required by the validation (as a warning). |
| `frame` | `false` draws no card and no title bar; the title becomes plain text in the primary colour. |
| `scale` | Text size relative to the fitted body size (`0.8` for references, `1.15` for a key message) |

A block holds one **part**, written directly in the block, or a list of parts under `parts:`. Parts are stacked in the order given.

#### text

```yaml
type: text
file: content/01_intro.md     # or: text: "inline text"
scale: 0.9                    # optional
```

Markdown subset, see [below](#writing-text-the-markdown-subset). The text never gets smaller than the theme's `min_pt`, whatever `scale` says.

#### table

```yaml
type: table
header: ["Source", "Target", "Note"]     # optional; the header row uses the primary colour
col_widths: [2, 3, 3]                    # relative weights; default: equal
rows:
  - ["`field_a`", "property one", "required"]
```

Cells accept the inline Markdown of the text part. Body rows alternate with the theme's `tint`.

#### flow

```yaml
type: flow
per_row: 4                    # boxes per row; longer chains wrap with elbow arrows
legend: "Solid: done. Dashed: planned."
steps:
  - {label: "First step", sub: "short note", status: done}
  - {label: "Second<br>step", status: planned}
```

Boxes are numbered. `status` must be one of the theme's status styles (`done`, `planned`, `concept` in every shipped theme). Solid versus dashed outlines carry the meaning, so the diagram survives a black-and-white print. The legend is plain text: say what the styles mean on this poster.

#### stats

```yaml
type: stats
items:
  - {value: "123", label: "things counted"}
```

Large numbers with a label underneath, spread evenly across the card.

#### image

```yaml
type: image
src: img/figure.svg           # PNG, JPG or SVG
caption: "Figure 1. What it shows."
max_height_mm: 120            # caps tall images; width follows
placeholder: true             # no error while the file is missing: a dashed box is drawn
height_mm: 40                 # height of that placeholder box
```

SVG stays vector. The SVG reader handles basic shapes, paths and groups; text inside an SVG uses whatever font the reader finds, so convert text to outlines before you use a figure that contains text. Raster images are embedded without resampling: supply about 150 dpi at the printed size (a photograph that fills a 400 mm wide card should be about 2400 px wide).

#### qr

```yaml
type: qr
size_mm: 34
items:
  - {url: "https://example.org", label: "Project<br>page"}
```

QR codes are drawn as vectors with error-correction level M; the label sits underneath. Test every code with a phone before printing.

#### logos

```yaml
type: logos
height_mm: 22
items:
  - {name: "Partner one"}
  - {name: "Partner two", src: img/logos/partner-two.png}
```

A row of logo pills, for example partners in a card. The header logos work the same way.

### layout

```yaml
layout:
  bands:
    - weight: 0                          # share of leftover height this band absorbs (0 = natural height)
      columns:
        - {width: 1.1, blocks: [intro]}  # width = relative column width
        - {width: 1, blocks: [numbers, howto]}   # blocks in one column stack top to bottom
```

Bands run top to bottom, columns left to right. Each block must appear exactly once. Leftover height is shared out among the bands by `weight`; inside a band, shorter cards are stretched to the tallest column, so empty space inside a card usually means its neighbour is much taller. Move content, change `width`, or give the band `weight: 0`.

### How the text size is fitted

The engine tries the body size from the theme's `autofit.max_pt` down to `min_pt` in `step_pt` steps and keeps the first size at which the whole body fits on the page. The report names the size it chose. If nothing fits, the build stops and says by how many millimetres the content is too tall: shorten texts, remove a block, or change the layout. If the poster is nearly empty even at the largest size, you get a warning that it is sparse.

## Writing text: the Markdown subset

| You write | You get |
|---|---|
| A blank line | A new paragraph |
| `- item` or `* item` | A bullet |
| `### Heading` | A sub-heading inside the card (only level 3) |
| `**bold**`, `*italic*` | Bold, italic |
| `` `code` `` | Inline code in the theme's monospace font |
| `[text](https://example.org)` | A clickable link, drawn in the link colour |
| `<br>` | A line break (not inside `` `code` ``) |

Nothing else is interpreted: no tables, no images, no numbered lists, no nested bullets. Keep a paragraph to about 40 words and a bullet to about 15; a poster is read in ten seconds from two metres first.

## Themes

A theme says how the poster looks. It lives in `themes/<id>/theme.yaml`. `themes/neutral/theme.yaml` is the commented reference for every key; read it next to this section.

| Theme | Colours | Typeface | State |
|---|---|---|---|
| `neutral` | Tailwind slate, blue, amber | DejaVu Sans Condensed | ready |
| `chublets` | chublets purple and gold | Fira Sans | ready |
| `research-squirrel` | squirrel-colours | Fira Sans | ready |
| `nfdi4objects` | N4O blues from squirrel-colours | PT Sans | ready |
| `leiza` | placeholder (inherits `neutral`) | Libre Franklin | pending |

`python main.py --list-themes` prints them.

### Two colour layers

```yaml
palette:                       # raw colours, named and valued exactly as in their source
  dark-green: "#004c55"
tokens:                        # semantic roles; the engine only ever asks for these
  primary: dark-green          # a token is a palette name, a #RRGGBB colour, or another token
```

Why two layers: the palette can be copied 1:1 from a brand guide (and checked against it), while the tokens decide where each colour is used. Swapping a brand means editing tokens, not code.

Required tokens: `primary`, `on_primary`, `secondary`, `on_secondary`, `secondary_tint`, `ink`, `muted`, `paper`, `card`, `tint`, `line`, `link`, `header_sub`. Optional with a fallback: `header_accent` (event line, falls back to `secondary`), `connector` and `on_connector` (flow arrows and number badges, fall back to `secondary` and `on_secondary`). Add any token you like and use it from accents and status styles.

| Token | Where it is used |
|---|---|
| `primary` / `on_primary` | Header band and its text, table header, big numbers, sub-headings, `done` boxes |
| `secondary` / `on_secondary` | Rule under the header, secondary card bars, logo outlines |
| `secondary_tint` | Fill of `concept` flow boxes |
| `ink` / `muted` | Body text / captions, legends |
| `paper` | Page colour and the fill of `planned` boxes |
| `card` / `tint` / `line` | Card background / table stripes / card outlines and table rules |
| `link` | Links in text |
| `header_sub`, `header_accent` | Subtitle and affiliations, event line on the header band |
| `connector` / `on_connector` | Flow arrows and badges / the number in a badge |

### Roles and accents

An **accent** is a named card style: `{bar: <token>, text: <token>, bullet: <token>}`. The shipped themes define `primary`, `secondary`, `neutral` and `highlight`; `primary`, `secondary` and `neutral` are required.

A **role** is the tag a block carries (`role: method`). The theme maps every role to an accent:

```yaml
roles:
  problem: primary
  method: secondary
  invitation: highlight
  references: neutral
```

This is the point of the indirection: re-theming a poster changes how every `method` card looks without touching `poster.yaml`. The shipped themes map these roles: `problem`, `context`, `aim`, `method`, `result`, `discussion`, `outlook`, `invitation`, `resources`, `references`. Add your own roles in a theme, or force a style on one block with `accent:`. A role the theme does not know falls back to `primary` and raises a warning.

### Status styles

```yaml
status:
  done:    {fill: primary, stroke: primary, text: on_primary}
  planned: {fill: paper,   stroke: primary, text: primary, dash: true}
```

Flow boxes use these. `done`, `planned` and `concept` are required; add more (`blocked`, `external`) and use them as `status:` in a flow. `dash: true` draws a dashed outline, so that status never depends on colour alone.

### Typography and shape

`typography` holds the font files (see [Fonts](#fonts)), the fixed sizes (`heading_pt`, `title_pt_min`, `title_pt_max`, `title_lines`, `subtitle_pt`, `authors_pt`, `affil_pt`, `min_pt`), the `autofit` range for the body text and a few ratios (`scale`: small text, table text, big numbers, sub-headings, line height). `min_pt` is a floor: nothing printed is smaller, and the build warns if any style would be.

`shape` holds corner radii, line widths, the dash pattern and spacing, plus `header_style`: `band` (light text on a coloured band) or `plain` (dark text on the page, with the secondary-colour rule underneath).

### Making your own theme

```cmd
python main.py --new-theme mylab --base neutral
```

This copies `themes/neutral/` to `themes/mylab/` and marks it `state: pending`. Then:

1. Replace `palette` with the colours of the brand guide, named as the guide names them, and fill in `source` (name, URL, licence, note). Say honestly which colours are derived or invented.
2. Point the tokens at palette names.
3. Set `typography.fonts` (copy the font files into `fonts/<family>/` with their licence first).
4. Run `python main.py --theme mylab` and read the contrast messages.
5. Set `state: ready`.

To change only a few things of an existing theme, write a short theme with `extends: neutral` and list only the differences; `themes/leiza/theme.yaml` does this. A theme is a folder so that logos or notes can sit beside the YAML.

### State: pending

A theme with `state: pending` builds, but `--strict` fails, so a poster with stand-in colours cannot be released by mistake. `leiza` is pending until its colours are supplied.

## Fonts

All fonts are in the shared library `fonts/`, one folder per family with its licence and a `SOURCES.md` (origin, date, SHA-256 of every file). A theme points to them with repository-relative paths.

| Folder | Families | Used by |
|---|---|---|
| `fonts/dejavu/` | DejaVu Sans Condensed, DejaVu Sans Bold, DejaVu Sans Mono | `neutral`, monospace fallback |
| `fonts/fira-sans/` | Fira Sans, Fira Mono | `chublets`, `research-squirrel` |
| `fonts/pt-sans/` | PT Sans, PT Mono | `nfdi4objects` |
| `fonts/libre-franklin/` | Libre Franklin | `leiza` |

Rules for adding a font:

- It must be a TrueType file with glyph outlines (`.ttf`). CFF-flavoured `.otf` files do not work.
- It must be a static weight. A variable font has to be cut into static instances first; `tools/make_static_librefranklin.py` shows how, using `fontTools`.
- You need six faces per theme: regular, bold, italic, bold italic, a heading face (usually bold) and a monospace face.
- The font's licence must allow embedding and redistribution, and the licence text must sit next to the files.

A fork that uses one theme can delete the other font folders. Keep `fonts/dejavu/` if the theme uses `DejaVuSansMono.ttf` as its monospace face.

## The checks

`validate` runs before every build.

| Result | Meaning | Examples |
|---|---|---|
| `ERROR` | The build stops | unknown block in the layout, missing content file, unknown accent or flow status, a theme key missing or a font file not found, contrast below 3:1 |
| `WARNING` | The build goes on; `--strict` turns it into a failure | `TODO` left in a text, block without `why`, unused block, unknown role, missing placeholder image, missing logo file, pending theme, sparse poster, contrast of text below 4.5:1, a text style below the `min_pt` floor, `status: draft` (only with `--strict`) |
| `NOTE` | Information only | large display text with contrast between 3:1 and 4.5:1 |

### Contrast

The check computes the WCAG contrast ratio of every pairing the engine draws: body text on page and card, table head, headings on card bars, flow box labels per status, the header band, links, arrows and badges. Thresholds: below 3:1 is an error for everything; text between 3:1 and 4.5:1 is a warning, display text in that range is a note, shapes need 3:1. The recommended 4.5:1 for text is stricter than WCAG asks of text this large; it is a safeguard for reading at a distance. `dist/layout_report.txt` records how many pairings were below the recommended level.

A real example from building the themes: chublets gold arrows on the lilac card came to 2.9:1 and were rejected, which is why the chublets theme sets `connector: primary`.

## Commands

| Command | What it does |
|---|---|
| `python main.py` | All steps |
| `python main.py --list` | List the steps |
| `python main.py --only render` | One step |
| `python main.py --from render` | This step and everything after |
| `python main.py --skip preview` | Everything except this step |
| `python main.py --dry-run` | Show the plan without running anything |
| `python main.py --strict` | Warnings become errors: the release check |
| `python main.py --theme nfdi4objects` | Build with another theme |
| `python main.py --list-themes` | List the themes |
| `python main.py --new-theme mylab --base neutral` | Create a theme from a base |

Every step also runs on its own, for example `python py/step_render.py`. Two builds in a row give byte-identical files: nothing in the output depends on the clock.

## Printing

- The PDF is one page at the chosen size (A0 = 841 × 1189 mm), vector graphics, fonts embedded as subsets.
- There is no bleed, no crop marks and no PDF/X conversion. If the print shop requires them, say so early; it would be an extra step.
- The PDF references the base fonts Helvetica and Times-Roman in its resource list without drawing any text with them (reportlab puts them there for its table and QR drawing). A strict preflight tool may mention them.
- Print a test at A3 (35 % scale): if the smallest text is readable there, it is readable on the A0 at arm's length.
- Check the colours on a proof: a screen shows more than ink does, and the pale tints may disappear.

## When something looks wrong

| Symptom | Cause and fix |
|---|---|
| `ERROR: the content does not fit on the page even at 28 pt` | Too much text. Shorten, remove a block, or move a block to a less crowded column. |
| Very long title is small | The size is fitted to `title_lines`. Set `header.title_lines: 3` (and lower `title_pt_min`) for a three-line title, or move the second half to `subtitle`. |
| A word is cut in the middle of a flow box | The label is wider than its box. Add `<br>`, shorten it, or lower `per_row`. |
| A card has a lot of empty space | Its column neighbour is much taller. Move content, change column `width`, or give the band `weight: 0`. |
| `<br>` appears literally | You put it inside backticks; outside them it breaks the line. |
| A box shows `[image: ...]` | The file is missing and `placeholder: true` is set. Add the file. |
| A glyph is missing in the PDF | The font lacks it. Check `layout_report.txt` for the typeface and test with another theme. |
| `theme 'x' not found` | The folder name must match `id:` and contain `theme.yaml`. |
| Build is not byte-identical | A file you added is read from a place that changes (for example a generated image). Keep generated inputs deterministic. |

## Extending the engine

Add a block type in `py/step_render.py`: write a class with `__init__(self, spec, ctx, width)` that sets `self.height`, and `draw(self, c, x, y_top)`; register it in the `ITEMS` dictionary and add its name to `PART_TYPES` in `py/step_validate.py`. Use `ctx.col[...]` (tokens), `ctx.style(...)` and `ctx.para(...)` for colours and text, so the new block follows the theme. If a fork needs a change in the engine that other posters would want too, make it in the template and merge it back into the forks.

## Not built yet

Ideas that came up and were deliberately left out of this version:

- Numbers and author data from files (`{{ stats.entries }}`, authors from `CITATION.cff`) instead of typed text
- Per-block provenance (`source:`, `verified:`) with a strict check that nothing unverified is printed
- More checks: image resolution at the printed size, a word budget per paragraph, naming the block that overflows
- Variants from one source: A4 handout, landscape, A1
- A 12-column grid and layout presets instead of relative widths
- Block types as plugins in `py/blocks/`
- Content in several languages (`content/en/`, `content/de/`)
