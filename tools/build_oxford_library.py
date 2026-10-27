"""Import an explicitly selected local Oxford collection into this static site.

Usage: python tools/build_oxford_library.py --source <Oxford directory>
       --downloads <Downloads directory> --work-dir <private audit directory>
       --date YYYY-MM-DD

Dependencies: PyMuPDF, mistune, Pillow. No source notebooks or scripts are executed.
The work directory MUST be outside the Git checkout: it contains private source paths.
"""
from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import html
import io
import json
import os
import re
import shutil
import tarfile
import zipfile
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

import fitz
import mistune

from oxford_privacy import clean_text, findings, inspect_pdf, redact_pdf, scrub_notebook, scrub_office
from oxford_ui import ASSETS, ROOT, TYPES, esc, reading_page, write_directory

DOWNLOAD_PATTERN = re.compile(
    r"(?:\bcp[1-4]\b|^cp[1-4][_ -]|prelim|^a1028[5789]|^a14119|calculusht|^da01|^el02|^gp49|"
    r"^mmps|normal.?modes|lvovsky|^numericalproblemset.*cp1|牛津物理.*cp1|^oxford[_ -]cp1|^oxford_yr1_answers)", re.I)
ACCEPTED = {".pdf", ".ipynb", ".py", ".m", ".md", ".tex", ".txt", ".csv", ".xlsx", ".png", ".jpg", ".jpeg", ".svg", ".docx", ".doc", ".cap", ".asv"}
ARCHIVES = {".zip", ".tgz", ".gz"}
CODE_EXTS = {".py", ".m", ".tex", ".asv"}
COURSE_NAMES = {"CP1": "Classical Mechanics & Special Relativity", "CP2": "Electricity, Magnetism & Optics", "CP3": "Mathematical Methods", "CP4": "Calculus, Normal Modes & Waves", "MM": "Mathematical Methods", "EM": "Electromagnetism", "ST": "Statistics", "TM": "Thermal Physics"}
PAPER_CODES = {"A10287": "CP1", "A10288": "CP2", "A10285": "CP3", "A10289": "CP4", "A14119": "SO"}
MARKDOWN = mistune.create_markdown(escape=True, plugins=["table", "math", "strikethrough"])


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1048576), b""):
            h.update(chunk)
    return h.hexdigest()


