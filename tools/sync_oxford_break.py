"""Copy the built Oxford Break game into play/oxford-break/.

Usage: python tools/sync_oxford_break.py [path-to-oxford-break-repo]
Run `python build.py` in the game repo first; this copies its docs/index.html.
"""
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
game = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT.parent / "oxford-break")
source = game / "docs" / "index.html"
target = ROOT / "play" / "oxford-break" / "index.html"
if not source.is_file():
    raise SystemExit(f"not found: {source}")
target.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(source, target)
print(f"copied {source} -> {target} ({target.stat().st_size // 1024} KB)")
