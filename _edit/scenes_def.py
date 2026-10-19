"""Process scenes: scroll-driven animations placed after a page (used by build.py)."""
import json, pathlib, html
esc = html.escape
SCENE_META = json.loads((pathlib.Path(__file__).resolve().parent.parent / "img" / "scene" / "scenes.json").read_text())

UNBUILT_NOTE = ("The design aims to translate the microscopic beauty of algae into modern surface techniques. "
                "The focus is on capturing the textures, forms and translucency seen in algae strands and colonies — "
                "celebrating the balance between nature's simplicity and its complex patterns, and showing how unseen "
                "ecosystems can inspire creative design.")

# (after_page, id, type, chapter no., project, title, subtitle, spec, steps, cfg)
# steps: (from, to, name, detail) in scene progress 0..1
SCENES = [
    (4, "unbuilt", "moodboard", "01", "Unbuilt", "The moodboard",
     "Algae, coral and underwater textures for Sarita Handa's home textiles.",
     "Client: Sarita Handa · bedding, cushions, soft furnishings",
     [(0, .34, "Inspiration gathers", "Images, textures and samples arrive, each at its own pace."),
      (.34, .6, "Colour board", "Eight Pantone TCX colours, drawn from the algae."),
      (.6, .7, "Keywords", "Growth · organic · natural rhythm · underwater textures."),
      (.7, 1, "Concept", "The note that ties the board together.")],
     {}),
    (12, "fables", "sketch", "02", "Fables of Mithila", "Sketch to garment",
     "A Madhubani-printed kaftan, from the first pen line to the finished coordinate set.",
     "Madhubani line work · print repeat 15 × 15 in",
     [(0, .34, "Sketch", "The flat sketch is drawn line by line."),
      (.34, .64, "Colour & print", "Colour and the Panchatantra print fill the silhouette."),
      (.64, .8, "The garment", "The finished kaftan."),
      (.8, 1, "Coordinates", "The full set of print coordinates.")],
     {"figure": "img/scene/fables-figure.webp", "lineup": "img/scene/fables-lineup.webp"}),
    (19, "saandra", "motif", "03", "Saandra", "Motif to print",
     "A jharokha-inspired motif, repeated and rotated into a dense, detailed print.",
     "Repeat 12 × 12 in · Spring / Summer ready-to-wear",
     [(0, .2, "One hand-drawn motif", "Starting from a single motif."),
      (.2, .5, "Duplicate & rotate", "Copies turn and settle into a half-drop."),
      (.5, .78, "Repeat unit", "The 12 × 12 in unit tiles seamlessly."),
      (.78, 1, "The finished print", "Saandra on its marigold ground.")],
     {"motif": "img/scene/saandra-motif.webp", "print": "img/scene/saandra-print.webp", "ground": "#f8b931",
      "rotate": "alt", "unit": "Repeat 12 × 12 in", "cardLabel": "Saandra — final print", "zoomTo": .4, "gapX": 1.12, "gapY": 1.04}),
    (25, "seed", "motif", "04", "Seed Scriptures", "Motif to print",
     "The pomegranate — from an ink sketch to a final motif to a repeating print.",
     "Repeat 8 × 8 in · half-drop",
     [(0, .2, "From sketch to motif", "An ink sketch becomes the final coloured motif."),
      (.2, .5, "Duplicate", "The pomegranate is repeated in a half-drop."),
      (.5, .78, "Repeat unit", "The 8 × 8 in unit on a cream ground."),
      (.78, 1, "The finished print", "As it appears on the collection.")],
     {"motif": "img/scene/seed-motif.webp", "sketch": "img/scene/seed-motif-sketch.webp", "print": "img/scene/seed-print.webp",
      "ground": "#fbf6cf", "rotate": "none", "unit": "Repeat 8 × 8 in", "cardLabel": "Seed Scriptures — final print", "zoomTo": .36, "gapX": 1.06, "gapY": 1.0}),
    (33, "roundup", "weave", "05", "Roundup", "Weave formation",
     "Woody's cowboy world in yarn — bold yellow, denim blue and ivory in a twill check.",
     "Acrylic yarn · 30s count · 24 reed · ~384 ends · 2/2 twill",
     [(0, .2, "Warp", "Lengthwise threads are set on the loom."),
      (.2, .48, "Weft", "The crosswise thread travels over, under, over…"),
      (.48, .7, "Twill & check", "Diagonal ribs and colour blocks appear."),
      (.7, 1, "The finished muffler", "Woven, finished and worn.")],
     {"pattern": "twill", "band": 4, "warp": ["#fffbec", "#04345c", "#fffbec", "#2a8fe6", "#ffd230", "#2a8fe6"],
      "weft": ["#ffd230", "#fffbec", "#04345c", "#fffbec", "#2a8fe6"], "photo": "img/scene/roundup-photo.webp"}),
    (38, "kargha", "weave", "06", "Kargha", "Weave formation",
     "Colour blocks and geometric diamonds, woven into a waist belt.",
     "Woven belt · geometry · repetition · colour",
     [(0, .2, "Warp", "Bands of red, marigold, pink and olive are set up."),
      (.2, .48, "Weft", "The weft travels over and under the warp."),
      (.48, .7, "Diamonds", "Floating threads lift into diamond motifs."),
      (.7, 1, "The finished belt", "Kargha, off the loom.")],
     {"pattern": "kargha", "band": 12, "warp": ["#d8322a", "#e8c22a", "#f1a0ae", "#55691f", "#e8c22a"],
      "weft": ["#f3ead2", "#f3ead2", "#55691f"], "photo": "img/scene/kargha-photo.webp"}),
]
AFTER = {sc[0]: sc for sc in SCENES}


