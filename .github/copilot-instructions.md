# Copilot Instructions for Jintian-JTST.github.io

## Big picture architecture
- This repo is a plain static GitHub Pages site (no framework, no bundler, no Jekyll).
- Each section is a folder with `index.html` (e.g., `about/`, `projects/`, `blog/`, `contact/`).
- `index.html` (root) is the custom homepage with a scroll-reveal hero animation.
- Shared presentation logic is centralized in:
  - `assets/css/styles.css` (global theme + layout + responsive behavior)
  - `assets/js/main.js` (nav active state, dynamic year, homepage reveal behavior)

## Structural patterns to preserve
- Keep site-wide links root-absolute (`/about/`, `/assets/css/styles.css`) rather than relative paths.
- Keep trailing slashes on section URLs (`/blog/` not `/blog`) to match current routing and `main.js` nav matching.
- Reuse the existing page shell on all pages:
  1) `<header class="navbar">` with the same nav links
  2) main content block (`.section`, `.card`, `.article`, etc.)
  3) footer with `<span data-year></span>`
  4) `<script src="/assets/js/main.js"></script>`
- Home-only animation depends on `body.home-page`; do not add this class to non-home pages.

## Content and component conventions
- Blog index is a list of article cards; each post lives in its own folder under `blog/<slug>/index.html`.
- To add a post, copy an existing post folder (for example `blog/experiment-notes/`) and update title, meta text, and body.
- Visual vocabulary is class-based and reused (`.container`, `.grid-2`, `.grid-3`, `.card`, `.badges`, `.badge`, `.meta`).
- Keep naming lowercase with hyphens for folders/slugs.

## Developer workflow (project-specific)
- No build step, transpile step, or package manager is used.
- Local preview is via the VS Code task `preview site` (Python HTTP server on `127.0.0.1:8000`).
- Deployment model is push static files directly to GitHub Pages.
- There is no test suite in this repo; validation is manual page-checking in browser.

## Integration points / external dependencies
- Static assets are served from `assets/` (`css/`, `js/`, `images/`).
- `_headers` defines cache headers (`Cache-Control: no-cache`) for hosting setups that honor it.
- External links currently exist in contact badges; keep them as normal anchor tags.

## Interaction and animation standard (must keep consistent)
- Use the existing motion language in `assets/css/styles.css`; do not introduce a second animation system for inner pages.
- Canonical interactions to reuse:
  - Links/buttons: `160ms ease` hover/focus transitions.
  - Cards/panels: `200–220ms` transitions with `cubic-bezier(0.2, 0.7, 0.2, 1)` and subtle lift/glow.
  - Homepage only: scroll-driven reveal via `--home-reveal` in `assets/js/main.js` + `body.home-page`.
- Interaction baseline: when hovering/focusing interactive buttons or cards, they should lift slightly (`translateY(...)`) and show accent glow (consistent with existing `rgba(92,219,213,...)` shadows).
- For clickable cards, reuse the homepage pattern: `class="card card-link"` (do not invent parallel card hover classes).
- If adding new interactive UI, match existing glow color and elevation style (`rgba(92,219,213,...)`, `var(--shadow)`).
- Do not add global scroll-reveal/fade-in observers for all pages unless explicitly requested; keep non-home pages motion-light.

## Editing guidance for AI agents
- Prefer small, surgical edits; avoid reformatting whole HTML files.
- When changing shared behavior, update both CSS and JS consistently (especially homepage reveal variables/classes).
- If introducing a new section/page, mirror existing nav/footer structure so `main.js` features continue to work.