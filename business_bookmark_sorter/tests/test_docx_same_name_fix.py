"""Tests for Word same-name / regenerate path (no live Word)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from business_bookmark_sorter.docx_export import (
    WD_SAVE_CHANGES,
    _paths_refer_to_same_file,
    close_word_document_if_open,
    is_same_name_as_open_document_error,
    regenerate_and_open_docx,
)
from business_bookmark_sorter.word_open import (
    WD_STORY,
    bring_word_to_front,
    open_docx_for_owner,
    open_docx_via_word_com,
    scroll_word_doc_to_end,
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


def test_close_saves_then_closes_when_doc_open():
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
    doc.Save.assert_called()
    doc.Close.assert_called()
    _args, kwargs = doc.Close.call_args
    assert kwargs.get("SaveChanges") == WD_SAVE_CHANGES


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
        "business_bookmark_sorter.word_open.open_docx_for_owner",
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
        "business_bookmark_sorter.word_open.open_docx_for_owner",
    ), patch(
        "business_bookmark_sorter.docx_export.time.sleep",
    ):
        out = regenerate_and_open_docx(md)

    assert calls["n"] == 2
    assert out.read_bytes() == b"ok"


def test_scroll_word_doc_to_end_uses_endkey():
    word = MagicMock()
    doc = MagicMock()
    scroll_word_doc_to_end(word, doc)
    doc.Activate.assert_called()
    word.Selection.EndKey.assert_called_with(WD_STORY)


def test_bring_word_to_front_sets_foreground():
    word = MagicMock()
    word.Hwnd = 7
    word.Caption = "Word"
    fake_client = MagicMock()
    fake_win32 = MagicMock()
    fake_win32.client = fake_client
    with patch("business_bookmark_sorter.word_open.ctypes") as fake_ctypes:
        fake_ctypes.windll.user32.ShowWindow.return_value = True
        fake_ctypes.windll.user32.SetForegroundWindow.return_value = True
        with patch.dict(
            "sys.modules", {"win32com": fake_win32, "win32com.client": fake_client}
        ):
            bring_word_to_front(word)
    word.Activate.assert_called()
    fake_ctypes.windll.user32.SetForegroundWindow.assert_called_with(7)


def test_open_docx_via_word_com_activates_and_scrolls_to_end(tmp_path):
    path = tmp_path / "Business Links.docx"
    path.write_bytes(b"x")
    word = MagicMock()
    doc = MagicMock()
    word.Documents.Count = 0
    word.Documents.Open.return_value = doc

    with patch(
        "business_bookmark_sorter.docx_export._get_word_application",
        return_value=word,
    ), patch(
        "business_bookmark_sorter.word_open.bring_word_to_front",
    ) as bring, patch(
        "business_bookmark_sorter.word_open.scroll_word_doc_to_end",
    ) as scroll:
        assert open_docx_via_word_com(path) is True

    word.Documents.Open.assert_called_once()
    assert word.Documents.Open.call_args[0][0] == str(path.resolve())
    bring.assert_called_once_with(word)
    scroll.assert_called_once_with(word, doc)


def test_open_docx_for_owner_falls_back_to_start(tmp_path):
    path = tmp_path / "Business Links.docx"
    path.write_bytes(b"x")
    with patch(
        "business_bookmark_sorter.word_open.open_docx_via_word_com",
        return_value=False,
    ) as com, patch(
        "business_bookmark_sorter.word_open.open_path_detached",
    ) as start:
        open_docx_for_owner(path)
    com.assert_called_once()
    start.assert_called_once_with(path)


def test_regenerate_uses_owner_open_helper(tmp_path):
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
        "business_bookmark_sorter.word_open.open_docx_for_owner",
    ) as opener, patch(
        "business_bookmark_sorter.docx_export.time.sleep",
    ):
        out = regenerate_and_open_docx(md)

    assert out == final.resolve()
    opener.assert_called_once_with(final.resolve())


def test_regenerate_writes_docx_from_current_markdown(tmp_path):
    """Regenerate replaces the docx bytes with the current markdown convert."""
    md = tmp_path / "Business Links.md"
    md.write_text("# Business Links\n\n- [KeepMe](https://example.com/keep)\n", encoding="utf-8")
    final = tmp_path / "Business Links.docx"
    final.write_bytes(b"STALE-DOCX-BYTES")

    def fake_convert(md_path: Path, docx_path: Path | None = None) -> Path:
        out = docx_path or md_path.with_suffix(".docx")
        out.write_bytes(md_path.read_bytes())
        return out

    with patch(
        "business_bookmark_sorter.docx_export.close_word_document_if_open",
        return_value=True,
    ), patch(
        "business_bookmark_sorter.docx_export.convert_md_to_docx",
        side_effect=fake_convert,
    ), patch(
        "business_bookmark_sorter.word_open.open_docx_for_owner",
    ), patch(
        "business_bookmark_sorter.docx_export.time.sleep",
    ):
        regenerate_and_open_docx(md)

    body = final.read_bytes()
    assert b"STALE-DOCX-BYTES" not in body
    assert b"KeepMe" in body


def test_append_filed_link_in_word_saves_without_rebuild(tmp_path):
    from business_bookmark_sorter.word_open import append_filed_link_in_word

    path = tmp_path / "Business Links.docx"
    path.write_bytes(b"x")
    word = MagicMock()
    doc = MagicMock()
    doc.Content.Text = "old notes I typed"
    doc.Content.End = 20
    word.Selection.Range = MagicMock()

    with patch(
        "business_bookmark_sorter.word_open._word_and_doc_for_path",
        return_value=(word, doc),
    ), patch(
        "business_bookmark_sorter.word_open.bring_word_to_front",
    ), patch(
        "business_bookmark_sorter.word_open.scroll_word_doc_to_end",
    ):
        assert append_filed_link_in_word(path, "New", "https://example.com/new") is True

    word.Selection.TypeParagraph.assert_called()
    doc.Hyperlinks.Add.assert_called()
    doc.Save.assert_called()
    doc.Close.assert_not_called()