def moodboard_html():
    mb = SCENE_META["moodboard"]
    # file, left%, top%, width%, rotation, enter-from dx%, dy%, start, end
    layout = [("mb-algae.webp", 0, 4, 44, -3, -150, 10, .02, .2), ("mb-radial.webp", 36, 0, 40, 4, 0, -170, .05, .28),
              ("mb-coral.webp", 70, 8, 30, 3, 150, -40, .03, .22), ("mb-cells.webp", 54, 34, 24, -2, 170, 30, .1, .34),
              ("mb-lines.webp", 26, 46, 32, -5, -20, 170, .12, .3), ("mb-weed.webp", 2, 58, 40, 2, -160, 80, .16, .36)]
    pieces = "".join(
        f'<figure class="mb-piece" style="left:{l}%;top:{t}%;width:{w}%" data-r="{r}" data-dx="{dx}" data-dy="{dy}" data-a="{a}" data-b="{b}">'
        f'<img data-src="img/scene/{f}" alt="" width="{mb[f]["w"]}" height="{mb[f]["h"]}"></figure>'
        for f, l, t, w, r, dx, dy, a, b in layout)
    chips = "".join(f'<span class="mb-chip" style="--c:{c["hex"]}"><i></i><small>{c["code"]}</small></span>'
                    for c in SCENE_META["unbuiltPalette"])
    words = "".join(f'<span class="mb-word">{w}</span>' for w in ["Growth", "Organic", "Natural rhythm", "Underwater textures"])
    return (f'<div class="mb"><div class="mb-collage">{pieces}</div><div class="mb-info">'
            f'<div class="mb-pal" aria-label="Colour board">{chips}</div><p class="mb-words">{words}</p>'
            f'<div class="mb-note"><h3>Concept</h3><p class="mb-note-text">{esc(UNBUILT_NOTE)}</p></div></div></div>')


