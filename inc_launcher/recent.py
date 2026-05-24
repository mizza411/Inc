"""Track recently opened launcher items (Phase 2 hub)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from inc_launcher.config import PACKAGE_DIR

RECENT_FILE = PACKAGE_DIR / "recent_items.json"
MAX_RECENT = 8


def _item_key(item: Dict[str, Any]) -> str:
    return f"{item.get('label', '')}|{item.get('action', '')}|{item.get('path', item.get('url', item.get('command', '')))}"


def load_recent() -> List[Dict[str, Any]]:
    if not RECENT_FILE.is_file():
        return []
    try:
        with RECENT_FILE.open(encoding="utf-8") as f:
            data = json.load(f)
        items = data.get("recent", [])
        return items if isinstance(items, list) else []
    except (OSError, json.JSONDecodeError, TypeError):
        return []


def save_recent(items: List[Dict[str, Any]]) -> None:
    RECENT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with RECENT_FILE.open("w", encoding="utf-8") as f:
        json.dump({"recent": items[:MAX_RECENT]}, f, indent=2)


def record_recent(item: Dict[str, Any], pillar_id: str | None = None) -> None:
    entry = {k: v for k, v in item.items() if not str(k).startswith("_")}
    if pillar_id:
        entry["pillar_id"] = pillar_id
    key = _item_key(entry)
    recent = [i for i in load_recent() if _item_key(i) != key]
    recent.insert(0, entry)
    save_recent(recent)


def list_pinned(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    pinned: List[Dict[str, Any]] = []
    for pillar in config.get("pillars", []):
        for item in pillar.get("items", []):
            if item.get("pinned"):
                entry = dict(item)
                entry["pillar_id"] = pillar.get("id", "")
                entry["pillar_label"] = pillar.get("label", "")
                pinned.append(entry)
    return pinned
