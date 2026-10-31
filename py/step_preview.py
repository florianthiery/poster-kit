"""Rasterise dist/poster.pdf to a small PNG so the layout can be checked at a glance."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import poster_utils as U  # noqa: E402

PREVIEW_WIDTH_PX = 1400


def main() -> int:
    args = U.parse_args(__doc__)
    if not U.PDF_PATH.is_file():
        print("ERROR: dist/poster.pdf not found; run the render step first")
        return 1
    import pypdfium2 as pdfium

    pdf = pdfium.PdfDocument(str(U.PDF_PATH))
    page = pdf[0]
    width_pt = page.get_width()
    image = page.render(scale=PREVIEW_WIDTH_PX / width_pt).to_pil().convert("RGB")
    image.save(U.PREVIEW_PATH, format="PNG")
    print(f"wrote {U.PREVIEW_PATH.relative_to(U.ROOT)} ({image.width} x {image.height} px)")
    return U.finish(args.strict)


if __name__ == "__main__":
    sys.exit(main())