def scene_html(sc):
    after, sid, typ, no, proj, title, sub, spec, steps, cfg = sc
    lis = "".join(f'<li data-a="{a}" data-b="{b}"><b>{k + 1:02d}</b><span>{esc(n)}</span><em>{esc(d)}</em></li>'
                  for k, (a, b, n, d) in enumerate(steps))
    stage = moodboard_html() if typ == "moodboard" else ""
    return (f'  <section class="scene" id="s-{sid}" data-after="{after}" data-scene="{typ}" data-title="{esc(title)}" '
            f"data-cfg='{json.dumps(cfg)}' aria-label=\"{esc(proj)} — {esc(title)}\">\n"
            f'    <div class="sc-pin">\n      <div class="sc-cap">\n'
            f'        <span class="sc-kick">{no} · {esc(proj)}</span>\n'
            f'        <h2 class="sc-title">{esc(title)}</h2>\n        <p class="sc-sub">{esc(sub)}</p>\n'
            f'        <ol class="sc-steps">{lis}</ol>\n        <div class="sc-bar"><i></i></div>\n'
            f'        <p class="sc-spec">{esc(spec)}</p>\n      </div>\n'
            f'      <div class="sc-stage">{stage}</div>\n    </div>\n  </section>')


def scene_data():
    return json.dumps({k: SCENE_META[k] for k in ("fablesFigure", "fablesLineup", "fablesLines")}, separators=(",", ":"))


# ---------------------------------------------------------------
# Baandh — tie & dye scene (after page 41)
# ---------------------------------------------------------------
SCENES.append(
    (41, "baandh", "tiedye", "07", "Baandh", "Fold, bind, dye",
     "Resist dyeing by hand — the cloth is folded and bound so the dye can't reach everywhere.",
     "Fan-fold · square folds · thread binding · pink dye",
     [(0, .2, "Fan-fold", "The cloth is pleated like a fan."),
      (.2, .34, "Square folds", "Then folded again into small squares."),
      (.34, .47, "Bind", "Thread is wrapped tightly to resist the dye."),
      (.47, .66, "Dye", "Into the dye bath — the bound areas stay pale."),
      (.66, .86, "Unfold", "Opened out, the grid pattern appears."),
      (.86, 1, "Cushions", "The technique becomes a cushion collection.")],
     {"sample": "img/scene/baandh-sample.webp", "note": "img/scene/baandh-note.webp",
      "photo": "img/scene/baandh-cushions.webp", "dye": "#c2185b"}))
AFTER = {sc[0]: sc for sc in SCENES}

# ---------------------------------------------------------------
# Case studies — short, readable text right after each title page.
# Written only from what is on the portfolio pages.
# ---------------------------------------------------------------
CASES = {
    4: ("01", "Unbuilt",
        "Surface design for Sarita Handa — premium Indian home textiles (bedding, cushions, soft furnishings) for upper-income homes, ages 35–50.",
        "Brand study → algae as inspiration → a colour board of eight Pantone TCX shades → motifs drawn from algae forms → print development.",
        "A print collection visualised as bedding, cushions, throws and upholstery in four room settings.",
        "Inspiration: microscopic algae · growth, organic, natural rhythm, underwater textures"),
    12: ("02", "Fables of Mithila",
         "A print collection that retells the Panchatantra in the visual language of Madhubani art.",
         "Story & concept → inspiration → motif development (animals, trees, clouds) → a ten-colour palette → print development.",
         "Three print coordinates, each on a 15 × 15 in repeat, styled as resort wear.",
         "Madhubani line work, detailing and ornamental compositions"),
    19: ("03", "Saandra",
         "Spring / Summer ready-to-wear prints (₹800–1,000) for urban women aged 18–30.",
         "Rajasthani architecture — jharokhas, jaalis, mehraabs, haveli facades → moodboard and six-colour palette → geometric motifs → prints on a 12 × 12 in repeat.",
         "Six prints styled as dresses. “Saandra” means dense and detailed.",
         "Client profile: students, young professionals and creative-field women across urban India"),
    25: ("04", "Seed Scriptures",
         "A print exploration of the pomegranate as a coded language of seeds — origin, growth, potential.",
         "WGSN colour research → keywords and brainstorming → initial ink motifs → final motifs → prints on an 8 × 8 in repeat.",
         "A print collection styled as womenswear for women aged 20–40 who value heritage, sustainability and comfort.",
         "Keywords: contrast, prosperity, cross-section, botanical, geometry, ancient"),
    33: ("05", "Roundup",
         "Translate the playful world of Toy Story — Woody's cowboy world — into woven textiles.",
         "Concept and Pantone palette → weave drafts (S and Z twill, herringbone, plain, honeycomb) → hand-weaving in acrylic yarn.",
         "Two woven mufflers, 80 × 16 in, photographed in a shoot.",
         "Acrylic · 30s count · 24 reed · ~384 ends · EPI 24 · PPI 24"),
    38: ("06", "Kargha",
         "A woven accessory celebrating the colours and geometry of traditional Indian textiles.",
         "Concept (geometry, repetition, colour, texture, craft, threads) → texture and material studies → motif development → colourways.",
         "A handwoven waist belt in contrasting colour blocks with rhythmic diamond motifs.",
         "Red · marigold · pink · olive · cream"),
    41: ("07", "Baandh",
         "Explore resist dyeing — folding, binding and wrapping cloth to create pattern.",
         "Sample-by-sample documentation in pink and indigo: fan-folds, square folds, pole wrapping and stitch-and-gather, each with hand-drawn notes.",
         "A collection of tie-dye cushion covers.",
         "Techniques recorded as process notes beside every sample"),
}


