"""Draw dist/poster.pdf from poster.yaml and content/*.md.

Layout model
------------
page   = header band (full bleed) + body bands
band   = a row of columns; its height is the tallest column unless fixed
column = a vertical stack of cards (blocks)
card   = optional title bar + one or more parts (text, table, flow, image,
         stats, qr, logos)

Colours, fonts, shapes and card styles come from the theme (themes/<id>/theme.yaml,
see py/theme.py); the engine only knows semantic tokens such as ``primary`` or ``card``.

The base text size is fitted automatically: the engine tries the largest size
from theme.autofit down to its minimum and keeps the first one for which the
whole body fits on the page. Change a text, re-run, and the type rescales.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parent))
import poster_utils as U  # noqa: E402
import theme as T  # noqa: E402
from step_validate import part_list  # noqa: E402

from reportlab.graphics import renderPDF  # noqa: E402
from reportlab.graphics.barcode.qr import QrCodeWidget  # noqa: E402
from reportlab.graphics.shapes import Drawing  # noqa: E402
from reportlab.lib.colors import HexColor  # noqa: E402
from reportlab.lib.enums import TA_CENTER, TA_LEFT  # noqa: E402
from reportlab.lib.pagesizes import A0, A1, A2, A3, A4  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.lib.utils import ImageReader  # noqa: E402
from reportlab.pdfbase import pdfmetrics  # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402
from reportlab.platypus import Paragraph, Table, TableStyle  # noqa: E402

SIZES = {"A0": A0, "A1": A1, "A2": A2, "A3": A3, "A4": A4}


# --------------------------------------------------------------------------
# Fonts and inline markup
# --------------------------------------------------------------------------
def register_fonts(theme: dict) -> None:
    files = theme["fonts"]
    for name, key in (
        ("PosterBody", "regular"),
        ("PosterBold", "bold"),
        ("PosterItalic", "italic"),
        ("PosterBoldItalic", "bold_italic"),
        ("PosterHead", "heading"),
        ("PosterMono", "mono"),
    ):
        pdfmetrics.registerFont(TTFont(name, str(files[key])))
    pdfmetrics.registerFontFamily(
        "PosterBody", normal="PosterBody", bold="PosterBold",
        italic="PosterItalic", boldItalic="PosterBoldItalic",
    )


_BOLD = re.compile(r"\*\*(.+?)\*\*")
_ITALIC = re.compile(r"(?<![\*\w])\*(?!\*)(.+?)(?<![\*\s])\*(?![\*\w])")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def inline(text: str, link_colour: str) -> str:
    """Small Markdown subset -> reportlab paragraph markup."""
    out = []
    for piece in re.split(r"(`[^`]+`)", text):
        if len(piece) > 1 and piece.startswith("`") and piece.endswith("`"):
            out.append(f'<font face="PosterMono">{escape(piece[1:-1])}</font>')
            continue
        q = escape(piece)
        q = _BOLD.sub(r"<b>\1</b>", q)
        q = _ITALIC.sub(r"<i>\1</i>", q)
        q = _LINK.sub(rf'<a href="\2" color="{link_colour}">\1</a>', q)
        out.append(q.replace("&lt;br&gt;", "<br/>"))     # <br> breaks a line, but not inside `code`
    return "".join(out)


def parse_markdown(src: str) -> list[tuple[str, str]]:
    """Return [(kind, text)] with kind in p | h | li."""
    blocks: list[tuple[str, str]] = []
    para: list[str] = []

    def flush() -> None:
        if para:
            blocks.append(("p", " ".join(para)))
            para.clear()

    for raw in src.splitlines():
        line = raw.rstrip()
        if not line.strip():
            flush()
        elif line.startswith("### "):
            flush()
            blocks.append(("h", line[4:].strip()))
        elif re.match(r"^[-*] ", line):
            flush()
            blocks.append(("li", line[2:].strip()))
        else:
            para.append(line.strip())
    flush()
    return blocks


# --------------------------------------------------------------------------
# Rendering context
# --------------------------------------------------------------------------
class Ctx:
    """Everything an item needs to measure itself at a given base size."""

    def __init__(self, cfg: dict, base_pt: float, report: "Report"):
        self.cfg = cfg
        self.theme = cfg["theme"]
        self.col = {k: HexColor(v) for k, v in self.theme["tokens"].items()}
        self.shape = self.theme["shape"]
        self.scale = self.theme["scale"]
        self.base = base_pt
        self.report = report
        self.pad = self.shape["card_pad_pt"]
        self.item_gap = base_pt * self.shape["item_gap"]
        self.heading_pt = self.theme["sizes"]["heading_pt"]
        self.link = self.theme["tokens"]["link"]
        self.bullet = self.col["primary"]
        # "small" text (labels, legends, captions): scale.small x base, but never below the floor
        self.small = max(base_pt * self.scale["small"], self.theme["sizes"]["min_pt"])

    def accent_name(self, spec: dict) -> str:
        """Card style of a block: an explicit `accent:` wins, then the theme's mapping of `role:`."""
        if spec.get("accent"):
            return spec["accent"]
        return self.theme["roles"].get(spec.get("role"), "primary")

    def accent(self, name: str) -> dict:
        spec = self.theme["accents"][name]
        return {"bar": self.col[spec["bar"]], "text": self.col[spec["text"]],
                "bullet": self.col[spec.get("bullet", spec["bar"])]}

    def style(self, name: str, pt: float, font="PosterBody", colour="ink", align=TA_LEFT,
              lead=None, **kw) -> ParagraphStyle:
        self.report.note_size(pt, name)
        lead = lead or self.scale["leading"]
        return ParagraphStyle(name, fontName=font, fontSize=pt, leading=pt * lead,
                              textColor=self.col[colour], alignment=align, **kw)

    def para(self, text: str, style: ParagraphStyle, width: float, bullet=None) -> Paragraph:
        p = Paragraph(inline(text, self.link), style, bulletText=bullet)
        p.wrap(width, 1e7)
        return p


