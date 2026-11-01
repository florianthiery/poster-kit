"""Gigha 1 (CIIC 506) worked through: the five readings with their weights (img/gigha-readings.png), the way one
reading travels from TEI to CIDOC CRM to a weighted statement (img/gigha-graph.png), and what the AMT engine derives
from the axioms (img/gigha-reasoning.png). Weights are read from the graphs of tei--epidoc-amt (AMT env var)."""
import os
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS
from htmlfig import render
from markup import edition_html
from common import *

AMT_DIR = Path(os.environ.get("AMT", "/tmp/w/new/amt"))
D = Namespace("http://data.ogham.link/amt/"); AMTV = Namespace("http://academic-meta-tool.xyz/vocab#")
OG = Namespace("http://ontology.ogham.link/"); FW = Namespace("http://w3id.org/fw_ontology/")
PROV = Namespace("http://www.w3.org/ns/prov#")

def readings(ttl):
    g = Graph(); g.parse(str(ttl))
    rows = []
    for st in g.subjects(RDF.predicate, OG.hasReading):
        r = g.value(st, RDF.object); ag = g.value(r, PROV.wasAttributedTo)
        rows.append(dict(w=float(g.value(st, AMTV.weight)), type=str(g.value(st, FW.hasType)).rsplit("/", 1)[-1],
                         reading=str(g.value(r, RDFS.label)), editor=str(g.value(ag, RDFS.label)), key=str(r).rsplit("_", 1)[-1]))
    return sorted(rows, key=lambda x: (-x["w"], x["editor"]))

CSS = """
.small { font-size: 24pt; color: var(--muted); }
.rows > div { display: flex; align-items: center; gap: 5mm; height: 17mm; }
.ed { width: 84mm; font-weight: 700; font-size: 26pt; color: var(--ink); white-space: nowrap; }
.rd { width: 104mm; font-family: BarlowSC, Barlow; font-weight: 700; font-size: 26pt; color: var(--deep); white-space: nowrap; letter-spacing: .02em; }
.bw { flex: 1; display: flex; align-items: center; }
.b { height: 11mm; border-radius: 1.5mm; display: flex; align-items: center; justify-content: flex-end; padding-right: 2mm; font-weight: 700; font-size: 24pt; }
.Vagueness { background: var(--sky); color: var(--ink); } .Uncertainty { background: var(--blue); color: #fff; } .FuzzinessWobbliness { background: var(--deep); color: #fff; }
.unc { color: var(--orange); text-decoration: underline dotted 2px; text-underline-offset: .18em; }
.gap { display: inline-block; width: .9em; height: .62em; border: 2.5px dashed var(--orange); border-radius: 3px; margin: 0 .12em; vertical-align: -.02em; }
.chain { display: flex; align-items: center; }
.node { background: var(--card); border: 1.2mm solid var(--deep); border-radius: 3mm; padding: 2mm 3mm; text-align: center; flex: none; width: 62mm; }
.node b { display: block; font-family: BarlowSC; font-size: 27pt; color: var(--deep); line-height: 1.08; }
.node span { font-size: 24pt; color: var(--muted); line-height: 1.1; }
.link { flex: 1; display: flex; flex-direction: column; align-items: center; min-width: 0; }
.link em { white-space: nowrap; font-style: normal; font-size: 24pt; color: var(--ink); line-height: 1.05; text-align: center; }
.link i { display: block; width: 100%; height: 0; border-top: 1.2mm solid var(--ink); position: relative; margin-top: 1mm; }
.link i::after { content: ''; position: absolute; right: -1mm; top: -2.6mm; border: 2.2mm solid transparent; border-left: 3.6mm solid var(--ink); border-right: 0; }
.link.der i { border-top: 1.2mm dashed var(--blue); } .link.der i::after { border-left-color: var(--blue); }
.layer { font-size: 24pt; font-weight: 700; color: var(--blue); letter-spacing: .03em; margin-bottom: 1.5mm; }
.stmt { border: 1.2mm solid var(--blue); background: #fff; border-radius: 3mm; padding: 2.5mm 4mm; }
.stmt .big { font-family: BarlowSC; font-weight: 700; font-size: 34pt; color: var(--deep); }
.derived { border: 1.2mm dashed var(--blue); background: #fff; border-radius: 3mm; padding: 2mm 3mm; text-align: center; }
.derived b { display: block; font-family: BarlowSC; font-size: 27pt; color: var(--blue); }
.badge { position: absolute; left: 3mm; top: 3mm; width: 14mm; height: 14mm; border-radius: 50%; background: var(--deep); color: #fff;
         font-family: BarlowSC; font-weight: 700; font-size: 34pt; display: flex; align-items: center; justify-content: center; border: 1.2mm solid #fff; }
.ph { position: relative; width: 63mm; height: 84mm; border-radius: 3mm; overflow: hidden; }
.ph img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.ax { display: flex; gap: 5mm; margin-top: 5mm; }
.ax > div { flex: 1; background: #fff; border: 1mm solid var(--line); border-radius: 3mm; padding: 2mm 4mm; font-size: 22pt; line-height: 1.15; color: var(--ink); }
.ax b { display: block; font-family: BarlowSC; font-size: 22pt; color: var(--deep); }
.tbl td { padding: 0 4mm 0 0; font-size: 25pt; height: 11mm; } .tbl td.n { font-family: BarlowSC; font-weight: 700; color: var(--blue); text-align: right; }
"""

