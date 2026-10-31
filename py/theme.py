"""Theme loading, resolution and the contrast check.

A theme lives in ``themes/<id>/theme.yaml``. It has two colour layers:

* ``palette``  raw named colours, copied 1:1 from the source of the palette
* ``tokens``   semantic roles (primary, ink, card, ...) that point to palette names

The renderer only ever asks for tokens, never for palette names, so a theme can
be swapped without touching the engine. Everything here is pure Python plus
PyYAML; nothing reads the clock.
"""
from __future__ import annotations

import copy
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
THEMES = ROOT / "themes"

# Tokens every theme must define. Others are optional and may be added freely.
REQUIRED_TOKENS = [
    "primary", "on_primary", "secondary", "on_secondary", "secondary_tint",
    "ink", "muted", "paper", "card", "tint", "line", "link", "header_sub",
]
# Optional tokens with their fallbacks.
TOKEN_FALLBACKS = {"header_accent": "secondary", "connector": "secondary", "on_connector": "on_secondary"}
REQUIRED_ACCENTS = ["primary", "secondary", "neutral"]
REQUIRED_STATUS = ["done", "planned", "concept"]
REQUIRED_FONTS = ["regular", "bold", "italic", "bold_italic", "heading", "mono"]

DEFAULT_SHAPE = {
    "card_radius": 30, "card_line": 3, "box_radius": 22, "box_line": 5,
    "dash": [22, 14], "logo_radius": 20, "logo_line": 4, "arrow_line": 7,
    "badge_line": 4, "header_rule": 14, "item_gap": 0.9, "card_pad_pt": 28,
    "header_style": "band",
}
DEFAULT_SCALE = {"small": 0.82, "table": 0.88, "stat_value": 2.6, "subheading": 1.12, "leading": 1.28}

HEX = re.compile(r"^#[0-9a-fA-F]{6}$")


class ThemeError(Exception):
    """Raised with a message that says what to fix in which file."""


