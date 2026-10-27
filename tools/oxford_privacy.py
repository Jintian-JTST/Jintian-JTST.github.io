"""Privacy checks for publication copies; originals are never modified."""
from __future__ import annotations

import copy
import io
import json
import re
import zipfile
from pathlib import Path

PATTERNS = {
    "candidate_id": re.compile(r"(?i)(?:candidate\s*(?:number|no\.?|id)|student\s*(?:number|no\.?|id)|学号|考生号)\s*[:#：]?\s*[A-Za-z]?\d{4,12}"),
    "college_id": re.compile(r"(?i)\bexet\d{3,10}\b"),
    "local_path": re.compile(r"(?i)(?:[A-Z]:[\\/](?:Users|Documents and Settings)[\\/][^\s\x00<>\"']+|/Users/[^\s<>\"']+)"),
    "personal_email": re.compile(r"(?i)\b[A-Z0-9._%+-]+@(?:gmail\.com|hotmail\.com|outlook\.com|qq\.com|163\.com|icloud\.com)\b"),
    "phone": re.compile(r"(?i)(?:phone|mobile|telephone|电话|手机)\s*[:：]\s*\+?[\d ()-]{9,20}\d"),
    "secret": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{30,}|sk-[A-Za-z0-9_-]{32,})\b"),
}


def findings(text: str) -> dict[str, list[str]]:
    return {kind: sorted({m.group() for m in pattern.finditer(text)})
            for kind, pattern in PATTERNS.items() if pattern.search(text)}


def clean_text(text: str) -> str:
    for kind, pattern in PATTERNS.items():
        replacement = "./data/resource" if kind == "local_path" else "[private information removed]"
        text = pattern.sub(lambda _: replacement, text)
    # Notebook traceback escape sequences do not belong in static reading pages.
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


def scrub_notebook(data: bytes) -> tuple[bytes, dict]:
    notebook = json.loads(data.decode("utf-8-sig"))
    original = copy.deepcopy(notebook)
    notebook["metadata"] = {k: v for k, v in notebook.get("metadata", {}).items()
                            if k in {"kernelspec", "language_info"}}
    all_flags = {}

    def walk(value):
        if isinstance(value, str):
            for kind, matches in findings(value).items():
                all_flags.setdefault(kind, set()).update(matches)
            return clean_text(value)
        if isinstance(value, list):
            return [walk(v) for v in value]
        if isinstance(value, dict):
            # Do not retain executable HTML / JavaScript / SVG notebook outputs.
            return {k: walk(v) for k, v in value.items()
                    if k not in {"text/html", "application/javascript", "image/svg+xml"}}
        return value

    for cell in notebook.get("cells", []):
        cell["metadata"] = {}
        cell.pop("id", None)
        cell["source"] = walk(cell.get("source", []))
        cell["outputs"] = walk(cell.get("outputs", []))
        for output in cell.get("outputs", []):
            output.pop("metadata", None)
    result = json.dumps(notebook, ensure_ascii=False, indent=1).encode("utf-8")
    return result, {"changed": notebook != original,
                    "findings": {k: sorted(v) for k, v in all_flags.items()}}


def scrub_office(data: bytes) -> tuple[bytes, dict]:
    """Remove local metadata and redact private strings in OOXML, preserving data."""
    target = io.BytesIO()
    flags = {}
    changed = False
    with zipfile.ZipFile(io.BytesIO(data)) as source, zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as dest:
        for entry in source.infolist():
            payload = source.read(entry)
            if entry.filename.endswith(".xml"):
                text = payload.decode("utf-8")
                for kind, matches in findings(text).items():
                    flags.setdefault(kind, set()).update(matches)
                revised = clean_text(text)
                if entry.filename == "docProps/core.xml":
                    revised = re.sub(r"(<(?:dc:creator|cp:lastModifiedBy)[^>]*>).*?(</(?:dc:creator|cp:lastModifiedBy)>)",
                                     r"\1\2", revised, flags=re.S)
                changed |= revised != text
                payload = revised.encode("utf-8")
            dest.writestr(entry, payload)
    return (target.getvalue() if changed else data), {
        "changed": changed, "findings": {k: sorted(v) for k, v in flags.items()}}


