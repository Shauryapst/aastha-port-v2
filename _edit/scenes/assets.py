"""Cuts the scene assets (motifs, figure, sketch lines, moodboard pieces, prints, photos)
out of the Canva pages in img/xl/. Run from the repo root:  python3 _edit/scenes/assets.py
Coordinates are in the 4200 x 1485 page images."""
import json, pathlib
import numpy as np, cv2
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
XL = ROOT / "img" / "xl"
OUT = ROOT / "img" / "scene"
OUT.mkdir(parents=True, exist_ok=True)

def page(n):
    return np.array(Image.open(XL / f"{n:02d}.webp").convert("RGB"))

def save(arr, name, q=86, maxw=None):
    im = Image.fromarray(arr)
    if maxw and im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(OUT / name, quality=q, method=5)
    return im.size

def crop(n, box, name, maxw=1600, q=84):
    l, t, r, b = box
    return save(page(n)[t:b, l:r], name, q=q, maxw=maxw)

def cutout(n, box, name, mode="paper", keep="largest", maxw=900, close=9, fill=True, ref=None):
    l, t, r, b = box
    rgb = page(n)[t:b, l:r]
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
    if mode == "paper":                       # textured white/grey watercolour paper
        bg = (hsv[..., 1] < 32) & (hsv[..., 2] > 200)
    else:                                     # flat cream background: distance from the corner colour
        ref = np.array(ref, np.float32)
        bg = np.linalg.norm(rgb.astype(np.float32) - ref, axis=2) < 34
    m = (~bg).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((close, close), np.uint8))
    num, lab, stats, _ = cv2.connectedComponentsWithStats(m)
    if num > 1:
        areas = stats[1:, cv2.CC_STAT_AREA]
        if keep == "largest":
            m = ((lab == 1 + int(np.argmax(areas))) * 255).astype(np.uint8)
        else:                                 # keep everything reasonably big
            keepids = [1 + i for i, a in enumerate(areas) if a > areas.max() * 0.02]
            m = (np.isin(lab, keepids) * 255).astype(np.uint8)
    # fill holes
    if fill:
        ff = m.copy(); h, w = m.shape
        cv2.floodFill(ff, np.zeros((h + 2, w + 2), np.uint8), (0, 0), 255)
        m = m | (~ff & 255)
    m = cv2.GaussianBlur(m, (3, 3), 0)
    ys, xs = np.where(m > 20)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    rgba = np.dstack([rgb, m])[y0:y1, x0:x1]
    size = save(rgba, name, q=88, maxw=maxw)
    return size, tuple(int(v) for v in (l + x0, t + y0, l + x1, t + y1)), m[y0:y1, x0:x1], rgb[y0:y1, x0:x1]