def case_html(n):
    no, proj, brief, process, outcome, tags = CASES[n]
    return (f'  <section class="case" data-after="{n}" data-title="Case study" aria-label="{esc(proj)} — case study">\n'
            f'    <p class="case-kick">{no} · {esc(proj)} · Case study</p>\n'
            f'    <div class="case-grid">'
            f'<div><h3>Brief</h3><p>{esc(brief)}</p></div>'
            f'<div><h3>Process</h3><p>{esc(process)}</p></div>'
            f'<div><h3>Outcome</h3><p>{esc(outcome)}</p></div></div>\n'
            f'    <p class="case-tags">{esc(tags)}</p>\n  </section>')


# ---------------------------------------------------------------
# Colourway studio — after the Saandra pages (page 24)
# (name, ground, colour for the pinks, colour for the blues)
# ---------------------------------------------------------------
COLOURWAYS = [
    ("Marigold — original", "#f8b931", "#e24d85", "#1173a0", True),
    ("Indigo night", "#343a72", "#c0579a", "#8f9be0", False),
    ("Berry", "#a32a68", "#e2a03f", "#5b2370", False),
    ("Emerald", "#1f5e57", "#e9a2ab", "#c8403f", False),
    ("Saandra palette", "#eee138", "#d82336", "#2f2aa9", False),
]
STUDIO_AFTER = 24


def studio_html():
    btns = "".join(
        f'<button type="button" class="st-way" data-name="{esc(n)}" data-ground="{g}" data-a="{a}" data-b="{b}"'
        f'{" data-original" if o else ""} aria-pressed="false" data-cur="btn" data-label="Try">'
        f'<span class="st-dots"><i style="background:{g}"></i><i style="background:{a}"></i><i style="background:{b}"></i></span>'
        f'<span class="st-wname">{esc(n)}</span></button>' for n, g, a, b, o in COLOURWAYS)
    return ('  <section class="studio" id="studio-saandra" data-after="24" data-title="Colourways" data-motif="img/scene/saandra-motif.webp" aria-label="Saandra — colourway studio">\n'
            '    <div class="st-cap">\n'
            '      <span class="sc-kick">03 · Saandra</span>\n'
            '      <h2 class="sc-title">Colourways</h2>\n'
            '      <p class="sc-sub">Tap a colourway to recolour the Saandra print live — the same motif and repeat, '
            'in palettes from Aastha\'s print development.</p>\n'
            f'      <div class="st-ways" role="group" aria-label="Colourways">{btns}</div>\n'
            '      <p class="sc-spec">Half-drop repeat · 12 × 12 in · alternate columns turned</p>\n'
            '    </div>\n'
            '    <div class="st-stage"><span class="st-name" aria-live="polite"></span></div>\n'
            '  </section>')


