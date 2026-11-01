"""Crop and downsize the stone photographs of the OG(H)AM repository (lguariento/og-h-am, folder images/) into
img/photos/. Set OGHAM_IMAGES to the folder `images` of a checkout. The crops are chosen by eye; every photo keeps
the rights of its owner (see img/README.md and the poster PRIMER, D2)."""
import os
from pathlib import Path
from PIL import Image
from common import IMG

SRC = Path(os.environ.get("OGHAM_IMAGES", "/tmp/w/og-h-am/images"))
OUT = IMG / "photos"
# name: (file, crop box as fractions of the picture (left, top, right, bottom), target width px)
PHOTOS = {
    "garranes": ("IRE/I-COR/I-COR-030_Garranes.jpg", (0.10, 0.10, 0.90, 0.62), 1400),
    "dyke": ("SCO/S-MOR-001-Brodie-b.jpg", (0.0, 0.0, 1.0, 0.62), 1400),
    "blackwaterfoot-1": ("SCO/S-BUT-001-Blackwaterfoot1.JPG", (0.0, 0.0, 1.0, 1.0), 480),
    "gigha-1": ("SCO/S-ARL-001-Gigha-a.jpg", (0.0, 0.0, 1.0, 1.0), 1400),
}

def main():
    OUT.mkdir(exist_ok=True)
    for name, (f, (l, t, r, b), w) in PHOTOS.items():
        im = Image.open(SRC / f).convert("RGB")
        W, H = im.size
        im = im.crop((int(l * W), int(t * H), int(r * W), int(b * H)))
        if im.width > w:
            im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
        im.save(OUT / f"{name}.jpg", quality=88, optimize=True)
        print(name, im.size)

if __name__ == "__main__":
    main()
