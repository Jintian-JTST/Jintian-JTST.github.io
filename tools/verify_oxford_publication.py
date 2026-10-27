"""Verify the exact deployed commit, public resource links and sample downloads."""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import subprocess
import time
from pathlib import Path
from urllib.parse import urlsplit

import requests

from publish_oxford_assets import API, api, session

BASE = "https://jintian-jtst.github.io"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--commit", required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    work = args.work_dir.resolve()
    catalog = json.loads((repo / "assets/projects/oxford-physics/catalog.json").read_text(encoding="utf-8"))
    client = session()
    build = {}
    for attempt in range(60):
        response = client.get(API + "/pages/builds/latest", timeout=30)
        response.raise_for_status()
        build = response.json()
        if build.get("commit") == args.commit and build.get("status") == "built":
            break
        if build.get("commit") == args.commit and build.get("status") == "errored":
            raise RuntimeError("GitHub Pages build failed")
        print(f'Waiting for Pages: {build.get("status")} / commit {str(build.get("commit", ""))[:8]}', flush=True)
        time.sleep(10)
    else:
        raise RuntimeError("Pages did not finish deploying the requested commit")
    tree = api(client, "GET", API + f"/git/trees/{args.commit}", params={"recursive": 1}).json()
    if tree.get("truncated"):
        raise RuntimeError("Remote repository tree was truncated")
    remote = {i["path"]: (i["sha"], i["size"]) for i in tree["tree"] if i["type"] == "blob"}
    command = ["git", "-c", "safe.directory=" + repo.as_posix(), "ls-tree", "-rz", "--long", args.commit]
    raw = subprocess.run(command, check=True, capture_output=True).stdout
    expected = {}
    for entry in raw.split(b"\0"):
        if not entry:
            continue
        info, name = entry.split(b"\t", 1)
        mode, kind, sha, size = info.split()
        if kind == b"blob":
            expected[name.decode("utf-8")] = (sha.decode(), int(size))
    if remote != expected:
        raise RuntimeError("Remote commit tree differs from the verified local commit")
    live_catalog = None
    for attempt in range(24):
        response = requests.get(BASE + "/assets/projects/oxford-physics/catalog.json", params={"v": args.commit[:12]}, timeout=30)
        if response.ok:
            live_catalog = response.json()
            if live_catalog == catalog:
                break
        time.sleep(5)
    if live_catalog != catalog:
        raise RuntimeError("The public catalog does not match the published collection")
    targets = {}
    for resource in catalog["resources"]:
        url = resource["downloadUrl"]
        targets[BASE + url if url.startswith("/") else url] = resource["bytes"]
        view = resource.get("viewUrl")
        if view:
            targets.setdefault(BASE + view if view.startswith("/") else view, None)
    for bundle in catalog["bundles"]:
        targets[bundle["url"]] = bundle["bytes"]
    for name in expected:
        if name.endswith(".html") and not name.startswith("assets/"):
            route = "/" + name
            if route.endswith("index.html"):
                route = route[:-10]
            targets.setdefault(BASE + route, None)
    def head(item):
        url, length = item
        response = requests.head(url, allow_redirects=True, headers={"Accept-Encoding": "identity"}, timeout=45)
        size = response.headers.get("Content-Length")
        result = {"url": url, "status": response.status_code, "expectedBytes": length, "contentLength": int(size) if size else None}
        if response.status_code != 200:
            result["error"] = "Public link is not readable"
        elif length is not None and size is not None and int(size) != length and not response.headers.get("Content-Encoding"):
            result["error"] = "Public size differs from catalog"
        return result
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        checks = list(pool.map(head, targets.items()))
    errors = [r for r in checks if r.get("error")]
    samples = [next(r for r in catalog["resources"] if r.get("featured") == "answers")]
    for kind in ("code", "notebook", "data"):
        samples.append(next(r for r in catalog["resources"] if r["type"] == kind))
    large = [r for r in catalog["resources"] if r["storage"] == "release"]
    if large:
        samples.append(min(large, key=lambda r: r["bytes"]))
    bundle = min(catalog["bundles"], key=lambda b: b["bytes"])
    samples.append({"id": "course-bundle", "downloadUrl": bundle["url"], "sha256": bundle["sha256"], "bytes": bundle["bytes"]})
    sample_results = []
    for sample in samples:
        url = sample["downloadUrl"]
        url = BASE + url if url.startswith("/") else url
        response = requests.get(url, stream=True, headers={"Accept-Encoding": "identity"}, timeout=(30, 180))
        response.raise_for_status()
        sha, size = hashlib.sha256(), 0
        for part in response.iter_content(1048576):
            sha.update(part)
            size += len(part)
        matched = sha.hexdigest() == sample["sha256"] and size == sample["bytes"]
        sample_results.append({"id": sample["id"], "url": url, "sha256": sha.hexdigest(), "bytes": size, "matched": matched})
        if not matched:
            errors.append({"error": "Downloaded sample hash differs", "id": sample["id"]})
    home = requests.get(BASE + "/", params={"v": args.commit[:12]}, timeout=30)
    home.raise_for_status()
    if home.text.replace("\r\n", "\n") != (repo / "index.html").read_text(encoding="utf-8").replace("\r\n", "\n"):
        errors.append({"error": "Live homepage differs from unchanged local homepage"})
    result = {"status": "LIVE_HTTP_OK" if not errors else "FAILED", "commit": args.commit,
              "url": BASE + "/projects/oxford-physics/", "build": {"status": build["status"], "commit": build["commit"]},
              "remoteFilesVerified": len(remote), "publicLinksChecked": len(checks), "resourceCount": len(catalog["resources"]),
              "checks": checks, "downloadSamples": sample_results, "errors": errors}
    (work / "qa/live-http-result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k not in {"checks", "downloadSamples"}}, ensure_ascii=False), flush=True)
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
