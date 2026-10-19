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

# The live address once deployed (e.g. "https://aastha-rajput.netlify.app"), no trailing slash.
# Fills in canonical / og:url / absolute share image and writes sitemap.xml. Leave "" until known.
SITE_URL = ""

# Real text about Aastha — shown in the contact section and read by search engines
ROLE = "Textile designer"
SCHOOL = "National Institute of Fashion Technology (NIFT), Srinagar"
BIO = ("A textile design student interested in blending traditional crafts with modern aesthetics — "
       "print and surface design, weaving and tie & dye, with a research-led process and an eye for photography.")
EXPERIENCE = [
    ("Internship — Fabindia", "Print design, fabric sourcing, silhouettes and surface ornamentation for women's ethnicwear; seasonal print concepts, khakas and embroidery directions."),
    ("Craft research & documentation (2025)", "Sozani embroidery, Srinagar."),
    ("Bagh print", "Designed and developed a stole using traditional Bagh block printing — motif development, colour selection, block placement and hand printing."),
    ("Tirathram and Company (ongoing)", "Photography shoot for their upcoming collection."),
]
SKILLS = ["Print design", "Surface design", "Painting", "Weaving", "Design process", "Fabric manipulation",
          "Motif development", "Concept development", "Photography", "Trend research (WGSN)"]
TOOLS = ["Photoshop", "Illustrator", "InDesign", "Lightroom", "Procreate", "Canva", "VN", "Word", "PowerPoint"]
EDUCATION = "Bachelor of Design, Textile Design (2023–2027) · NIFT Srinagar"

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

# Index: an editorial grid; every card keeps flipping through its project's pages
IX_SPAN = {"intro": 5, "unbuilt": 7, "mithila": 7, "saandra": 5, "seed": 4, "roundup": 4, "kargha": 4, "baandh": 8, "thanks": 4}
IX_COL = {"intro": "#e9dcc0", "unbuilt": "#c9933a", "mithila": "#e0573b", "saandra": "#8a78d8", "seed": "#e0709a",
          "roundup": "#4f93d6", "kargha": "#93b552", "baandh": "#7f9be0", "thanks": "#e9dcc0"}

def ix_pages(x, y, most=5):
    span = list(range(x, y + 1))
    if len(span) <= most:
        return span
    step = (len(span) - 1) / (most - 1)
    return sorted({span[round(k * step)] for k in range(most)})

index_items = []
for k, (a, b, s, x, y) in enumerate(CHAPTERS):
    rng = f"{x:02d}" if x == y else f"{x:02d}–{y:02d}"
    pages = ix_pages(x, y)
    imgs = "".join(f'<img alt="" data-src="img/thumb/{n:02d}.webp" width="1100" height="389"{" class=on" if j == 0 else ""}>' for j, n in enumerate(pages))
    dots = "".join(f'<i{" class=on" if j == 0 else ""}></i>' for j in range(len(pages)))
    count = f"{y - x + 1} page{'s' if y > x else ''}"
    big = "" if a in ("intro", "thanks") else f'<span class="ix-big">{k:02d}</span>'
    index_items.append(
f'''      <li class="ix-card ix-{a}" style="--span:{IX_SPAN[a]};--c:{IX_COL[a]}"><button type="button" class="ix-item" data-go="{x}" data-cur="btn" data-label="Open">
        <span class="ix-thumb"><span class="ix-slides">{imgs}</span><span class="ix-stitch" aria-hidden="true"></span>{big}<span class="ix-dots" aria-hidden="true">{dots}</span><span class="ix-count">{count}</span></span>
        <span class="ix-text"><span class="ix-num">{rng}</span><span class="ix-title">{esc(b)}</span><span class="ix-sub">{esc(s)}</span></span>
      </button></li>''')

def contact_html():
    exp = "".join(f"<li><b>{esc(t)}</b><span>{esc(d)}</span></li>" for t, d in EXPERIENCE)
    return f'''  <section class="contact" id="contact" data-after="45" data-title="Contact" aria-labelledby="ctTitle">
    <div class="ct-main">
      <p class="sc-kick">Contact</p>
      <h2 class="ct-title" id="ctTitle">Let’s talk textiles.</h2>
      <p class="ct-lede">Questions about a project, or want to work together on print, weave or surface design? Write to Aastha directly.</p>
      <div class="ct-actions">
        <a class="ct-mail" href="mailto:{EMAIL}" data-copy="{EMAIL}" data-cur="btn" data-label="Copy"><span>{EMAIL}</span><em>Copy</em></a>
        <a class="ct-pill" href="mailto:{NIFT}" data-cur="btn" data-label="Mail">{NIFT}</a>
        <a class="ct-pill" href="{LINKEDIN}" target="_blank" rel="noopener me" data-cur="btn" data-label="Open">LinkedIn ↗</a>
        <a class="ct-pill" href="{BEHANCE}" target="_blank" rel="noopener me" data-cur="btn" data-label="Open">Behance ↗</a>
      </div>
    </div>
    <div class="ct-about">
      <img src="img/portrait.webp" alt="Portrait of {esc(NAME)}" width="400" height="500" loading="lazy" decoding="async">
      <div>
        <h3>About {esc(NAME.split()[0])}</h3>
        <p>{esc(BIO)}</p>
        <p class="ct-edu">{esc(EDUCATION)}</p>
        <h3>Experience</h3><ul class="ct-exp">{exp}</ul>
        <h3>Skills</h3><p class="ct-tags">{" · ".join(esc(x) for x in SKILLS)}</p>
        <h3>Software</h3><p class="ct-tags">{" · ".join(esc(x) for x in TOOLS)}</p>
      </div>
    </div>
  </section>'''

