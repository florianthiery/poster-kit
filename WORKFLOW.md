# Workflow on Windows (cmd)

Every command below is meant for the Windows command prompt (`cmd`), started in the folder of this repository.
Each command sits in its own block and can be pasted as one line. This file lives in the repository, so the same
steps apply to every poster you develop here.

- [One-time setup](#one-time-setup)
- [a) Build the PDFs](#a-build-the-pdfs)
- [b) Push the changes to GitHub](#b-push-the-changes-to-github)
- [c) Working on an individual poster](#c-working-on-an-individual-poster)
- [Receiving a patch ZIP from a Claude session](#receiving-a-patch-zip-from-a-claude-session)
- [Updating the core](#updating-the-core)
- [Problems](#problems)

## One-time setup

Install [Python 3.11 or newer](https://www.python.org/downloads/) (tick *Add python.exe to PATH*) and [Git for Windows](https://git-scm.com/download/win). Then:

```cmd
git clone https://github.com/florianthiery/poster-kit.git
```

```cmd
cd poster-kit
```

```cmd
py -m venv .venv
```

```cmd
.venv\Scripts\activate
```

```cmd
pip install -r requirements.txt
```

Tell Git who you are (once per computer):

```cmd
git config --global user.name "Florian Thiery"
```

```cmd
git config --global user.email "thiery.florian@googlemail.com"
```

Every later session starts with `cd poster-kit` and `.venv\Scripts\activate` (the prompt then begins with `(.venv)`).

## a) Build the PDFs

The demo poster (every option in place):

```cmd
python main.py --poster demo
```

Result: `posters\demo\dist\poster.pdf` (print file) and `posters\demo\dist\poster-preview.png` (quick look).

All posters in one go, each in its own theme:

```cmd
python tools\build_all.py
```

All posters, each additionally in every theme (for comparing looks; goes to `posters\<id>\dist\themes\`):

```cmd
python tools\build_all.py --all-themes
```

One poster in another theme, without changing its file:

```cmd
python main.py --poster demo --theme nfdi4objects
```

What is available:

```cmd
python main.py --list-posters
```

```cmd
python main.py --list-themes
```

Release check (warnings become errors; use it before every print or submission):

```cmd
python main.py --poster demo --strict
```

For the demo this fails on purpose (a placeholder image is missing); for a finished poster it must pass.

## b) Push the changes to GitHub

Look at what changed:

```cmd
git status
```

Take everything that changed (new posters, edited texts, rebuilt PDFs):

```cmd
git add -A
```

Save it with a message that says what and why:

```cmd
git commit -m "chnt31: results block rewritten, figure 1 added"
```

Send it to GitHub:

```cmd
git push
```

The first push of a new branch asks for `git push -u origin <branchname>`; Git prints that command itself.

If `git push` is rejected because the repository changed on GitHub in the meantime:

```cmd
git pull --rebase
```

and then `git push` again.

Optional, one branch per poster (keeps the main branch clean until the poster is done):

```cmd
git checkout -b poster/chnt31
```

```cmd
git push -u origin poster/chnt31
```

## c) Working on an individual poster

Everything for one poster lives in `posters\<id>\`; the core (engine, themes, fonts, `shared\logos`) is shared. The
cycle is the same for every poster, and it is written down per poster in its `PRIMER.md`.

1. **Start** (in a Claude session, see [INTERVIEW.md](INTERVIEW.md)): Claude asks for the basics of the poster
   (event, title, authors, funders, key message, numbers) in a short dialogue and writes them into
   `posters\<id>\brief.yaml`, the single source of the poster's facts. The same session creates the poster folder
   from the skeleton. Or by hand:

   ```cmd
   python main.py --new-poster chnt31 --theme chublets
   ```

2. **Work**: change `brief.yaml` (facts), `content\*.md` (texts), `poster.yaml` (blocks and layout), `img\` (figures,
   portraits). After each change:

   ```cmd
   python main.py --poster chnt31
   ```

   and open `posters\chnt31\dist\poster-preview.png`.

3. **Record**: a decision goes with its date into `PRIMER.md` (Teil A4), a change into the change log, a question
   into Teil D. The table of blocks for Teil C:

   ```cmd
   python main.py --poster chnt31 --blocks
   ```

4. **Save** to GitHub as in b).

5. **Finish**: `status: final` in `poster.yaml`, `status: confirmed` in `brief.yaml`, no `TODO` left, then

   ```cmd
   python main.py --poster chnt31 --strict
   ```

   and commit the poster folder including `dist\poster.pdf`.

## Receiving a patch ZIP from a Claude session

A session that changes this repository hands you a ZIP with a `PATCH-README.md` at its root that says what it contains
and how to check it. Unpack it over the repository (existing files are replaced), without touching anything else:

```cmd
powershell -NoProfile -Command "Expand-Archive -Path C:\Users\you\Downloads\patch.zip -DestinationPath . -Force"
```

Then build (a), look at `git status` to see what the patch changed, and commit (b). Delete `PATCH-README.md` from the
repository root once you have read it, or leave it out of the commit.

## Updating the core

If you work in a fork and the original repository gained new features, add it as `upstream` once:

```cmd
git remote add upstream https://github.com/florianthiery/poster-kit.git
```

and pull its changes whenever you like:

```cmd
git pull upstream main
```

Poster folders do not collide with core changes, because a poster only touches `posters\<id>\` and `shared\`.

## Problems

| Message or symptom | What to do |
|---|---|
| `'python' is not recognized` | Python is not on the PATH: use `py` instead of `python`, or reinstall Python with *Add python.exe to PATH* ticked. |
| `ERROR: which poster?` | There is more than one poster: add `--poster <id>`. |
| `ModuleNotFoundError` | The virtual environment is not active: run `.venv\Scripts\activate`, then `pip install -r requirements.txt`. |
| `git push` asks for a password | GitHub no longer accepts passwords: sign in through the browser window Git opens, or use a personal access token. |
| The PDF looks different from the preview | Open the PDF in a viewer that shows embedded fonts (Acrobat, SumatraPDF); the preview is only a small raster picture. |
