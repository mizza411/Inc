"""Every table in a packed docx gets a visible full grid."""

from __future__ import annotations

import zipfile
from pathlib import Path

from business_bookmark_sorter.docx_export import _inject_inline_table_borders

_DOC = """<?xml version="1.0" encoding="UTF-8"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>
<w:tbl><w:tblPr><w:tblBorders><w:top w:val="nil"/></w:tblBorders><w:tblStyle w:val="Table"/></w:tblPr>
<w:tr><w:tc><w:p><w:r><w:t>A</w:t></w:r></w:p></w:tc></w:tr></w:tbl>
<w:tbl><w:tr><w:tc><w:p><w:r><w:t>B</w:t></w:r></w:p></w:tc></w:tr></w:tbl>
</w:body></w:document>
"""


def _write_docx(path: Path, document_xml: str) -> None:
    with zipfile.ZipFile(path, "w") as zout:
        zout.writestr("word/document.xml", document_xml)


def _document_xml(path: Path) -> str:
    with zipfile.ZipFile(path) as zin:
        return zin.read("word/document.xml").decode("utf-8")


def test_every_table_gets_a_grid_after_the_style(tmp_path: Path) -> None:
    path = tmp_path / "ideas.docx"
    _write_docx(path, _DOC)
    _inject_inline_table_borders(path)
    _inject_inline_table_borders(path)
    xml = _document_xml(path)

    assert xml.count("<w:tblBorders>") == 2
    assert 'w:val="nil"' not in xml
    assert xml.count('w:val="single"') == 12
    assert 'w:color="000000"' in xml

    first = xml.split("</w:tbl>", 1)[0]
    assert first.index('w:val="Table"') < first.index("<w:tblBorders>")
    second = xml.split("</w:tbl>", 1)[1]
    assert "<w:tblBorders>" in second
    assert "insideV" in second
