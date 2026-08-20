"""Convert destination links.md to .docx and open in Word (Windows)."""

from __future__ import annotations

import io
import os
import re
import shutil
import subprocess
import time
import zipfile
from pathlib import Path

# Word COM can stall on dialogs; Close must stay on the calling STA thread.
# Never kill WINWORD.EXE from this module.
WORD_COM_CLOSE_TIMEOUT_SEC = 10

_PANDOC_REFERENCE_DOC = Path(__file__).resolve().parent / "pandoc_reference.docx"


def _pandoc_reference_doc() -> Path | None:
    """Return bundled Pandoc reference doc when present."""
    return _PANDOC_REFERENCE_DOC if _PANDOC_REFERENCE_DOC.is_file() else None


_TABLE_BORDERS_XML = (
    "<w:tblBorders>"
    '<w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    "</w:tblBorders>"
)


def _inject_inline_table_borders(docx_path: Path) -> None:
    """Ensure each table in document.xml has explicit grid borders (Word-visible)."""
    with zipfile.ZipFile(docx_path, "r") as zin:
        names = zin.namelist()
        if "word/document.xml" not in names:
            return
        doc_xml = zin.read("word/document.xml").decode("utf-8")

    if "w:tblBorders" in doc_xml:
        return

    def _patch_tbl_pr(match: re.Match[str]) -> str:
        inner = match.group(1)
        if "w:tblBorders" in inner:
            return match.group(0)
        return f"<w:tblPr>{_TABLE_BORDERS_XML}{inner}</w:tblPr>"

    doc_xml = re.sub(
        r"<w:tblPr>(.*?)</w:tblPr>",
        _patch_tbl_pr,
        doc_xml,
        flags=re.DOTALL,
    )

    buf = io.BytesIO()
    with zipfile.ZipFile(docx_path, "r") as zin, zipfile.ZipFile(
        buf, "w", zipfile.ZIP_DEFLATED
    ) as zout:
        for item in zin.infolist():
            data = doc_xml.encode("utf-8") if item.filename == "word/document.xml" else zin.read(item.filename)
            zout.writestr(item, data)
    docx_path.write_bytes(buf.getvalue())


def docx_path_for_md(md_path: Path) -> Path:
    return md_path.with_suffix(".docx")


def _pandoc_available() -> bool:
    return shutil.which("pandoc") is not None


def _paths_refer_to_same_file(a: str, b: str) -> bool:
    """True when two filesystem paths likely name the same document."""
    try:
        return Path(a).resolve().as_posix().lower() == Path(b).resolve().as_posix().lower()
    except OSError:
        return os.path.normcase(os.path.abspath(a)) == os.path.normcase(os.path.abspath(b))


def _get_word_application():
    """Attach to a running Word instance if possible (never starts a silent kill)."""
    import win32com.client  # type: ignore[import-untyped]

    for getter in (
        lambda: win32com.client.GetActiveObject("Word.Application"),
        lambda: win32com.client.GetObject(Class="Word.Application"),
        lambda: win32com.client.GetObject("Word.Application"),
    ):
        try:
            return getter()
        except Exception:
            continue
    return None


def _doc_matches_target(full: str, target: str, target_name: str) -> bool:
    if _paths_refer_to_same_file(full, target):
        return True
    try:
        p = Path(full)
        if p.name.lower() != target_name:
            return False
        # Same master export filename under sorter folder (junction / OneDrive path drift)
        if target_name != "business links.docx":
            return False
        full_n = full.lower().replace("\\", "/")
        target_n = target.lower().replace("\\", "/")
        return ("business_bookmark_sorter" in full_n) or (
            "business_bookmark_sorter" in target_n
        )
    except Exception:
        return False


def _close_word_document_if_open_impl(docx_path: Path) -> bool:
    """Close *docx_path* in a running Word instance when that file is open.

    Closes **without** saving: regenerate rebuilds from markdown, so keeping
    Word's buffer would fight the new export (and SaveAs same-name errors).
    Must run on the **calling (STA) thread** — Word COM hangs if Close is
    issued from a worker thread. Never kills WINWORD.EXE.
    Returns True if a matching doc was closed.
    """
    target = str(docx_path.resolve())
    target_name = docx_path.name.lower()
    word = _get_word_application()
    if word is None:
        return False

    try:
        # Suppress Save / Protected View prompts that block Close.
        word.DisplayAlerts = 0  # wdAlertsNone
    except Exception:
        pass

    closed = False
    # Indexed access is more reliable than iterating the COM collection.
    try:
        count = int(word.Documents.Count)
    except Exception:
        return False

    for i in range(count, 0, -1):
        try:
            doc = word.Documents.Item(i)
            full = str(doc.FullName)
        except Exception:
            continue
        if not _doc_matches_target(full, target, target_name):
            continue
        try:
            # Mark clean so Word will not prompt despite unsaved buffer.
            doc.Saved = True
        except Exception:
            pass
        try:
            doc.Close(SaveChanges=0)  # wdDoNotSaveChanges
            closed = True
        except Exception:
            try:
                doc.Close(False)
                closed = True
            except Exception:
                continue
    return closed


