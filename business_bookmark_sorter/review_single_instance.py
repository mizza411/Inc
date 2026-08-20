"""Single-instance guard for Business links Bookmark Reviewer (BB-LINKS-UX-1 Phase 3)."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from business_bookmark_sorter.paths import DATA_DIR

logger = logging.getLogger(__name__)

_MUTEX_NAME = "Global\\IncBusinessBookmarkReviewer_v1"
_mutex_handle = None
FOCUS_REQUEST_PATH = DATA_DIR / "review_focus_request.flag"


def ensure_single_instance() -> bool:
    """
    Return True if this process should run the Reviewer.
    Return False if another Reviewer instance already holds the mutex.
    """
    if sys.platform != "win32":
        return True

    import ctypes

    global _mutex_handle
    kernel32 = ctypes.windll.kernel32
    _mutex_handle = kernel32.CreateMutexW(None, False, _MUTEX_NAME)
    last_error = kernel32.GetLastError()
    if last_error == 183:  # ERROR_ALREADY_EXISTS
        logger.info("Business links Bookmark Reviewer already running — requesting focus.")
        return False
    return True


def request_focus_existing() -> Path:
    """Signal the running Reviewer to raise its window."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    FOCUS_REQUEST_PATH.write_text("focus\n", encoding="utf-8")
    return FOCUS_REQUEST_PATH


def consume_focus_request() -> bool:
    """Return True once if a second launch asked to focus the window."""
    if not FOCUS_REQUEST_PATH.is_file():
        return False
    try:
        FOCUS_REQUEST_PATH.unlink()
    except OSError:
        return False
    return True