def readings_fig(rows):
    mx = max(r["w"] for r in rows)
    out = []
    for r in rows:
        rd = edition_html(AMT_DIR / "data" / "S-ARL-001.xml", "transliteration") if r["key"] == "KF" else r["reading"]
        out.append(f"<div><div class='ed'>{r['editor']}</div><div class='rd'>{rd}</div>"
                   f"<div class='bw'><div class='b {r['type']}' style='width:{r['w'] / mx * 100:.1f}%'>{r['w']:.4f}</div></div></div>")
    head = "<div class='layer' style='margin-bottom:2mm'>Stone 4: Gigha 1, CIIC 506. Five editors, five readings</div>"
    render(f"{head}<div class='rows'>{''.join(out)}</div>", 292, IMG / "gigha-readings.png", CSS)

def graph_fig(rows):
    kf = next(r for r in rows if r["key"] == "KF")
    html = f"""
<div class='layer'>CIDOC CRM + CRMtex (axis 1)</div>
<div class='chain'>
  <div class='node'><b>Gigha 1</b><span>E22 object</span></div>
  <div class='link'><em>carries</em><i></i></div>
  <div class='node'><b>Inscription</b><span>CRMtex TX1</span></div>
  <div class='link'><em>identified as</em><i></i></div>
  <div class='node'><b>Reading</b><span>CRMtex TX7</span></div>
  <div class='link'><em>attributed to</em><i></i></div>
  <div class='node'><b>Editor KF</b><span>E21 · PROV-O</span></div>
</div>
<div class='layer' style='margin-top:14mm'>Academic Meta Tool (axis 2)</div>
<div class='stmt'><span class='big'>Gigha 1 hasReading [---]MAQ[---]COGIN[---]</span><br>
 <span style='font-size:27pt'>weight <b>{kf['w']:.4f}</b> · type <b>fuzziness + wobbliness</b></span></div>"""
    render(html, 392, IMG / "gigha-graph.png", CSS)

