"""Package paths for network_ask_reminder."""

from __future__ import annotations

from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
INC_ROOT = PACKAGE_DIR.parent
CONFIG_EXAMPLE = PACKAGE_DIR / "config.example.json"
CONFIG_LOCAL = PACKAGE_DIR / "config.json"
DATA_DIR = PACKAGE_DIR / "data"
DEFAULT_LOG = DATA_DIR / "ask_log.jsonl"
