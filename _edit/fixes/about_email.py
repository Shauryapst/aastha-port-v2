"""Page 2 (About): the Gmail line said aastharajput164@gmail,com — the address is 184 and
needs a full stop. Replaces the 6 with an 8 drawn in the same typeface (DM Sans) and trims
the comma to a full stop. Keeps the original as _edit/fixes/02-original.webp."""
import pathlib
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[2]
XL, ORIG = ROOT / "img/xl/02.webp", ROOT / "_edit/fixes/02-original.webp"
FONT = pathlib.Path("/home/claude/work/fonts/DMSans.ttf")
if not ORIG.exists():
    ORIG.write_bytes(XL.read_bytes())
im = np.array(Image.open(ORIG).convert("RGB"))
X0, Y0 = 3770, 1425                                   # the Gmail line
crop = im[Y0:Y0 + 37, X0:X0 + 360].copy()
L = crop.mean(2)
ink = L < 150

# the 6 (x 171-184, y 7-25) and the comma's tail (below the baseline at y 25)
six = np.zeros_like(ink); six[5:28, 169:186] = ink[5:28, 169:186]
tail = np.zeros_like(ink); tail[25:32, 283:292] = ink[25:32, 283:292]
colour = np.median(crop[ink & (L < 90)], axis=0)
mask = cv2.dilate((six | tail).astype(np.uint8), np.ones((3, 3), np.uint8))
bgr = cv2.cvtColor(crop, cv2.COLOR_RGB2BGR)
clean = cv2.cvtColor(cv2.inpaint(bgr, mask, 4, cv2.INPAINT_TELEA), cv2.COLOR_BGR2RGB)

# draw an 8 at 8x and scale down so its height matches the 4 beside it (18 px)
S = 8
font = ImageFont.truetype(str(FONT), 30 * S)
try: font.set_variation_by_axes([14, 400])
except Exception: pass
g = Image.new("L", (40 * S, 40 * S), 0); ImageDraw.Draw(g).text((4 * S, 0), "8", font=font, fill=255)
g = g.crop(g.getbbox())
h = 18; w = round(g.width * h / g.height)
g = np.array(g.resize((w, h), Image.LANCZOS)).astype(float) / 255
x, y = 171 + (13 - w) // 2, 7
region = clean[y:y + h, x:x + w].astype(float)
clean[y:y + h, x:x + w] = (region * (1 - g[..., None]) + colour * g[..., None]).round().astype(np.uint8)

out = im.copy(); out[Y0:Y0 + 37, X0:X0 + 360] = clean
page = Image.fromarray(out)
page.save(XL, quality=88, method=6)
for wdt, path, q in [(2400, "img/02.webp", 82), (1800, "img/w1800/02.webp", 80), (1200, "img/w1200/02.webp", 78), (1100, "img/thumb/02.webp", 72)]:
    page.resize((wdt, round(wdt * page.height / page.width)), Image.LANCZOS).save(ROOT / path, quality=q, method=6)
Image.fromarray(clean).resize((360 * 4, 37 * 4), Image.NEAREST).save("/tmp/claude-0/-home-claude/0f348994-d046-59b4-bb8e-a823778e9c3b/scratchpad/l2fix.png")
print("8 size", w, h, "colour", colour)
