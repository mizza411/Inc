"""Paul Pearl engagement tray lifecycle breadcrumbs (absolute path under package)."""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

from paths import PACKAGE_DIR

LOG_PATH = PACKAGE_DIR / "paul_pearl_engagement.log"


def lifecycle_log_path() -> Path:
    return LOG_PATH


def append_lifecycle(message: str, *, log_path: Path | None = None) -> None:
    """Append one INFO breadcrumb. Never raises to callers. No secrets."""
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
        pass