def extras_after(n):
    """Everything that follows page n: case study, process scene, colourway studio."""
    out = []
    if n in CASES:
        out.append(case_html(n))
    if n in AFTER:
        out.append(scene_html(AFTER[n]))
    if n == STUDIO_AFTER:
        out.append(studio_html())
    return out


# ---------------------------------------------------------------
# Print libraries & the shoot — built from the separate images
# (img/lib/, cut from "PORTFOLIO SLIDES/IMAGES" by _edit/lib.json)
# after_page: (no, project, title, subtitle, [(file, caption)], kind)
# ---------------------------------------------------------------
LIB_META = {m["file"]: m for m in json.loads((pathlib.Path(__file__).resolve().parent / "lib.json").read_text())}

def _files(prefix):
    return sorted([f for f in LIB_META if f.startswith(prefix)], key=lambda f: [int(x) for x in f.split(".")[0].split("-")[-2:]])

LIBS = {
    9:  ("01", "Unbuilt", "Print library", "Eight algae prints, each with its own palette — shown large so the brush texture reads.",
         [(f, f"Print {k + 1:02d}") for k, f in enumerate(_files("unbuilt-"))], "prints"),
    18: ("02", "Fables of Mithila", "Print library", "Nine prints across three coordinate sets · repeat 15 × 15 in.",
         [(f, f"Set {k // 3 + 1} · print {k % 3 + 1}") for k, f in enumerate(_files("fables-"))], "prints"),
    24: ("03", "Saandra", "Print library", "Six prints from Rajasthani architecture · repeat 12 × 12 in.",
         [(f, f"Print {k + 1:02d}") for k, f in enumerate(_files("saandra-"))], "prints"),
    32: ("04", "Seed Scriptures", "Print library", "Five pomegranate prints · repeat 8 × 8 in.",
         [(f, f"Print {k + 1:02d}") for k, f in enumerate(_files("seed-"))], "prints"),
    37: ("05", "Roundup", "The shoot", "Both handwoven mufflers, worn — muffler 1 in blue twill and honeycomb, muffler 2 in the yellow-and-blue check.",
         [(f, ("Muffler 1" if "blue" in f else "Muffler 2")) for f in _files("shoot-blue-") + _files("shoot-yellow-")], "shoot"),
}


def lib_html(n):
    no, proj, title, sub, items, kind = LIBS[n]
    cards = "".join(
        f'<figure class="lib-card"><button type="button" class="lib-open" data-full="img/lib/full/{f}" data-thumb="img/lib/{f}" data-cap="{esc(proj)} — {esc(c)}" '
        f'data-cur="btn" data-label="View" aria-label="View {esc(proj)} {esc(c)} large">'
        f'<img src="img/lib/{f}" loading="lazy" decoding="async" alt="{esc(proj)} — {esc(c)}" width="{LIB_META[f]["w"]}" height="{LIB_META[f]["h"]}">'
        f'</button><figcaption>{esc(c)}</figcaption></figure>' for f, c in items)
    return (f'  <section class="lib lib--{kind}" data-after="{n}" data-title="{esc(title)}" aria-label="{esc(proj)} — {esc(title)}">\n'
            f'    <div class="lib-head"><span class="sc-kick">{no} · {esc(proj)}</span><h2 class="lib-title">{esc(title)}</h2>'
            f'<p class="lib-sub">{esc(sub)}</p></div>\n'
            f'    <div class="lib-grid">{cards}</div>\n  </section>')


_prev_extras = extras_after
def extras_after(n):
    out = _prev_extras(n)
    if n in LIBS:
        out.insert(0, lib_html(n))
    return out