def inspect_pdf(path: Path) -> dict:
    import fitz
    flags = {}
    full_text = []
    with fitz.open(path) as doc:
        first_page = doc[0].get_text() if len(doc) else ""
        for page in doc:
            text = page.get_text()
            full_text.append(text)
            for kind, matches in findings(text).items():
                flags.setdefault(kind, set()).update(matches)
            for annotation in page.annots() or []:
                for kind, matches in findings(json.dumps(annotation.info, ensure_ascii=False)).items():
                    flags.setdefault(kind, set()).update(matches)
        metadata_flags = findings(json.dumps(doc.metadata, ensure_ascii=False))
        return {"pages": len(doc), "first_page": first_page[:8000],
                "findings": {k: sorted(v) for k, v in flags.items()},
                "metadata_findings": metadata_flags,
                "text_length": sum(map(len, full_text)), "encrypted": doc.is_encrypted}


def redact_pdf(path: Path, output: Path, scan: dict) -> dict:
    import fitz
    count = 0
    with fitz.open(path) as doc:
        # TeX and office exporters often hide workstation paths in Form XObjects.
        # Remove those strings from the object dictionary, retaining the artwork.
        object_updates = 0
        for xref in range(1, doc.xref_length()):
            if doc.xref_is_stream(xref) and doc.xref_get_key(xref, "Type") == ("name", "/Metadata"):
                payload = doc.xref_stream(xref)
                try:
                    xml = payload.decode("utf-8")
                except UnicodeDecodeError:
                    xml = ""
                if xml and findings(xml):
                    doc.update_stream(xref, clean_text(xml).encode("utf-8"), compress=True)
                    object_updates += 1
            if not findings(doc.xref_object(xref)):
                continue
            for key in doc.xref_get_keys(xref):
                kind, value = doc.xref_get_key(xref, key)
                if not findings(value):
                    continue
                if kind == "string":
                    doc.xref_set_key(xref, key, fitz.get_pdf_str(clean_text(value)))
                    object_updates += 1
                elif key in {"A", "AA"}:
                    doc.xref_set_key(xref, key, "null")
                    object_updates += 1
        if findings(doc.get_xml_metadata()):
            doc.del_xml_metadata()
        for page in doc:
            matches = findings(page.get_text())
            for values in matches.values():
                for value in values:
                    for rect in page.search_for(value):
                        page.add_redact_annot(rect, fill=(1, 1, 1))
                        count += 1
            if matches:
                page.apply_redactions(images=0, graphics=0)
            for annotation in page.annots() or []:
                info = annotation.info
                updates = {k: clean_text(info.get(k, ""))
                           for k in ("content", "title", "subject")}
                if any(updates[k] != info.get(k, "") for k in updates):
                    annotation.set_info(**updates)
        editable = {"author", "title", "subject", "keywords", "creator", "producer", "creationDate", "modDate", "trapped"}
        doc.set_metadata({k: clean_text(v or "") for k, v in doc.metadata.items() if k in editable})
        for name in doc.embfile_names():
            doc.embfile_del(name)
        doc.save(output, garbage=4, deflate=True)
    # A white rectangle alone is insufficient: verify the stored text as well.
    with fitz.open(output) as check:
        remaining = findings("\n".join(page.get_text() for page in check))
        if remaining:
            raise ValueError("Private strings remain after PDF redaction")
    if findings(output.read_bytes().decode("latin1", errors="ignore")):
        raise ValueError("Private strings remain in hidden PDF objects")
    return {"changed": True, "redactions": count, "metadataStringsCleaned": object_updates}