class Report:
    def __init__(self, min_pt: float):
        self.min_pt = min_pt
        self.sizes: dict[str, float] = {}
        self.lines: list[str] = []

    def note_size(self, pt: float, where: str) -> None:
        self.sizes[where] = min(pt, self.sizes.get(where, pt))


# --------------------------------------------------------------------------
# Items (parts of a card)
# --------------------------------------------------------------------------
class TextItem:
    def __init__(self, spec: dict, ctx: Ctx, width: float):
        self.width = width
        scale = spec.get("scale", 1.0)
        pt = max(ctx.base * scale, ctx.theme["sizes"]["min_pt"])
        src = U.read_text(spec["file"]) if "file" in spec else spec["text"]
        if "TODO" in src:
            U.warn(f"unresolved TODO in {spec.get('file', 'inline text')}")
        body = ctx.style("body", pt)
        bullet = ctx.style("bullet", pt, leftIndent=pt * 1.15, bulletIndent=0,
                           bulletFontName="PosterBold", bulletFontSize=pt * 1.1, bulletColor=ctx.bullet)
        sub = ctx.style("subheading", pt * ctx.scale["subheading"], font="PosterBold", colour="primary")
        self.flow: list[tuple[Paragraph, float, float]] = []
        for kind, text in parse_markdown(src):
            if kind == "li":
                p = ctx.para(text, bullet, width, bullet="•")
                self.flow.append((p, 0, pt * 0.42))
            elif kind == "h":
                p = ctx.para(text, sub, width)
                self.flow.append((p, pt * 0.35, pt * 0.3))
            else:
                p = ctx.para(text, body, width)
                self.flow.append((p, 0, pt * 0.6))
        self.height = sum(b + p.height + a for p, b, a in self.flow) - (self.flow[-1][2] if self.flow else 0)

    def draw(self, c, x: float, y_top: float) -> None:
        y = y_top
        for p, before, after in self.flow:
            y -= before + p.height
            p.drawOn(c, x, y)
            y -= after


class TableItem:
    def __init__(self, spec: dict, ctx: Ctx, width: float):
        self.width = width
        pt = max(ctx.base * spec.get("scale", ctx.scale["table"]), ctx.theme["sizes"]["min_pt"])
        head = ctx.style("table-head", pt, font="PosterBold", colour="on_primary")
        cell = ctx.style("table-cell", pt)
        rows = []
        if spec.get("header"):
            rows.append([ctx.para(h, head, 1e4) for h in spec["header"]])
        for r in spec["rows"]:
            rows.append([Paragraph(inline(str(v), ctx.link), cell) for v in r])
        weights = spec.get("col_widths") or [1] * len(rows[0])
        total = float(sum(weights))
        widths = [width * w / total for w in weights]
        pad = pt * 0.38
        style = [
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), pad), ("RIGHTPADDING", (0, 0), (-1, -1), pad),
            ("TOPPADDING", (0, 0), (-1, -1), pad * 0.8), ("BOTTOMPADDING", (0, 0), (-1, -1), pad * 0.8),
            ("LINEBELOW", (0, 0), (-1, -1), 1.2, ctx.col["line"]),
        ]
        if spec.get("header"):
            style.append(("BACKGROUND", (0, 0), (-1, 0), ctx.col["primary"]))
            first_body = 1
        else:
            first_body = 0
        for i in range(first_body, len(rows)):
            if (i - first_body) % 2 == 1:
                style.append(("BACKGROUND", (0, i), (-1, i), ctx.col["tint"]))
        self.table = Table(rows, colWidths=widths, style=TableStyle(style))
        _, self.height = self.table.wrap(width, 1e7)

    def draw(self, c, x: float, y_top: float) -> None:
        self.table.drawOn(c, x, y_top - self.height)


