"""Fixes spelling mistakes baked into the Canva slide images by moving letters that are
already on the same slide (same font, size and colour) — nothing is redrawn.
Run from the repo root after a fresh export of img/xl:  python3 _edit/typos/fix_typos.py
Coordinates are in the 4200 x 1485 images; the 2400 px versions are rebuilt from them.

  p14  Colour Exporation  -> Colour Exploration   (l taken from "Colour")
  p26  geometery          -> geometry
  p26  Braintorming       -> Brainstorming        (s taken from "Inspiration")
  p36  STARIGHT DRAFT     -> STRAIGHT DRAFT
  p39  GEOMETERY          -> GEOMETRY
"""
import pathlib
import numpy as np, cv2
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
load = lambda n: np.array(Image.open(ROOT / f"img/xl/{n:02d}.webp").convert("RGB")).astype(np.float32)

class Line:
    """One line of text: rows t..b. Letters are the ink components in it."""
    def __init__(self, a, t, b, paper_dy, flat=False):
        self.a, self.t, self.b, self.dy, self.flat = a, t, b, paper_dy, flat
        self.orig = a.copy()
        L = self.orig[t:b].mean(axis=2)
        self.paperL = np.percentile(L, 90)
        self.inkL = np.percentile(L, 0.5)
        m = (L < self.paperL - 40).astype(np.uint8)
        self.n, self.lab, self.st, _ = cv2.connectedComponentsWithStats(m)

    def letters(self, x0, x1):
        """Mask of the components whose left edge is in [x0, x1)."""
        sel = np.zeros(self.lab.shape, np.uint8)
        for i in range(1, self.n):
            if x0 <= self.st[i][0] < x1 and self.st[i][4] > 15: sel[self.lab == i] = 1
        return cv2.dilate(sel, np.ones((3, 3), np.uint8)).astype(np.float32)

    def clear(self, x0, x1):
        a, t, b = self.a, self.t, self.b
        if self.flat: a[t:b, x0:x1] = np.median(self.orig[t:b, x0:x1].reshape(-1, 3), axis=0)
        else: a[t:b, x0:x1] = self.orig[t + self.dy:b + self.dy, x0:x1]

    def place(self, sel, dx, src=None):
        """Draw the selected letters dx pixels to the side (from src line, default this one)."""
        src = src or self
        o = src.orig[src.t:src.b]
        L = o.mean(axis=2)
        h, w = sel.shape
        ys, xs = np.nonzero(sel)
        x0, x1 = xs.min(), xs.max() + 1
        win = L[:, max(0, x0 - 20):x1 + 20]                     # paper and ink measured locally
        paper = np.percentile(win, 90); ink = np.percentile(L[:, x0:x1][sel[:, x0:x1] > 0], 3)
        al = (np.clip((paper - L) / max(20, (paper - ink) * 0.8), 0, 1) * sel)[..., None]
        dst = self.a[self.t:self.t + h, x0 + dx:x1 + dx]
        self.a[self.t:self.t + h, x0 + dx:x1 + dx] = dst * (1 - al[:, x0:x1]) + o[:, x0:x1] * al[:, x0:x1]

def save(n, a):
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    im.save(ROOT / f"img/xl/{n:02d}.webp", quality=80, method=4)
    im.resize((2400, 849), Image.LANCZOS).save(ROOT / f"img/{n:02d}.webp", quality=82, method=4)

# --- p26: geometery -> geometry (drop the e between t and r) -------------------
a = load(26)
ln = Line(a, 790, 905, 0, flat=True)
moved = ln.letters(1690, 1760)                 # r, y
ln.clear(1637, 1820); ln.place(ln.letters(1600, 1637), 0)   # keep the t whole
ln.place(moved, -57)
# --- p26: Braintorming -> Brainstorming (s from "Inspiration", same slide) ------
ln = Line(a, 984, 1026, 46)
rest = ln.letters(2700, 2850)                  # t o r m i n g
s = ln.letters(3142, 3150)                     # the s of "Inspiration"
ln.clear(2702, 2870); ln.place(ln.letters(2680, 2700), 0)   # keep the n whole
ln.place(rest, 20)
ln.place(s, 2704 - 3143)
save(26, a)

# --- p14: Colour Exporation -> Colour Exploration (l from "Colour") -------------
a = load(14)
ln = Line(a, 595, 650, 50)
lcol = ln.letters(3234, 3248)
rest = ln.letters(3394, 3560)                  # o r a t i o n
ln.clear(3394, 3560)
ln.place(rest, 14)
ln.place(lcol, 3395 - 3236)
save(14, a)

# --- p39: GEOMETERY -> GEOMETRY (drop the second-to-last E) --------------------
a = load(39)
ln = Line(a, 1398, 1458, -62)
ry = ln.letters(856, 900)                      # R, Y
ln.clear(833, 920); ln.place(ln.letters(780, 833), 0)      # keep E+T whole
ln.place(ry, -23)
save(39, a)

# --- p36: STARIGHT DRAFT -> STRAIGHT DRAFT (swap A and R) ----------------------
a = load(36)
ln = Line(a, 955, 1005, 60)
A, R = ln.letters(1222, 1226), ln.letters(1246, 1250)
rest = ln.letters(1268, 1500)                  # I G H T  D R A F T
ln.clear(1222, 1520); ln.place(ln.letters(1200, 1222), 0)  # keep the T whole
ln.place(R, 1229 - 1247)
ln.place(A, 1251 - 1223)
ln.place(rest, 6)
save(36, a)
print("fixed pages 14, 26, 36, 39")
