"""Shared constants, paths and small helpers for the poster pipeline.

Nothing in here reads the clock: every artefact changes only when a source
changes, so a rebuild is byte-identical (see PRIMER.md, A3).
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

# Fixed release label. It appears in the layout report and nowhere else.
RELEASE = "2026-10-09"

ROOT = Path(__file__).resolve().parent.parent       # the kit: py/, themes/, fonts/, shared/, posters/
FONTS = ROOT / "fonts"
POSTERS = ROOT / "posters"
SHARED = ROOT / "shared"                            # logos and images that several posters use

# Set by select_poster(); every poster lives in posters/<id>/.
POSTER_ID = ""
POSTER_DIR = ROOT
CONFIG = CONTENT = IMG = DIST = PDF_PATH = PREVIEW_PATH = REPORT_PATH = ROOT


def list_posters() -> list[str]:
    """Poster ids: folders in posters/ with a poster.yaml; names starting with '_' are skeletons."""
    if not POSTERS.is_dir():
        return []
    return sorted(p.name for p in POSTERS.iterdir()
                  if p.is_dir() and not p.name.startswith("_") and (p / "poster.yaml").is_file())


def select_poster(pid: str | None = None) -> str:
    """Point every path at posters/<id>/. Without an id: $POSTER, or the only poster there is."""
    import os

    global POSTER_ID, POSTER_DIR, CONFIG, CONTENT, IMG, DIST, PDF_PATH, PREVIEW_PATH, REPORT_PATH
    pid = pid or os.environ.get("POSTER")
    ids = list_posters()
    if not pid:
        if len(ids) == 1:
            pid = ids[0]
        else:
            raise SystemExit("ERROR: which poster? use --poster <id>; available: " + (", ".join(ids) or "none (create one: python main.py --new-poster <id>)"))
    folder = POSTERS / pid
    if not (folder / "poster.yaml").is_file():
        raise SystemExit(f"ERROR: poster '{pid}' not found (looked for posters/{pid}/poster.yaml); available: {', '.join(ids) or 'none'}")
    POSTER_ID, POSTER_DIR = pid, folder
    CONFIG, CONTENT, IMG, DIST = folder / "poster.yaml", folder / "content", folder / "img", folder / "dist"
    PDF_PATH, PREVIEW_PATH, REPORT_PATH = DIST / "poster.pdf", DIST / "poster-preview.png", DIST / "layout_report.txt"
    import theme as T
    T.set_poster_dir(folder)
    return pid


def find(rel: str) -> Path:
    """Resolve a path written in poster.yaml: first inside the poster folder, then in the kit
    (so ``shared/logos/leiza.svg`` works from every poster). Returns the poster-side path if neither exists."""
    own = POSTER_DIR / rel
    if own.is_file():
        return own
    kit = ROOT / rel
    return kit if kit.is_file() else own


_warnings: list[str] = []


def ensure_dirs() -> None:
    DIST.mkdir(parents=True, exist_ok=True)


BRIEF_REF = __import__("re").compile(r"\{\{\s*(brief(?:\.[A-Za-z0-9_\-]+)+)\s*\}\}")


def load_brief() -> dict:
    """posters/<id>/brief.yaml: the facts of the poster (event, title, authors, funders, numbers)."""
    path = POSTER_DIR / "brief.yaml"
    if not path.is_file():
        return {}
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def _lookup(obj, dotted: str):
    cur = obj
    for part in dotted.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        elif isinstance(cur, list) and part.isdigit() and int(part) < len(cur):
            cur = cur[int(part)]
        else:
            raise KeyError(dotted)
    return cur


def fill(obj, brief: dict, missing: list[str]):
    """Replace ``{{ brief.a.b }}`` in every string. A string that is only a reference becomes the value itself
    (a list or mapping included), so ``authors: "{{ brief.authors }}"`` works; inside longer text it must be a scalar."""
    if isinstance(obj, dict):
        return {k: fill(v, brief, missing) for k, v in obj.items()}
    if isinstance(obj, list):
        return [fill(v, brief, missing) for v in obj]
    if not isinstance(obj, str) or "{{" not in obj:
        return obj
    whole = BRIEF_REF.fullmatch(obj.strip())
    if whole:
        try:
            return _lookup({"brief": brief}, whole.group(1))
        except KeyError:
            missing.append(whole.group(1))
            return obj

    def sub(m):
        try:
            val = _lookup({"brief": brief}, m.group(1))
        except KeyError:
            missing.append(m.group(1))
            return m.group(0)
        if isinstance(val, (dict, list)):
            missing.append(f"{m.group(1)} (is a list or mapping; use it as a whole value, not inside text)")
            return m.group(0)
        return str(val)

    return BRIEF_REF.sub(sub, obj)


def fill_text(text: str) -> str:
    """The same for a Markdown file; only ``{{ brief.... }}`` is touched, other braces stay."""
    if "{{" not in text:
        return text
    missing: list[str] = []
    out = fill(text, load_brief(), missing)
    if missing:
        raise SystemExit("ERROR: brief.yaml has no entry for: " + ", ".join(sorted(set(missing))))
    return out


def load_config(path: Path | None = None, theme: str | None = None) -> dict:
    """Read the selected poster's poster.yaml, fill in the brief, and replace ``theme`` by the resolved theme."""
    import theme as T

    with open(path or CONFIG, encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)
    missing: list[str] = []
    cfg = fill(cfg, load_brief(), missing)
    if missing:
        raise SystemExit("ERROR: poster.yaml refers to entries that brief.yaml does not have: "
                         + ", ".join(sorted(set(missing))))
    try:
        cfg["theme"] = T.resolve(cfg, theme)
    except T.ThemeError as exc:
        raise SystemExit("ERROR: " + str(exc))
    return cfg


def warn(message: str) -> None:
    """Print a warning in a form main.py can count; --strict turns it into an error."""
    if message in _warnings:
        return
    _warnings.append(message)
    print(f"WARNING: {message}")


def finish(strict: bool) -> int:
    """Exit code for a step: non-zero only if strict and warnings were raised."""
    if strict and _warnings:
        print(f"FAILED (--strict): {len(_warnings)} warning(s)")
        return 1
    return 0


def read_text(rel: str) -> str:
    """Read a content file given relative to the poster folder (or the kit)."""
    path = find(rel)
    if not path.is_file():
        raise SystemExit(f"ERROR: content file not found: {rel}")
    return fill_text(path.read_text(encoding="utf-8"))


def parse_args(description: str):
    import argparse

    ap = argparse.ArgumentParser(description=description)
    ap.add_argument("--strict", action="store_true", help="warnings become errors")
    ap.add_argument("--theme", help="theme id, overrides 'theme:' in poster.yaml")
    ap.add_argument("--poster", help="poster id (folder in posters/)")
    args = ap.parse_args()
    select_poster(args.poster)
    return args


if __name__ == "__main__":
    print(f"RELEASE={RELEASE} ROOT={ROOT}", file=sys.stdout)
