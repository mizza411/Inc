"""Reopen Business Links.docx in the same Word instance, in front, at the newest link."""

from __future__ import annotations

import ctypes
import os
import subprocess
from pathlib import Path

WD_STORY = 6  # Selection.EndKey: move to end of document
SW_RESTORE = 9
WD_WINDOW_STATE_NORMAL = 0


def open_path_detached(path: Path) -> None:
    """Open *path* in the default app without blocking the caller."""
    path = path.resolve()
    if os.name == "nt":
        subprocess.Popen(  # noqa: S603
            ["cmd", "/c", "start", "", str(path)],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=True,
        )
        return

    import webbrowser

    webbrowser.open(path.as_uri())


def scroll_word_doc_to_end(word, doc) -> None:
    """Put the cursor on the newest filed link (last line of the flat list)."""
    try:
        doc.Activate()
    except Exception:
        pass
    try:
        word.Selection.EndKey(WD_STORY)
        return
    except Exception:
        pass
    try:
        last = doc.Paragraphs.Last.Range
        last.Select()
        last.Collapse(0)  # wdCollapseEnd
    except Exception:
        pass


def bring_word_to_front(word) -> None:
    """Show this Word instance in front of other Word documents."""
    try:
        word.Visible = True
    except Exception:
        pass
    try:
        word.WindowState = WD_WINDOW_STATE_NORMAL
    except Exception:
        pass
    try:
        word.Activate()
    except Exception:
        pass
    hwnd = None
    try:
        hwnd = int(word.Hwnd)
    except Exception:
        hwnd = None
    if hwnd:
        try:
            user32 = ctypes.windll.user32
            user32.ShowWindow(hwnd, SW_RESTORE)
            user32.SetForegroundWindow(hwnd)
        except Exception:
            pass
    try:
        import win32com.client  # type: ignore[import-untyped]

        shell = win32com.client.Dispatch("WScript.Shell")
        if hwnd:
            shell.AppActivate(hwnd)
        else:
            shell.AppActivate(str(word.Caption))
    except Exception:
        pass


def open_docx_via_word_com(docx_path: Path) -> bool:
    """Open *docx_path* in the existing Word instance (or start one). Never Quit."""
    try:
        import win32com.client  # type: ignore[import-untyped]
    except ImportError:
        return False

    from business_bookmark_sorter.docx_export import (
        _doc_matches_target,
        _get_word_application,
    )

    path = str(docx_path.resolve())
    target_name = docx_path.name.lower()
    word = _get_word_application()
    if word is None:
        try:
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = True
        except Exception:
            return False

    doc = None
    try:
        count = int(word.Documents.Count)
    except Exception:
        count = 0
    for i in range(count, 0, -1):
        try:
            existing = word.Documents.Item(i)
            full = str(existing.FullName)
        except Exception:
            continue
        if _doc_matches_target(full, path, target_name):
            doc = existing
            break
    if doc is None:
        try:
            doc = word.Documents.Open(
                path,
                ConfirmConversions=False,
                AddToRecentFiles=False,
            )
        except Exception:
            return False

    try:
        bring_word_to_front(word)
        scroll_word_doc_to_end(word, doc)
    except Exception:
        pass
    return True


def open_docx_for_owner(docx_path: Path) -> None:
    """Prefer the same Word instance, in front, last line selected; else ``start``."""
    if open_docx_via_word_com(docx_path):
        return
    open_path_detached(docx_path)


def _word_and_doc_for_path(docx_path: Path):
    """Return (word, doc) for *docx_path*, opening it if needed. Never Quit."""
    try:
        import win32com.client  # type: ignore[import-untyped]
    except ImportError:
        return None, None

    from business_bookmark_sorter.docx_export import (
        _doc_matches_target,
        _get_word_application,
    )

    path = str(docx_path.resolve())
    target_name = docx_path.name.lower()
    word = _get_word_application()
    if word is None:
        try:
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = True
        except Exception:
            return None, None

    doc = None
    try:
        count = int(word.Documents.Count)
    except Exception:
        count = 0
    for i in range(count, 0, -1):
        try:
            existing = word.Documents.Item(i)
            full = str(existing.FullName)
        except Exception:
            continue
        if _doc_matches_target(full, path, target_name):
            doc = existing
            break
    if doc is None:
        try:
            doc = word.Documents.Open(
                path,
                ConfirmConversions=False,
                AddToRecentFiles=False,
            )
        except Exception:
            return word, None
    return word, doc


def append_filed_link_in_word(docx_path: Path, title: str, url: str) -> bool:
    """Add the new filed link at the end of the open Word doc. Do not rebuild it."""
    if not docx_path.is_file():
        return False
    word, doc = _word_and_doc_for_path(docx_path)
    if word is None or doc is None:
        return False

    title = (title or "Untitled").replace("\n", " ").strip()
    url = (url or "").strip()
    try:
        live = str(doc.Content.Text)
    except Exception:
        live = ""
    if url and url in live:
        bring_word_to_front(word)
        scroll_word_doc_to_end(word, doc)
        return True
    if not url and title and title in live:
        bring_word_to_front(word)
        scroll_word_doc_to_end(word, doc)
        return True

    try:
        word.Selection.EndKey(WD_STORY)
        word.Selection.TypeParagraph()
        if url:
            doc.Hyperlinks.Add(
                Anchor=word.Selection.Range,
                Address=url,
                TextToDisplay=title or url,
            )
        else:
            word.Selection.TypeText(title)
        doc.Save()
    except Exception:
        return False

    bring_word_to_front(word)
    scroll_word_doc_to_end(word, doc)
    return True