class FlowItem:
    """A row (or rows) of numbered boxes joined by arrows."""

    def __init__(self, spec: dict, ctx: Ctx, width: float):
        self.ctx, self.width = ctx, width
        steps = spec["steps"]
        self.steps = steps
        n = len(steps)
        self.per_row = spec.get("per_row", n)
        self.arrow = ctx.base * 1.5
        self.row_gap = ctx.base * 1.7
        self.box_w = (width - (self.per_row - 1) * self.arrow) / self.per_row
        pad = ctx.base * 0.55
        self.pad = pad
        inner = self.box_w - 2 * pad
        self.cells = []
        for s in steps:
            status = s.get("status", "done")
            if status not in ctx.theme["status_styles"]:
                raise SystemExit(f"ERROR: flow step '{s.get('label')}' has status '{status}'; "
                                 f"theme '{ctx.theme['id']}' defines: {', '.join(ctx.theme['status_styles'])}")
            fg = ctx.theme["status_styles"][status]["text"]
            lab = ctx.style(f"flow-label-{status}", ctx.base, font="PosterBold", colour=fg, align=TA_CENTER)
            sub = ctx.style(f"flow-sub-{status}", ctx.small, colour=fg, align=TA_CENTER, lead=1.22)
            lp = ctx.para(s["label"], lab, inner)
            sp = ctx.para(s["sub"], sub, inner) if s.get("sub") else None
            self.cells.append((lp, sp))
        self.box_h = max(lp.height + (sp.height + ctx.base * 0.25 if sp else 0) for lp, sp in self.cells) + 2 * pad + ctx.base * 0.5
        self.rows = [list(range(i, min(i + self.per_row, n))) for i in range(0, n, self.per_row)]
        self.legend = None
        if spec.get("legend"):
            self.legend = ctx.para(spec["legend"], ctx.style("legend", ctx.small, colour="muted"), width)
        legend_h = (self.legend.height + ctx.base * 0.6) if self.legend else 0
        self.height = len(self.rows) * self.box_h + (len(self.rows) - 1) * self.row_gap + legend_h

    def _box_xy(self, idx: int, y_top: float):
        r = next(i for i, row in enumerate(self.rows) if idx in row)
        k = self.rows[r].index(idx)
        x = k * (self.box_w + self.arrow)
        y = y_top - r * (self.box_h + self.row_gap) - self.box_h
        return x, y

    def draw(self, c, x0: float, y_top: float) -> None:
        ctx = self.ctx
        sh = ctx.shape
        conn = ctx.col["connector"]
        for idx, (lp, sp) in enumerate(self.cells):
            style = ctx.theme["status_styles"][self.steps[idx].get("status", "done")]
            bx, by = self._box_xy(idx, y_top)
            bx += x0
            c.saveState()
            c.setLineWidth(sh["box_line"])
            c.setFillColor(ctx.col[style["fill"]]); c.setStrokeColor(ctx.col[style["stroke"]])
            if style.get("dash"):
                c.setDash(sh["dash"], 0)
            c.roundRect(bx, by, self.box_w, self.box_h, sh["box_radius"], stroke=1, fill=1)
            c.restoreState()
            content_h = lp.height + (sp.height + ctx.base * 0.25 if sp else 0)
            ty = by + self.box_h - (self.box_h - content_h) / 2
            lp.drawOn(c, bx + self.pad, ty - lp.height)
            if sp:
                sp.drawOn(c, bx + self.pad, ty - lp.height - ctx.base * 0.25 - sp.height)
            # step number badge
            r = ctx.base * 0.52
            c.saveState()
            c.setFillColor(conn); c.setStrokeColor(ctx.col["paper"]); c.setLineWidth(sh["badge_line"])
            c.circle(bx + r * 0.4, by + self.box_h - r * 0.4, r, stroke=1, fill=1)
            c.setFillColor(ctx.col["on_connector"]); c.setFont("PosterBold", r * 1.15)
            c.drawCentredString(bx + r * 0.4, by + self.box_h - r * 0.4 - r * 0.4, str(idx + 1))
            c.restoreState()
        # arrows within rows, elbow connectors between rows
        c.saveState()
        c.setStrokeColor(conn); c.setFillColor(conn); c.setLineWidth(sh["arrow_line"])
        for r, row in enumerate(self.rows):
            for a, b in zip(row, row[1:]):
                ax, ay = self._box_xy(a, y_top)
                bx, _ = self._box_xy(b, y_top)
                y = ay + self.box_h / 2
                x1, x2 = x0 + ax + self.box_w + 6, x0 + bx - 6
                c.line(x1, y, x2 - 14, y)
                self._head(c, x2, y, 0)
            if r + 1 < len(self.rows):
                last, first = row[-1], self.rows[r + 1][0]
                lx, ly = self._box_xy(last, y_top)
                fx, fy = self._box_xy(first, y_top)
                xs, ys = x0 + lx + self.box_w / 2, ly - 6
                xe, ye = x0 + fx + self.box_w / 2, fy + self.box_h + 6
                ym = (ys + ye) / 2
                c.line(xs, ys, xs, ym); c.line(xs, ym, xe, ym); c.line(xe, ym, xe, ye + 14)
                self._head(c, xe, ye, -90)
        c.restoreState()
        if self.legend:
            self.legend.drawOn(c, x0, y_top - self.height)

    @staticmethod
    def _head(c, x: float, y: float, angle: float) -> None:
        c.saveState()
        c.translate(x, y); c.rotate(angle)
        p = c.beginPath()
        p.moveTo(0, 0); p.lineTo(-26, 15); p.lineTo(-26, -15); p.close()
        c.drawPath(p, stroke=0, fill=1)
        c.restoreState()


