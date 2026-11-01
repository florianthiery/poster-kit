"""Shared constants of the figures: palette of the caa-uk theme, fonts, paths. Nothing here is drawn."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
from matplotlib import font_manager

HERE = Path(__file__).resolve().parent
POSTER = HERE.parent
ROOT = POSTER.parents[1]
IMG = POSTER / "img"

# theme caa-uk (themes/caa-uk/theme.yaml)
DEEP, BLUE, INK, MUTED = "#0B4F7A", "#1998D8", "#12324A", "#47627A"
SKY, CARD, TINT, LINE = "#8FD0F2", "#E8F4FB", "#D2EAF7", "#A9D3EA"
ORANGE, ORANGE_TINT = "#C2410C", "#FDEBDD"

for f in ("barlow/Barlow-Regular.ttf", "barlow/Barlow-Bold.ttf", "barlow/BarlowSemiCondensed-Bold.ttf",
          "noto-sans-ogham/NotoSansOgham-Regular.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "fonts" / f))
matplotlib.rcParams["font.family"] = "Barlow"
matplotlib.rcParams["svg.fonttype"] = "path"
MM = 1 / 25.4
