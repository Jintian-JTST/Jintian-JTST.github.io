"""Verify the resource inventory, publication copies, links and archive CRCs."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from oxford_privacy import findings


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for part in iter(lambda: stream.read(1048576), b""):
            h.update(part)
    return h.hexdigest()


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.append(values["id"])
        for attribute in ("href", "src"):
            if values.get(attribute):
                self.links.append(values[attribute])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-dir", type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    work = args.work_dir.resolve()
    asset_root = repo / "assets/projects/oxford-physics"
    page_root = repo / "projects/oxford-physics"
    catalog = json.loads((asset_root / "catalog.json").read_text(encoding="utf-8"))
    manifest = json.loads((work / "manifest.json").read_text(encoding="utf-8"))
    errors = []
    assert len({r["id"] for r in catalog["resources"]}) == len(catalog["resources"])
    resources_by_id = {r["id"]: r for r in catalog["resources"]}
    files_checked = 0
    originals_checked = 0
    for resource in catalog["resources"]:
        public = urlsplit(resource["downloadUrl"])
        path = (work / "release-assets" / public.path.rsplit("/", 1)[-1]
                if resource["storage"] == "release" else repo / public.path.lstrip("/"))
        if not path.is_file():
            errors.append("Missing resource: " + resource["id"])
            continue
        if path.stat().st_size != resource["bytes"] or sha256(path) != resource["sha256"]:
            errors.append("Publication copy changed: " + resource["id"])
        if resource["storage"] == "site" and path.stat().st_size > 20 * 1048576:
            errors.append("Large resource incorrectly placed in Pages: " + resource["id"])
        files_checked += 1
    for candidate in manifest["candidates"]:
        if candidate.get("sourceSha256"):
            if sha256(candidate["sourcePath"]) != candidate["sourceSha256"]:
                errors.append("An original changed: " + candidate.get("resourceId", "source"))
            originals_checked += 1
        if candidate["status"] not in {"待发布", "已发布", "重复", "未收录", "待定位", "已展开"}:
            errors.append("Unaccounted inventory status")
        if candidate.get("resourceId") and candidate["resourceId"] not in resources_by_id:
            errors.append("Inventory references an absent resource")
    archive_count = 0
    for bundle in catalog["bundles"]:
        path = work / "release-assets" / urlsplit(bundle["url"]).path.rsplit("/", 1)[-1]
        if sha256(path) != bundle["sha256"]:
            errors.append("Course bundle hash mismatch")
        with zipfile.ZipFile(path) as archive:
            if archive.testzip() is not None:
                errors.append("Course bundle CRC failure")
            for name in archive.namelist():
                if findings(name):
                    errors.append("Private identifier in bundle member name")
        archive_count += 1
    pages = list(page_root.rglob("*.html")) + [repo / "projects/index.html"]
    reference_count = 0
    for path in pages:
        text = path.read_text(encoding="utf-8")
        if findings(text):
            errors.append("Private text in HTML: " + str(path.relative_to(repo)))
        document = References()
        document.feed(text)
        if len(document.ids) != len(set(document.ids)):
            errors.append("Duplicate HTML IDs: " + str(path.relative_to(repo)))
        for ref in document.links:
            parsed = urlsplit(ref)
            if parsed.scheme in {"https", "http", "data", "mailto", "tel"}:
                continue
            if parsed.scheme:
                errors.append("Unexpected link protocol: " + parsed.scheme)
                continue
            if not parsed.path:
                continue
            target = repo / unquote(parsed.path.lstrip("/")) if parsed.path.startswith("/") else path.parent / unquote(parsed.path)
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                errors.append("Broken local reference: " + str(path.relative_to(repo)) + " -> " + ref[:180])
            reference_count += 1
    for path in [asset_root / "catalog.json"]:
        if findings(path.read_text(encoding="utf-8")):
            errors.append("Private text in public catalog")
    css = (asset_root / "math/katex.min.css").read_text(encoding="utf-8")
    for ref in re.findall(r"url\(([^)]+)\)", css):
        if not (asset_root / "math" / ref.strip("\"'")).is_file():
            errors.append("Missing KaTeX font: " + ref)
    site_bytes = sum(p.stat().st_size for p in repo.rglob("*") if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts)
    if site_bytes > 750 * 1048576:
        errors.append("Pages publication exceeds the 750 MiB budget")
    book = next(r for r in catalog["resources"] if r.get("featured") == "answers")
    if book["pages"] != 183 or not book["viewUrl"]:
        errors.append("User-specified revised answer book is missing or unreadable")
    course_links = sum(len(r.get("related", [])) for r in catalog["resources"])
    if course_links == 0:
        errors.append("No problem-sheet / personal-answer links were generated")
    result = {"status": "STATIC_QA_OK" if not errors else "FAILED", "resources": files_checked,
              "originalsUnchanged": originals_checked, "htmlPages": len(pages), "localReferences": reference_count,
              "archivesCRCChecked": archive_count, "problemAnswerLinks": course_links, "siteMB": round(site_bytes / 1048576, 1),
              "counts": dict(Counter(c["status"] for c in manifest["candidates"])), "errors": errors}
    (work / "qa/static-result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False), flush=True)
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