class StatsItem:
    def __init__(self, spec: dict, ctx: Ctx, width: float):
        self.ctx, self.width = ctx, width
        items = spec["items"]
        n = len(items)
        self.gap = ctx.base * 0.8
        self.tw = (width - (n - 1) * self.gap) / n
        val = ctx.style("stat-value", ctx.base * ctx.scale["stat_value"], font="PosterHead", colour="primary", align=TA_CENTER, lead=1.05)
        lab = ctx.style("stat-label", ctx.small, colour="ink", align=TA_CENTER, lead=1.2)
        self.cells = [(ctx.para(i["value"], val, self.tw), ctx.para(i["label"], lab, self.tw)) for i in items]
        self.height = max(v.height + l.height for v, l in self.cells) + ctx.base * 0.3

    def draw(self, c, x: float, y_top: float) -> None:
        for k, (v, l) in enumerate(self.cells):
            tx = x + k * (self.tw + self.gap)
            v.drawOn(c, tx, y_top - v.height)
            l.drawOn(c, tx, y_top - v.height - l.height)


class QrItem:
    """QR codes in a row; each code has its label centred underneath."""

    def __init__(self, spec: dict, ctx: Ctx, width: float):
        self.ctx, self.width = ctx, width
        self.items = spec["items"]
        n = len(self.items)
        self.size = spec.get("size_mm", 52) * mm
        self.gap = ctx.base * 0.8
        self.iw = (width - (n - 1) * self.gap) / n
        lab = ctx.style("qr-label", ctx.small, align=TA_CENTER, lead=1.2)
        self.labels = [ctx.para(i["label"], lab, self.iw) for i in self.items]
        self.label_gap = ctx.base * 0.35
        self.height = self.size + self.label_gap + max(p.height for p in self.labels)

    def draw(self, c, x: float, y_top: float) -> None:
        for k, (it, lab) in enumerate(zip(self.items, self.labels)):
            ix = x + k * (self.iw + self.gap)
            qx = ix + (self.iw - self.size) / 2
            widget = QrCodeWidget(it["url"], barLevel="M")
            x0, y0, x1, y1 = widget.getBounds()
            d = Drawing(self.size, self.size,
                        transform=[self.size / (x1 - x0), 0, 0, self.size / (y1 - y0), 0, 0])
            d.add(widget)
            renderPDF.draw(d, c, qx, y_top - self.size)
            lab.drawOn(c, ix, y_top - self.size - self.label_gap - lab.height)


class ImageItem:
    def __init__(self, spec: dict, ctx: Ctx, width: float):
        self.ctx, self.width, self.spec = ctx, width, spec
        path = U.ROOT / spec["src"]
        self.path = path
        self.missing = not path.is_file()
        self.draw_w = width
        if self.missing:
            self.draw_h = spec.get("height_mm", 120) * mm
        elif path.suffix.lower() == ".svg":
            from svglib.svglib import svg2rlg
            self.drawing = svg2rlg(str(path))
            self.draw_h = width * self.drawing.height / self.drawing.width
        else:
            self.reader = ImageReader(str(path))
            iw, ih = self.reader.getSize()
            self.draw_h = width * ih / iw
        cap_max = spec.get("max_height_mm")
        if cap_max and self.draw_h > cap_max * mm:
            factor = cap_max * mm / self.draw_h
            self.draw_h *= factor
            self.draw_w *= factor
        self.caption = None
        if spec.get("caption"):
            self.caption = ctx.para(spec["caption"], ctx.style("caption", ctx.small, colour="muted", lead=1.2), width)
        self.height = self.draw_h + ((self.caption.height + ctx.base * 0.4) if self.caption else 0)

    def draw(self, c, x: float, y_top: float) -> None:
        ox = x + (self.width - self.draw_w) / 2
        oy = y_top - self.draw_h
        if self.missing:
            c.saveState()
            c.setFillColor(self.ctx.col["tint"]); c.setStrokeColor(self.ctx.col["line"]); c.setDash([14, 10], 0); c.setLineWidth(4)
            c.rect(ox, oy, self.draw_w, self.draw_h, stroke=1, fill=1)
            c.setFillColor(self.ctx.col["muted"]); c.setFont("PosterBody", self.ctx.small)
            c.drawCentredString(ox + self.draw_w / 2, oy + self.draw_h / 2, f"[image: {self.spec['src']}]")
            c.restoreState()
        elif self.path.suffix.lower() == ".svg":
            sc = self.draw_w / self.drawing.width
            self.drawing.width *= sc; self.drawing.height *= sc; self.drawing.scale(sc, sc)
            renderPDF.draw(self.drawing, c, ox, oy)
        else:
            c.drawImage(self.reader, ox, oy, self.draw_w, self.draw_h, mask="auto")
        if self.caption:
            self.caption.drawOn(c, x, oy - self.ctx.base * 0.4 - self.caption.height)


