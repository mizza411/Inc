"""Prevent multiple Inc Launcher tray processes (Phase 3)."""

from __future__ import annotations

import logging
import sys

logger = logging.getLogger(__name__)

_MUTEX_NAME = "Global\\IncLauncher_SingleInstance_v1"
_mutex_handle = None


def ensure_single_instance() -> bool:
    """
    Return True if this process should run the tray app.
    Return False if another instance is already running.
    """
    if sys.platform != "win32":
        return True

    import ctypes

    global _mutex_handle
    kernel32 = ctypes.windll.kernel32
    _mutex_handle = kernel32.CreateMutexW(None, False, _MUTEX_NAME)
    last_error = kernel32.GetLastError()
    # ERROR_ALREADY_EXISTS == 183
    if last_error == 183:
        logger.warning("Inc Launcher is already running (tray icon near the clock).")
        return False
    return True
