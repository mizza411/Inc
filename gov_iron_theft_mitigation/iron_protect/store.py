"""Simple JSON store for pilot demo data (no secrets)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_DATA = {
    "assets": [],
    "tickets": [],
    "users": [],
    "devices": [],
}


class JsonStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path
        self._data: dict[str, Any] = {
            "assets": [],
            "tickets": [],
            "users": [],
            "devices": [],
        }
        if path and path.exists():
            self.load()

    def load(self) -> None:
        if not self.path:
            return
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        for key in DEFAULT_DATA:
            self._data[key] = list(raw.get(key, []))

    def save(self) -> None:
        if not self.path:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(self._data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def section(self, name: str) -> list[dict[str, Any]]:
        if name not in self._data:
            raise KeyError(name)
        return self._data[name]

    def replace_section(self, name: str, rows: list[dict[str, Any]]) -> None:
        self._data[name] = list(rows)
        self.save()
