# Aastha Rajput — Portfolio (v2)

The Canva pages shown one after another, full width, with a magnifier.

## Deploy
Drag this whole folder onto https://app.netlify.com/drop — done. (Or push it to GitHub and
connect the repo in Netlify; no build command, publish directory `.`.)

## What's in here
- `index.html` — the site (all the code is in this one file)
- `img/01.webp … 45.webp` — the 45 Canva pages, 2400 px wide
- `img/xl/` — the same pages at 4200 px, used by the magnifier and on retina screens
- `og.jpg` — preview image when the link is shared
- `_edit/` — only needed if you change page titles or chapters (see below)

## How it behaves
- Pages sit as cards with space around and between them.
- Loading screen: the name writes itself in letter by letter, then the screen splits open onto the cover.
- Scrolling (mouse/trackpad) is smoothed; arrow keys, the ‹ › buttons and the right-hand rail glide to land each page centred.
- Every page gently zooms as it reaches the middle of the screen; project title pages drift slightly slower (parallax).
- Jumping to a project from the Index flashes its name in the middle of the screen.
- Magnifier: click a page, then scroll to zoom in/out (or `+` / `−`); click again to close. The lens wobbles as it moves.
  On phones: press and hold a page.
- The cursor ring labels what you're over (Zoom, Open, Copy…) and snaps onto buttons.
- Index: project thumbnails tilt in 3D under the mouse.
- Thank-you page: the email and Behance lines underline themselves and a "Back to top" button rises in.
- Motion is switched off for visitors who have "reduce motion" turned on. No animation ever hides a page.
- Each page has its own link, e.g. `/#p12` opens Fables of Mithila.

## Process scenes (scroll-driven)
Between pages, six pinned "studio" scenes play as you scroll (forwards and backwards):
- **Unbuilt — moodboard:** collage pieces slide in at different speeds, the Pantone TCX board fills in, keywords, then the concept note.
- **Fables of Mithila — sketch to garment:** the flat sketch draws itself, colour and print fill the silhouette, the coordinates appear.
- **Saandra / Seed Scriptures — motif to print:** one motif (Seed starts from the ink sketch) duplicates, rotates into a half-drop repeat, the repeat unit is marked, then the final print arrives as a swatch.
- **Roundup / Kargha — weave formation:** warp drops onto the loom, the weft travels over and under, the pattern appears, then the cloth turns into the finished product.
- **Baandh — fold, bind, dye:** the cloth is fan-folded, folded into squares, bound, dipped in a dye bath and unfolded to reveal her real sample, then the cushions.

Pressing → / ↓ on a title page glides through its scene. Assets are cut from the pages by `_edit/scenes/assets.py`;
scene text and timings live in `_edit/scenes_def.py`; the animation code is `scenes.js`.

## Case studies & colourway studio
- After every project's title page there is a short **case study** (Brief · Process · Outcome) as real text — edit `CASES` in `_edit/scenes_def.py`.
- After the Saandra pages, the **colourway studio** recolours her real motif live in five palettes — edit `COLOURWAYS` in the same file (`studio.js` does the recolouring).

## Print libraries, the shoot & backgrounds
- The separate images from Canva ("PORTFOLIO SLIDES/IMAGES") are cut into single prints and photos in `img/lib/`
- Large view uses `img/lib/full/` — re-cut from the full-resolution exports, gently lifted (+5% contrast, +7% colour, no auto-levels so grounds stay true), 2× Lanczos and sharpened. Zoom resizes the image for real instead of scaling it, so it stays crisp. Rebuild with `python3 _edit/lib_enhance.py <folder of source crops>`.
  (list in `_edit/lib.json`). They appear as **print libraries** after Unbuilt, Fables of Mithila, Saandra and Seed Scriptures,
  and as **The shoot** after the Roundup photos. Click any print or photo for a large view; click again to zoom.
  Sections and captions are set in `LIBS` in `_edit/scenes_def.py`.
- The dark scene and studio backgrounds use her cover watercolour (lettering removed): `img/bg/watercolour-dark.webp`;
  the print libraries sit on a faint wash of `img/bg/watercolour.webp`.

## Spelling fixes in the slides
A few typos are baked into the Canva images. `_edit/typos/fix_typos.py` fixes them by moving letters that already
exist on the same slide (same font and colour): Exploration (p14), geometry and Brainstorming (p26),
STRAIGHT DRAFT (p36), GEOMETRY (p39). Re-run it after replacing the slide images with a fresh Canva export.

## Updating
- **Changed a page in Canva?** Download it as PNG and replace `img/NN.webp` and `img/xl/NN.webp`
  (2400 px and 4200 px wide, WebP). Or ask Claude to redo the conversion.
- **Added or removed pages / renamed a section?** Edit the lists at the top of `_edit/build.py`,
  then run `python3 _edit/build.py` — it rewrites `index.html`.
- **Clickable email/Behance/LinkedIn areas** on pages 2 and 45 are set in `HOTSPOTS` in `_edit/build.py`.
- Index: drifting watercolour, a moving ribbon of project names, an editorial grid; each card flips through its project's pages (`img/thumb/`, 1100px) with a slow pan inside a running stitch in the project's colour.
- Right rail: a thread with a stitch per page and a bead per project, dyed up to the current page, ending in a needle.
- SEO: descriptive title/description, Open Graph + Twitter cards (og.jpg 1200×630), JSON-LD (Person + ProfilePage with the 7 projects), real-text contact & about section, h2 per case study, robots.txt. **Set `SITE_URL` in `_edit/build.py` once the Netlify address is known** and rebuild — that adds canonical/og:url, absolute image URLs and writes sitemap.xml.
- Contact: a Contact button in the top bar opens a card (copy email, LinkedIn, Behance); full contact + about section after the last page.
- Pages left out: `SKIP` in `_edit/build.py` (37, the shoot collage, duplicates the Shoot grid). The site renumbers itself (44 pages); image files keep their Canva numbers.

