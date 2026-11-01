"""Map of the corpus: every findspot with a coordinate, doubtful and lost records set apart, five stones named.

Reads the crosswalk's out/places.geojson (CRWALK env var, default ../../../../tei--epidoc-crosswalk/out/places.geojson)
and Natural Earth land polygons (NE_LAND env var). The record status is taken from the series letter of the
identifier, exactly as tei--epidoc-crosswalk does (X doubtful, L lost, otherwise numbered).
"""
import json, os, sys
from pathlib import Path
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import numpy as np
from common import *

CW = Path(os.environ.get("CRWALK", "/tmp/w/new/cw/out/places.geojson"))
LAND = Path(os.environ.get("NE_LAND", "/tmp/w/geo/ne_10m_land.geojson"))
W_MM, H_MM = 150, 192
X0, X1, Y0, Y1 = -11.0, 2.2, 49.6, 59.5
NAMED = {"I-COR-030": ("Garranes", (-1.2, 0.0)), "S-MOR-001": ("Dyke", (0, 0)),
         "S-BUT-001": ("Blackwaterfoot 1", (0, 0)),
         "S-ARL-001": ("Gigha 1", (0, 0))}

def status(key):
    last = key.split("-")[-1]
    return "doubtful" if last.startswith("X") else "lost" if last.startswith("L") else "numbered"

def polys():
    for f in json.load(open(LAND))["features"]:
        g = f["geometry"]
        for poly in (g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]):
            ring = np.array(poly[0])
            if ring[:, 0].max() < X0 - 1 or ring[:, 0].min() > X1 + 1 or ring[:, 1].max() < Y0 - 1 or ring[:, 1].min() > Y1 + 1:
                continue
            yield ring

def main(out):
    feats = json.load(open(CW))["features"]
    pts = {"numbered": [], "doubtful": [], "lost": []}
    named = {}
    for f in feats:
        k = f["properties"]["stone_key"]; x, y = f["geometry"]["coordinates"]
        pts[status(k)].append((x, y))
        if k in NAMED: named[k] = (x, y)
    fig = plt.figure(figsize=(W_MM * MM, H_MM * MM), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(X0, X1); ax.set_ylim(Y0, Y1)
    ax.set_aspect(1 / np.cos(np.radians(55.3)))
    ax.axis("off")
    ax.add_collection(PatchCollection([Polygon(r, closed=True) for r in polys()], facecolor=CARD, edgecolor=LINE, linewidth=0.8))
    s = 16
    ax.scatter(*zip(*pts["numbered"]), s=s, c=DEEP, alpha=0.55, linewidths=0, zorder=3)
    ax.scatter(*zip(*pts["lost"]), s=s * 3.2, facecolors="white", edgecolors=INK, linewidths=1.6, zorder=4)
    ax.scatter(*zip(*pts["doubtful"]), s=s * 3.2, c=ORANGE, edgecolors="white", linewidths=0.8, zorder=5)
    # the five stones: ring, label, leader line from the label edge nearest to the point
    for k, (name, _) in NAMED.items():
        x, y = named[k]
        ax.scatter([x], [y], s=s * 11, facecolors="none", edgecolors=INK, linewidths=2.2, zorder=6)
    labels = {"I-COR-030": (-10.9, 52.7, "left"), "S-MOR-001": (2.0, 58.9, "right"),
              "S-BUT-001": (-10.9, 56.6, "left"), "S-ARL-001": (-10.9, 55.0, "left")}
    fig.canvas.draw()
    inv = ax.transData.inverted()
    for k, (tx, ty, ha) in labels.items():
        x, y = named[k]
        t = ax.text(tx, ty, NAMED[k][0], fontsize=22, fontweight="bold", color=INK, ha=ha, va="center", zorder=7,
                    bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=INK, lw=1.2))
        fig.canvas.draw()
        bb = t.get_bbox_patch().get_window_extent()
        (bx0, by0), (bx1, by1) = inv.transform((bb.x0, bb.y0)), inv.transform((bb.x1, bb.y1))
        sx = bx1 if ha == "left" else bx0
        ax.plot([x, sx], [y, (by0 + by1) / 2], color=INK, lw=1.2, zorder=6)
    # legend in the sea south-west of Cornwall
    lx, ly = -10.9, 50.7
    rows = [("numbered", pts["numbered"], dict(c=DEEP, alpha=0.55, s=s * 3.2, linewidths=0)),
            ("doubtful (X)", pts["doubtful"], dict(c=ORANGE, edgecolors="white", linewidths=0.8, s=s * 3.2)),
            ("lost (L)", pts["lost"], dict(facecolors="white", edgecolors=INK, linewidths=1.6, s=s * 3.2))]
    for i, (lab, p, kw) in enumerate(rows):
        yy = ly - i * 0.36
        ax.scatter([lx + 0.15], [yy], zorder=8, **kw)
        ax.text(lx + 0.45, yy, f"{len(p)} {lab}", fontsize=22, color=INK, va="center", zorder=8)
    fig.savefig(out, dpi=200, facecolor="white")
    n = {k: len(v) for k, v in pts.items()}
    print(out, n, sum(n.values()), "named:", sorted(named))
    return n

if __name__ == "__main__":
    main(IMG / "map-corpus.png")
