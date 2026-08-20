"""Tests for Word same-name / regenerate path (no live Word)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from business_bookmark_sorter.docx_export import (
    _paths_refer_to_same_file,
    close_word_document_if_open,
    is_same_name_as_open_document_error,
    regenerate_and_open_docx,
)


def test_paths_refer_to_same_file(tmp_path):
    a = tmp_path / "Business Links.docx"
    a.write_text("x", encoding="utf-8")
    assert _paths_refer_to_same_file(str(a), str(a.resolve()))


def test_is_same_name_error_detects_word_message():
    exc = RuntimeError(
        "(-2147352567, 'Exception occurred.', (0, 'Microsoft Word', "
        '"Word cannot give a document the same name as an open document.\\n'
        'Type a different name...", '
        "'wdmain11.chm', 24633, -2147352567), None)"
    )
    assert is_same_name_as_open_document_error(exc)
    assert not is_same_name_as_open_document_error(RuntimeError("pandoc failed"))


def test_close_without_save_when_doc_open():
    doc = MagicMock()
    doc.FullName = r"C:\dev\Inc\business_bookmark_sorter\Business Links.docx"
    word = MagicMock()
    word.Documents.Count = 1
    word.Documents.Item.return_value = doc

    fake_client = MagicMock()
    fake_client.GetActiveObject.return_value = word
    fake_win32 = MagicMock()
    fake_win32.client = fake_client

    with patch.dict("sys.modules", {"win32com": fake_win32, "win32com.client": fake_client}):
        with patch(
            "business_bookmark_sorter.docx_export._paths_refer_to_same_file",
            return_value=True,
        ):
            closed = close_word_document_if_open(
                Path(r"C:\dev\Inc\business_bookmark_sorter\Business Links.docx"),
                timeout=2,
            )
    assert closed is True
    assert word.DisplayAlerts == 0
    assert doc.Saved is True
    doc.Close.assert_called()
    doc.Save.assert_not_called()


def test_replace_renames_locked_final(tmp_path):
    from business_bookmark_sorter.docx_export import _replace_with_temp

    final = tmp_path / "Business Links.docx"
    final.write_bytes(b"old")
    temp = tmp_path / "Business Links.__regen__.docx"
    temp.write_bytes(b"new")

    with patch(
        "business_bookmark_sorter.docx_export.close_word_document_if_open",
        return_value=True,
    ), patch(
        "business_bookmark_sorter.docx_export.time.sleep",
    ):
        # Simulate first unlink failing then rename succeeding
        real_unlink = Path.unlink
        calls = {"n": 0}

        def flaky_unlink(self, *args, **kwargs):
            if self == final and calls["n"] == 0:
                calls["n"] += 1
                raise OSError(32, "used by another process")
            return real_unlink(self, *args, **kwargs)

        with patch.object(Path, "unlink", flaky_unlink):
            out = _replace_with_temp(temp, final)

    assert out == final
    assert final.read_bytes() == b"new"
    baks = list(tmp_path.glob("Business Links.openbak_*.docx"))
    assert len(baks) == 1


def test_regenerate_uses_temp_then_replace(tmp_path):
    md = tmp_path / "Business Links.md"
    md.write_text("# Business Links\n", encoding="utf-8")
    final = tmp_path / "Business Links.docx"
    final.write_bytes(b"old")

    def fake_convert(md_path: Path, docx_path: Path | None = None) -> Path:
        out = docx_path or md_path.with_suffix(".docx")
        out.write_bytes(b"new-from-md")
        return out

    with patch(
        "business_bookmark_sorter.docx_export.close_word_document_if_open",
        return_value=True,
    ), patch(
        "business_bookmark_sorter.docx_export.convert_md_to_docx",
        side_effect=fake_convert,
    ), patch(
        "business_bookmark_sorter.docx_export._open_path_detached",
    ), patch(
        "business_bookmark_sorter.docx_export.time.sleep",
    ):
        out = regenerate_and_open_docx(md)

    assert out == final.resolve()
    assert final.read_bytes() == b"new-from-md"
    assert not (tmp_path / "Business Links.__regen__.docx").exists()


def test_regenerate_retries_on_same_name_error(tmp_path):
    md = tmp_path / "Business Links.md"
    md.write_text("# x\n", encoding="utf-8")
    calls = {"n": 0}

    def flaky_convert(md_path: Path, docx_path: Path | None = None) -> Path:
        calls["n"] += 1
        out = docx_path or md_path.with_suffix(".docx")
        if calls["n"] == 1:
            raise RuntimeError(
                "(-2147352567, 'Exception occurred.', (0, 'Microsoft Word', "
                '"Word cannot give a document the same name as an open document.", '
                "'wdmain11.chm', 24633, -2147352567), None)"
            )
        out.write_bytes(b"ok")
        return out

    with patch(
        "business_bookmark_sorter.docx_export.close_word_document_if_open",
        return_value=True,
    ), patch(
        "business_bookmark_sorter.docx_export.convert_md_to_docx",
        side_effect=flaky_convert,
    ), patch(
        "business_bookmark_sorter.docx_export._open_path_detached",
    ), patch(
        "business_bookmark_sorter.docx_export.time.sleep",
    ):
        out = regenerate_and_open_docx(md)

    assert calls["n"] == 2
    assert out.read_bytes() == b"ok"
