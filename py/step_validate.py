"""Check poster.yaml, the theme and the files they point to before anything is drawn."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import poster_utils as U  # noqa: E402
import theme as T  # noqa: E402

PART_TYPES = {"text", "table", "flow", "image", "stats", "qr", "logos", "people", "supporters", "gallery", "image_row", "timeline", "cite"}
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

    brief = U.load_brief()
    if brief:
        todos = []

        def scan(o, where=""):
            if isinstance(o, dict):
                for k, val in o.items():
                    scan(val, f"{where}.{k}" if where else str(k))
            elif isinstance(o, list):
                for i, val in enumerate(o):
                    scan(val, f"{where}.{i}")
            elif isinstance(o, str) and "TODO" in o:
                todos.append(where)
        scan(brief)
        if todos:
            U.warn(f"brief.yaml has {len(todos)} unresolved TODO(s), first: {', '.join(todos[:4])}")
        if str(brief.get("status", "")) == "interview":
            U.warn("brief.yaml status is 'interview': confirm the facts and set it to 'confirmed'")
    foot = cfg.get("footer")
    if foot:
        for k in foot:
            if k not in ("height_mm", "text", "meta", "licence", "qr"):
                errors.append(f"footer: unknown key '{k}' (allowed: height_mm, text, meta, licence, qr)")
        if not any(foot.get(k) for k in ("text", "meta", "licence", "qr")):
            errors.append("footer: give at least one of text, meta, licence, qr")
    if cfg["header"].get("logos_valign", "top") not in ("top", "center"):
        errors.append("header.logos_valign must be top or center")
    blocks = cfg["blocks"]
    primer = U.POSTER_DIR / "PRIMER.md"
    if not primer.is_file():
        U.warn(f"posters/{U.POSTER_ID}/PRIMER.md is missing: it records why the poster looks the way it does "
               f"(template: posters/_template/PRIMER.md)")
    else:
        text = primer.read_text(encoding="utf-8")
        missing = [bid for bid in blocks if f"`{bid}`" not in text]
        if missing and U.POSTER_ID != "demo":
            print(f"NOTE: PRIMER.md does not mention block(s) {', '.join(missing)}; "
                  f"`python main.py --poster {U.POSTER_ID} --blocks` prints the table for Teil C")
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
        if spec.get("valign", "top") not in ("top", "center"):
            errors.append(f"block '{bid}': valign must be top or center")
        for part in part_list(spec):
            ptype = part.get("type")
            if ptype not in PART_TYPES:
                errors.append(f"block '{bid}': unknown part type {ptype!r}")
                continue
            if ptype == "text" and "file" in part and not U.find(part["file"]).is_file():
                errors.append(f"block '{bid}': content file missing: {part['file']}")
            for ref in ([part["file"]] if ptype == "text" and "file" in part else []) + \
                       ([part["src"]] if part.get("src") else []):
                found = U.find(ref)
                if found.is_file() and U.POSTER_DIR not in found.parents and ref.split("/")[0] in ("content", "img", "data"):
                    U.warn(f"block '{bid}': {ref} is taken from the kit root, not from the poster folder "
                           f"(a stale file there? the poster's own copy is missing)")
            if ptype == "image":
                exists = U.find(part["src"]).is_file()
                if not exists and not part.get("placeholder"):
                    errors.append(f"block '{bid}': image missing: {part['src']}")
                if not exists and part.get("placeholder"):
                    U.warn(f"block '{bid}': image missing, placeholder will be drawn: {part['src']}")
            if ptype == "people":
                if not part.get("items"):
                    errors.append(f"block '{bid}': people needs a non-empty 'items' list")
                for who in part.get("items") or []:
                    if not who.get("name"):
                        errors.append(f"block '{bid}': a person has no 'name'")
                    elif who.get("photo") and not U.find(who["photo"]).is_file():
                        U.warn(f"block '{bid}': photo missing for {who['name']}, initials will be drawn: {who['photo']}")
                    elif who.get("photo") and U.find(who["photo"]).suffix.lower() not in (".png", ".jpg", ".jpeg", ".svg"):
                        errors.append(f"block '{bid}': photo of {who['name']} must be PNG, JPG or SVG: {who['photo']}")
                if part.get("shape", "circle") not in ("circle", "rounded", "square"):
                    errors.append(f"block '{bid}': people.shape must be circle, rounded or square")
            if ptype == "supporters":
                groups = part.get("groups") or ([{"items": part["items"]}] if part.get("items") else [])
                if not groups:
                    errors.append(f"block '{bid}': supporters needs 'groups' (or 'items')")
                for g in groups:
                    if g.get("style", part.get("style", "panel")) not in ("panel", "pill", "plain"):
                        errors.append(f"block '{bid}': supporters.style must be panel, pill or plain")
                    for it in g.get("items") or []:
                        if not it.get("name"):
                            errors.append(f"block '{bid}': a supporter has no 'name' (needed as fallback and alt text)")
                        elif it.get("src") and not U.find(it["src"]).is_file():
                            U.warn(f"block '{bid}': logo file missing, name will be drawn instead: {it['src']}")
            if ptype == "gallery":
                if not part.get("items"):
                    errors.append(f"block '{bid}': gallery needs a non-empty 'items' list")
                if part.get("fit", "cover") not in ("cover", "contain"):
                    errors.append(f"block '{bid}': gallery.fit must be cover or contain")
                for it in part.get("items") or []:
                    if not it.get("src"):
                        errors.append(f"block '{bid}': a gallery picture has no 'src'")
                    elif not U.find(it["src"]).is_file():
                        U.warn(f"block '{bid}': gallery picture missing, a dashed box is drawn: {it['src']}")
            if ptype == "image_row":
                if not part.get("items"):
                    errors.append(f"block '{bid}': image_row needs a non-empty 'items' list")
                for it in part.get("items") or []:
                    if not it.get("src"):
                        errors.append(f"block '{bid}': an image_row picture has no 'src'")
                    elif not U.find(it["src"]).is_file():
                        U.warn(f"block '{bid}': image_row picture missing, a dashed box is drawn: {it['src']}")
            if ptype == "timeline":
                if not part.get("items"):
                    errors.append(f"block '{bid}': timeline needs a non-empty 'items' list")
                if part.get("orientation", "vertical") not in ("vertical", "horizontal"):
                    errors.append(f"block '{bid}': timeline.orientation must be vertical or horizontal")
                for it in part.get("items") or []:
                    if not it.get("label"):
                        errors.append(f"block '{bid}': a timeline entry has no 'label'")
                    elif it.get("status", "done") not in th["status_styles"]:
                        errors.append(f"block '{bid}': timeline status '{it.get('status')}' is not a status style of theme "
                                      f"'{th['id']}' (has: {', '.join(th['status_styles'])})")
            if ptype == "cite" and not part.get("text"):
                src = part.get("source", "CITATION.cff")
                if not U.find(src).is_file():
                    errors.append(f"block '{bid}': cite needs {src} (or a 'text:'); not found in the poster folder or the kit")
            if ptype == "flow":
                for step in part["steps"]:
                    st = step.get("status", "done")
                    if st not in th["status_styles"]:
                        errors.append(f"block '{bid}': flow step '{step.get('label')}' has status '{st}', "
                                      f"theme defines: {', '.join(th['status_styles'])}")

    for logo in cfg["header"].get("logos", []) or []:
        if logo.get("src") and not U.find(logo["src"]).is_file():
            U.warn(f"logo file missing, name pill will be drawn instead: {logo['src']}")

    if errors:
        print("\n".join("ERROR: " + e for e in errors))
        return 1
    print(f"OK: theme '{th['id']}', {len(blocks)} blocks, {len(cfg['layout']['bands'])} bands")
    return U.finish(args.strict)


if __name__ == "__main__":
    sys.exit(main())
