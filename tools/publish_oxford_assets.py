"""Upload only audited, catalogued Oxford assets using the existing Git login.

Credentials remain in memory. This script never prints or persists them.
Requires an already-pushed commit and the private audit directory from the importer.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import time
from pathlib import Path
from urllib.parse import urlsplit

import requests

REPOSITORY = "Jintian-JTST/Jintian-JTST.github.io"
API = "https://api.github.com/repos/" + REPOSITORY


def session() -> requests.Session:
    environment = dict(os.environ, GIT_TERMINAL_PROMPT="0", GCM_INTERACTIVE="never")
    repo = Path(__file__).resolve().parents[1].as_posix()
    credential = subprocess.run(["git", "-c", "safe.directory=" + repo, "credential", "fill"],
                                input="protocol=https\nhost=github.com\n\n", text=True,
                                capture_output=True, env=environment, check=True)
    values = dict(line.split("=", 1) for line in credential.stdout.splitlines() if "=" in line)
    if not values.get("password"):
        raise RuntimeError("No existing GitHub credential is available")
    client = requests.Session()
    client.headers.update({"Authorization": "Bearer " + values["password"],
                           "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"})
    return client


def api(client: requests.Session, method: str, url: str, **kwargs) -> requests.Response:
    if urlsplit(url).hostname not in {"api.github.com", "uploads.github.com"}:
        raise ValueError("Refusing to send GitHub credentials to an unexpected host")
    for attempt in range(4):
        response = client.request(method, url, timeout=(30, 600), **kwargs)
        if response.status_code not in {429, 502, 503, 504}:
            break
        time.sleep(min(20, 2 ** (attempt + 1)))
        if hasattr(kwargs.get("data"), "seek"):
            kwargs["data"].seek(0)
    if not response.ok:
        message = ""
        try:
            message = response.json().get("message", "")
        except ValueError:
            pass
        raise RuntimeError(f"GitHub returned {response.status_code}: {message[:180]}")
    return response


def sha256(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1048576), b""):
            result.update(block)
    return result.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--publish", action="store_true", help="Publish the fully verified draft release")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    work = args.work_dir.resolve()
    catalog = json.loads((repo / "assets/projects/oxford-physics/catalog.json").read_text(encoding="utf-8"))
    tag = catalog["releaseTag"]
    expected = {urlsplit(r["downloadUrl"]).path.rsplit("/", 1)[-1]: {"bytes": r["bytes"], "sha256": r["sha256"]}
                for r in catalog["resources"] if r["storage"] == "release"}
    expected.update({urlsplit(b["url"]).path.rsplit("/", 1)[-1]: b for b in catalog["bundles"]})
    for name, info in expected.items():
        path = work / "release-assets" / name
        if path.stat().st_size != info["bytes"] or sha256(path) != info["sha256"]:
            raise RuntimeError("Audited release asset changed: " + name)
    client = session()
    response = client.get(API + "/releases/tags/" + tag, timeout=30)
    if response.status_code == 404:
        release = api(client, "POST", API + "/releases", json={
            "tag_name": tag, "target_commitish": args.commit,
            "name": "Oxford Physics study collection · " + catalog["updatedAt"],
            "body": "Course materials, personal solutions, experiment data and code linked from the Oxford Physics library.\n\nPersonal solutions are study notes by Jintian Wang; course materials retain their original authorship. Notebooks are distributed with saved outputs and have not been executed.\n\nThe website provides individual reading links; these archives provide grouped downloads.",
            "draft": True, "prerelease": False}).json()
    else:
        response.raise_for_status()
        release = response.json()
    upload_url = release["upload_url"].split("{", 1)[0]
    if urlsplit(upload_url).hostname != "uploads.github.com":
        raise RuntimeError("Unexpected release upload host")
    existing = {}
    for page in range(1, 20):
        batch = api(client, "GET", API + f'/releases/{release["id"]}/assets', params={"per_page": 100, "page": page}).json()
        existing.update({a["name"]: a for a in batch})
        if len(batch) < 100:
            break
    verified = []
    for index, (name, info) in enumerate(expected.items(), 1):
        asset = existing.get(name)
        if asset:
            if asset["size"] != info["bytes"] or (asset.get("digest") and asset["digest"] != "sha256:" + info["sha256"]):
                raise RuntimeError("An existing immutable release asset differs: " + name)
            print(f"Verified existing {index}/{len(expected)}: {name}", flush=True)
        else:
            print(f'Uploading {index}/{len(expected)}: {name} ({info["bytes"]/1048576:.1f} MB)', flush=True)
            with (work / "release-assets" / name).open("rb") as stream:
                asset = api(client, "POST", upload_url, params={"name": name}, data=stream,
                            headers={"Content-Type": "application/octet-stream", "Content-Length": str(info["bytes"])}).json()
            if asset["size"] != info["bytes"] or asset.get("digest") != "sha256:" + info["sha256"]:
                raise RuntimeError("Remote upload digest did not match: " + name)
        verified.append({"name": name, "id": asset["id"], "size": asset["size"], "sha256": info["sha256"], "url": asset["browser_download_url"]})
        (work / "release-upload-progress.json").write_text(json.dumps(verified, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.publish and release["draft"]:
        release = api(client, "PATCH", API + f'/releases/{release["id"]}', json={"draft": False, "make_latest": "false"}).json()
    result = {"id": release["id"], "tag": tag, "draft": release["draft"], "url": release["html_url"], "commit": args.commit, "assets": verified}
    (work / "release-verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"release": result["url"], "draft": result["draft"], "verifiedAssets": len(verified)}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
