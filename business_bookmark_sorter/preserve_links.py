"""Keep already-saved Business Links lines; only append newly filed queue items."""

from __future__ import annotations

import re
import zipfile
from pathlib import Path
from typing import Iterable, List

_MD_LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
_SKIP_PARA_STYLES = frozenset({"Heading1", "FirstParagraph", "Title", "Subtitle"})
_SKIP_TEXT_PREFIXES = ("exported from", "one flat list", "one document", "source of truth")


def extract_md_link_lines(path: Path) -> List[str]:
    if not path.is_file():
        return []
    lines: List[str] = []
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if line.startswith("- "):
            lines.append(line)
    return lines


def _relationship_targets(rels_xml: str) -> dict[str, str]:
    targets: dict[str, str] = {}
    for m in re.finditer(r"<Relationship\s+([^>]+)/?>", rels_xml):
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
        rid = attrs.get("Id")
        target = attrs.get("Target")
        typ = (attrs.get("Type") or "").lower()
        if rid and target and "hyperlink" in typ:
            targets[rid] = target
    return targets


def _para_style(para_xml: str) -> str:
    m = re.search(r'w:pStyle\s+w:val="([^"]+)"', para_xml)
    return m.group(1) if m else ""


def _para_text(para_xml: str) -> str:
    parts = re.findall(r"<w:t[^>]*>([^<]*)</w:t>", para_xml)
    return "".join(parts).strip()


def extract_docx_link_lines(path: Path) -> List[str]:
    if not path.is_file():
        return []
    try:
        with zipfile.ZipFile(path) as z:
            names = set(z.namelist())
            if "word/document.xml" not in names:
                return []
            xml = z.read("word/document.xml").decode("utf-8", errors="replace")
            rels = ""
            if "word/_rels/document.xml.rels" in names:
                rels = z.read("word/_rels/document.xml.rels").decode(
                    "utf-8", errors="replace"
                )
    except (OSError, zipfile.BadZipFile):
        return []

    url_by_rid = _relationship_targets(rels)
    lines: List[str] = []
    for para in re.findall(r"<w:p[ >].*?</w:p>", xml, flags=re.DOTALL):
        style = _para_style(para)
        if style in _SKIP_PARA_STYLES:
            continue
        text = _para_text(para)
        if not text:
            continue
        if text.lower().startswith(_SKIP_TEXT_PREFIXES):
            continue
        hid = re.search(r"<w:hyperlink[^>]*r:id=\"([^\"]+)\"", para)
        if hid:
            url = (url_by_rid.get(hid.group(1)) or "").strip()
            if url:
                lines.append(f"- [{text}]({url})")
                continue
        lines.append(f"- {text}")
    return lines


def link_identity(line: str) -> str:
    """Dedupe key: URL if present, else normalized line text."""
    found = _MD_LINK.search(line)
    if found:
        return found.group(2).strip().lower()
    return re.sub(r"\s+", " ", line.strip().lower())


def merge_link_lines(existing: Iterable[str], incoming: Iterable[str]) -> List[str]:
    """Keep existing order; append incoming lines whose URL/title is new."""
    out: List[str] = []
    seen: set[str] = set()
    for source in (existing, incoming):
        for raw in source:
            line = raw.strip()
            if not line.startswith("- "):
                continue
            key = link_identity(line)
            if not key or key in seen:
                continue
            seen.add(key)
            out.append(line)
    return out


def existing_link_lines(md_path: Path) -> List[str]:
    """Prefer the saved .docx (what you last saved in Word), then leftover .md lines."""
    docx_path = md_path.with_suffix(".docx")
    from_docx = extract_docx_link_lines(docx_path)
    from_md = extract_md_link_lines(md_path)
    if from_docx:
        return merge_link_lines(from_docx, from_md)
    return from_md
