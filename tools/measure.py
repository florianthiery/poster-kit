"""Where does the height go? Natural height of every band, column and card of a poster.

    python tools/measure.py --poster chnt31-fdox            # at the smallest body size (the hardest case)
    python tools/measure.py --poster chnt31-fdox --pt 32    # at another body size

Use it when a build stops with "over by N mm": the tallest column of each band is marked, and
shortening anything else in that band changes nothing.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "py"))
import poster_utils as U  # noqa: E402
import step_render as R  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--poster", help="poster id (default: the only poster, or $POSTER)")
    ap.add_argument("--pt", type=float, help="body size in pt (default: the theme's minimum)")
    ap.add_argument("--theme", help="measure with another theme")
    args = ap.parse_args()
    U.select_poster(args.poster)
    cfg = U.load_config(theme=args.theme)
    R.register_fonts(cfg["theme"])
    hd = cfg["header"]
    pt = args.pt or cfg["theme"]["autofit"]["min_pt"]
    # the title at its smallest allowed size, as the build would end up with when the page is full
    title_min = int(hd.get("title_pt_min", cfg["theme"]["sizes"]["title_pt_min"]))
    for label, hdr in (("title at its largest allowed size", hd), ("title at title_pt_min", dict(hd, title_pt_max=title_min))):
        lay = R.Layout(dict(cfg, header=hdr), pt)
        print(f"== {U.POSTER_ID}: {label}")
        print("\n".join(lay.measure_lines()))
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
