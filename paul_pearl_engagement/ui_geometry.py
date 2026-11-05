"""Save/restore Paul Pearl Settings window position and size."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Optional

from paths import PACKAGE_DIR

logger = logging.getLogger(__name__)
GEOMETRY_FILENAME = "paul_pearl_ui_geometry.json"
DEFAULT_GEOMETRY = "420x280"
_SAVE_AFTER_MS = 400


def geometry_path() -> Path:
    return PACKAGE_DIR / GEOMETRY_FILENAME


def load_geometry() -> Optional[str]:
    path = geometry_path()
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            raw = data.get("settings_geometry")
            if isinstance(raw, str) and raw.strip():
                return raw.strip()
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        pass
    return None


def save_geometry(value: str) -> None:
    path = geometry_path()
    payload: dict[str, Any] = {"settings_geometry": value}
    try:
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        logger.debug("geometry save failed: %s", exc)


def bind_geometry_persist(window) -> None:
    """Debounced save on move/resize. Call after window is mapped."""

    after_id: dict[str, Any] = {"id": None}

    def _persist(_event=None) -> None:
        try:
            save_geometry(window.geometry())
        except Exception:
            pass

    def _schedule(_event=None) -> None:
        aid = after_id.get("id")
        if aid is not None:
            try:
                window.after_cancel(aid)
            except Exception:
                pass
        after_id["id"] = window.after(_SAVE_AFTER_MS, _persist)

    window.bind("<Configure>", _schedule)


def place_on_screen(window, geometry: Optional[str] = None) -> None:
    """Apply saved or default geometry; nudge on-screen if off-screen."""
    geo = geometry or load_geometry() or DEFAULT_GEOMETRY
    try:
        window.geometry(geo)
        window.update_idletasks()
        w = window.winfo_width()
        h = window.winfo_height()
        x = window.winfo_x()
        y = window.winfo_y()
        sw = window.winfo_screenwidth()
        sh = window.winfo_screenheight()
        if w < 80 or h < 80:
            window.geometry(DEFAULT_GEOMETRY)
            return
        nx = min(max(0, x), max(0, sw - w))
        ny = min(max(0, y), max(0, sh - h))
        if nx != x or ny != y:
            window.geometry(f"{w}x{h}+{nx}+{ny}")
    except Exception:
        try:
            window.geometry(DEFAULT_GEOMETRY)
        except Exception:
            pass