def close_word_document_if_open(
    docx_path: Path,
    timeout: float = WORD_COM_CLOSE_TIMEOUT_SEC,
) -> bool:
    """Close without save before regenerate. Never kills WINWORD.EXE.

    *timeout* is kept for API compatibility but unused: Word COM must not run
    on a background thread (STA deadlock / silent hang).
    """
    del timeout  # API compat; do not thread Word COM
    try:
        import win32com.client  # type: ignore[import-untyped]  # noqa: F401
    except ImportError:
        return False

    return bool(_close_word_document_if_open_impl(docx_path))


def is_same_name_as_open_document_error(exc: BaseException) -> bool:
    """Detect Word COM 'same name as an open document' failures."""
    text = str(exc).lower()
    return "same name as an open document" in text or (
        "-2147352567" in text and "word" in text
    )


def is_file_lock_error(exc: BaseException) -> bool:
    text = str(exc).lower()
    return (
        "winerror 32" in text
        or "being used by another process" in text
        or "file locked" in text
    )


def _replace_with_temp(temp_docx: Path, docx_path: Path) -> Path:
    """Move temp into final path; if final is locked, close Word and rename aside.

    Returns the path the caller should open (normally *docx_path*; sibling
    ``*.updated.docx`` only if the master file stays locked after Close).
    """
    if not temp_docx.is_file():
        raise RuntimeError(f"Temp docx missing after convert: {temp_docx}")

    if not docx_path.exists():
        temp_docx.replace(docx_path)
        return docx_path

    close_word_document_if_open(docx_path)
    time.sleep(0.5)

    try:
        docx_path.unlink()
    except OSError:
        close_word_document_if_open(docx_path)
        time.sleep(0.7)
        bak = docx_path.with_name(
            f"{docx_path.stem}.openbak_{int(time.time())}{docx_path.suffix}"
        )
        try:
            docx_path.rename(bak)
        except OSError:
            sibling = docx_path.with_name(
                f"{docx_path.stem}.updated{docx_path.suffix}"
            )
            try:
                if sibling.exists():
                    sibling.unlink()
            except OSError:
                pass
            try:
                temp_docx.replace(sibling)
            except OSError as exc:
                raise RuntimeError(
                    f"Word/OneDrive still locking {docx_path.name}. "
                    f"Close that Word tab, then File again. ({exc})"
                ) from exc
            return sibling

    temp_docx.replace(docx_path)
    return docx_path


def _open_path_detached(path: Path) -> None:
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


def _convert_with_pandoc(md_path: Path, docx_path: Path) -> None:
    docx_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["pandoc", str(md_path), "-o", str(docx_path)]
    ref = _pandoc_reference_doc()
    if ref is not None:
        cmd.extend(["--reference-doc", str(ref)])
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        err = (result.stderr or result.stdout or "pandoc failed").strip()
        raise RuntimeError(err)
    _inject_inline_table_borders(docx_path)


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
    """Retry a few times on lock (OneDrive / Word)."""
    last: Exception | None = None
    for attempt in range(4):
        try:
            write_fn()
            return
        except OSError as exc:
            last = exc
            close_word_document_if_open(path)
            time.sleep(0.35 + attempt * 0.25)
        except PermissionError as exc:
            last = exc
            close_word_document_if_open(path)
            time.sleep(0.35 + attempt * 0.25)
        except RuntimeError as exc:
            if is_file_lock_error(exc) or is_same_name_as_open_document_error(exc):
                last = exc
                close_word_document_if_open(path)
                time.sleep(0.35 + attempt * 0.25)
                continue
            raise
    raise RuntimeError(f"File locked or not writable: {path} ({last})") from last


def regenerate_and_open_docx(md_path: Path) -> Path:
    """Close open docx if present, rebuild from md (via temp), open in default app.

    Avoids Word error: cannot give a document the same name as an open document.
    Never kills WINWORD.EXE.
    """
    md_path = md_path.resolve()
    docx_path = docx_path_for_md(md_path)
    temp_docx = docx_path.with_name(docx_path.stem + ".__regen__.docx")
    open_path = {"path": docx_path}

    def _build() -> None:
        close_word_document_if_open(docx_path)
        time.sleep(0.45)
        if temp_docx.is_file():
            try:
                temp_docx.unlink()
            except OSError:
                pass
        try:
            convert_md_to_docx(md_path, temp_docx)
        except Exception as exc:
            if is_same_name_as_open_document_error(exc) or is_file_lock_error(exc):
                close_word_document_if_open(docx_path)
                time.sleep(0.6)
                convert_md_to_docx(md_path, temp_docx)
            else:
                raise
        open_path["path"] = _replace_with_temp(temp_docx, docx_path)

    try:
        _write_with_retry(docx_path, _build)
    except Exception as exc:
        if temp_docx.is_file():
            try:
                temp_docx.unlink()
            except OSError:
                pass
        if is_same_name_as_open_document_error(exc) or is_file_lock_error(exc):
            raise RuntimeError(
                f"Word/OneDrive still has {docx_path.name} locked. Close that Word tab "
                f"(File → Close), then File again. Details: {exc}"
            ) from exc
        raise

    _open_path_detached(open_path["path"])
    return open_path["path"]
