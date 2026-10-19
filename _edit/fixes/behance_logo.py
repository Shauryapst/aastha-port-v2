"""Adds a Behance mark beside the Behance line on the last page (p45),
matching the envelope icon above it (same width, same white)."""
import pathlib
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "img" / "xl" / "45.webp"
ORIG = ROOT / "_edit" / "fixes" / "45-original.webp"
if not ORIG.exists():
    ORIG.write_bytes(SRC.read_bytes())
page = Image.open(ORIG).convert("RGBA")

S = 4                                     # draw large, then scale down for smooth edges
W, H = 110, 66                            # envelope is 110 px wide; centred on the name line
font = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf", 78 * S)
mark = Image.new("L", (W * S * 2, H * S * 2), 0)
d = ImageDraw.Draw(mark)
d.text((0, 0), "Bē", font=font, fill=255)
mark = mark.crop(mark.getbbox())
mark = mark.resize((W, round(W * mark.height / mark.width)), Image.LANCZOS)
colour = Image.new("RGBA", mark.size, (247, 252, 250, 255))
colour.putalpha(mark)
cx, cy = 3207, 1399                       # envelope centre x; name line centre y
page.alpha_composite(colour, (cx - mark.width // 2, cy - mark.height // 2))
page = page.convert("RGB")
page.save(SRC, quality=90, method=6)
page.resize((2400, round(2400 * page.height / page.width)), Image.LANCZOS).save(ROOT / "img" / "45.webp", quality=88, method=6)
page.resize((1100, round(1100 * page.height / page.width)), Image.LANCZOS).save(ROOT / "img" / "thumb" / "45.webp", quality=72, method=6)
print("mark", mark.size)
