"""Prevent multiple Inc Launcher tray processes (Phase 3 + INC-TRAY-RESTART-1)."""

from __future__ import annotations

import logging
import sys
import time
from collections.abc import Sequence

logger = logging.getLogger(__name__)

_MUTEX_NAME = "Global\\IncLauncher_SingleInstance_v1"
_mutex_handle = None

BYPASS_FLAG = "--tray-restart"


def bypass_requested(argv: Sequence[str] | None = None) -> bool:
    """True when argv includes the Restart handoff flag."""
    return BYPASS_FLAG in list(sys.argv if argv is None else argv)


def release_single_instance() -> None:
    """Close the mutex handle so a replacement process can acquire it."""
    if sys.platform != "win32":
        return
    global _mutex_handle
    if not _mutex_handle:
        return
    import ctypes

    try:
        ctypes.windll.kernel32.CloseHandle(_mutex_handle)
    except Exception:
        logger.exception("Failed to release single-instance mutex")
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


def acquire_for_start(
    *,
    bypass: bool = False,
    retries: int = 40,
    delay_s: float = 0.1,
) -> bool:
    """
    Take the single-instance mutex for a normal start or Restart handoff.

    On ``bypass`` (``--tray-restart``), retry briefly so the old process can
    release the mutex after ``exit_before_spawn`` teardown.
    """
    if not bypass:
        return ensure_single_instance()

    for attempt in range(max(1, retries)):
        if ensure_single_instance():
            if attempt:
                logger.info(
                    "Single-instance mutex acquired after Restart handoff (%s tries)",
                    attempt + 1,
                )
            return True
        release_single_instance()
        time.sleep(delay_s)

    logger.error(
        "Restart handoff failed: could not acquire single-instance lock after %s tries",
        retries,
    )
    return False