def draw_logo(c, ctx: Ctx, item: dict, x: float, y: float, w: float, h: float, style: ParagraphStyle) -> None:
    """One logo pill: the image if a file exists, otherwise the name as text."""
    c.saveState()
    c.setFillColor(ctx.col["paper"]); c.setStrokeColor(ctx.col["secondary"]); c.setLineWidth(ctx.shape["logo_line"])
    c.roundRect(x, y, w, h, ctx.shape["logo_radius"], stroke=1, fill=1)
    c.restoreState()
    src = item.get("src")
    if src and (U.ROOT / src).is_file() and src.lower().endswith(".svg"):
        from svglib.svglib import svg2rlg
        d = svg2rlg(str(U.ROOT / src))
        s = min((w - 40) / d.width, (h - 30) / d.height)
        d.width *= s; d.height *= s; d.scale(s, s)
        renderPDF.draw(d, c, x + (w - d.width) / 2, y + (h - d.height) / 2)
    elif src and (U.ROOT / src).is_file():
        reader = ImageReader(str(U.ROOT / src))
        iw, ih = reader.getSize()
        s = min((w - 40) / iw, (h - 30) / ih)
        c.drawImage(reader, x + (w - iw * s) / 2, y + (h - ih * s) / 2, iw * s, ih * s, mask="auto")
    else:
        p = ctx.para(item["name"], style, w - 30)
        p.drawOn(c, x + 15, y + (h - p.height) / 2)


class LogosItem:
    def __init__(self, spec: dict, ctx: Ctx, width: float):
        self.ctx, self.width, self.items = ctx, width, spec["items"]
        n = len(self.items)
        self.gap = ctx.base * 0.8
        self.w = (width - (n - 1) * self.gap) / n
        self.h = spec.get("height_mm", 30) * mm
        self.style = ctx.style("logo", ctx.small, font="PosterBold", colour="primary", align=TA_CENTER, lead=1.15)
        self.height = self.h

    def draw(self, c, x: float, y_top: float) -> None:
        for k, it in enumerate(self.items):
            draw_logo(c, self.ctx, it, x + k * (self.w + self.gap), y_top - self.h, self.w, self.h, self.style)


ITEMS = {"text": TextItem, "table": TableItem, "flow": FlowItem, "image": ImageItem,
         "stats": StatsItem, "qr": QrItem, "logos": LogosItem}


# --------------------------------------------------------------------------
# Card
# --------------------------------------------------------------------------
class Card:
    def __init__(self, bid: str, spec: dict, ctx: Ctx, width: float):
        self.id, self.spec, self.ctx, self.width = bid, spec, ctx, width
        self.accent_name = ctx.accent_name(spec)
        self.accent = ctx.accent(self.accent_name)
        pad = ctx.pad
        inner = width - 2 * pad
        self.framed = spec.get("frame", True)
        self.title = spec.get("title")
        self.head_h = 0.0
        if self.title:
            hs = ctx.style(f"card-heading", ctx.heading_pt, font="PosterHead", lead=1.12)
            hs.textColor = self.accent["text"] if self.framed else ctx.col["primary"]
            self.head = ctx.para(self.title, hs, inner)
            self.head_h = self.head.height + pad * 1.1
        ctx.bullet = self.accent["bullet"]
        self.items = [ITEMS[p["type"]](p, ctx, inner) for p in part_list(spec)]
        self.content_h = sum(i.height for i in self.items) + ctx.item_gap * (len(self.items) - 1)
        self.height = self.head_h + 2 * pad + self.content_h

    def draw(self, c, x: float, y_top: float, h: float) -> None:
        ctx, pad = self.ctx, self.ctx.pad
        if self.framed:
            c.saveState()
            path = c.beginPath()
            path.roundRect(x, y_top - h, self.width, h, ctx.shape["card_radius"])
            c.clipPath(path, stroke=0, fill=0)
            c.setFillColor(ctx.col["card"]); c.rect(x, y_top - h, self.width, h, stroke=0, fill=1)
            if self.title:
                c.setFillColor(self.accent["bar"]); c.rect(x, y_top - self.head_h, self.width, self.head_h, stroke=0, fill=1)
            c.restoreState()
            c.saveState()
            c.setStrokeColor(ctx.col["line"]); c.setLineWidth(ctx.shape["card_line"])
            c.roundRect(x, y_top - h, self.width, h, ctx.shape["card_radius"], stroke=1, fill=0)
            c.restoreState()
        if self.title:
            self.head.drawOn(c, x + pad, y_top - self.head_h / 2 - self.head.height / 2)
        y = y_top - self.head_h - pad
        for item in self.items:
            item.draw(c, x + pad, y)
            y -= item.height + ctx.item_gap


