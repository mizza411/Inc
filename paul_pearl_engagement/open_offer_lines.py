"""Open the sole study doc still used at startup/slots: offer_lines.docx."""

from __future__ import annotations

import logging
import os

from lifecycle_log import append_lifecycle
from paths import offer_lines_docx_required, resolve_offer_lines_docx

logger = logging.getLogger(__name__)


def open_offer_lines_docx() -> dict:
    """Open offer_lines.docx via the OS. Returns a small result dict."""
    path = resolve_offer_lines_docx()
    if path is None:
        try:
            path = offer_lines_docx_required()
        except FileNotFoundError as exc:
            logger.error("%s", exc)
            append_lifecycle("offer_lines.docx open failed")
            return {"ok": False, "error": str(exc), "path": None}
    try:
        os.startfile(str(path))  # type: ignore[attr-defined]
        append_lifecycle("opened offer_lines.docx")
        return {"ok": True, "path": str(path)}
    except OSError as exc:
        logger.error("startfile failed: %s", exc)
        append_lifecycle("offer_lines.docx open failed")
        return {"ok": False, "error": str(exc), "path": str(path)}


def maybe_open_on_startup(*, enabled: bool) -> dict | None:
    if not enabled:
        return None
    return open_offer_lines_docx()
