"""Cut static Libre Franklin instances from the Google Fonts variable fonts.

Why: reportlab cannot choose a weight on a variable font, and Google Fonts ships
Libre Franklin only as `LibreFranklin[wght].ttf` (+ Italic). This is a one-off
helper, not part of the build; its output is committed to fonts/libre-franklin/.

    pip install fonttools
    python tools/make_static_librefranklin.py <dir-with-the-two-variable-fonts> <output-dir>

The input directory must contain `LibreFranklin[wght].ttf` and
`LibreFranklin-Italic[wght].ttf` (download from
https://github.com/google/fonts/tree/main/ofl/librefranklin).
"""
from __future__ import annotations

import sys
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

JOBS = [
    ("LibreFranklin[wght].ttf", "LibreFranklin-Regular.ttf", 400),
    ("LibreFranklin[wght].ttf", "LibreFranklin-Bold.ttf", 700),
    ("LibreFranklin-Italic[wght].ttf", "LibreFranklin-Italic.ttf", 400),
    ("LibreFranklin-Italic[wght].ttf", "LibreFranklin-BoldItalic.ttf", 700),
]


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    src_dir, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)
    for src, out, weight in JOBS:
        font = TTFont(src_dir / src, recalcTimestamp=False)
        inst = instancer.instantiateVariableFont(font, {"wght": weight}, inplace=False, updateFontNames=True)
        inst.save(out_dir / out)
        print(f"wrote {out_dir / out} (wght={weight})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
