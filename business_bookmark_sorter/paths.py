"""Paths relative to Inc repo root."""

from __future__ import annotations

import os
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
INC_ROOT = PACKAGE_DIR.parent
CONFIG_PATH = PACKAGE_DIR / "config" / "routes.json"
DATA_DIR = PACKAGE_DIR / "data"
QUEUE_PATH = DATA_DIR / "queue.json"
DISCOVER_PATH = DATA_DIR / "discover_report.json"
INBOX_MD = INC_ROOT / "business_bookmark_sorter" / "Business Links.md"


def default_chrome_bookmarks_path() -> Path:
    local = os.environ.get("LOCALAPPDATA", "")
    if not local:
        raise OSError("LOCALAPPDATA is not set")
    return (
        Path(local)
        / "Google"
        / "Chrome"
        / "User Data"
        / "Default"
        / "Bookmarks"
    )
