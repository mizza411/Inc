"""Open the Paul Pearl market / air-gap note (extra tray menu — not startup/schedule)."""

from __future__ import annotations

import logging
import os

from paths import paul_pearl_note_required, resolve_paul_pearl_note

logger = logging.getLogger(__name__)


def open_paul_pearl_note() -> dict:
    """Open paul_pearl_market_airgap.md via the OS. Returns a small result dict."""
    path = resolve_paul_pearl_note()
    if path is None:
        try:
            path = paul_pearl_note_required()
        except FileNotFoundError as exc:
            logger.error("%s", exc)
            return {"ok": False, "error": str(exc), "path": None}
    try:
        os.startfile(str(path))  # type: ignore[attr-defined]
        return {"ok": True, "path": str(path)}
    except OSError as exc:
        logger.error("startfile failed: %s", exc)
        return {"ok": False, "error": str(exc), "path": str(path)}
