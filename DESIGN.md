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

## Checks

```powershell
python scripts/check-site.py
node --check assets/js/main.js
python -m http.server 8766 --bind 127.0.0.1
```

Check all pages at 1440, 1024, 390 and 320 pixels. Also verify no JavaScript,
reduced motion, missing GSAP/ScrollTrigger, opening replay and Escape, anchors and
history restoration, keyboard focus, image close/focus return, and native video
playback. The first home screen is one natural viewport; no scroll pinning is used.

Ambient motion stops offscreen, in hidden tabs and with reduced motion. The footer
also has an ambient-motion toggle. The opening animation has an independent
watchdog, so animation-library failure cannot lock scrolling.
