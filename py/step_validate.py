"""Check poster.yaml, the theme and the files they point to before anything is drawn."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import poster_utils as U  # noqa: E402
import theme as T  # noqa: E402

PART_TYPES = {"text", "table", "flow", "image", "stats", "qr", "logos"}
PAGE_SIZES = {"A0", "A1", "A2", "A3", "A4"}


def part_list(spec: dict) -> list[dict]:
    """A block is either one part itself or a list of parts under 'parts'."""
    return spec["parts"] if "parts" in spec else [spec]


def check_theme(th: dict, errors: list[str]) -> None:
    if th["state"] != "ready":
        U.warn(f"theme '{th['id']}' is '{th['state']}': its colours are placeholders, not final")
    for row in T.contrast_report(th):
        msg = f"{row['label']}: {row['fg']} on {row['bg']} = {row['ratio']:.2f}:1"
        if row["level"] == "error":
            errors.append(f"contrast below 3:1, {msg}")
        elif row["level"] == "warn":
            U.warn(f"contrast below 4.5:1 for text, {msg}")
        elif row["level"] == "note":
            print(f"NOTE: {msg} (fine for large display text)")


def main() -> int:
    args = U.parse_args(__doc__)
    cfg = U.load_config(theme=args.theme)
    th = cfg["theme"]
    errors: list[str] = []

    for key in ("meta", "page", "header", "blocks", "layout"):
        if key not in cfg:
            errors.append(f"missing top-level key: {key}")
    if errors:
        print("\n".join("ERROR: " + e for e in errors))
        return 1

    if cfg["page"].get("size") not in PAGE_SIZES:
        errors.append(f"page.size must be one of {sorted(PAGE_SIZES)}")

    check_theme(th, errors)
    if args.strict and cfg["meta"].get("status") == "draft":
        U.warn("meta.status is 'draft': set it to 'final' for the release build")

    blocks = cfg["blocks"]
    used: list[str] = []
    for band in cfg["layout"]["bands"]:
        for col in band["columns"]:
            for bid in col["blocks"]:
                if bid not in blocks:
                    errors.append(f"layout refers to unknown block: {bid}")
                used.append(bid)
    for bid in sorted(set(blocks) - set(used)):
        U.warn(f"block '{bid}' is defined but not used in the layout")
    for bid in sorted({b for b in used if used.count(b) > 1}):
        errors.append(f"block '{bid}' is placed more than once")

    for bid, spec in blocks.items():
        if "why" not in spec:
            U.warn(f"block '{bid}' has no 'why' note (the layout report would be silent about it)")
        if spec.get("accent") and spec["accent"] not in th["accents"]:
            errors.append(f"block '{bid}': accent '{spec['accent']}' is not defined in theme '{th['id']}' "
                          f"(has: {', '.join(th['accents'])})")
        if spec.get("role") and spec["role"] not in th["roles"] and not spec.get("accent"):
            U.warn(f"block '{bid}': role '{spec['role']}' is not mapped by theme '{th['id']}', "
                   f"falling back to accent 'primary' (mapped roles: {', '.join(th['roles'])})")
        for part in part_list(spec):
            ptype = part.get("type")
            if ptype not in PART_TYPES:
                errors.append(f"block '{bid}': unknown part type {ptype!r}")
                continue
            if ptype == "text" and "file" in part and not (U.ROOT / part["file"]).is_file():
                errors.append(f"block '{bid}': content file missing: {part['file']}")
            if ptype == "image":
                exists = (U.ROOT / part["src"]).is_file()
                if not exists and not part.get("placeholder"):
                    errors.append(f"block '{bid}': image missing: {part['src']}")
                if not exists and part.get("placeholder"):
                    U.warn(f"block '{bid}': image missing, placeholder will be drawn: {part['src']}")
            if ptype == "flow":
                for step in part["steps"]:
                    st = step.get("status", "done")
                    if st not in th["status_styles"]:
                        errors.append(f"block '{bid}': flow step '{step.get('label')}' has status '{st}', "
                                      f"theme defines: {', '.join(th['status_styles'])}")

    for logo in cfg["header"].get("logos", []) or []:
        if logo.get("src") and not (U.ROOT / logo["src"]).is_file():
            U.warn(f"logo file missing, name pill will be drawn instead: {logo['src']}")

    if errors:
        print("\n".join("ERROR: " + e for e in errors))
        return 1
    print(f"OK: theme '{th['id']}', {len(blocks)} blocks, {len(cfg['layout']['bands'])} bands")
    return U.finish(args.strict)


if __name__ == "__main__":
    sys.exit(main())
