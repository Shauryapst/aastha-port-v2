"""Re-cuts the print-library / shoot images from the original exports and
makes them crisp and lively for the large (zoomable) view.

  python3 _edit/lib_enhance.py <folder with the source crops>

The source crops are the boxes in lib.json cut from "PORTFOILO  SLIDES/IMAGES"
at full resolution (one <file>.webp each). Seed Scriptures images are trimmed
to the print swatch only (lib.json "sub").

Writes  img/lib/<file>        card image (same size as before)
        img/lib/full/<file>   large view: 2x Lanczos, sharpened, up to 2800px
"""
import json, sys, pathlib
from PIL import Image, ImageEnhance, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = pathlib.Path(sys.argv[1])
META = json.loads((ROOT / "_edit" / "lib.json").read_text())
FULL = ROOT / "img" / "lib" / "full"
FULL.mkdir(parents=True, exist_ok=True)
MAX_FULL = 2800


def tone(im, photo):
    """Lift the flat, slightly greyed look of the export without changing her palette."""
    # gentle on purpose: grounds and palettes are design decisions, so no auto-levels
    im = ImageEnhance.Contrast(im).enhance(1.03 if photo else 1.05)
    im = ImageEnhance.Color(im).enhance(1.03 if photo else 1.07)
    return im


for m in META:
    name, photo = m["file"], m["proj"].startswith("shoot")
    im = Image.open(SRC / name).convert("RGB")
    if "sub" in m:
        x, y, w, h = m["sub"]
        im = im.crop((x, y, x + w, y + h))
    im = tone(im, photo)

    # large view: upscale so a 2.2x zoom on a retina screen still has real pixels
    s = min(2.0, MAX_FULL / max(im.size))
    big = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS) if s > 1 else im
    big = big.filter(ImageFilter.UnsharpMask(radius=2, percent=70 if photo else 85, threshold=2))
    big.save(FULL / name, quality=88, method=6)

    # card image: same footprint as before, a touch of sharpening after downsizing
    card = im.resize((m["w"], m["h"]), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1, percent=45, threshold=2))
    card.save(ROOT / "img" / "lib" / name, quality=86, method=6)
    print(name, im.size, "->", big.size, card.size)
