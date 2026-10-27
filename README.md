# Jintian JTST

Personal website for Jintian Wang, built as a plain static site and published with GitHub Pages.

## Structure

- `index.html` — home
- `projects/` — a compact directory of research, interactive systems/software, and learning experiments
- `projects/oxford-physics/` — a searchable Oxford Physics study library, including personal solutions, course material, past papers, and lab code
- `about/` — Oxford academic identity, research interests, and selected experience
- `contact/` — public contact links
- `assets/projects/` — curated Proof of Work media and reports
- `assets/cv/` — public research CV, with private contact details removed

Project assets are selected for publication rather than copied wholesale. See `assets/projects/README.md` for evidence and privacy status.

The Oxford study collection is a separately curated academic archive. Its directory works without JavaScript; filtering progressively enhances the static file list. The revised first-year answer book is labelled as personal work by Jintian Wang. Small files are served by Pages; large files and grouped downloads are immutable GitHub Release assets. Markdown, saved notebooks and source code have static reading pages. Notebook code is never executed during import.

To refresh the collection, run `tools/build_oxford_library.py` with explicit `--source`, `--downloads`, `--work-dir` and `--date` arguments. The private work directory must be outside this checkout. Review its inventory and pending items, then run `tools/check_oxford_library.py --work-dir <private-directory>` and browser QA before publication. The private inventory contains original file paths and must not be committed. `tools/publish_oxford_assets.py` uploads only catalogued, hash-checked files using the existing Git credential manager; credentials are never persisted or printed. Original source files are never modified.

The homepage features Muon g-2 / PSXM research, SecondTouchReality, and OneTapReality. The logo opening sequence auto-exits, supports Escape, and is skipped with reduced motion or JavaScript disabled.

## Content ownership

Home introduces selected work; About holds the biography and experience timeline; project pages hold methods, contributions and evidence. Contact is the full profile directory, including the Oxford email and ORCID. Short previews link to these pages instead of repeating complete descriptions.

The compound-pendulum page uses the existing curated photographs and plots. Its candidate-numbered report is not published. Transformer and MiniMind material is labelled as learning work, with no completed-model claim.
