# Visual system and motion

This is a buildless HTML/CSS/JavaScript site. GitHub Pages serves the source
directly; no package installation or frontend build is needed.

## Shared components

- `assets/css/styles.css` holds the silver/cyan visual system, responsive gallery,
  open case-study chapters, navigation, buttons and native image dialog.
- `assets/js/main.js` progressively adds opening playback, navigation visibility,
  scroll reveals, pointer interactions and the image viewer. Content is visible
  by default. Every image-viewer link also opens the original without JavaScript.
- GSAP **3.15.0** and ScrollTrigger are vendored locally. Their upstream copyright
  headers, README, licence link and hashes are under `assets/vendor/gsap/`.
- Orbix remains the JTST display typeface; body text uses the system sans-serif
  stack. Font licensing remains under `assets/fonts/`.

## Project media

Run `python scripts/build-covers.py` to regenerate the seven self-contained SVG
concept illustrations. It uses only Python's standard library and embeds the
existing curated photos/logo without modifying the originals. Covers are labelled
as concepts; scientific evidence remains in separate, uncropped figures.

The Oxford Physics library owns its content, data and `.oxford-library` layouts.
Changes to shared navigation and buttons should also be checked against that page.
The redesigned Projects gallery includes its academic resources group using
`covers/oxford-physics.svg`. A `work-card featured-work` inside a `directory-grid`
provides the full-width library gateway. The library keeps its own resource
index, reading pages and scripts.

## Opening

The home opening is an inline SVG traced from `assets/images/none.png`: every
contour (outer circle, inner frames, trident) is drawn with a stroke-dash
animation, and the original artwork (clipped to the traced shape) fills in as the
strokes finish. It fades and the solid white JTST wordmark appears on a pure-black starfield with drifting motes. The
whole opening takes about 1.6 s.

## Interactive explorers

`assets/js/lab.js` powers the `[data-lab]` widgets on the Muon g-2 page (hand-fit
of a toy wiggle spectrum with live χ²/ndf) and the compound-pendulum page (RK4
comparison of linear and quadratic drag). Widgets are `hidden` until the script
runs, animate only on request and respect reduced motion.

## Discovery

Top-level pages carry Open Graph/Twitter tags with `assets/images/og-card.jpg`.
Home and About include a schema.org `Person` block. `llms.txt`, `sitemap.xml`,
`robots.txt` and `404.html` live at the root; update `llms.txt` and the sitemap
when a project page is added.

## Checks

```powershell
python scripts/check-site.py
node --check assets/js/main.js
python -m http.server 8766 --bind 127.0.0.1
```

Check all pages at 1440, 1024, 390 and 320 pixels. Also verify no JavaScript,
reduced motion, missing GSAP/ScrollTrigger, opening replay and Escape, anchors and
history restoration, keyboard focus, image close/focus return, and native video
playback. The first home screen is one viewport. On it the page follows wheel and touch
input directly (with slight drag); on release a damped spring, seeded with the
release velocity, carries it to the nearest page, committing once the coasting
position passes a threshold (`initHeroSnap` in `main.js`). Below the hero,
scrolling is native. Reduced motion turns this off.

Ambient motion stops offscreen, in hidden tabs and with reduced motion. The footer
also has an ambient-motion toggle. The opening animation has an independent
watchdog, so animation-library failure cannot lock scrolling.
