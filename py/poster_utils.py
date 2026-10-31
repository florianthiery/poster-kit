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

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "poster.yaml"
CONTENT = ROOT / "content"
FONTS = ROOT / "fonts"
IMG = ROOT / "img"
DIST = ROOT / "dist"

PDF_PATH = DIST / "poster.pdf"
PREVIEW_PATH = DIST / "poster-preview.png"
REPORT_PATH = DIST / "layout_report.txt"

_warnings: list[str] = []


def ensure_dirs() -> None:
    DIST.mkdir(parents=True, exist_ok=True)


def load_config(path: Path | None = None, theme: str | None = None) -> dict:
    """Read poster.yaml and replace its ``theme`` entry by the fully resolved theme."""
    import theme as T

    with open(path or CONFIG, encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)
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
    """Read a content file given relative to the repository root."""
    path = ROOT / rel
    if not path.is_file():
        raise SystemExit(f"ERROR: content file not found: {rel}")
    return path.read_text(encoding="utf-8")


def parse_args(description: str):
    import argparse

    ap = argparse.ArgumentParser(description=description)
    ap.add_argument("--strict", action="store_true", help="warnings become errors")
    ap.add_argument("--theme", help="theme id, overrides 'theme:' in poster.yaml")
    return ap.parse_args()


if __name__ == "__main__":
    print(f"RELEASE={RELEASE} ROOT={ROOT}", file=sys.stdout)
