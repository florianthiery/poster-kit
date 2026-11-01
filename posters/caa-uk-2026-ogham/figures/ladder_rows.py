"""The ladder of doubt: one row per stone. Photograph, inscription in Ogham and transliteration with the editors'
doubt markup, the weights of its readings as one bar, and a short statement of the problem. One PNG per row
(img/row-<stone>.png) plus a legend (img/row-legend.png). Reads tei--epidoc-amt (AMT env var) and img/photos/."""
import os
from pathlib import Path
from lxml import etree
from htmlfig import render, DPI
from markup import edition_html, weights, NS
from common import *

AMT = Path(os.environ.get("AMT", "/tmp/w/new/amt"))
W_MM = 785
PHOTO_W, TEXT_W = 92, 232
ROWS = [
    dict(name="garranes", n=1, file="I-COR-030", base="I-COR-030" and "garranes", suffix=None, title="Garranes", ref="CIIC 81",
         fs=1.5, pos="50% 40%", text="Three restored letters, otherwise secure. One reading: weight 1.0."),
    dict(name="dyke", n=2, file="S-MOR-001", base="dyke", suffix=None, title="Dyke", ref="no CIIC number",
         fs=1.0, pos="50% 20%", text="12 unclear letters, 9 gaps, 3 pairs of alternatives. Still one reading: weight 1.0."),
    dict(name="blackwaterfoot-1", n=3, file="S-BUT-001", base="blackwaterfoot-1", suffix="_1", title="Blackwaterfoot 1", ref="inscription 1",
         fs=1.6, pos="50% 50%", text="Four competing readings, three with no editor named. The weight is a share between them."),
]
CSS = """
.row { display: flex; gap: 7mm; align-items: stretch; height: 58mm; }
.ph { position: relative; width: %dmm; border-radius: 3mm; overflow: hidden; background: var(--tint); flex: none; }
.ph img { position: absolute; inset: 0; width: 100%%; height: 100%%; object-fit: cover; }
.badge { position: absolute; left: 3mm; top: 3mm; width: 14mm; height: 14mm; border-radius: 50%%; background: var(--deep); color: #fff;
         font-family: BarlowSC; font-weight: 700; font-size: 34pt; display: flex; align-items: center; justify-content: center; border: 1.2mm solid #fff; }
.deg { font-family: BarlowSC; font-weight: 700; font-size: 22pt; letter-spacing: .08em; text-transform: uppercase; color: var(--orange); }
.mid { flex: 1; background: var(--card); border-radius: 3mm; padding: 3mm 7mm 4mm; display: flex; flex-direction: column; }
.two { display: flex; gap: 9mm; flex: 1; align-items: center; }
.two > div { flex: 1; }
.og { font-family: Ogham, sans-serif; font-size: calc(22pt * var(--fs)); line-height: 1.5; color: var(--deep); }
.tr { font-family: BarlowSC, Barlow, sans-serif; font-weight: 700; font-size: calc(25pt * var(--fs)); line-height: 1.28; color: var(--deep); letter-spacing: .02em; }
.unc { color: var(--orange); text-decoration: underline dotted 2px; text-underline-offset: .18em; }
.sup, .sup .br { color: var(--muted); }
.gap { display: inline-block; width: .9em; height: .62em; border: 2.5px dashed var(--orange); border-radius: 3px; margin: 0 .12em; vertical-align: -.02em; }
.og .gap { width: 1.1em; height: .7em; }
.ch { display: inline-flex; flex-direction: column; vertical-align: middle; font-size: .55em; line-height: 1.02; color: var(--orange); border-left: 2px solid var(--orange); border-right: 2px solid var(--orange); padding: 0 .12em; margin: 0 .08em; }
.og .ch { font-size: .62em; }
.glyph { color: var(--orange); font-family: Barlow; }
.bar { display: flex; height: 11mm; margin-top: 3mm; border-radius: 2mm; overflow: hidden; gap: 1.2mm; }
.seg { display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 22pt; }
.seg.none { background: var(--tint); color: var(--ink); } .seg.Vagueness { background: var(--sky); color: var(--ink); }
.seg.Uncertainty { background: var(--blue); color: #fff; } .seg.FuzzinessWobbliness { background: var(--deep); color: #fff; }
.txt { width: %dmm; flex: none; padding: 2mm 0; display: flex; flex-direction: column; justify-content: center; }
.txt h3 { font-family: BarlowSC; font-weight: 700; font-size: 32pt; color: var(--deep); line-height: 1.05; }
.txt .ref { font-size: 24pt; color: var(--muted); margin: 0 0 1.5mm; }
.txt p { font-size: 25pt; line-height: 1.17; }
.leg { display: flex; flex-wrap: wrap; gap: 3mm 9mm; align-items: center; font-size: 24pt; color: var(--ink); }
.leg .sw { display: inline-block; width: 13mm; height: 7mm; border-radius: 1.5mm; vertical-align: middle; margin-right: 2.5mm; }
.leg .t { font-family: BarlowSC, Barlow; font-weight: 700; font-size: 26pt; color: var(--deep); margin-right: 2mm; }
""" % (PHOTO_W, TEXT_W)

