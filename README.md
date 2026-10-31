# poster-kit

A neutral repository for conference posters. Texts live in Markdown, structure in one YAML file, colours and typefaces in swappable **themes**. One command renders a vector PDF (A0 to A4, fonts embedded) and fits the text size to the page, so a changed sentence costs one re-run.

Every poster is a folder in `posters/`, next to the shared core (engine, themes, fonts, logos). The demo poster shows every feature and explains itself; `python main.py --new-poster <id>` starts your own.

## Quick start

```cmd
pip install -r requirements.txt
```

```cmd
python main.py
```

Open `posters/demo/dist/poster.pdf`, or `posters/demo/dist/poster-preview.png` for a quick look. Try another look with `python main.py --theme chublets`. Start a poster of your own with `python main.py --new-poster chnt31 --theme chublets`; once there is more than one poster, say which one: `python main.py --poster chnt31`.

## Where to change what

| To change | Edit |
|---|---|
| A text | `posters/<id>/content/*.md` |
| Which blocks, in which order and columns | `posters/<id>/poster.yaml` |
| Facts: event, title, authors, funders, numbers with sources | `posters/<id>/brief.yaml` (started in a conversation, see [INTERVIEW.md](INTERVIEW.md)) |
| Colours, fonts, shapes | choose a theme: `theme:` in `poster.yaml`, or write one in `themes/` |
| An image, a portrait | `posters/<id>/img/`, `img/people/`; an `image` or `people` part in a block |
| Funders, partners, logos | `shared/logos/` (once, for all posters) and a `supporters` part |
| Why the poster looks as it does | `posters/<id>/PRIMER.md` |

Commands for Windows `cmd` (build, push to GitHub, work on a poster): [WORKFLOW.md](WORKFLOW.md). [GUIDE.md](GUIDE.md) explains every option, the block types, the themes, the checks and how posters live in this repository.

## Themes

| Id | Colours | Typeface |
|---|---|---|
| `neutral` | slate, blue, amber | DejaVu Sans Condensed |
| `chublets` | purple, gold | Fira Sans |
| `research-squirrel` | [squirrel-colours](https://github.com/Research-Squirrel-Engineers/squirrel-colours) | Fira Sans |
| `nfdi4objects` | N4O blues | PT Sans |
| `leiza` | LEIZA corporate design; variants `leiza:red` (general), `leiza:blue` (research), `leiza:yellow` (transfer) | Libre Franklin |

`python main.py --list-themes` lists them; `python main.py --new-theme mylab` creates one.

## Layout of the repository

```
poster-kit/
├── GUIDE.md           everything the repository can do
├── PRIMER.md          work plan of the core (German)
├── WORKFLOW.md        Windows cmd: build, push to GitHub, work on a poster
├── INTERVIEW.md       how a poster starts in a conversation (German)
├── main.py            the only entry point
├── posters/
│   ├── demo/          the demo poster: every option in place
│   ├── _template/     skeleton for --new-poster (not built unless asked)
│   └── <id>/          one folder per poster: brief.yaml, poster.yaml, content/, img/, PRIMER.md, dist/
├── shared/logos/      logos several posters use (institutes, funders, networks)
├── themes/<id>/       theme.yaml per theme
├── fonts/<family>/    shared font library with licences
├── py/                engine: theme.py, poster_utils.py, one module per step
└── tools/             build_all.py (all posters, all themes), font helper
```

## Licence

Code: MIT, see `LICENSE`. Fonts: see `fonts/<family>/` for each licence. Colour palettes: see `source:` in each theme. The sample images are generated placeholders without rights.

## AI use

The engine, themes and documentation were drafted with Claude (Anthropic) and reviewed by Florian Thiery.

## Windows (cmd)

```
py -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt && python main.py
```

## Using it inside an existing repository

Clone or download this repository and copy it as one folder into the repository that should hold the posters (or fork it and develop the posters here, which is the intended way). Everything in the kit is relative to itself, so a subfolder works unchanged:

```
python poster-kit/main.py --new-poster chnt31
python poster-kit/main.py --poster chnt31
```

To update the core later, replace everything in the folder except `posters/`, `shared/` and any theme you added under `themes/`.
