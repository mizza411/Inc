"""Simple Windows mutex so a second engagement tray exits instead of duplicating."""

from __future__ import annotations

import ctypes
import logging
import sys

from menu_labels import APP_TITLE

logger = logging.getLogger(__name__)

_MUTEX_NAME = "Local\\PaulPearlEngagementTray"
_ERROR_ALREADY_EXISTS = 183
_handle = None


def try_acquire() -> bool:
    """Return True if this process owns the mutex. False if another instance holds it."""
    global _handle
    try:
        kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
        handle = kernel32.CreateMutexW(None, False, _MUTEX_NAME)
        if not handle:
            return True
        already = kernel32.GetLastError() == _ERROR_ALREADY_EXISTS
        if already:
            kernel32.CloseHandle(handle)
            return False
        _handle = handle
        return True
    except Exception as exc:
        logger.debug("mutex acquire failed (allowing start): %s", exc)
        return True


def release() -> None:
    global _handle
    if _handle is None:
        return
    try:
        ctypes.windll.kernel32.CloseHandle(_handle)  # type: ignore[attr-defined]
    except Exception:
        pass
    _handle = None


def notify_already_running() -> None:
    msg = f"{APP_TITLE} tray is already running."
    try:
        from plyer import notification

        notification.notify(
            title=APP_TITLE,
            message=msg,
            app_name=APP_TITLE,
            timeout=4,
        )
    except Exception:
        print(msg, file=sys.stderr)