# --------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------
class Header:
    def __init__(self, cfg: dict, ctx: Ctx, page_w: float, margin: float, gap: float):
        self.ctx, self.cfg = ctx, cfg
        hd = cfg["header"]
        sz = cfg["theme"]["sizes"]
        self.band = ctx.shape["header_style"] == "band"
        self.rule = ctx.shape["header_rule"]
        # colours on the band (white-ish on primary) or on the page (dark on paper)
        c_title, c_authors, c_sub, c_event = (("on_primary", "on_primary", "header_sub", "header_accent") if self.band
                                              else ("primary", "ink", "muted", "muted"))
        self.margin = margin
        self.logos = hd.get("logos") or []
        self.logo_w = hd.get("logos_w_mm", 150) * mm if self.logos else 0
        self.logo_h = hd.get("logo_h_mm", 34) * mm
        self.logo_gap = gap * 0.6
        text_w = page_w - 2 * margin - (self.logo_w + gap * 1.5 if self.logos else 0)
        # largest title size that fits within the allowed number of lines
        # (title_lines can be set per poster under header: it is a preference, not a limit)
        max_lines = int(hd.get("title_lines", sz["title_lines"]))
        pt_min = int(hd.get("title_pt_min", sz["title_pt_min"]))
        pt = int(hd.get("title_pt_max", sz["title_pt_max"]))
        while True:
            st = ParagraphStyle("title", fontName="PosterBold", fontSize=pt, leading=pt * 1.08,
                                textColor=ctx.col[c_title])
            self.title = Paragraph(escape(hd["title"]).replace("&lt;br&gt;", "<br/>"), st)
            self.title.wrap(text_w, 1e7)
            if len(self.title.blPara.lines) <= max_lines or pt <= pt_min:
                break
            pt -= 2
        self.title_pt = pt
        n_lines = len(self.title.blPara.lines)
        self.title_note = None
        if n_lines > max_lines:
            self.title_note = (f"title runs to {n_lines} lines at the minimum size ({pt} pt): the header grows and the body text "
                   f"gets less room; shorten the title, move words to the subtitle or lower title_pt_min")
        ctx.report.note_size(pt, "title")
        names = ", ".join(f'{escape(a["name"])}<super>{a.get("affil", "")}</super>' for a in hd["authors"])
        au = ctx.style("authors", sz["authors_pt"], font="PosterBold", colour=c_authors)
        self.authors = Paragraph(names, au)
        self.authors.wrap(text_w, 1e7)
        aff = "<br/>".join(f"<super>{i + 1}</super> {escape(a)}" for i, a in enumerate(hd["affiliations"]))
        af = ParagraphStyle("affil", fontName="PosterBody", fontSize=sz["affil_pt"], leading=sz["affil_pt"] * 1.3,
                            textColor=ctx.col[c_sub])
        ctx.report.note_size(sz["affil_pt"], "affiliations")
        self.affil = Paragraph(aff, af); self.affil.wrap(text_w, 1e7)
        self.event = None
        if hd.get("event"):
            ev = ctx.style("event", sz["affil_pt"], font="PosterBold", colour=c_event)
            self.event = ctx.para(hd["event"], ev, text_w)
        self.subtitle = None
        if hd.get("subtitle"):
            sub = ctx.style("subtitle", sz["subtitle_pt"], colour=c_sub, lead=1.15)
            self.subtitle = ctx.para(hd["subtitle"], sub, text_w)
        self.text_w = text_w
        top_pad, bot_pad = margin * 0.7, margin * 0.6
        sub_h = (self.subtitle.height + gap * 0.4) if self.subtitle else 0
        left_h = (self.event.height + gap * 0.3 if self.event else 0) + self.title.height + sub_h + gap * 0.6 + self.authors.height + gap * 0.3 + self.affil.height
        stack_h = len(self.logos) * self.logo_h + max(len(self.logos) - 1, 0) * self.logo_gap
        self.top_pad = top_pad
        self.height = top_pad + max(left_h, stack_h) + bot_pad
        self.gap = gap
        self.page_w = page_w

    def draw(self, c, page_h: float) -> None:
        ctx, m = self.ctx, self.margin
        c.saveState()
        if self.band:
            c.setFillColor(ctx.col["primary"]); c.rect(0, page_h - self.height, self.page_w, self.height, stroke=0, fill=1)
        c.setFillColor(ctx.col["secondary"]); c.rect(0, page_h - self.height - self.rule, self.page_w, self.rule, stroke=0, fill=1)
        c.restoreState()
        y = page_h - self.top_pad
        if self.event:
            y -= self.event.height; self.event.drawOn(c, m, y); y -= self.gap * 0.3
        y -= self.title.height; self.title.drawOn(c, m, y)
        if self.subtitle:
            y -= self.gap * 0.4 + self.subtitle.height; self.subtitle.drawOn(c, m, y)
        y -= self.gap * 0.6
        y -= self.authors.height; self.authors.drawOn(c, m, y); y -= self.gap * 0.3
        y -= self.affil.height; self.affil.drawOn(c, m, y)
        if self.logos:
            style = ctx.style("logo-header", ctx.small, font="PosterBold", colour="primary", align=TA_CENTER, lead=1.15)
            lx = self.page_w - m - self.logo_w
            ly = page_h - self.top_pad
            for it in self.logos:
                ly -= self.logo_h
                draw_logo(c, ctx, it, lx, ly, self.logo_w, self.logo_h, style)
                ly -= self.logo_gap