def decode(data: bytes) -> str:
    for encoding in ("utf-8-sig", "gb18030", "cp1252"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            pass
    return data.decode("utf-8", errors="replace")


def slug(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value[:75].rstrip("-") or "resource"


def allowed(relative: str) -> tuple[bool, str]:
    parts = PurePosixPath(relative).parts
    if not parts:
        return False, "不属于学习资料"
    if parts[0] == ".yr1":
        if len(parts) == 2 and parts[1] == "HT.md":
            return True, ""
        if len(parts) > 2 and parts[1] in {"CP1", "CP2", "CP3", "CP4", "LAB", "Prelims", "SepPre"}:
            return True, ""
        return False, "行政/迎新材料，或已展开的重复课程包"
    if parts[0] == ".yr2" and len(parts) > 2:
        return True, ""
    if parts[0] == "freshman" and len(parts) > 2 and parts[1] in {"CP", "all"}:
        return True, ""
    if parts[0] == "matlab":
        return True, ""
    return False, "入学、行政或其他非课程材料"


def discover(source: Path, downloads: Path, work: Path) -> list[dict]:
    candidates = []
    paths = []
    for current, directories, names in os.walk(source):
        directories[:] = [d for d in directories if d not in {"societies", ".git", "node_modules", "__pycache__"}]
        paths.extend(Path(current) / name for name in names)
    for path in sorted(paths):
        rel = path.relative_to(source).as_posix()
        if rel.startswith("societies/"):
            continue
        accept, reason = allowed(rel)
        candidates.append({"sourcePath": str(path), "logicalPath": rel, "scope": "Oxford", "eligible": accept,
                           "reason": reason, "originalBytes": path.stat().st_size})
    for path in sorted(downloads.iterdir()):
        if not path.is_file() or not DOWNLOAD_PATTERN.search(path.name):
            continue
        administrative = bool(re.search(r"prizes|commendation|scholarship|application|certificate|invoice", path.name, re.I))
        candidates.append({"sourcePath": str(path), "logicalPath": "Downloads/" + path.name, "scope": "Downloads",
                           "eligible": not administrative, "reason": "个人行政/奖项信件" if administrative else "",
                           "originalBytes": path.stat().st_size})
    # Record native notebooks honestly rather than claiming their unexported contents were imported.
    notebook_root = downloads.parent / "Documents" / "OneNote 笔记本"
    if notebook_root.is_dir():
        for path in sorted(notebook_root.rglob("*.one")):
            candidates.append({"sourcePath": str(path), "logicalPath": path.name, "scope": "OneNote",
                               "eligible": False, "reason": "原生 OneNote 文件，尚未确认学术内容；如需收录须先导出", "status": "待定位",
                               "originalBytes": path.stat().st_size})
    expanded = []
    for candidate in candidates:
        path = Path(candidate["sourcePath"])
        if candidate["logicalPath"] == "matlab/CO_Prelims_CO6_Template.doc":
            conversions = [work / "converted" / ("CO6-submission-template" + ext) for ext in (".docx", ".pdf")]
            if all(p.exists() for p in conversions):
                candidate.update(eligible=False, status="未收录", sourceSha256=digest(path),
                                 reason="原始 DOC 含账号标识；已以清理后的 DOCX 和 PDF 转换版收录，原件保留")
                for converted in conversions:
                    expanded.append({"sourcePath": str(converted), "derivedFrom": str(path), "scope": "converted",
                                     "logicalPath": "matlab/CO6-template/" + converted.name, "eligible": True,
                                     "reason": "旧版 Word 的公开转换副本", "originalBytes": converted.stat().st_size})
                continue
        if not candidate["eligible"] or path.suffix.lower() not in ARCHIVES:
            continue
        try:
            archive_hash = digest(path)
            candidate["sourceSha256"] = archive_hash
            folder = work / "unpacked" / archive_hash[:16]
            entries = []
            if path.suffix.lower() == ".zip":
                with zipfile.ZipFile(path) as archive:
                    if archive.testzip() is not None:
                        raise ValueError("ZIP CRC 校验失败")
                    entries = [(i.filename, archive.read(i)) for i in archive.infolist() if not i.is_dir()]
            else:
                with tarfile.open(path) as archive:
                    entries = [(i.name, archive.extractfile(i).read()) for i in archive.getmembers() if i.isfile()]
            if len(entries) > 2000 or sum(len(b) for _, b in entries) > 1024**3:
                raise ValueError("压缩包超过预定课程导入范围")
            for name, data in entries:
                member = PurePosixPath(name.replace("\\", "/"))
                if member.is_absolute() or ".." in member.parts or ":" in name or "__MACOSX" in member.parts:
                    continue
                if member.suffix.lower() not in ACCEPTED:
                    continue
                target = folder.joinpath(*member.parts)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                expanded.append({"sourcePath": str(target), "archiveSource": str(path), "archiveMember": member.as_posix(),
                                 "logicalPath": str(PurePosixPath(candidate["logicalPath"]).parent / path.stem / member),
                                 "scope": candidate["scope"], "eligible": True, "reason": "", "originalBytes": len(data)})
            candidate.update(eligible=False, status="已展开", reason="压缩包已逐项审核；其中课程文件及代码分别收录，并提供清理后的课程打包下载")
        except Exception as error:
            candidate.update(eligible=False, status="待定位", reason=f"压缩包读取失败：{type(error).__name__}")
    return candidates + expanded


def metadata(candidate: dict, first_page: str = "") -> dict:
    logical = candidate["logicalPath"]
    path = PurePosixPath(logical)
    name = path.name
    low = logical.lower()
    stage = "year1" if logical.startswith((".yr1/", "matlab/", "freshman/CP/")) else "other"
    if logical.startswith(".yr2/"):
        stage = "year2"
    course = "Physics"
    code_match = re.search(r"(?i)(?:^|[/ _-])(CP[1-4])(?:[ /_-]|$)", logical)
    if code_match:
        course = code_match.group(1).upper()
        stage = "year1"
    for code, label in PAPER_CODES.items():
        if code.lower() in name.lower():
            course, stage = label, "year1"
    if logical.startswith(".yr2/") and "/LAB/" not in logical:
        course = path.parts[1]
    if "/LAB/" in logical:
        after = logical.split("/LAB/", 1)[1]
        course = after.split("/")[0] if "/" in after else "Lab methods"
    if logical.startswith("matlab/"):
        course = "MATLAB"
    if logical.startswith("freshman/all/"):
        folder = path.parts[2]
        course = folder.split("-", 1)[0].upper() if folder != ".handbooks" else "Handbooks"
        stage = "year1" if course.startswith("P") else "year2" if course.startswith("A") else "other"
    if "organized_papers/SO/" in logical or re.search(r"(?i)short.option|so_prelims|^sp_", name):
        course = "SO"
    if course == "Physics":
        inferred = re.search(r"(?i)\b(?:CP[1-4])\b", first_page[:800])
        if inferred:
            course, stage = inferred.group().upper(), "year1"
        elif name.startswith("CalculusHT"):
            course, stage = "CP4", "year1"
        elif name.startswith(("DA01", "EL02", "GP49")):
            course = name[:4]
            stage = "year2" if course == "GP49" else "year1"
    ext = path.suffix.lower()
    kind = "lecture"
    if ext in CODE_EXTS:
        kind = "code"
    elif ext == ".ipynb":
        kind = "notebook"
    elif ext in {".csv", ".xlsx", ".cap"}:
        kind = "data"
    elif ext in {".png", ".jpg", ".jpeg", ".svg"}:
        kind = "image"
    elif ext in {".md", ".txt"}:
        kind = "revision"
    elif "handbook" in low or ".handbooks" in low:
        kind = "handbook"
    elif re.search(r"mock|模拟", name, re.I):
        kind = "mock"
    elif re.search(r"marking.?report|examiner.?report|chairs.?report|阅卷", name, re.I):
        kind = "feedback" if "chairs" not in low and "examiner" not in low else "revision"
    elif name == "SelectedProblems.pdf":
        kind = "selected"
    elif name == "notes.pdf" and "/SO/" in logical:
        kind = "revision"
    elif "/Prelims/" in logical or "/SepPre/" in logical or re.search(r"(?i)(?:cp[1-4]|a1028[5789]).*(?:june|jun_|sept|sep\d)", name):
        kind = "past-paper"
    elif re.search(r"(?i)(?:_sol(?:[_. -]|\d)|solution|answer.?key)", name):
        kind = "official-solution"
    elif re.search(r"(?i)ps[ _-]?\d|problem|probs|questions|(?:^|[-_])ps(?:[._-]|$)", name):
        kind = "problem"
    elif re.search(r"revision|cheat|review|复习", name, re.I):
        kind = "revision"
    elif "/LAB/" in logical:
        kind = "lab-manual"
    if re.search(r"JINTIAN.?WANG|GP04me|^EL02 \(1\)\.pdf|^GP49\.pdf|^op13\.docx|^report\.txt", name, re.I):
        kind = "personal-solution" if "CP1" in name else "report"
    featured = None
    title = clean_text(path.stem).replace("_", " ")
    title = re.sub(r"\s+", " ", title).strip()
    if name == "Oxford_YR1_Answers_Revised.pdf":
        title, kind, course, stage, featured = "大一习题答案合集（修订版）", "personal-solution", "CP1–CP4", "year1", "answers"
    elif name == "CP1 PS2 JINTIAN WANG_compressed.pdf":
        title = "CP1 · Classical Mechanics · PS2 手写解答"
    elif name == "GP04me.pdf":
        title = "GP04 · Driven Oscillations · 手写实验记录"
    elif name == "EL02 (1).pdf":
        title = "EL02 · LCR Circuits · 手写实验记录"
    elif name == "JINTIAN WANG.pdf":
        title = "OP13 · Rydberg Constant · 个人实验报告"
    elif name == "selected_questions.csv":
        title, kind, course, featured = "我的历年试卷选题清单", "selected", "Prelims", "selected"
    elif name == "selected_pages.csv":
        title, kind, course = "历年试卷选页清单", "selected", "Prelims"
    elif name == "HT.md":
        title, kind, course = "Hilary Term · 物理与数学复习笔记", "revision", "CP1–CP4"
    elif name.startswith("CO6-submission-template"):
        title, kind, course = "CO65 · Monte Carlo Integration · 个人报告", "report", "MATLAB"
    if candidate["scope"] == "Downloads" and name in {"CP3_June2021.pdf", "CP2-Jun_2025.pdf"}:
        # Visually reviewed: these are handwritten answer sets, not exam papers.
        # The author is not stated, so do not attribute them to the student or university.
        kind = "reference-solution"
        title += " · 手写参考解答"
    exam_year, session = None, ""
    if kind in {"past-paper", "reference-solution"}:
        # Only explicit dates on the actual paper are accepted as exam years.
        head = first_page[:5000]
        date_match = re.search(r"(?i)\b(June|September|Sept(?:ember)?|Jun|Sep)\.?\s*(20\d{2}|19\d{2})\b", head)
        if not date_match:
            date_match = re.search(r"(?i)\b(June|September|Sept|Jun|Sep)\.?[ _-]*(20\d{2}|19\d{2})\b", name)
        if date_match:
            exam_year = int(date_match.group(2))
            session = "September" if date_match.group(1).lower().startswith("sep") else "June"
        else:
            explicit = re.search(r"\b(20\d{2}|19\d{2})\b", head)
            if explicit:
                exam_year = int(explicit.group(1))
        if not session:
            session = "September" if "/SepPre/" in logical else "June" if "/Prelims/" in logical else ""
        if exam_year:
            title = f"{exam_year} · {course} · {session or 'Examination'}" + (" · 手写参考解答" if kind == "reference-solution" else "")
    categories = [stage]
    if kind in {"past-paper", "reference-solution"} or "/Prelims/" in logical or "/SepPre/" in logical:
        categories.append("exams")
    if kind in {"personal-solution", "report", "feedback", "selected"}:
        categories.append("mine")
    if "/LAB/" in logical or logical.startswith("matlab/") or kind in {"code", "notebook", "data"}:
        categories.append("lab")
    if kind == "image" and "/SelectedProblems/" in logical:
        categories.append("mine")
    result = {"title": title, "course": course, "courses": ["CP1", "CP2", "CP3", "CP4"] if course == "CP1–CP4" else [course], "stage": stage, "type": kind, "categories": sorted(set(categories)),
              "examYear": exam_year, "session": session, "originalName": clean_text(name), "format": ext[1:].upper(), "featured": featured}
    if featured == "answers":
        result["chapters"] = [{"label": "CP1 · Mechanics", "page": 3}, {"label": "CP2 · E&M / Optics", "page": 54}, {"label": "CP3 · Methods", "page": 104}, {"label": "CP4 · Calculus / Waves", "page": 143}]
    return result


def text_preview(resource: dict, path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".ipynb":
        notebook = json.loads(path.read_text(encoding="utf-8"))
        cells = []
        for cell in notebook.get("cells", []):
            source = cell.get("source", "")
            source = "".join(source) if isinstance(source, list) else source
            content = MARKDOWN(source) if cell.get("cell_type") == "markdown" else f'<pre><code>{esc(source)}</code></pre>'
            for output in cell.get("outputs", []):
                data = output.get("data", {})
                if "image/png" in data:
                    encoded = data["image/png"]
                    encoded = "".join(encoded) if isinstance(encoded, list) else encoded
                    # Reject arbitrary markup masquerading as a data image.
                    try:
                        raw = base64.b64decode(encoded, validate=False)
                        if raw.startswith(b"\x89PNG\r\n\x1a\n"):
                            content += f'<div class="notebook-output"><img src="data:image/png;base64,{base64.b64encode(raw).decode()}" alt="Notebook 中保存的图表" loading="lazy"></div>'
                    except ValueError:
                        pass
                output_text = output.get("text", data.get("text/plain", ""))
                output_text = "".join(output_text) if isinstance(output_text, list) else output_text
                if output_text:
                    content += f'<pre class="notebook-output">{esc(output_text)}</pre>'
            cells.append(f'<section class="notebook-cell">{content}</section>')
        return '<p class="library-noscript">静态 Notebook 阅读页：展示保存的代码和输出，未重新运行。</p>' + "".join(cells)
    text = decode(path.read_bytes())
    if ext == ".md":
        return MARKDOWN(text)
    if ext == ".csv":
        rows = list(csv.reader(io.StringIO(text)))
        shown = rows[:201]
        table = ''.join('<tr>' + ''.join(f'<{"th" if i == 0 else "td"}>{esc(c)}</{"th" if i == 0 else "td"}>' for c in row) + '</tr>' for i, row in enumerate(shown))
        return f'<p>文本预览 · {max(0,len(rows)-1)} 行数据。超过 200 行时，请下载完整文件。</p><div class="reading-table"><table>{table}</table></div>'
    lines = text.splitlines()
    truncated = len(lines) > 1000 or len(text) > 150000
    preview = "\n".join(lines[:1000])[:150000]
    notice = '<p>当前显示文件开头，完整内容请下载。</p>' if truncated else ''
    return notice + f'<pre><code>{esc(preview)}</code></pre>'


def link_attachments(content: str, source_path: Path, source_map: dict) -> str:
    def replace(match):
        attr, value = match.group(1), html.unescape(match.group(2))
        if value.startswith(("https://", "http://", "data:", "#", "/assets/", "/projects/")):
            return match.group()
        local = source_path.parent / unquote(value.split("#", 1)[0])
        linked = source_map.get(str(local.resolve()).casefold())
        if linked:
            suffix = "#" + value.split("#", 1)[1] if "#" in value else ""
            return f'{attr}="{esc(linked["downloadUrl"] + suffix)}"'
        # Unknown local references remain text instead of broken local-file links.
        return 'data-unavailable-attachment="true"'
    return re.sub(r'(href|src)="([^"]+)"', replace, content)


def book_preview(resource: dict, source: Path) -> str:
    with fitz.open(source) as doc:
        chapters = [(title, page) for level, title, page in doc.get_toc() if level == 2]
    clean_chapters = [(re.sub(r"^\d+\.\d+\s+", "", title), page) for title, page in chapters]
    toc = ''.join(f'<li><a href="{esc(resource["downloadUrl"])}#page={page}">{esc(title)}<span> · p. {page}</span></a></li>' for title, page in clean_chapters)
    return f'''<p>Jintian Wang 的个人习题解答与计算笔记 · 修订版。内容供学习参考。</p>
      <p><a class="button primary" href="{esc(resource['downloadUrl'])}">打开完整 PDF · {resource['pages']} 页 ↗</a></p>
      <details open><summary>按题单跳转</summary><ol class="answers-toc">{toc}</ol></details>
      <iframe class="pdf-embed" title="大一习题答案合集 PDF" src="{esc(resource['downloadUrl'])}#view=FitH" loading="lazy"></iframe>
      <p>若设备未显示内嵌 PDF，请使用上方“打开完整 PDF”或下载链接。</p>'''


def selected_preview(resource: dict, candidate: dict, resources: list[dict], source_map: dict) -> tuple[str, int]:
    rows = list(csv.DictReader(io.StringIO(decode(Path(candidate["sourcePath"]).read_bytes()))))
    by_paper = defaultdict(list)
    for item in rows:
        by_paper[item["file"]].append(item)
    source_dir = Path(candidate["sourcePath"]).parent
    paper_map = {}
    for item in resources:
        if item["type"] == "past-paper":
            for alias in item.get("aliases", []):
                paper_map[Path(alias).stem.casefold()] = item
    groups = []
    for paper, questions in by_paper.items():
        original = paper_map.get(paper.casefold())
        heading = esc(paper.replace("_", " "))
        if original:
            heading = f'<a href="{esc(original["downloadUrl"])}">{heading} ↗</a>'
        links = []
        used = set()
        for item in questions:
            page = item.get("page", "")
            question = item.get("question", "")
            key = (page, question)
            if key in used:
                continue
            used.add(key)
            label = f'第 {page} 页' + (f' · Q{question}' if question else '')
            image_path = source_dir / ("images" if "question" in item else "pages") / item.get("image", "")
            image = source_map.get(str(image_path.resolve()).casefold())
            target = image.get("viewUrl") if image else original["downloadUrl"] + "#page=" + page if original else None
            links.append(f'<a href="{esc(target)}">{esc(label)}</a>' if target else f'<span>{esc(label)}（原附件待定位）</span>')
        groups.append(f'<section class="selection-paper"><h2>{heading}</h2><div class="selection-questions">{"".join(links)}</div></section>')
    return f'<p>从保存的选题清单整理，共 {len(rows)} 条记录。点击题号查看选题图片；点击试卷标题打开原卷。</p>' + "".join(groups), len(rows)


def relate(resources: list[dict], private_resources: dict | None = None) -> None:
    book = next((r for r in resources if r.get("featured") == "answers"), None)
    if not book:
        return
    book_doc = fitz.open(private_resources[book["id"]]["preparedPath"]) if private_resources else None
    for resource in resources:
        if resource["type"] != "problem" or resource["course"] not in {"CP1", "CP2", "CP3", "CP4"}:
            continue
        name = resource["originalName"].lower()
        course = resource["course"]
        page = None
        number = re.search(r"(?:ps|sheet|set)[ _-]?(\d)", name)
        n = int(number.group(1)) if number else None
        if course == "CP1":
            if "sr" in name or "relativ" in name:
                page = {1: 45, 2: 50}.get(n)
            elif "mechanic" in name or " cm" in name:
                page = {0: 3, 1: 7, 2: 13, 3: 19, 4: 25, 5: 31, 6: 36}.get(n)
        elif course == "CP2":
            if "circuit" in name:
                page = 54
            elif "em" in name and "problem" in name:
                page = 70
            elif "geom" in name:
                page = 94
            elif "wave" in name and "opt" in name:
                page = 99
        elif course == "CP3":
            if "complex" in name:
                page = 104
            elif "ode" in name:
                page = {1: 108, 2: 112, 3: 115, 4: 119}.get(n)
            elif "vm" in name or "v&m" in name:
                page = {1: 122, 2: 128, 3: 133, 4: 138}.get(n)
        elif course == "CP4":
            if "nm" in name or "normal" in name:
                page = 169
            elif " mv " in name or " mc " in name or "calculusht_ps" in name:
                page = {1: 157, 2: 160, 3: 163, 4: 166}.get(n, 157)
            elif "calculus_problem" in name or " cl " in name:
                page = 143
        if page and private_resources and book_doc:
            private = private_resources[resource["id"]]
            cache_dir = Path(private["preparedPath"]).parent.parent / "scans"
            cache = cache_dir / (private["candidate"]["sourceSha256"] + ".json")
            if cache.is_file():
                question_text = json.loads(cache.read_text(encoding="utf-8")).get("first_page", "")
                answer_text = book_doc[page - 1].get_text() + book_doc[min(page, len(book_doc) - 1)].get_text()
                generic = {"classical", "mechanics", "electricity", "magnetism", "mathematical", "methods", "calculus", "waves", "oxford", "university", "physics", "department", "problem", "problems", "sheet", "sheet", "page", "questions"}
                def phrases(text):
                    words = re.findall(r"[a-z]+", text.casefold())
                    return {tuple(words[i:i+4]) for i in range(max(0,len(words)-3))
                            if any(len(w) > 4 and w not in generic for w in words[i:i+4])}
                if len(phrases(question_text) & phrases(answer_text)) < 2:
                    page = None
            else:
                page = None
        if page:
            resource.setdefault("related", []).append({"label": "对应个人解答 ↗", "url": book["downloadUrl"] + f"#page={page}"})
    if book_doc:
        book_doc.close()


def refresh_pages(repo: Path, work: Path) -> None:
    """Reapply reviewed catalog labels and links without recopying source files."""
    catalog_path = repo / ASSETS.lstrip("/") / "catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    manifest_path = work / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    private_resources = manifest["resources"]
    for resource in catalog["resources"]:
        private = private_resources[resource["id"]]
        candidate = private["candidate"]
        cache = work / "scans" / (candidate["sourceSha256"] + ".json")
        scan = json.loads(cache.read_text(encoding="utf-8")) if cache.exists() else {}
        resource.update(metadata(candidate, scan.get("first_page", "")))
        resource.pop("related", None)
    relate(catalog["resources"], private_resources)
    source_map = {}
    for resource in catalog["resources"]:
        for candidate in private_resources[resource["id"]]["sources"]:
            source_map[str(Path(candidate["sourcePath"]).resolve()).casefold()] = resource
    for resource in catalog["resources"]:
        if not resource.get("viewUrl", "") or not resource["viewUrl"].startswith(ROOT + "read/"):
            continue
        private = private_resources[resource["id"]]
        candidate = private["candidate"]
        path = Path(private["preparedPath"])
        if resource.get("featured") == "answers":
            content = book_preview(resource, path)
        elif resource["type"] == "selected" and path.suffix == ".csv":
            content, amount = selected_preview(resource, candidate, catalog["resources"], source_map)
            if resource.get("featured") == "selected":
                catalog["selectionCount"] = amount
        else:
            content = text_preview(resource, path)
        content = link_attachments(content, Path(candidate["sourcePath"]), source_map)
        math_head = f'<link rel="stylesheet" href="{ASSETS}math/katex.min.css"><script defer src="{ASSETS}math/katex.min.js"></script><script defer src="{ASSETS}math/auto-render.min.js"></script><script defer src="{ASSETS}math-render.js"></script>'
        output = repo / "projects/oxford-physics/read" / (resource["id"] + ".html")
        output.write_text(reading_page(resource, content, extra_head=math_head), encoding="utf-8")
    catalog["resources"].sort(key=lambda r: (0 if r.get("featured") == "answers" else 1 if r.get("featured") == "selected" else 2,
                                             {"year1": 0, "year2": 1, "other": 2}[r["stage"]], r["course"],
                                             TYPES[r["type"]], -(r.get("examYear") or 0), r["title"].casefold()))
    for bundle in catalog["bundles"]:
        if "/oxford-prelims-" in bundle["url"]:
            bundle["title"] = "历年试卷与参考解答"
    manifest["bundles"] = catalog["bundles"]
    catalog_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    write_directory(repo, catalog)
    print(json.dumps({"catalogRefreshed": len(catalog["resources"]), "verifiedProblemAnswerLinks": sum(len(r.get("related", [])) for r in catalog["resources"])}, ensure_ascii=False), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--downloads", type=Path)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--date")
    parser.add_argument("--refresh-pages", action="store_true")
    parser.add_argument("--reuse-audited-copies", action="store_true", help="Reuse unchanged copies from the previous private audit, with SHA-256 verification")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    if args.refresh_pages:
        refresh_pages(repo, args.work_dir.resolve())
        return
    if not args.source or not args.downloads or not args.date:
        parser.error("--source, --downloads and --date are required for an import")
    source, downloads, work = args.source.resolve(), args.downloads.resolve(), args.work_dir.resolve()
    if work == repo or repo in work.parents:
        raise SystemExit("Private work directory must be outside the public checkout")
    work.mkdir(parents=True, exist_ok=True)
    for folder in ("scans", "prepared", "release-assets", "qa"):
        (work / folder).mkdir(exist_ok=True)
    public = repo / ASSETS.lstrip("/")
    files = public / "files"
    readers = repo / "projects/oxford-physics/read"
    files.mkdir(parents=True, exist_ok=True)
    readers.mkdir(parents=True, exist_ok=True)
    candidates = discover(source, downloads, work)
    previous = {}
    previous_manifest = work / "manifest.json"
    if args.reuse_audited_copies and previous_manifest.is_file():
        previous_data = json.loads(previous_manifest.read_text(encoding="utf-8"))
        previous = {item["candidate"]["sourceSha256"]: item for item in previous_data["resources"].values()}
    resources, private_resources, seen = [], {}, {}
    tag = "oxford-library-" + args.date
    release_root = f"https://github.com/Jintian-JTST/Jintian-JTST.github.io/releases/download/{tag}/"
    print(f"Discovered {len(candidates)} candidates; auditing publication copies", flush=True)
    for position, candidate in enumerate(candidates, 1):
        if not candidate["eligible"]:
            candidate.setdefault("status", "未收录")
            continue
        path = Path(candidate["sourcePath"])
        if path.suffix.lower() not in ACCEPTED:
            candidate.update(status="未收录", reason="非课程资料格式或编辑器临时文件")
            continue
        if not path.stat().st_size:
            candidate.update(status="未收录", reason="空文件")
            continue
        if re.search(r"^~\$|^\.DS_Store$|^desktop\.ini$", path.name, re.I):
            candidate.update(status="未收录", reason="系统或 Office 临时文件")
            continue
        try:
            source_hash = digest(path)
            candidate["sourceSha256"] = source_hash
            if source_hash in seen:
                resource = seen[source_hash]
                resource["aliases"].append(clean_text(path.name))
                candidate.update(status="重复", resourceId=resource["id"], reason="与已收录文件 SHA-256 相同")
                private_resources[resource["id"]]["sources"].append(candidate)
                continue
            ext = path.suffix.lower()
            scan = {}
            if ext == ".pdf":
                cache = work / "scans" / (source_hash + ".json")
                if cache.exists():
                    scan = json.loads(cache.read_text(encoding="utf-8"))
                else:
                    scan = inspect_pdf(path)
                    cache.write_text(json.dumps(scan, ensure_ascii=False), encoding="utf-8")
                if "object_findings" not in scan:
                    scan["object_findings"] = findings(path.read_bytes().decode("latin1", errors="ignore"))
                    cache.write_text(json.dumps(scan, ensure_ascii=False), encoding="utf-8")
            resource = metadata(candidate, scan.get("first_page", ""))
            resource_id = "r-" + source_hash[:16]
            asset_name = slug(resource["title"]) + "-" + source_hash[:12] + ext
            prepared = work / "prepared" / asset_name
            privacy = {"changed": False}
            prior = previous.get(source_hash)
            if prior and prepared.is_file() and digest(prepared) == prior["candidate"]["publishedSha256"]:
                privacy = prior["candidate"].get("privacy", privacy)
            elif ext == ".pdf":
                if scan.get("findings") or scan.get("metadata_findings") or scan.get("object_findings"):
                    privacy = redact_pdf(path, prepared, scan)
                else:
                    shutil.copy2(path, prepared)
            elif ext == ".ipynb":
                payload, privacy = scrub_notebook(path.read_bytes())
                prepared.write_bytes(payload)
            elif ext in {".docx", ".xlsx"}:
                payload, privacy = scrub_office(path.read_bytes())
                prepared.write_bytes(payload)
            elif ext in CODE_EXTS | {".md", ".txt", ".csv", ".svg"}:
                payload = path.read_bytes()
                text = decode(payload)
                flags = findings(text)
                if flags:
                    prepared.write_text(clean_text(text), encoding="utf-8")
                    privacy = {"changed": True, "findings": flags}
                else:
                    shutil.copy2(path, prepared)
                if ext == ".svg" and re.search(r"(?i)<script|\bon\w+\s*=|<foreignObject", text):
                    raise ValueError("SVG 含可执行内容，需另行审核")
            else:
                # Images retain visual content but shed EXIF/GPS when present.
                if ext in {".jpg", ".jpeg", ".png"}:
                    from PIL import Image
                    with Image.open(path) as image:
                        if image.getexif() or image.info.get("exif"):
                            image.save(prepared)
                            privacy = {"changed": True, "reason": "移除图像 EXIF 元数据"}
                        else:
                            shutil.copy2(path, prepared)
                else:
                    binary_flags = findings(path.read_bytes().decode("latin1", errors="ignore"))
                    if binary_flags:
                        raise ValueError("专有二进制文件含私人标识，需先导出")
                    shutil.copy2(path, prepared)
            if not prepared.exists():
                shutil.copy2(path, prepared)
            published_hash, byte_count = digest(prepared), prepared.stat().st_size
            asset_name = slug(resource["title"]) + "-" + published_hash[:12] + ext
            large = byte_count > 20 * 1048576
            target = (work / "release-assets" if large else files) / asset_name
            if not target.exists() or digest(target) != published_hash:
                shutil.copy2(prepared, target)
            download_url = release_root + asset_name if large else ASSETS + "files/" + asset_name
            previewable = ext in CODE_EXTS | {".ipynb", ".md", ".txt", ".csv"}
            view_url = (ROOT + "read/" + resource_id + ".html" if previewable or resource.get("featured") == "answers"
                        else download_url if ext in {".pdf", ".png", ".jpg", ".jpeg", ".svg"} and not large else None)
            resource.update(id=resource_id, bytes=byte_count, sha256=published_hash, downloadUrl=download_url,
                            viewUrl=view_url, storage="release" if large else "site", aliases=[clean_text(path.name)])
            if scan:
                resource["pages"] = scan["pages"]
            candidate.update(status="待发布", resourceId=resource_id, publishedSha256=published_hash,
                             privacy=privacy, reason="已生成并检查公开副本")
            seen[source_hash] = resource
            resources.append(resource)
            private_resources[resource_id] = {"candidate": candidate, "sources": [candidate], "preparedPath": str(prepared), "publishPath": str(target)}
        except Exception as error:
            candidate.update(status="待定位", reason=f"{type(error).__name__}: {str(error)[:180]}")
        if position % 15 == 0:
            print(f"Audited {position}/{len(candidates)}; {len(resources)} unique resources", flush=True)
            (work / "manifest-progress.json").write_text(json.dumps(candidates, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Publication copies ready: {len(resources)} unique files", flush=True)
    source_map = {}
    for resource in resources:
        for candidate in private_resources[resource["id"]]["sources"]:
            source_map[str(Path(candidate["sourcePath"]).resolve()).casefold()] = resource
    selection_count = 0
    for resource in resources:
        private = private_resources[resource["id"]]
        path = Path(private["preparedPath"])
        candidate = private["candidate"]
        if not resource.get("viewUrl") or not resource["viewUrl"].startswith(ROOT + "read/"):
            continue
        try:
            if resource.get("featured") == "answers":
                content = book_preview(resource, path)
            elif resource["type"] == "selected" and path.suffix == ".csv":
                content, amount = selected_preview(resource, candidate, resources, source_map)
                if resource.get("featured") == "selected":
                    selection_count = amount
            else:
                content = text_preview(resource, path)
            content = link_attachments(content, Path(candidate["sourcePath"]), source_map)
            math_head = f'<link rel="stylesheet" href="{ASSETS}math/katex.min.css"><script defer src="{ASSETS}math/katex.min.js"></script><script defer src="{ASSETS}math/auto-render.min.js"></script><script defer src="{ASSETS}math-render.js"></script>'
            output = readers / (resource["id"] + ".html")
            output.write_text(reading_page(resource, content, extra_head=math_head), encoding="utf-8")
        except Exception as error:
            # The original file remains downloadable; never advertise a broken reader.
            resource["viewUrl"] = None
            candidate["previewIssue"] = f"{type(error).__name__}: {str(error)[:150]}"
    relate(resources, private_resources)
    # Only remove stale derivatives created in these two dedicated output folders.
    # Original files live outside the checkout and are never removed or renamed.
    referenced_files = {urlsplit(r["downloadUrl"]).path.rsplit("/", 1)[-1] for r in resources if r["storage"] == "site"}
    referenced_readers = {r["id"] + ".html" for r in resources if r.get("viewUrl", "") and r["viewUrl"].startswith(ROOT + "read/")}
    for folder, referenced, pattern in [(files, referenced_files, r".+-[0-9a-f]{12}\.[a-z0-9]+"), (readers, referenced_readers, r"r-[0-9a-f]{16}\.html")]:
        for generated in folder.iterdir():
            if generated.is_file() and re.fullmatch(pattern, generated.name) and generated.name not in referenced:
                if generated.resolve().parent != folder.resolve():
                    raise ValueError("Refusing to remove a generated file outside its output folder")
                generated.unlink()
    resources.sort(key=lambda r: (0 if r.get("featured") == "answers" else 1 if r.get("featured") == "selected" else 2,
                                   {"year1": 0, "year2": 1, "other": 2}[r["stage"]], r["course"],
                                   TYPES[r["type"]], -(r.get("examYear") or 0), r["title"].casefold()))
    bundles = []
    grouped = defaultdict(list)
    for resource in resources:
        if resource["type"] == "image":
            continue
        group = "prelims" if resource["type"] in {"past-paper", "reference-solution"} else "personal-answers" if resource["type"] == "personal-solution" else resource["stage"]
        grouped[group].append(resource)
    bundle_titles = {"prelims": "历年试卷与参考解答", "personal-answers": "个人答案", "year1": "大一课程与实验", "year2": "大二课程与实验", "other": "其他课程讲义"}
    for group, items in sorted(grouped.items()):
        name = f"oxford-{group}-{args.date}.zip"
        output = work / name
        with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=3) as archive:
            member_names = set()
            for resource in items:
                private = private_resources[resource["id"]]
                member = clean_text(private["candidate"]["logicalPath"]).replace(".yr1/", "year1/").replace(".yr2/", "year2/")
                if member in member_names:
                    p = PurePosixPath(member)
                    member = str(p.with_name(p.stem + "-" + resource["id"][-8:] + p.suffix))
                member_names.add(member)
                info = zipfile.ZipInfo(member, tuple(map(int, args.date.split("-"))) + (0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                with archive.open(info, "w") as dest, open(private["preparedPath"], "rb") as src:
                    shutil.copyfileobj(src, dest, 1048576)
            info = zipfile.ZipInfo("README.txt", tuple(map(int, args.date.split("-"))) + (0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, "Oxford Physics personal study collection.\nPersonal solutions are study notes by Jintian Wang. Course materials retain their original authorship.\nNotebooks have NOT been executed. Private identifiers have been removed from publication copies.\n")
        bundle_hash = digest(output)
        name = output.stem + "-" + bundle_hash[:12] + ".zip"
        final_output = work / "release-assets" / name
        shutil.move(str(output), final_output)
        bundles.append({"title": bundle_titles[group], "url": release_root + name, "bytes": final_output.stat().st_size, "sha256": bundle_hash})
        print(f"Packaged {group}: {len(items)} resources", flush=True)
    catalog = {"version": 1, "updatedAt": args.date, "releaseTag": tag, "selectionCount": selection_count,
               "resources": resources, "bundles": bundles}
    (public / "catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    write_directory(repo, catalog)
    manifest = {"updatedAt": args.date, "repository": "Jintian-JTST/Jintian-JTST.github.io", "releaseTag": tag,
                "counts": dict(Counter(c["status"] for c in candidates)), "candidates": candidates,
                "resources": private_resources, "bundles": bundles}
    (work / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = {"resources": len(resources), "candidates": len(candidates), "statuses": manifest["counts"],
               "siteMB": round(sum(r["bytes"] for r in resources if r["storage"] == "site") / 1048576, 1),
               "releaseMB": round((sum(r["bytes"] for r in resources if r["storage"] == "release") + sum(b["bytes"] for b in bundles)) / 1048576, 1),
               "selectedRecords": selection_count, "readers": len(list(readers.glob("*.html")))}
    (work / "build-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
