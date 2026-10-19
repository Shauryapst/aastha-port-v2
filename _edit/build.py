"""Generates index.html for the v2 portfolio (a stack of the 45 Canva pages).
Edit PAGES / CHAPTERS / HOTSPOTS below and run:  python3 build.py
"""
import json, html, pathlib

NAME = "Aastha Rajput"
TAGLINE = "Textile design portfolio 2026"
EMAIL = "aastharajput184@gmail.com"
NIFT = "astha.rajput@nift.ac.in"
BEHANCE = "https://www.behance.net/ARa0953289"
LINKEDIN = "https://www.linkedin.com/in/aastha-rajput-44491b2b2"

CHAPTERS = [
    # id, title, subtitle, first page, last page
    ("intro",   "Introduction",      "Cover, about and contents",            1, 3),
    ("unbuilt", "Unbuilt",           "Surface design · home textiles",       4, 11),
    ("mithila", "Fables of Mithila", "Print design · Madhubani narratives",  12, 18),
    ("saandra", "Saandra",           "Print design · Rajasthani geometry",   19, 24),
    ("seed",    "Seed Scriptures",   "Print design · the pomegranate",       25, 32),
    ("roundup", "Roundup",           "Woven mufflers",                       33, 37),
    ("kargha",  "Kargha",            "Woven waist belt",                     38, 40),
    ("baandh",  "Baandh",            "Tie & dye",                            41, 44),
    ("thanks",  "Thank you",         "Contact",                              45, 45),
]

PAGES = [
    "Cover", "About Aastha", "Contents",
    # Unbuilt
    "Title", "Brand study & moodboard", "Inspiration & colour board", "Motif development",
    "Print development", "Print development", "Home textiles in use", "Home textiles in use",
    # Fables of Mithila
    "Title", "Concept & inspiration", "Design process & palette", "Motif development",
    "Print coordinates", "Print coordinates", "Print coordinates",
    # Saandra
    "Title", "Concept note", "Moodboard & client profile", "Motif development",
    "Print development", "Print development",
    # Seed Scriptures
    "Title", "Keywords & design process", "Inspiration & concept", "Colour forecast & audience",
    "Motif generation", "Prints & silhouettes", "Prints & silhouettes", "Final line-up",
    # Roundup
    "Title", "Concept & palette", "Muffler 1 — weave drafts", "Muffler 2 — weave drafts", "The shoot",
    # Kargha
    "Title", "Concept, texture & material", "Motifs & colourways",
    # Baandh
    "Title", "Tie & dye samples", "Tie & dye samples", "Cushion collection",
    # Thank you
    "Thank you",
]
assert len(PAGES) == 45

# Clickable areas on a page, in % of the page (left, top, width, height).
HOTSPOTS = {
    2: [
        ("link",  LINKEDIN, "LinkedIn",                 74.2, 93.6, 13.4, 5.0),
        ("email", NIFT,     "Email " + NIFT,            88.4, 93.6, 10.0, 2.6),
        ("email", EMAIL,    "Email " + EMAIL,           88.4, 96.2, 10.0, 2.6),
    ],
    45: [
        ("email", EMAIL,    "Email " + EMAIL,           74.6, 83.2, 23.0, 6.4),
        ("link",  BEHANCE,  "Behance",                  74.6, 90.8, 13.8, 6.4),
    ],
}

def chapter_of(n):
    for c in CHAPTERS:
        if c[3] <= n <= c[4]:
            return c

def fx_for(n):
    c = chapter_of(n)
    if n == 1:
        return "none"
    if n == c[3]:
        return "iris"            # chapter title pages open like an aperture
    cycle = ["rise", "wipe", "zoom", "curtain", "drift"]
    return cycle[(n - c[3] - 1) % len(cycle)]

esc = html.escape
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from scenes_def import extras_after, scene_data

TOC_STAMPS = ["unbuilt", "fables", "saandra", "seed", "roundup", "kargha", "baandh"]
TOC_TILT = [-4, 3, -2, 5, -3, 4, -5]

