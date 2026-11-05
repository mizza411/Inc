"""Resolve Inc paths for Paul Pearl engagement.

Startup/schedule sole auto-open: offer_lines.docx.
Extra tray menu (not schedule): Paul Pearl market/air-gap note.
"""

from __future__ import annotations

import os
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
INC_ROOT = PACKAGE_DIR.parent

DOCX_NAME = "offer_lines.docx"
REL_UNDER_INC = Path("Upstream-Drive-Consultancy") / DOCX_NAME

# PAUL-PEARL-UPSTREAM-1 Phase 0 lock
NOTE_REL = Path("Paul-Pearl") / "paul_pearl_market_airgap.md"

_DOCX_CANDIDATES = (
    INC_ROOT / REL_UNDER_INC,
    Path(r"C:\dev\Inc") / REL_UNDER_INC,
    Path(os.environ.get("INC_ROOT", "")) / REL_UNDER_INC if os.environ.get("INC_ROOT") else None,
)

_NOTE_CANDIDATES = (
    INC_ROOT / NOTE_REL,
    Path(r"C:\dev\Inc") / NOTE_REL,
    Path(os.environ.get("INC_ROOT", "")) / NOTE_REL if os.environ.get("INC_ROOT") else None,
)


def resolve_offer_lines_docx() -> Path | None:
    for p in _DOCX_CANDIDATES:
        if p is None:
            continue
        try:
            if p.is_file():
                return p.resolve()
        except OSError:
            continue
    return None


def offer_lines_docx_required() -> Path:
    found = resolve_offer_lines_docx()
    if found is None:
        raise FileNotFoundError(
            "offer_lines.docx not found. Expected under "
            r"C:\dev\Inc\Upstream-Drive-Consultancy\offer_lines.docx "
            "(rebuild: pandoc offer_lines.md -o offer_lines.docx)."
        )
    return found


def resolve_paul_pearl_note() -> Path | None:
    for p in _NOTE_CANDIDATES:
        if p is None:
            continue
        try:
            if p.is_file():
                return p.resolve()
        except OSError:
            continue
    return None


def paul_pearl_note_required() -> Path:
    found = resolve_paul_pearl_note()
    if found is None:
        raise FileNotFoundError(
            "Paul Pearl note not found. Expected under "
            r"C:\dev\Inc\Paul-Pearl\paul_pearl_market_airgap.md"
        )
    return found