def sketch_lines(rgb, mask, min_len=0.02, eps=0.0016):
    """Pen lines for the 'sketch' stage: edges of the figure, as simplified polylines (0..1 coords)."""
    h, w = mask.shape
    g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    g = cv2.bilateralFilter(g, 9, 40, 9)
    e = cv2.Canny(g, 70, 160)
    e[mask < 128] = 0
    outline = cv2.Canny(mask, 50, 150)                      # the silhouette itself
    e = cv2.dilate(e | outline, np.ones((2, 2), np.uint8))
    cs, _ = cv2.findContours(e, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    lines = []
    diag = (w * w + h * h) ** 0.5
    for c in cs:
        L = cv2.arcLength(c, False)
        if L < min_len * diag:
            continue
        a = cv2.approxPolyDP(c, eps * diag, False)[:, 0, :]
        # contours of thin lines come back as a double loop; keep the first half
        if len(a) > 6 and cv2.arcLength(c, True) - 2 * L < 4:
            a = a[: len(a) // 2 + 1]
        pts = [[round(float(x) / w, 4), round(float(y) / h, 4)] for x, y in a]
        lines.append(pts)
    lines.sort(key=lambda p: min(q[1] for q in p))         # draw from the top down
    return lines

def swatch(n, box):
    l, t, r, b = box
    c = page(n)[t:b, l:r].reshape(-1, 3).mean(axis=0)
    return "#%02x%02x%02x" % tuple(int(v) for v in c)

meta = {}

# --- Fables of Mithila: sketch -> garment (middle kaftan figure, page 16) ---
size, box, m, rgb = cutout(16, (2940, 60, 3420, 1440), "fables-figure.webp", keep="all", maxw=760, close=5)
meta["fablesFigure"] = {"w": size[0], "h": size[1], "box": box}
meta["fablesLines"] = sketch_lines(rgb, m)
lineup = (2380, 60, 3880, 1440)
crop(16, lineup, "fables-lineup.webp", maxw=2000)
meta["fablesLineup"] = {"box": lineup}

# --- Saandra: motif -> print (fleur motif, page 22) ---
size, box, *_ = cutout(22, (900, 330, 1330, 880), "saandra-motif.webp", keep="all", maxw=520, close=3, fill=False)
meta["saandraMotif"] = {"w": size[0], "h": size[1]}
crop(19, (1500, 0, 4200, 1050), "saandra-print.webp", maxw=1800)

BG29 = page(29)[1380:1460, 1500:1600].reshape(-1, 3).mean(axis=0)
# --- Seed Scriptures: sketch motif -> final motif -> print (pages 29, 30) ---
size, box, *_ = cutout(29, (120, 700, 440, 1080), "seed-motif-sketch.webp", mode="flat", maxw=420, ref=BG29)
meta["seedSketch"] = {"w": size[0], "h": size[1]}
size, box, *_ = cutout(29, (1930, 900, 2330, 1350), "seed-motif.webp", mode="flat", keep="largest", maxw=480, ref=BG29)
meta["seedMotif"] = {"w": size[0], "h": size[1]}
crop(30, (180, 425, 700, 920), "seed-print.webp", maxw=1000)

# --- Unbuilt: moodboard pieces (pages 5, 6) ---
pieces = {
    "mb-radial.webp": (5, (2694, 420, 3216, 730)),
    "mb-cells.webp":  (5, (3110, 740, 3505, 1290)),
    "mb-coral.webp":  (5, (3500, 670, 4020, 1410)),
    "mb-lines.webp":  (5, (2460, 720, 2960, 1365)),
    "mb-algae.webp":  (6, (0, 0, 1180, 1485)),
    "mb-weed.webp":   (6, (1000, 995, 1800, 1460)),
}
meta["moodboard"] = {}
for name, (n, b) in pieces.items():
    s = crop(n, b, name, maxw=900)
    meta["moodboard"][name] = {"w": s[0], "h": s[1]}
# Pantone TCX colour board (page 6): sample the middle of each chip
tcx = [("15-0732", (3123, 860)), ("13-5309", (3351, 860)), ("12-1808", (3579, 860)), ("15-5519", (3810, 860)),
       ("18-5128", (3123, 1120)), ("14-0443", (3351, 1120)), ("19-1555", (3579, 1120)), ("18-0940", (3810, 1120))]
meta["unbuiltPalette"] = [{"code": c + " TCX", "hex": swatch(6, (x - 40, y - 40, x + 40, y + 40))} for c, (x, y) in tcx]

# --- woven products ---
crop(37, (2135, 25, 4130, 1460), "roundup-photo.webp", maxw=1800)
crop(38, (2050, 0, 4200, 990), "kargha-photo.webp", maxw=1800)


# --- Baandh: tie & dye (pages 42, 44) ---
crop(42, (1572, 315, 1972, 745), "baandh-sample.webp", maxw=800)           # the fan-folded pink sample
crop(42, (1530, 990, 2100, 1270), "baandh-note.webp", maxw=600, q=88)       # her note: "Fanfold it"
crop(44, (1500, 0, 4200, 1485), "baandh-cushions.webp", maxw=1800)

(OUT / "scenes.json").write_text(json.dumps(meta, separators=(",", ":")))
print("lines:", len(meta["fablesLines"]), "points:", sum(len(l) for l in meta["fablesLines"]))
print("palette:", meta["unbuiltPalette"])
for f in sorted(OUT.iterdir()): print(f.name, f.stat().st_size)
