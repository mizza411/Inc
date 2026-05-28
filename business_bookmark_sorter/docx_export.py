"""Convert destination links.md to .docx and open in Word (Windows)."""

from __future__ import annotations

import os
import shutil
import subprocess
import time
from pathlib import Path


def docx_path_for_md(md_path: Path) -> Path:
    return md_path.with_suffix(".docx")


def _pandoc_available() -> bool:
    return shutil.which("pandoc") is not None


def close_word_document_if_open(docx_path: Path) -> None:
    """Save and close the docx in Word if it is open. Never kills WINWORD.EXE."""
    try:
        import win32com.client  # type: ignore[import-untyped]
    except ImportError:
        return

    resolved = str(docx_path.resolve()).lower()
    word = win32com.client.Dispatch("Word.Application")
    for doc in list(word.Documents):
        try:
            if str(Path(doc.FullName).resolve()).lower() == resolved:
                doc.Save()
                doc.Close()
        except Exception:
            continue


def _convert_with_pandoc(md_path: Path, docx_path: Path) -> None:
    docx_path.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["pandoc", str(md_path), "-o", str(docx_path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        err = (result.stderr or result.stdout or "pandoc failed").strip()
        raise RuntimeError(err)


def _convert_with_word(md_path: Path, docx_path: Path) -> None:
    import win32com.client  # type: ignore[import-untyped]

    docx_path.parent.mkdir(parents=True, exist_ok=True)
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    doc = None
    try:
        doc = word.Documents.Open(str(md_path.resolve()), ReadOnly=True)
        doc.SaveAs2(str(docx_path.resolve()), FileFormat=16)
    finally:
        if doc is not None:
            doc.Close(False)
        word.Quit()


def convert_md_to_docx(md_path: Path, docx_path: Path | None = None) -> Path:
    """Build or refresh docx beside the markdown file."""
    md_path = md_path.resolve()
    if not md_path.is_file():
        raise FileNotFoundError(f"Markdown not found: {md_path}")

    out = (docx_path or docx_path_for_md(md_path)).resolve()
    last_err: Exception | None = None

    if _pandoc_available():
        try:
            _convert_with_pandoc(md_path, out)
            return out
        except Exception as exc:
            last_err = exc

    try:
        _convert_with_word(md_path, out)
        return out
    except ImportError as exc:
        last_err = exc
    except Exception as exc:
        last_err = exc

    hint = "Install Pandoc (https://pandoc.org) or pywin32 + Microsoft Word."
    msg = str(last_err) if last_err else "No converter available"
    raise RuntimeError(f"Could not create docx: {msg}. {hint}")


def _write_with_retry(path: Path, write_fn) -> None:
    """Retry once on lock (OneDrive / Word)."""
    for attempt in range(2):
        try:
            write_fn()
            return
        except OSError as exc:
            if attempt == 0:
                time.sleep(0.4)
                continue
            raise RuntimeError(f"File locked or not writable: {path} ({exc})") from exc
        except PermissionError as exc:
            if attempt == 0:
                time.sleep(0.4)
                continue
            raise RuntimeError(f"Permission denied: {path} ({exc})") from exc


def regenerate_and_open_docx(md_path: Path) -> Path:
    """Close open docx if safe, rebuild from md, open in default app."""
    md_path = md_path.resolve()
    docx_path = docx_path_for_md(md_path)

    def _build() -> None:
        close_word_document_if_open(docx_path)
        convert_md_to_docx(md_path, docx_path)

    _write_with_retry(docx_path, _build)

    if os.name == "nt":
        os.startfile(docx_path)  # noqa: S606 — intentional Windows open
    else:
        import webbrowser

        webbrowser.open(docx_path.as_uri())

    return docx_path