def seo_head():
    desc = (f"{NAME} — textile designer at NIFT Srinagar. Portfolio of print, surface, weave and tie & dye projects: "
            "Unbuilt, Fables of Mithila, Saandra, Seed Scriptures, Roundup, Kargha and Baandh.")
    abs_ = (lambda u: f"{SITE_URL}/{u}") if SITE_URL else (lambda u: u)
    out = [f'<meta name="description" content="{esc(desc)}">',
           '<meta name="robots" content="index,follow,max-image-preview:large">',
           f'<meta name="author" content="{esc(NAME)}">',
           f'<meta property="og:site_name" content="{esc(NAME)} — Textile Design Portfolio">',
           f'<meta property="og:title" content="{esc(NAME)} — Textile Designer Portfolio">',
           f'<meta property="og:description" content="{esc(desc)}">',
           '<meta property="og:type" content="profile">',
           f'<meta property="profile:first_name" content="{esc(NAME.split()[0])}">',
           f'<meta property="profile:last_name" content="{esc(NAME.split()[-1])}">',
           f'<meta property="og:image" content="{abs_("og.jpg")}">',
           '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
           f'<meta property="og:image:alt" content="{esc(NAME)} — textile design portfolio cover">',
           '<meta property="og:locale" content="en_IN">',
           '<meta name="twitter:card" content="summary_large_image">',
           f'<meta name="twitter:title" content="{esc(NAME)} — Textile Designer Portfolio">',
           f'<meta name="twitter:description" content="{esc(desc)}">',
           f'<meta name="twitter:image" content="{abs_("og.jpg")}">']
    if SITE_URL:
        out += [f'<link rel="canonical" href="{SITE_URL}/">', f'<meta property="og:url" content="{SITE_URL}/">']
    return "\n".join(out)

def jsonld():
    from scenes_def import CASES
    abs_ = (lambda u: f"{SITE_URL}/{u}") if SITE_URL else (lambda u: u)
    person = {"@type": "Person", "@id": "#aastha", "name": NAME, "jobTitle": ROLE, "description": BIO,
              "email": f"mailto:{EMAIL}", "image": abs_("img/portrait.webp"),
              "affiliation": {"@type": "CollegeOrUniversity", "name": SCHOOL},
              "alumniOf": {"@type": "CollegeOrUniversity", "name": SCHOOL},
              "knowsAbout": SKILLS + ["Textile design", "Block printing", "Tie and dye", "Handloom weaving"],
              "sameAs": [LINKEDIN, BEHANCE]}
    works = []
    for i, (cid, title, sub, start, end) in enumerate([c for c in CHAPTERS if c[0] not in ("intro", "thanks")]):
        c = CASES.get(start)
        works.append({"@type": "ListItem", "position": i + 1, "item": {
            "@type": "CreativeWork", "name": title, "genre": sub, "creator": {"@id": "#aastha"},
            "description": c[2] if c else sub, "image": abs_(f"img/{start:02d}.webp"),
            "url": abs_(f"#p{start}")}})
    page = {"@type": "ProfilePage", "name": f"{NAME} — Textile Design Portfolio", "mainEntity": {"@id": "#aastha"},
            "inLanguage": "en", "hasPart": {"@type": "ItemList", "name": "Projects", "itemListElement": works}}
    if SITE_URL:
        page["url"] = SITE_URL + "/"
    return json.dumps({"@context": "https://schema.org", "@graph": [person, page]}, ensure_ascii=False, indent=1).replace("</", "<\\/")

sections.append(contact_html())       # contact + about, after the last page

ribbon = "".join(f'<span><i style="background:{IX_COL[a]}"></i>{esc(b)}</span>' for a, b, s, x, y in CHAPTERS if a not in ("intro", "thanks"))

tpl = pathlib.Path(__file__).with_name("template.html").read_text()
out = (tpl.replace("{{NAME}}", esc(NAME))
          .replace("{{TAGLINE}}", esc(TAGLINE))
          .replace("{{SECTIONS}}", "\n".join(sections))
          .replace("{{TICKS}}", "\n    ".join(ticks))
          .replace("{{INDEX}}", "\n".join(index_items))
          .replace("{{RIBBON}}", ribbon + ribbon)
          .replace("{{BRAND}}", "".join(f'<span class="bl" style="--i:{i}" aria-hidden="true">{esc(ch)}</span>' for i, ch in enumerate(NAME)))
          .replace("{{SEO}}", seo_head())
          .replace("{{JSONLD}}", jsonld())
          .replace("{{EMAIL}}", EMAIL).replace("{{NIFT}}", NIFT).replace("{{LINKEDIN}}", LINKEDIN).replace("{{BEHANCE}}", BEHANCE)
          .replace("{{DATA}}", json.dumps(data, ensure_ascii=False))
          .replace("{{SCENEDATA}}", scene_data()))
pathlib.Path(__file__).resolve().parent.parent.joinpath("index.html").write_text(out)
print("index.html written:", len(out), "bytes")

root = pathlib.Path(__file__).resolve().parent.parent
robots = "User-agent: *\nAllow: /\n" + (f"\nSitemap: {SITE_URL}/sitemap.xml\n" if SITE_URL else "")
root.joinpath("robots.txt").write_text(robots)
if SITE_URL:
    import datetime
    root.joinpath("sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
        f'  <url><loc>{SITE_URL}/</loc><lastmod>{datetime.date.today()}</lastmod>'
        + "".join(f"<image:image><image:loc>{SITE_URL}/img/{n:02d}.webp</image:loc></image:image>" for n in range(1, 46))
        + '</url>\n</urlset>\n')
