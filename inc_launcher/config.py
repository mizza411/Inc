"""Load launcher_config.json and resolve paths relative to Inc repo root."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

PACKAGE_DIR = Path(__file__).resolve().parent
INC_ROOT = PACKAGE_DIR.parent
DEFAULT_CONFIG = PACKAGE_DIR / "launcher_config.json"


def load_config(config_path: Path | None = None) -> Dict[str, Any]:
    path = Path(config_path or DEFAULT_CONFIG)
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    data["_config_path"] = str(path)
    data["_inc_root"] = str(INC_ROOT)
    return data


def resolve_path(relative: str, inc_root: Path | None = None) -> Path:
    root = inc_root or INC_ROOT
    return (root / relative).resolve()


def list_pillars(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    return config.get("pillars", [])


def list_global_actions(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    return config.get("global_actions", [])


def config_file_path(config_path: Path | None = None) -> Path:
    return Path(config_path or DEFAULT_CONFIG)


def is_interval_nudges_enabled(config_path: Path | None = None) -> bool:
    config = load_config(config_path)
    return bool((config.get("schedules") or {}).get("enabled", False))


def set_interval_nudges_enabled(enabled: bool, config_path: Path | None = None) -> None:
    path = config_file_path(config_path)
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    schedules = data.setdefault("schedules", {})
    schedules["enabled"] = enabled
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")