# --------------------------------------------------------------------------
# Layout
# --------------------------------------------------------------------------
class Layout:
    def __init__(self, cfg: dict, base_pt: float):
        self.cfg = cfg
        page = cfg["page"]
        w, h = SIZES[page["size"]]
        if page.get("orientation", "portrait") == "landscape":
            w, h = h, w
        self.page_w, self.page_h = w, h
        self.margin = page["margin_mm"] * mm
        self.gap = page["gap_mm"] * mm
        self.report = Report(cfg["theme"]["sizes"]["min_pt"])
        self.ctx = Ctx(cfg, base_pt, self.report)
        self.base = base_pt
        self.header = Header(cfg, self.ctx, w, self.margin, self.gap)
        self.body_top = h - self.header.height - self.header.rule - self.gap
        self.body_bottom = self.margin
        self.avail = self.body_top - self.body_bottom
        inner_w = w - 2 * self.margin
        self.bands = []
        for band in cfg["layout"]["bands"]:
            cols = band["columns"]
            weights = [c_.get("width", 1) for c_ in cols]
            usable = inner_w - self.gap * (len(cols) - 1)
            col_cards = []
            for cdef, wt in zip(cols, weights):
                cw = usable * wt / sum(weights)
                cards = [Card(bid, cfg["blocks"][bid], self.ctx, cw) for bid in cdef["blocks"]]
                col_cards.append((cw, cards))
            heights = [sum(cd.height for cd in cards) + self.gap * (len(cards) - 1) for _, cards in col_cards]
            self.bands.append({"def": band, "cols": col_cards, "natural": max(heights), "weight": band.get("weight", 1)})
        self.natural = sum(b["natural"] for b in self.bands) + self.gap * (len(self.bands) - 1)
        self.slack = self.avail - self.natural

    def fits(self) -> bool:
        return self.slack >= 0

    def draw(self, c) -> None:
        self.header.draw(c, self.page_h)
        total_w = sum(b["weight"] for b in self.bands)
        y = self.body_top
        for b in self.bands:
            extra = self.slack * b["weight"] / total_w if total_w else 0
            b["height"] = b["natural"] + extra
            x = self.margin
            for cw, cards in b["cols"]:
                col_nat = sum(cd.height for cd in cards) + self.gap * (len(cards) - 1)
                spare = (b["height"] - col_nat) / len(cards)
                cy = y
                for cd in cards:
                    ch = cd.height + spare
                    cd.draw(c, x, cy, ch)
                    cd.final_h = ch
                    cy -= ch + self.gap
                x += cw + self.gap
            y -= b["height"] + self.gap