def reasoning_fig(rows):
    stone = rows[0]
    kf = next(r for r in rows if r["key"] == "KF")
    left = f"""
<div class='layer'>Axioms: what the engine can derive</div>
<svg viewBox='-1 -1 269 86' width='267mm' height='84mm' xmlns='http://www.w3.org/2000/svg' style='font-family:Barlow,sans-serif'>
 <defs>
  <marker id='a' markerWidth='6' markerHeight='6' refX='5' refY='3' orient='auto'><path d='M0,0 L6,3 L0,6 z' fill='#12324A'/></marker>
  <marker id='d' markerWidth='6' markerHeight='6' refX='5' refY='3' orient='auto'><path d='M0,0 L6,3 L0,6 z' fill='#1998D8'/></marker>
 </defs>
 <g stroke='#0B4F7A' stroke-width='1.2'>
  <rect x='0' y='2' width='88' height='22' rx='4' fill='#0B4F7A'/>
  <rect x='0' y='40' width='88' height='22' rx='4' fill='#0B4F7A'/>
  <rect x='112' y='20' width='62' height='24' rx='4' fill='#0B4F7A'/>
  <rect x='200' y='0' width='65' height='22' rx='4' fill='#0B4F7A'/>
  <rect x='200' y='56' width='65' height='24' rx='4' fill='#fff' stroke='#1998D8' stroke-dasharray='3 2'/>
 </g>
 <g fill='#fff' text-anchor='middle' font-weight='700' font-size='8.4'>
  <text x='44' y='13.5'>hasEditionReading</text><text x='44' y='51.5'>hasHistoricalReading</text>
  <text x='143' y='31.5'>hasReading</text><text x='233.5' y='11.5'>attributedTo</text>
 </g>
 <g fill='#fff' text-anchor='middle' font-size='6'>
  <text x='44' y='20.5'>edition of the OG(H)AM team</text><text x='44' y='58.5'>apparatus, earlier editors</text>
  <text x='143' y='39'>stone to reading</text><text x='233.5' y='18.5'>reading to editor, weight 1</text>
 </g>
 <text x='233.5' y='66.5' text-anchor='middle' font-weight='700' font-size='8.4' fill='#0B4F7A'>readByEditor</text>
 <text x='233.5' y='74' text-anchor='middle' font-size='6' fill='#0B4F7A'>derived, never asserted</text>
 <g stroke='#12324A' stroke-width='1.2' fill='none'>
  <path d='M89,13 L110,28' marker-end='url(#a)'/><path d='M89,51 L110,36' marker-end='url(#a)'/>
  <path d='M176,26 L198,13' marker-end='url(#a)'/>
 </g>
 <g stroke='#1998D8' stroke-width='1.2' fill='none' stroke-dasharray='3 2'>
  <path d='M176,38 L198,62' marker-end='url(#d)'/><path d='M233.5,24 L233.5,54' marker-end='url(#d)'/>
 </g>
 <g font-size='6.4' fill='#12324A' text-anchor='middle'>
  <text x='99' y='15'>is a</text><text x='101' y='58'>is a</text><text x='192' y='26' >then</text><text x='177' y='60' fill='#1998D8'>gives</text>
 </g>
 <text x='44' y='71' text-anchor='middle' font-size='6' fill='#47627A'>disjoint: no reading is both</text>
</svg>"""
    byed = "".join(f"<tr><td>{r['editor']}</td><td class='n'>{r['w']:.4f}</td></tr>" for r in rows)
    right = f"<div class='layer'>Derived for Gigha 1</div><table class='tbl'>{byed}</table>"
    render(f"<div style='display:flex;gap:9mm;align-items:center'><div style='flex:1'>{left}</div><div style='width:116mm'>{right}</div></div>", 392,
           IMG / "gigha-reasoning.png", CSS)

def photo_fig():
    render(f"<div class='ph'><img src='file://{IMG}/photos/gigha-1.jpg'><div class='badge'>4</div></div>", 63, IMG / "gigha-photo.png", CSS)

if __name__ == "__main__":
    rows = readings(AMT_DIR / "out" / "gigha1.amt.ttl")
    for r in rows: print(r["editor"], r["w"], r["type"])
    readings_fig(rows); graph_fig(rows); reasoning_fig(rows); photo_fig()
