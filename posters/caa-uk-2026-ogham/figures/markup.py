"""Turn an EpiDoc edition <div> into HTML that shows the doubt markup, and read the weights of a stone from its AMT graph."""
from lxml import etree
from rdflib import Graph, Namespace, RDF
import os
from pathlib import Path

NS = {"t": "http://www.tei-c.org/ns/1.0"}
T = "{http://www.tei-c.org/ns/1.0}"

def walk(el, first_lb=[True]):
    out = []
    if el.text: out.append(el.text)
    for c in el:
        tag = etree.QName(c).localname if isinstance(c.tag, str) else None
        if tag is None:                      # comment
            pass
        elif tag == "lb":
            out.append("" if first_lb[0] else "<br>"); first_lb[0] = False
        elif tag == "gap":
            out.append("<span class='gap'></span>")
        elif tag == "unclear":
            out.append(f"<span class='unc'>{walk(c, first_lb)}</span>")
        elif tag == "supplied":
            out.append(f"<span class='sup'><span class='br'>[</span>{walk(c, first_lb)}<span class='br'>]</span></span>")
        elif tag == "choice":
            alts = "".join(f"<span>{''.join(a.itertext()).strip()}</span>" for a in c)
            out.append(f"<span class='ch'>{alts}</span>")
        elif tag == "g":
            out.append("<span class='glyph'>◇</span>")
        elif tag == "ab" and c.get("type") == "list":
            pass
        else:
            out.append(walk(c, first_lb))
        if c.tail: out.append(c.tail)
    return "".join(out)

def edition_html(xml_path, subtype, index=0):
    root = etree.parse(str(xml_path)).getroot()
    div = root.xpath(f"//t:div[@type='edition'][@subtype='{subtype}']", namespaces=NS)[index]
    return " ".join(walk(div, [True]).split(" ")).strip()

def weights(ttl_path, subject_suffix=None):
    """[(weight, fw type), ...] of the hasReading statements (or hasInscriptionReading of one inscription), largest first."""
    g = Graph(); g.parse(str(ttl_path))
    AMT = Namespace("http://academic-meta-tool.xyz/vocab#"); OG = Namespace("http://ontology.ogham.link/")
    FW = Namespace("http://w3id.org/fw_ontology/"); RDFN = RDF
    rows = []
    for s in g.subjects(RDFN.predicate, OG.hasInscriptionReading if subject_suffix else OG.hasReading):
        subj = g.value(s, RDFN.subject)
        if subject_suffix and not str(subj).endswith(subject_suffix): continue
        w = float(g.value(s, AMT.weight)); t = g.value(s, FW.hasType)
        rows.append((w, str(t).rsplit("/", 1)[-1] if t else "none"))
    return sorted(rows, reverse=True)
