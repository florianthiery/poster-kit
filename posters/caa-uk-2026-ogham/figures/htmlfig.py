"""Render a small HTML snippet to a PNG at print size (Chromium via Playwright).

The page is laid out in millimetres, so a font-size of 30pt in the CSS is 30pt on the printed poster when the
figure is placed at its natural width. The theme fonts are loaded from fonts/ with @font-face.
"""
import os, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright
from common import *

DPI = 200
FONTS = f"""
@font-face {{ font-family: Barlow; font-weight: 400; src: url('file://{ROOT}/fonts/barlow/Barlow-Regular.ttf'); }}
@font-face {{ font-family: Barlow; font-weight: 700; src: url('file://{ROOT}/fonts/barlow/Barlow-Bold.ttf'); }}
@font-face {{ font-family: BarlowSC; font-weight: 700; src: url('file://{ROOT}/fonts/barlow/BarlowSemiCondensed-Bold.ttf'); }}
@font-face {{ font-family: Ogham; src: url('file://{ROOT}/fonts/noto-sans-ogham/NotoSansOgham-Regular.ttf'); }}
:root {{ --deep:{DEEP}; --blue:{BLUE}; --ink:{INK}; --muted:{MUTED}; --sky:{SKY}; --card:{CARD}; --tint:{TINT};
        --line:{LINE}; --orange:{ORANGE}; --otint:{ORANGE_TINT}; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: Barlow, sans-serif; color: var(--ink); background: #fff; }}
"""

def render(body_html, width_mm, out, css=""):
    html = f"<html><head><meta charset='utf-8'><style>{FONTS}{css}</style></head><body>" \
           f"<div id='fig' style='width:{width_mm}mm;display:inline-block'>{body_html}</div></body></html>"
    px = width_mm * 96 / 25.4
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": int(px) + 40, "height": 800}, device_scale_factor=DPI / 96)
        tmp = Path(tempfile.gettempdir()) / f"fig-{os.getpid()}.html"
        tmp.write_text(html, encoding="utf-8")
        pg.goto(f"file://{tmp}")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(300)
        pg.locator("#fig").screenshot(path=str(out))
        b.close()
    return out