def fit_layout(cfg: dict) -> Layout:
    """Body text first: the largest body size that fits wins. If even the smallest does not fit, the
    title gives way, in steps, down to title_pt_min, and the body sizes are tried again."""
    af = cfg["theme"]["autofit"]
    hd = cfg["header"]
    sz = cfg["theme"]["sizes"]
    pt_min = int(hd.get("title_pt_min", sz["title_pt_min"]))
    cap = int(hd.get("title_pt_max", sz["title_pt_max"]))
    first = cap
    while True:
        trial = dict(cfg, header=dict(hd, title_pt_max=cap))
        pt = af["max_pt"]
        while pt >= af["min_pt"] - 1e-9:
            lay = Layout(trial, pt)
            if lay.fits():
                if cap < first:
                    U.warn(f"title reduced to fit the page ({lay.header.title_pt} pt instead of up to {first} pt)")
                if lay.header.title_note:
                    U.warn(lay.header.title_note)
                return lay
            pt -= af["step_pt"]
        if cap <= pt_min:
            break
        cap = max(pt_min, cap - 6)
    lay = Layout(cfg, af["min_pt"])
    raise SystemExit(
        f"ERROR: the content does not fit on the page even at {af['min_pt']} pt body and {pt_min} pt title "
        f"(over by {-lay.slack / mm:.0f} mm). Shorten texts, drop a block or widen the layout."
    )


def theme_lines(th: dict) -> list[str]:
    src = th.get("source") or {}
    lines = [f"theme: {th['id']} ({th['name']}), state {th['state']}"
             + (f", extends {th['extends']}" if th.get("extends") else "")]
    if src:
        lines.append(f"  colours from: {src.get('name', '')} {src.get('url', '')} (licence {src.get('licence', 'unstated')})".rstrip())
    if th.get("font_family"):
        lines.append(f"  typeface: {th['font_family']}")
    rows = T.contrast_report(th)
    worst = min(rows, key=lambda r: r["ratio"]) if rows else None
    flagged = [r for r in rows if r["level"] != "ok"]
    lines.append(f"  contrast: {len(rows)} pairings checked, {len(flagged)} below the recommended level"
                 + (f", lowest {worst['ratio']:.2f} ({worst['label']})" if worst else ""))
    return lines


def write_report(lay: Layout, strict_warn: list[str]) -> None:
    cfg = lay.cfg
    af = cfg["theme"]["autofit"]
    lines = [
        f"Layout report for {cfg['meta']['short_title']} (build {U.RELEASE})",
        f"page: {cfg['page']['size']} {cfg['page'].get('orientation', 'portrait')} ({lay.page_w / mm:.0f} x {lay.page_h / mm:.0f} mm)",
        f"base text size chosen by autofit: {lay.base:.1f} pt (range {af['min_pt']}-{af['max_pt']})",
        f"header title size: {lay.header.title_pt} pt",
        *theme_lines(cfg["theme"]),
        f"body height: {lay.avail / mm:.0f} mm available, {lay.natural / mm:.0f} mm natural, slack {lay.slack / mm:.0f} mm",
        "",
        "Blocks (why each one looks the way it does):",
    ]
    for b in lay.bands:
        for cw, cards in b["cols"]:
            for cd in cards:
                lines.append(f"- {cd.id}: {cw / mm:.0f} mm wide, {cd.height / mm:.0f} mm natural, "
                             f"{getattr(cd, 'final_h', cd.height) / mm:.0f} mm drawn")
                lines.append(f"    why: {cd.spec.get('why', '(none)')}")
    lines += ["", "Smallest size used per style (pt):"]
    for k, v in sorted(lay.report.sizes.items()):
        lines.append(f"  {k}: {v:.1f}")
    U.ensure_dirs()
    U.REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = U.parse_args(__doc__)
    cfg = U.load_config(theme=args.theme)
    U.ensure_dirs()
    register_fonts(cfg["theme"])
    lay = fit_layout(cfg)

    min_pt = cfg["theme"]["sizes"]["min_pt"]
    for name, pt in sorted(lay.report.sizes.items()):
        if pt < min_pt:
            U.warn(f"text style '{name}' is {pt:.1f} pt, below the {min_pt} pt legibility floor")
    max_ratio = cfg["theme"]["autofit"].get("max_slack_ratio", 0.12)
    if lay.slack / lay.avail > max_ratio and lay.base >= cfg["theme"]["autofit"]["max_pt"] - 1e-9:
        U.warn(f"body is sparse ({lay.slack / mm:.0f} mm of slack at the largest text size); "
               "raise autofit.max_pt or add content")

    meta = cfg["meta"]
    c = canvas.Canvas(str(U.PDF_PATH), pagesize=(lay.page_w, lay.page_h), invariant=1,
                      initialFontName="PosterBody")
    c.setTitle(meta["title"]); c.setAuthor(meta["author"]); c.setSubject(meta.get("subject", ""))
    c.setKeywords(meta.get("keywords", "")); c.setCreator(f"{meta['short_title']} (reportlab)")
    lay.draw(c)
    c.showPage()
    c.save()
    write_report(lay, [])
    print(f"wrote {U.PDF_PATH.relative_to(U.ROOT)}  base {lay.base:.1f} pt, title {lay.header.title_pt} pt, "
          f"slack {lay.slack / mm:.0f} mm")
    return U.finish(args.strict)


if __name__ == "__main__":
    sys.exit(main())
