# poster-template

A neutral repository for conference posters. Texts live in Markdown, structure in one YAML file, colours and typefaces in swappable **themes**. One command renders a vector PDF (A0 to A4, fonts embedded) and fits the text size to the page, so a changed sentence costs one re-run.

Fork it for each poster. The demo poster that ships with it shows every feature and explains itself.

## Quick start

```cmd
pip install -r requirements.txt
```

```cmd
python main.py
```

Open `dist/poster.pdf`, or `dist/poster-preview.png` for a quick look. Try another look with `python main.py --theme chublets`.

## Where to change what

| To change | Edit |
|---|---|
| A text | `content/*.md` |
| Which blocks, in which order and columns | `poster.yaml` |
| Title, authors, logos | `poster.yaml`, section `header` |
| Colours, fonts, shapes | choose a theme: `theme:` in `poster.yaml`, or write one in `themes/` |
| An image | put it into `img/`, add an `image` part to a block |

[GUIDE.md](GUIDE.md) explains every option, the themes, the checks and the fork workflow.

## Themes

| Id | Colours | Typeface |
|---|---|---|
| `neutral` | slate, blue, amber | DejaVu Sans Condensed |
| `chublets` | purple, gold | Fira Sans |
| `research-squirrel` | [squirrel-colours](https://github.com/Research-Squirrel-Engineers/squirrel-colours) | Fira Sans |
| `nfdi4objects` | N4O blues | PT Sans |
| `leiza` | placeholder, pending | Libre Franklin |

`python main.py --list-themes` lists them; `python main.py --new-theme mylab` creates one.

## Layout of the repository

```
poster-template/
├── GUIDE.md           everything the repository can do
├── PRIMER.md          work plan and decisions (German)
├── main.py            the only entry point
├── poster.yaml        what is on the poster (demo content)
├── content/           texts (input)
├── img/               images and logos (input)
├── themes/<id>/       theme.yaml per theme (input)
├── fonts/<family>/    shared font library with licences (input)
├── py/                engine: theme.py, poster_utils.py, one module per step
├── tools/             one-off helpers (static font instances)
└── dist/              poster.pdf, preview, reports (generated)
```

## Licence

Code: MIT, see `LICENSE`. Fonts: see `fonts/<family>/` for each licence. Colour palettes: see `source:` in each theme. The sample images are generated placeholders without rights.

## AI use

The engine, themes and documentation were drafted with Claude (Anthropic) and reviewed by Florian Thiery.

## Windows (cmd)

```
py -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt && python main.py
```

For the drop-in folder, use `poster-kit\requirements.txt` and `python poster-kit\main.py`.

## Drop-in use inside an existing repository

The whole kit is one folder, `poster-kit/`, and every path in it is relative to itself. Unzip it into the root of a repository you already have (for example a fork of the poster's project) and nothing outside the folder is touched:

```
unzip poster-kit.zip
pip install -r poster-kit/requirements.txt
python poster-kit/main.py --theme chublets
```

Then replace the demo content inside `poster-kit/` (`poster.yaml`, `content/`, `img/`). `poster-kit/dist/` holds the output. Updating the engine later means replacing everything in the folder except your own `poster.yaml`, `content/`, `img/` and any theme you added under `themes/`.
