"""Keep saved Business Links lines when filing again."""

from __future__ import annotations

import zipfile
from pathlib import Path

from business_bookmark_sorter.preserve_links import (
    extract_docx_link_lines,
    extract_md_link_lines,
    merge_link_lines,
)


def test_merge_keeps_existing_and_appends_new():
    existing = [
        "- [KeepMe](https://example.com/keep)",
        "- [HandTypedExtra](https://example.com/extra)",
    ]
    incoming = [
        "- [KeepMe](https://example.com/keep)",
        "- [NewFiled](https://example.com/new)",
    ]
    merged = merge_link_lines(existing, incoming)
    assert merged == [
        "- [KeepMe](https://example.com/keep)",
        "- [HandTypedExtra](https://example.com/extra)",
        "- [NewFiled](https://example.com/new)",
    ]


def test_extract_md_link_lines_skips_header(tmp_path):
    path = tmp_path / "Business Links.md"
    path.write_text(
        "# Business Links\n\n_Exported._\n\n- [A](https://a.example)\n",
        encoding="utf-8",
    )
    assert extract_md_link_lines(path) == ["- [A](https://a.example)"]


def _write_mini_docx(path: Path, body_xml: str, rels_xml: str) -> None:
    ctype = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        "</Types>"
    )
    pkg_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        "</Relationships>"
    )
    doc_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f"<w:body>{body_xml}</w:body></w:document>"
    )
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("[Content_Types].xml", ctype)
        z.writestr("_rels/.rels", pkg_rels)
        z.writestr("word/document.xml", doc_xml)
        z.writestr("word/_rels/document.xml.rels", rels_xml)


def test_extract_docx_link_lines_reads_hyperlink(tmp_path):
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId9" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" '
        'Target="https://example.com/extra" TargetMode="External"/>'
        "</Relationships>"
    )
    body = (
        '<w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>Business Links</w:t></w:r></w:p>'
        "<w:p><w:pPr><w:pStyle w:val=\"Compact\"/></w:pPr>"
        '<w:hyperlink r:id="rId9"><w:r><w:t>HandTypedExtra</w:t></w:r></w:hyperlink></w:p>'
    )
    path = tmp_path / "Business Links.docx"
    _write_mini_docx(path, body, rels)
    assert extract_docx_link_lines(path) == [
        "- [HandTypedExtra](https://example.com/extra)"
    ]