def deep_merge(base: dict, over: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def available() -> list[str]:
    if not THEMES.is_dir():
        return []
    return sorted(p.name for p in THEMES.iterdir()
                  if p.is_dir() and not p.name.startswith("_") and (p / "theme.yaml").is_file())


def _read(theme_id: str) -> dict:
    path = THEMES / theme_id / "theme.yaml"
    if not path.is_file():
        raise ThemeError(f"theme '{theme_id}' not found; available: {', '.join(available()) or 'none'} "
                         f"(looked for themes/{theme_id}/theme.yaml)")
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if data.get("id", theme_id) != theme_id:
        raise ThemeError(f"themes/{theme_id}/theme.yaml has id '{data.get('id')}', expected '{theme_id}'")
    return data


def load_chain(theme_id: str, seen: tuple[str, ...] = ()) -> dict:
    """Read a theme and everything it extends; the child overrides the parent."""
    if theme_id in seen:
        raise ThemeError("theme 'extends' cycle: " + " -> ".join(seen + (theme_id,)))
    raw = _read(theme_id)
    parent = raw.get("extends")
    if parent:
        merged = deep_merge(load_chain(parent, seen + (theme_id,)), {k: v for k, v in raw.items() if k != "extends"})
        merged["extends"] = parent
        return merged
    return raw


def resolve(cfg: dict, cli_theme: str | None = None) -> dict:
    """Return the fully resolved theme for a poster config.

    Order of precedence: --theme on the command line, then ``theme:`` in
    poster.yaml (an id, or a complete inline theme), then ``theme_overrides:``.
    """
    spec = cli_theme or cfg.get("theme")
    if spec is None:
        raise ThemeError("poster.yaml has no 'theme:' key; set it to one of: " + ", ".join(available()))
    raw = spec if isinstance(spec, dict) else load_chain(str(spec))
    if not isinstance(spec, dict):
        raw.setdefault("id", str(spec))
    raw = deep_merge(raw, cfg.get("theme_overrides") or {})
    return _finalise(raw)


def _finalise(raw: dict) -> dict:
    errors: list[str] = []
    tid = raw.get("id", "(inline)")

    def err(msg: str) -> None:
        errors.append(f"theme '{tid}': {msg}")

    palette = raw.get("palette") or {}
    for name, value in palette.items():
        if not (isinstance(value, str) and HEX.match(value)):
            err(f"palette entry '{name}' must be a hex colour like #RRGGBB, got {value!r}")

    tokens_raw = dict(raw.get("tokens") or {})
    for key, fb in TOKEN_FALLBACKS.items():
        tokens_raw.setdefault(key, fb)          # a fallback is an alias to another token
    for t in REQUIRED_TOKENS:
        if t not in tokens_raw:
            err(f"token '{t}' is missing in tokens:")

    def token_value(name: str, trail: tuple[str, ...] = ()) -> str | None:
        """A token is a palette name, a #RRGGBB colour, or an alias to another token."""
        ref = tokens_raw[name]
        if isinstance(ref, str) and HEX.match(ref):
            return ref
        if ref in palette:
            return palette[ref]
        if ref in tokens_raw and ref not in trail and ref != name:
            return token_value(ref, trail + (name,))
        err(f"token '{name}': '{ref}' is not a palette name, a #RRGGBB colour or another token")
        return None

    tokens = {k: v for k in tokens_raw if (v := token_value(k)) is not None}

    accents = raw.get("accents") or {}
    for a in REQUIRED_ACCENTS:
        if a not in accents:
            err(f"accent '{a}' is missing in accents:")
    for aname, spec in accents.items():
        for key in ("bar", "text"):
            if spec.get(key) not in tokens:
                err(f"accents.{aname}.{key}: unknown token {spec.get(key)!r}")
        if spec.get("bullet", spec.get("bar")) not in tokens:
            err(f"accents.{aname}.bullet: unknown token {spec.get('bullet')!r}")

    roles = raw.get("roles") or {}
    for role, aname in roles.items():
        if aname not in accents:
            err(f"roles.{role}: unknown accent {aname!r}")

    status = raw.get("status") or {}
    for s in REQUIRED_STATUS:
        if s not in status:
            err(f"status style '{s}' is missing in status:")
    for sname, spec in status.items():
        for key in ("fill", "stroke", "text"):
            if spec.get(key) not in tokens:
                err(f"status.{sname}.{key}: unknown token {spec.get(key)!r}")

    typo = raw.get("typography") or {}
    fonts_in = typo.get("fonts") or {}
    fonts: dict[str, str] = {}
    for key in REQUIRED_FONTS:
        rel = fonts_in.get(key)
        if not rel:
            err(f"typography.fonts.{key} is missing")
            continue
        path = ROOT / rel
        if not path.is_file():
            err(f"typography.fonts.{key}: file not found: {rel}")
        fonts[key] = str(path)

    sizes = typo.get("sizes") or {}
    for k in ("heading_pt", "title_pt_max", "title_pt_min", "title_lines", "authors_pt", "affil_pt",
              "subtitle_pt", "min_pt"):
        if k not in sizes:
            err(f"typography.sizes.{k} is missing")
    autofit = typo.get("autofit") or {}
    for k in ("min_pt", "max_pt", "step_pt"):
        if k not in autofit:
            err(f"typography.autofit.{k} is missing")

    shape = deep_merge(DEFAULT_SHAPE, raw.get("shape") or {})
    if shape["header_style"] not in ("band", "plain"):
        err("shape.header_style must be 'band' or 'plain'")
    scale = deep_merge(DEFAULT_SCALE, typo.get("scale") or {})

    if errors:
        raise ThemeError("\n".join(errors))

    return {
        "id": tid, "name": raw.get("name", tid), "state": raw.get("state", "ready"),
        "extends": raw.get("extends"), "source": raw.get("source") or {},
        "palette": palette, "tokens": tokens, "accents": accents, "roles": roles,
        "status_styles": status, "fonts": fonts, "font_family": typo.get("family", ""),
        "sizes": sizes, "autofit": autofit, "shape": shape, "scale": scale,
    }


# --------------------------------------------------------------------------
# Contrast (WCAG 2.x relative luminance)
# --------------------------------------------------------------------------
def luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

    def lin(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast(fg: str, bg: str) -> float:
    a, b = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def contrast_pairs(theme: dict) -> list[tuple[str, str, str, str]]:
    """(label, foreground token, background token, kind) for every pairing the engine draws.

    kind 'text'     small and medium text: below 4.5 is a warning, below 3.0 an error
    kind 'heading'  large display text: below 4.5 is a note, below 3.0 an error
    kind 'graphic'  filled shapes and strokes: below 3.0 is an error
    """
    t = theme["tokens"]
    pairs = [
        ("body text on page", "ink", "paper", "text"),
        ("body text on card", "ink", "card", "text"),
        ("muted text on card", "muted", "card", "text"),
        ("muted text on page", "muted", "paper", "text"),
        ("links on card", "link", "card", "text"),
        ("table cells on stripe", "ink", "tint", "text"),
        ("table head", "on_primary", "primary", "text"),
        ("sub-headings on card", "primary", "card", "text"),
        ("big numbers on card", "primary", "card", "heading"),
        ("logo text on page", "primary", "paper", "text"),
        ("step number on badge", "on_connector", "connector", "text"),
        ("arrows and badges on card", "connector", "card", "graphic"),
    ]
    for aname, a in theme["accents"].items():
        pairs.append((f"card title, accent '{aname}'", a["text"], a["bar"], "heading"))
        pairs.append((f"bullets, accent '{aname}'", a.get("bullet", a["bar"]), "card", "graphic"))
    for sname, s in theme["status_styles"].items():
        pairs.append((f"flow box label, status '{sname}'", s["text"], s["fill"], "text"))
    if theme["shape"]["header_style"] == "band":
        pairs += [("header title", "on_primary", "primary", "heading"),
                  ("header subtitle and affiliations", "header_sub", "primary", "text"),
                  ("header event line", "header_accent", "primary", "heading")]
    else:
        pairs += [("header title", "primary", "paper", "heading"),
                  ("header affiliations", "muted", "paper", "text")]
    return [p for p in pairs if p[1] in t and p[2] in t]


def contrast_report(theme: dict) -> list[dict]:
    """Rows with ratio, threshold and level (ok | note | warn | error)."""
    t = theme["tokens"]
    rows = []
    for label, fg, bg, kind in contrast_pairs(theme):
        ratio = contrast(t[fg], t[bg])
        if ratio < 3.0:
            level = "error"                    # below 3:1 nothing is legible enough, whatever the size
        elif kind == "graphic":
            level = "ok"                       # 3:1 is the WCAG minimum for shapes and strokes
        elif ratio < 4.5:
            level = "warn" if kind == "text" else "note"
        else:
            level = "ok"
        rows.append({"label": label, "fg": fg, "bg": bg, "kind": kind, "ratio": ratio, "level": level})
    return rows
