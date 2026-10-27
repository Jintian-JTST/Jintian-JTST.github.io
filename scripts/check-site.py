"""Check static entry points and their local links without third-party packages."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.refs = []
        self.h1_count = 0
        self.images_without_alt = 0

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "h1":
            self.h1_count += 1
        if tag == "img" and "alt" not in attrs:
            self.images_without_alt += 1
        name = "href" if tag in {"a", "link"} else "src"
        if tag in {"a", "link", "script", "img", "source", "iframe"} and attrs.get(name):
            self.refs.append(attrs[name])


def resolve(source, reference):
    url = urlsplit(reference)
    if url.scheme or url.netloc:
        return None, None
    path = unquote(url.path)
    target = ROOT / path.lstrip("/") if path.startswith("/") else source.parent / path
    if not path:
        target = source
    if target.is_dir():
        target /= "index.html"
    return target.resolve(), unquote(url.fragment)


def main():
    pages = {}
    problems = []
    paths = [ROOT / "index.html", ROOT / "about/index.html", ROOT / "contact/index.html"]
    paths.extend(sorted((ROOT / "projects").rglob("index.html")))
    for path in paths:
        page = Page()
        content = path.read_text(encoding="utf-8-sig")
        page.feed(content)
        pages[path.resolve()] = page
        label = path.relative_to(ROOT)
        if page.h1_count != 1:
            problems.append(f"{label}: expected one h1, found {page.h1_count}")
        if len(set(page.ids)) != len(page.ids):
            problems.append(f"{label}: duplicate element ids")
        if page.images_without_alt:
            problems.append(f"{label}: images missing alt text")
        if "\ufffd" in content:
            problems.append(f"{label}: replacement character in source")
    ref_count = 0
    for source, page in pages.items():
        for reference in page.refs:
            target, fragment = resolve(source, reference)
            if target is None:
                continue
            ref_count += 1
            if not target.is_relative_to(ROOT):
                problems.append(f"{source.relative_to(ROOT)}: reference escapes site root: {reference}")
            elif not target.is_file():
                problems.append(f"{source.relative_to(ROOT)}: missing {reference}")
            elif fragment and target in pages and fragment not in pages[target].ids:
                problems.append(f"{source.relative_to(ROOT)}: missing anchor {reference}")
    css = ROOT / "assets/css/styles.css"
    url_pattern = r'''url\(\s*(?:"([^"]*)"|'([^']*)'|([^'"\)\s]+))\s*\)'''
    for match in re.finditer(url_pattern, css.read_text(encoding="utf-8-sig")):
        reference = next(value for value in match.groups() if value is not None)
        if reference.startswith("data:"):
            continue
        target, _ = resolve(css, reference)
        if target is not None and not target.is_file():
            problems.append(f"styles.css: missing {reference}")
    if problems:
        print("\n".join(problems))
        return 1
    print(f"STATIC_QA_OK pages={len(pages)} local_refs={ref_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