def row(r):
    xml = AMT / "data" / f"{r['file']}.xml"
    og = edition_html(xml, "ogham"); tr = edition_html(xml, "transliteration")
    ws = weights(AMT / "out" / f"{r['base']}.amt.ttl", r["suffix"])
    segs = "".join(f"<div class='seg {t}' style='flex:{w}'>{w:.2f}</div>" for w, t in ws)
    html = (f"<div class='row' style='--fs:{r['fs']}'><div class='ph'><img src='file://{IMG}/photos/{r['name']}.jpg' style='object-position:{r['pos']}'>"
            f"<div class='badge'>{r['n']}</div></div>"
            f"<div class='mid'><div class='two'><div class='og'>{og}</div><div class='tr'>{tr}</div></div><div class='bar'>{segs}</div></div>"
            f"<div class='txt'><div class='deg'>Degree {r['n']}</div><h3>{r['title']}</h3><div class='ref'>{r['ref']}</div><p>{r['text']}</p></div></div>")
    render(html, W_MM, IMG / f"row-{r['name']}.png", CSS)
    print(r["name"], [f"{w:.4f}" for w, _ in ws])

def legend():
    html = ("<div class='leg'>"
            "<span><span class='tr'>[A]</span> <span style='color:var(--muted)'>restored by the editor</span></span>"
            "<span><span class='tr unc'>A</span> <span>unclear</span></span>"
            "<span><span class='gap' style='width:1.6em;height:.8em;vertical-align:middle'></span> <span>gap, lost</span></span>"
            "<span><span class='ch' style='font-size:.9em'><span>M</span><span>A</span></span> <span>alternative letters</span></span>"
            "<span style='margin-left:6mm'><span class='sw' style='background:var(--sky)'></span>vague (certainty below 1)</span>"
            "<span><span class='sw' style='background:var(--blue)'></span>uncertain (readers disagree)</span>"
            "<span><span class='sw' style='background:var(--deep)'></span>both</span></div>")
    render(html, W_MM, IMG / "row-legend.png", CSS)

def composite():
    """All rows and the legend in one image, so the poster adds no gaps between them."""
    from PIL import Image
    names = ["row-legend"] + [f"row-{r['name']}" for r in ROWS]
    ims = [Image.open(IMG / f"{n}.png") for n in names]
    gap = int(2.5 * DPI / 25.4)
    sheet = Image.new("RGB", (ims[0].width, sum(i.height for i in ims) + gap * (len(ims) - 1)), "white")
    y = 0
    for i in ims:
        sheet.paste(i, (0, y)); y += i.height + gap
    sheet.save(IMG / "ladder-all.png")
    print("ladder-all.png", sheet.size)

if __name__ == "__main__":
    for r in ROWS: row(r)
    legend()
    composite()
