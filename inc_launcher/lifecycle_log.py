"""Inc Launcher tray lifecycle breadcrumbs (file log under this package).

Lines: starting, Exit selected, Restart selected, shutting down.
Absolute path (not CWD). No secrets. One file for this product.
"""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

from inc_launcher.config import PACKAGE_DIR

LOG_PATH = PACKAGE_DIR / "tray_lifecycle.log"


def lifecycle_log_path() -> Path:
    return LOG_PATH


def append_lifecycle(message: str, *, log_path: Path | None = None) -> None:
    """Append one INFO breadcrumb. Never raises to callers."""
    path = log_path if log_path is not None else LOG_PATH
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pid = os.getpid()
        line = f"{ts} INFO pid={pid} {message}\n"
        with path.open("a", encoding="utf-8") as handle:
            handle.write(line)
            handle.flush()
    except Exception:
        # Lifecycle log must not take down the tray.
        pass
