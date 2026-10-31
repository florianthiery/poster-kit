# Guide

Everything this repository can do, in one place. Read the quick start, then use the rest as a reference.

- [Quick start](#quick-start)
- [Posters in this repository](#posters-in-this-repository)
- [The brief: one source for the facts](#the-brief-one-source-for-the-facts)
- [How the pieces fit](#how-the-pieces-fit)
- [poster.yaml](#posteryaml)
- [Writing text: the Markdown subset](#writing-text-the-markdown-subset)
- [Themes](#themes)
- [Fonts](#fonts)
- [The checks](#the-checks)
- [Commands](#commands)
- [Workflow on Windows](WORKFLOW.md)
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

(With one poster in `posters/`, as shipped, no further argument is needed. With several, say which: `python main.py --poster demo`.)

You get three files in `posters/demo/dist/`:

| File | What it is |
|---|---|
| `poster.pdf` | The poster: one page, vector graphics, fonts embedded |
| `poster-preview.png` | A small raster preview for a quick look |
| `layout_report.txt` | Base text size, size of every block, the `why:` note of every block, the theme and its contrast result |

The demo poster explains itself: every block shows one feature, and `posters/demo/poster.yaml` and `posters/demo/content/` are the source of everything you see.

## Posters in this repository

The repository is the **core** (engine, themes, fonts, shared logos); every poster is a folder in `posters/`. You develop your posters here, next to the core, and improvements to the core are available to all of them at once.

```
posters/<id>/
├── brief.yaml      the facts: event, title, authors, funders, numbers with sources
├── poster.yaml     structure: blocks and layout (reads the brief)
├── content/        texts (Markdown)
├── img/            figures, photographs, portraits (img/people/)
├── themes/         optional: a theme that belongs to this poster only
├── PRIMER.md       why the poster looks the way it does (German work plan)
└── dist/           poster.pdf, preview, reports (generated)
```

### Start a new poster

```cmd
python main.py --new-poster chnt31 --theme chublets
```

This copies `posters/_template/` (a small skeleton with a `brief.yaml` full of `TODO`, a `poster.yaml`, three text stubs and a blank `PRIMER.md`) to `posters/chnt31/`. To start from the demo instead, which has every option in place: `--from-poster demo`. Then:

1. Fill in `posters/chnt31/brief.yaml`: event, title, authors, funders, links, numbers. The easiest way is a conversation in a Claude session that asks for it and writes the file; the protocol is in [INTERVIEW.md](INTERVIEW.md). Then `PRIMER.md` Teil A1 (event, deadline, format) and the goal.
2. In `poster.yaml` set `page` and check `header` (it reads the brief).
3. Write the texts in `content/*.md`; keep the `why:` of each block honest.
4. Put figures into `img/`, portraits into `img/people/`; logos that other posters also use go into `shared/logos/`.
5. Build with `python main.py --poster chnt31` and look at `posters/chnt31/dist/poster-preview.png`. Repeat.
6. Before printing: `meta.status: final`, no `TODO` left, `python main.py --poster chnt31 --strict`.

`python main.py --list-posters` shows what exists. Folders whose name starts with `_` (`_template`) are skeletons: they are not listed and not built unless you ask (`--poster _template`).

### Where files are looked up

Every path in `poster.yaml` (`file:`, `src:`, `photo:`, logo files) is looked up first inside the poster folder, then from the repository root. So `img/figure1.png` is `posters/chnt31/img/figure1.png`, and `shared/logos/leiza.svg` is the shared logo, the same from every poster. A file of the same name inside the poster folder wins, which lets one poster replace a shared logo.

Themes work the same way: `posters/chnt31/themes/<id>/theme.yaml` is found before `themes/<id>/`. Use that for a look that belongs to one poster only; use `theme_overrides:` in `poster.yaml` for a few changed values; use `themes/` for a look that several posters share.

### The poster PRIMER

Each poster has its own `PRIMER.md`, in German like the other PRIMER files: Teil A (occasion, goal, rules, the table of decisions with dates, commands), Teil B (steps P0 to P5 with status), Teil C (every block: why it is there, where its numbers come from) and Teil D (open points), plus a change log. It is how a poster stays workable over many sessions: whoever continues reads Teil A and the open step, and changes nothing the PRIMER does not explain.

`python main.py --poster chnt31 --blocks` prints the block table (id, role, title, `why`) as Markdown, ready to paste into Teil C; the build reminds you with a `NOTE` when a block does not appear in the PRIMER.

The kit's own `PRIMER.md` in the repository root is the plan of the core and does not belong to any poster.

### Keeping the core current

Work on a poster only touches `posters/<id>/` (and `shared/` for logos). If you keep the poster work in a fork of this repository, pull the core from the original with `git pull upstream main`: the poster folders do not collide with core changes. If you want the engine in an existing repository instead, copy the whole kit into a subfolder; see *Using it inside an existing repository* in `README.md`.

## The brief: one source for the facts

`posters/<id>/brief.yaml` holds everything that is a *fact* about the poster: event, title, subtitle, key message, authors and affiliations, the people to show, funders and partners, QR links, and the numbers with their sources. `poster.yaml` holds what is *structure*: which blocks, in which order, how they look. The two are joined by references:

```yaml
# brief.yaml
event: {name: "CHNT31"}
poster: {title: "From list to graph"}
authors:
  - {name: "Ada Example", affil: "1"}
numbers:
  - {value: "123", label: "things counted", source: "example count", queried: "2025-12-01"}
```

```yaml
# poster.yaml
header:
  event: "{{ brief.event.name }} · Poster"     # inside text: the value is inserted
  title: "{{ brief.poster.title }}"
  authors: "{{ brief.authors }}"               # a string that is only a reference takes over the whole list
blocks:
  numbers:
    type: stats
    items: "{{ brief.numbers }}"               # value and label are drawn; source and date stay in the brief
```

The same `{{ brief.poster.key_message }}` works in `content/*.md`. A path uses dots and list positions (`brief.authors.0.name`). A reference to something that is not in the brief is an error that names it. Only `{{ brief.… }}` is touched; other braces in your texts stay as they are.

Why: a number or a name that appears twice is typed once, and a changed fact changes everywhere on the next build. The brief is also what a conversation produces first (see [INTERVIEW.md](INTERVIEW.md)): while `status: interview`, the build warns about every remaining `TODO`; set `confirmed` when the facts are agreed. The brief is optional: a poster without `brief.yaml` works as before.

## How the pieces fit

| Layer | Files | Answers | Changes |
|---|---|---|---|
| Facts | `posters/<id>/brief.yaml` | Who, where, which numbers, which funders? | when a fact changes |
| Content | `posters/<id>/content/*.md`, `img/` | What is written and shown? | every revision |
| Structure | `posters/<id>/poster.yaml` | Which blocks, in which order and columns? | per poster |
| Memory | `posters/<id>/PRIMER.md` | Why is it like this, where do the numbers come from? | with every decision |
| Look | `themes/<id>/theme.yaml`, `fonts/`, `shared/logos/` | Colours, typefaces, shapes, card styles | per brand or event |
| Engine | `main.py`, `py/` | Draws the PDF | rarely |

The build runs three steps: `validate` (checks the files and the theme), `render` (draws the PDF) and `preview` (makes the PNG).

## poster.yaml

Paths in `poster.yaml` are relative to the poster folder and then to the repository root, see [Where files are looked up](#where-files-are-looked-up).

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
  # subtitle_pt: 52                      # size and weight of the subtitle (theme default otherwise)
  # subtitle_bold: true
  # authors_pt: 36                       # sizes of the author line and of the affiliations
  # affil_pt: 26
  # logos_valign: center                 # logo stack centred against the text (default: top)
  authors:
    - {name: "Ada Example", affil: "1"}  # affil: the number(s) of the affiliation(s) below
  affiliations:
    - "Example Institute, Example City"
  logos_w_mm: 120
  logo_h_mm: 26
  logos:
    - {name: "Example logo", src: shared/logos/example-logo.svg}   # with src: the file (SVG, PNG, JPG)
    - {name: "Institute name"}                                  # without src: the name in a pill
```

The title takes the largest size between `title_pt_min` and `title_pt_max` that fits in `title_lines` lines. `title_lines` is a preference: if the title still needs more lines at the minimum size, it simply wraps further, the header grows, the body text gets less room and the build warns. If the page is full even with the smallest body size, the title is reduced in steps (down to `title_pt_min`) and the body sizes are tried again; the build says so. The three keys can be set under `header:` in `poster.yaml` for one poster, without touching the theme. Logos are stacked on the right, each in a pill with the theme's secondary colour as outline; `logos_valign: center` centres the stack against the text, which looks better when one large logo sits next to a tall text column. `authors_pt`, `affil_pt` and `subtitle_pt` replace the theme's sizes for one poster (the themes are quite prominent; 36 and 26 pt are calmer on a crowded poster). Affiliation numbers are set as small raised numerals.

A long abstract title does not belong in the title line: a short title in one large line plus the long one as a bold subtitle (`subtitle_pt: 52`, `subtitle_bold: true`) reads better and leaves the page more room than three title lines.

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
| `valign` | `center` centres the content in the card below the heading (default: top). For `people` and `supporters` in a band that is taller than their content. |
| `center_last` | `true`: in a block with several parts the last one (typically a figure) is centred in the space left under the text. |

A block holds one **part** (text, table, flow, stats, image, image_row, qr, logos, people, supporters, gallery, timeline, cite), written directly in the block, or a list of parts under `parts:`. Parts are stacked in the order given.

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
  - {name: "Partner two", src: shared/logos/partner-two.png}
```

A row of logo pills, for example partners in a card. The header logos work the same way.

#### people

```yaml
type: people
per_row: 4                    # people per row; default: up to 4. An incomplete last row is centred
shape: circle                 # circle | rounded | square
size_mm: 38                   # photo diameter; default: fills the cell (at most 70 mm)
ring: true                    # outline in the theme's secondary colour; false for none
show_names: true              # false: photos only
items:
  - {name: "Ada Example", role: "Presenting", photo: img/people/ada.jpg}
  - {name: "Dr. Ben Sample", photo: img/people/ben.jpg, focus: [0.5, 0.25], zoom: 1.3}
  - {name: "Chris Placeholder"}          # no photo: initials on a tinted disc
```

Names, an optional line under the name (`role`), no institution: the institutions are in the header. The photo is cropped to a square from the middle of the picture; `focus: [x, y]` (0 to 1, from the top left) moves the crop centre, which matters for portraits where the face sits in the upper third, and `zoom` (1 or more) crops tighter. PNG, JPG and SVG work. A missing photo is not an error: the person appears with initials (the build warns), so the card works before the photographs arrive. Use photographs with the consent of the people shown.

#### supporters

```yaml
type: supporters
columns: 2                    # groups side by side; default 1 (stacked)
style: panel                  # panel (white box with a thin line) | pill (outlined in the secondary colour) | plain (no box)
height_mm: 22                 # logo height; each logo keeps its proportions
align: left                   # left | center
groups:
  - label: "Funded by"
    note: "Grant no. 000000"                       # optional small line under the label
    items:
      - {name: "Example Funder", src: shared/logos/example-funder.svg}
  - label: "In cooperation with"
    style: pill                                    # a group may set its own style, height_mm and align
    items:
      - {name: "Example Network", src: shared/logos/example-network.svg}
      - {name: "Partner without a logo file"}      # no src: the name is printed in a box
```

For funders, partners, networks and hosts: labelled groups of logos. Rows are filled greedily, which can give 4 + 1; `per_row: 3` (on the part or on one group) makes the rows even instead (5 logos become 3 + 2). For a fully controlled layout use one group per row, each with its own `height_mm` and `align: center`. Logos are placed by their proportions, wrap to the next row when the row is full, and a missing file falls back to the name, so a first draft needs no logos at all. For a single row without labels, `items:` directly in the part is enough. The older `logos` part still works and draws equal-width pills; `supporters` is the one to use for real funder lines. Check the usage terms of every logo (funders usually publish them with rules) and note them next to the file in `shared/logos/README.md`.

#### gallery

```yaml
type: gallery
columns: 2                    # default 2
cell_height_mm: 36            # default: 0.72 x the cell width
fit: cover                    # cover (crop to fill) | contain (whole picture on a tint); a picture may set its own
items:
  - {src: img/site-a.jpg, caption: "Site A, 2025."}
  - {src: img/plan.svg, caption: "Plan.", fit: contain}
  - {src: img/site-b.jpg, caption: "Site B.", focus: [0.8, 0.4]}   # focus: crop centre, 0 to 1 from the top left
```

Several pictures in a grid, a caption under each. `fit: contain` shows the whole picture on the card's tint, which looks like white space at the sides; `matte: false` omits tint and frame. For two or three pictures that should sit side by side at one height, `image_row` is the better part. A missing file is not an error: a dashed box with the file name is drawn (the build warns), so the layout can be judged before all pictures exist. For one large picture with a long caption use `image`.

#### image_row

```yaml
type: image_row
max_height_mm: 60             # the row is never taller than this; height_mm sets an exact height
gap_mm: 6                     # default: a little under one text line
items:
  - {src: img/before.jpg, caption: "Before."}
  - {src: img/after.png}                    # captions are optional, also for single pictures
  - {src: img/missing.png, ratio: 1.5}      # a missing file is a dashed box; ratio = width / height (default 4:3)
```

Pictures side by side at one common height, evenly spaced and never cropped. Without a height the row is as tall as it can be while filling the card width exactly; with `max_height_mm` or `height_mm` a shorter row is spread over equal slots, and a caption may use its whole slot. Raster and SVG can be mixed. Transparent PNGs keep their transparency, so a picture pair needs no pre-composed image.

#### timeline

```yaml
type: timeline
orientation: vertical         # vertical (default, for narrow cards) | horizontal
per_row: 4                    # horizontal only: points per row
items:
  - {when: "2026", label: "Prototype", sub: "first release", status: done}
  - {when: "2027", label: "Pilot", status: planned}
  - {when: "later", label: "Roll-out", status: concept}
```

Dated steps along a line. `status` takes the theme's status styles (as in `flow`): solid dot for done, dashed for planned and concept, so status never rests on colour alone. `when` and `sub` are optional.

#### cite

```yaml
type: cite
label: "How to cite"          # default
# source: CITATION.cff        # default; the poster's own folder first, then the kit's
# text: "Own reference line"  # overrides the generated line
```

A reference line built from `CITATION.cff` (authors, year, title, version, DOI or URL; a `preferred-citation` wins; more than six authors become "et al."). Put a `CITATION.cff` into `posters/<id>/` for the poster's own citation; without one the kit's is used. Typically a second part in the card with the QR codes.

### footer

```yaml
footer:                       # optional, a top-level key next to header and page
  height_mm: 24               # default 26
  text: "{{ brief.event.name }}"            # bold line
  meta: "DOI 10.xxxx/xxxxx"                 # second line, muted
  licence: "CC BY 4.0"        # badge on the right
  qr: https://example.org/poster            # QR code on the left
```

A strip at the bottom of the page: a thin rule, an optional QR code, one or two lines of text and a licence badge. Every key is optional, but at least one is needed. The body gives up the space, so text size and title adapt as usual. Without `footer:` nothing is drawn (there is no DRAFT line).

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

Autofit fills every free millimetre: when a block gets shorter, the body text grows (28 to 29.5 pt, say) instead of leaving air. If you would rather give figures the room, raise their `max_height_mm`, or cap the text size for this poster:

```yaml
theme_overrides:
  typography: {autofit: {max_pt: 30}}
```

The layout report notes when autofit has grown the text above its minimum.

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
| `leiza` | LEIZA corporate design, three variants: `red` (general), `blue` (research), `yellow` (transfer) | Libre Franklin | ready |

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

To change only a few things of an existing theme, write a short theme with `extends: neutral` and list only the differences. A theme is a folder so that logos or notes can sit beside the YAML.

### State: pending

A theme with `state: pending` builds, but `--strict` fails, so a poster with stand-in colours cannot be released by mistake. A copy made with `--new-theme` starts as pending; set `state: ready` when the palette is final.

### Variants

Some brands do not have one look but several, each led by one colour. LEIZA is the example: red is the general colour, blue stands for research, yellow for transfer, and a poster normally uses one of them, not all three together. A theme can therefore define `variants:`; each variant overrides tokens, accents, roles, status styles or shape of the theme:

```yaml
variant: red                       # the default when nobody names one
variants:
  red:
    label: "general"
    tokens: {primary: leiza-rot-d2, secondary: leiza-rot, ...}
  yellow:
    label: "transfer"
    tokens: {primary: black, secondary: leiza-gelb, on_secondary: black, ...}
    shape: {header_style: plain}   # white text on yellow cannot be read, so this look has a plain header
```

Choose one with `theme: leiza:blue` in `poster.yaml`, or `theme: leiza` plus `theme_variant: blue`, or on the command line with `--theme leiza:blue`. `python main.py --list-themes` lists the variants, and `tools/build_all.py --all-themes` builds every one of them. Everything in a theme is checked per variant: the contrast check runs on the variant that is built.

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

The check computes the WCAG contrast ratio of every pairing the engine draws: body text on page and card, table head, headings on card bars, flow box labels per status, the header band, links, arrows and badges. Thresholds: below 3:1 is an error for everything; text between 3:1 and 4.5:1 is a warning, display text in that range is a note, shapes need 3:1. The recommended 4.5:1 for text is stricter than WCAG asks of text this large; it is a safeguard for reading at a distance. `dist/layout_report.txt` (in the poster folder) records how many pairings were below the recommended level.

A real example from building the themes: chublets gold arrows on the lilac card came to 2.9:1 and were rejected, which is why the chublets theme sets `connector: primary`.

## Commands

Step-by-step instructions for Windows `cmd`, including Git and GitHub, are in [WORKFLOW.md](WORKFLOW.md).

| Command | What it does |
|---|---|
| `python main.py` | All steps for the only poster (or `$POSTER`) |
| `python main.py --poster chnt31` | All steps for one poster |
| `python main.py --list-posters` | List the posters |
| `python main.py --new-poster chnt31 [--theme chublets] [--from-poster demo]` | Create a poster from the skeleton (or from another poster) |
| `python tools/measure.py --poster ID [--pt N]` | Natural height of every band, column and card (where the height goes) |
| `python tools/build_all.py [--poster ID] [--all-themes] [--strict] [--check-repro]` | Build every poster (and every theme) in one go; `--strict` only checks posters marked `status: final`; `--check-repro` builds twice and compares the PDFs |
| `python main.py --poster chnt31 --blocks` | Block table as Markdown for the poster's PRIMER |
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
| `ERROR: which poster?` | There is more than one poster: add `--poster <id>` (or set the environment variable `POSTER`). |
| A word is cut in the middle of a flow box | The label is wider than its box. Add `<br>`, shorten it, or lower `per_row`. |
| A card has a lot of empty space | Its column neighbour is much taller. Move content, change column `width`, or give the band `weight: 0`. |
| `<br>` appears literally | You put it inside backticks; outside them it breaks the line. |
| A box shows `[image: ...]` | The file is missing and `placeholder: true` is set. Add the file. |
| A glyph is missing in the PDF | The font lacks it. Check `layout_report.txt` for the typeface and test with another theme. |
| `theme 'x' not found` | The folder name must match `id:` and contain `theme.yaml`. |
| Build is not byte-identical | A file you added is read from a place that changes (for example a generated image). Keep generated inputs deterministic. |

**The build stops with "over by N mm".** Run `python tools/measure.py --poster <id>`: it prints the natural height of every band, column and card at the smallest text size and marks the tallest column of each band. Only the tallest column counts, so shortening a shorter neighbour gains nothing. The failed build also writes this table into `dist/layout_report.txt`, marked `FAILED`, so an old report cannot pass for the current one. The order of cuts that has worked: drop number tiles that a figure already shows, put the references into the bottom band, cap figure heights (`max_height_mm`), shorten texts, reduce margin and gap.

**Figures taken from slides are small.** A slide PNG on A0 has text of about 10 pt. Redraw the figure for the poster, or use a native `flow` or `timeline`; at least crop the slide footer (step numbers, page numbers) so it does not collide with the poster's own numbering.

**Logo files with a white border** look off-centre in a pill. Crop them (Pillow, alpha channel) before use. Logos that already say "Funded by" or "In cooperation with" need no group label.

**Look at the preview, not only at `result: ok`.** Raised numerals, white space in a contained picture and awkward title breaks show up only in the image. Crop the header and the bands and look at each.

## Continuous integration

`.github/workflows/build.yml` builds on every push and pull request: the demo in every theme, a reproducibility check (two builds, identical PDFs), and a strict check of posters marked `status: final`. The PDFs and previews are attached to the run as an artifact. `.gitattributes` keeps line endings stable (LF in text files, binary for fonts, PDFs and images), so Windows checkouts do not show phantom changes.

## Extending the engine

Add a block type in `py/step_render.py`: write a class with `__init__(self, spec, ctx, width)` that sets `self.height`, and `draw(self, c, x, y_top)`; register it in the `ITEMS` dictionary and add its name to `PART_TYPES` in `py/step_validate.py`. Use `ctx.col[...]` (tokens), `ctx.style(...)` and `ctx.para(...)` for colours and text, so the new block follows the theme. If a poster needs a change in the engine that other posters would want too, make it in the core: all posters in the repository get it.

## Not built yet

Ideas that came up and were deliberately left out of this version:

- Numbers and author data from files (`{{ stats.entries }}`, authors from `CITATION.cff`) instead of typed text
- Per-block provenance (`source:`, `verified:`) with a strict check that nothing unverified is printed
- More checks: image resolution at the printed size, a word budget per paragraph, naming the block that overflows
- Variants from one source: A4 handout, landscape, A1
- A 12-column grid and layout presets instead of relative widths
- Block types as plugins in `py/blocks/`
- Content in several languages (`content/en/`, `content/de/`)
- More block types, see the ideas in the PRIMER: before/after image pair, glossary