def toc_html():
    projects = [c for c in CHAPTERS if c[0] not in ("intro", "thanks")]
    items = []
    for k, ((cid, title, sub, start, end), stamp) in enumerate(zip(projects, TOC_STAMPS)):
        items.append(
            f'<li style="--i:{k};--r:{TOC_TILT[k]}deg">'
            f'<a class="stamp" href="#p{start}" data-go="{start}" data-cur="btn" data-label="Open" aria-label="{k + 1:02d} {esc(title)} — {esc(sub)}">'
            f'<span class="stamp-img"><img src="img/toc/{stamp}.webp" alt="" width="420" height="420" decoding="async"></span>'
            f'<svg class="postmark" viewBox="0 0 120 120" aria-hidden="true"><defs><path id="pm{k}" d="M60 60 m-41 0 a41 41 0 1 1 82 0 a41 41 0 1 1 -82 0"/></defs>'
            f'<circle cx="60" cy="60" r="52"/><circle cx="60" cy="60" r="30"/>'
            f'<text><textPath href="#pm{k}" startOffset="2%">NIFT · TEXTILE DESIGN · 2026 ·</textPath></text>'
            f'<text class="pm-n" x="60" y="68" text-anchor="middle">{k + 1:02d}</text></svg>'
            f'<span class="stamp-meta"><b>{k + 1:02d}</b><span class="stamp-name">{esc(title)}</span><em>{esc(sub)}</em></span>'
            f'</a></li>')
    word = "".join(f'<span style="--j:{j}">{ch}</span>' for j, ch in enumerate("CONTENTS"))
    return (f'  <section class="pg pg-toc" id="p3" data-i="3" data-x="0" aria-label="Page 3 of 45: Contents">\n'
            f'    <div class="frame"><div class="art toc">\n'
            f'      <h2 class="toc-word" aria-label="Contents">{word}</h2>\n'
            f'      <p class="toc-note">Seven projects · tap a stamp to open it</p>\n'
            f'      <ol class="toc-list">{"".join(items)}</ol>\n'
            f'    </div></div>\n  </section>')
sections = []
for n in range(1, 46):
    c = chapter_of(n)
    title = PAGES[n - 1]
    hots = ""
    for kind, target, label, l, t, w, h in HOTSPOTS.get(n, []):
        style = f"left:{l}%;top:{t}%;width:{w}%;height:{h}%"
        if kind == "email":
            hots += (f'\n      <a class="hot" href="mailto:{esc(target)}" data-copy="{esc(target)}" '
                     f'style="{style}" aria-label="{esc(label)}" data-cur="link" data-label="Copy"></a>')
        else:
            hots += (f'\n      <a class="hot" href="{esc(target)}" target="_blank" rel="noopener" '
                     f'style="{style}" aria-label="{esc(label)}" data-cur="link" data-label="Open"></a>')
    eager = n <= 3
    # where a phone held upright starts each page (0 = left edge, 1 = right edge)
    x = 0.6 if n == 1 else 0.82 if n == 45 else 1 if n == c[3] else 0
    if n == 3:                                   # contents page: live, animated stamps
        sections.append(toc_html()); sections.extend(extras_after(n)); continue
    sections.append(
f'''  <section class="pg{" ch-start" if n == c[3] else ""}" id="p{n}" data-i="{n}" data-x="{x}" aria-label="Page {n} of 45: {esc(c[1])}, {esc(title)}">
    <div class="frame"><div class="art">
      <img src="img/{n:02d}.webp" srcset="img/{n:02d}.webp 2400w, img/xl/{n:02d}.webp 4200w" sizes="(max-aspect-ratio: 1/1) 260vh, 92vw" data-n="{n}" width="2400" height="849" alt="{esc(c[1])} — {esc(title)}"{' fetchpriority="high"' if n == 1 else ''}{'' if eager else ' loading="lazy"'} decoding="async" draggable="false">{hots}
    </div></div>
  </section>''')
    sections.extend(extras_after(n))

data = {
    "pages": PAGES,
    "chapters": [{"id": a, "title": b, "sub": s, "start": x, "end": y} for a, b, s, x, y in CHAPTERS],
}

ticks = []
for n in range(1, 46):
    c = chapter_of(n)
    cls = "tick" + (" cs" if n == c[3] and n != 1 else "")
    ticks.append(f'<button type="button" class="{cls}" data-go="{n}" aria-label="Page {n}: {esc(c[1])} — {esc(PAGES[n-1])}" data-cur="btn"></button>')

index_items = []
for a, b, s, x, y in CHAPTERS:
    rng = f"{x:02d}" if x == y else f"{x:02d}–{y:02d}"
    index_items.append(
f'''      <li><button type="button" class="ix-item" data-go="{x}" data-cur="btn" data-label="Open">
        <span class="ix-thumb"{' style="--ox:50%"' if x in (1, 45) else ''}><img alt="" data-src="img/{x:02d}.webp" width="2400" height="849"></span>
        <span class="ix-text"><span class="ix-num">{rng}</span><span class="ix-title">{esc(b)}</span><span class="ix-sub">{esc(s)}</span></span>
      </button></li>''')

tpl = pathlib.Path(__file__).with_name("template.html").read_text()
out = (tpl.replace("{{NAME}}", esc(NAME))
          .replace("{{TAGLINE}}", esc(TAGLINE))
          .replace("{{SECTIONS}}", "\n".join(sections))
          .replace("{{TICKS}}", "\n    ".join(ticks))
          .replace("{{INDEX}}", "\n".join(index_items))
          .replace("{{DATA}}", json.dumps(data, ensure_ascii=False))
          .replace("{{SCENEDATA}}", scene_data()))
pathlib.Path(__file__).resolve().parent.parent.joinpath("index.html").write_text(out)
print("index.html written:", len(out), "bytes")
