"""Load and patch-save the two clocks that auto-open Inc Hub.

Other schedule rows are left as they are. This module does not open a window.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from inc_launcher.config import config_file_path, load_config
from inc_launcher.scheduled_nudges import DAY_NAMES, parse_days, parse_time

# Only these rows open Inc Hub. Do not add task.md, Problem ID, bookmarks, or YouTube.
HUB_OPEN_TIME_IDS: tuple[str, ...] = ("daily_inc_hub", "network_ask_mwf")


class HubOpenTimeError(ValueError):
    """The clock change was refused. The config file was not written."""


@dataclass(frozen=True)
class HubOpenTime:
    id: str
    hour: int
    minute: int
    days: tuple[str, ...]

    @property
    def time_text(self) -> str:
        return f"{self.hour:02d}:{self.minute:02d}"


def _ordered_days(days: Iterable[str]) -> tuple[str, ...]:
    chosen = parse_days(days)
    if not chosen:
        raise HubOpenTimeError("Pick at least one day.")
    return tuple(day for day in DAY_NAMES if day in chosen)


def validate_hub_open_time(hour: int, minute: int, days: Iterable[str]) -> None:
    """Raise HubOpenTimeError when the clock cannot be saved. Does not write."""
    _check_clock(hour, minute, days)


def _check_clock(hour: int, minute: int, days: Iterable[str]) -> tuple[str, tuple[str, ...]]:
    try:
        parsed_hour, parsed_minute = parse_time(f"{int(hour):02d}:{int(minute):02d}")
    except (TypeError, ValueError) as exc:
        raise HubOpenTimeError("Enter an hour from 0 to 23 and a minute from 0 to 59.") from exc
    try:
        ordered = _ordered_days(days)
    except ValueError as exc:
        raise HubOpenTimeError(str(exc)) from exc
    return f"{parsed_hour:02d}:{parsed_minute:02d}", ordered


def _row_from_item(item: dict) -> HubOpenTime:
    hour, minute = parse_time(str(item["time"]))
    ordered = _ordered_days(item.get("days") or [])
    return HubOpenTime(id=str(item["id"]), hour=hour, minute=minute, days=ordered)


def load_hub_open_times(config_path: Path | None = None) -> dict[str, HubOpenTime]:
    """Return the two Hub-opening clocks. Raises if either id is missing."""
    config = load_config(config_path)
    items = (config.get("schedules") or {}).get("items") or []
    found: dict[str, HubOpenTime] = {}
    for item in items:
        item_id = str(item.get("id"))
        if item_id in HUB_OPEN_TIME_IDS:
            found[item_id] = _row_from_item(item)
    missing = [item_id for item_id in HUB_OPEN_TIME_IDS if item_id not in found]
    if missing:
        raise HubOpenTimeError("Hub open time rows are missing: " + ", ".join(missing))
    return found


def save_hub_open_time(
    entry_id: str,
    hour: int,
    minute: int,
    days: Iterable[str],
    config_path: Path | None = None,
) -> None:
    """Patch one Hub-opening row's time and days. Other keys and rows stay."""
    if entry_id not in HUB_OPEN_TIME_IDS:
        raise HubOpenTimeError("That clock is not a Hub open time.")
    time_text, ordered_days = _check_clock(hour, minute, days)

    path = config_file_path(config_path)
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    items = (data.get("schedules") or {}).get("items") or []
    target = None
    for item in items:
        if str(item.get("id")) == entry_id:
            target = item
            break
    if target is None:
        raise HubOpenTimeError("Hub open time row was not found.")

    target["time"] = time_text
    target["days"] = list(ordered_days)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


GEOMETRY_SETTINGS_KEY = "hub_open_times_window"
MIN_WINDOW_WIDTH = 320
MIN_WINDOW_HEIGHT = 200


def place_on_visible_screen(
    x: int,
    y: int,
    width: int,
    height: int,
    screen_width: int,
    screen_height: int,
) -> tuple[int, int, int, int]:
    """Keep a saved spot on the visible screen. A fully off-screen spot moves to 40, 40."""
    width = int(width)
    height = int(height)
    if width < MIN_WINDOW_WIDTH or height < MIN_WINDOW_HEIGHT:
        width, height = 640, 360
    if screen_width > 0:
        width = min(width, screen_width)
    if screen_height > 0:
        height = min(height, screen_height)
    x = int(x)
    y = int(y)
    on_screen = x + width > 0 and y + height > 0 and x < screen_width and y < screen_height
    if not on_screen:
        return 40, 40, width, height
    return x, y, width, height


def load_hub_open_times_geometry(config_path: Path | None = None) -> dict[str, int] | None:
    config = load_config(config_path)
    block = (config.get("settings") or {}).get(GEOMETRY_SETTINGS_KEY)
    if not isinstance(block, dict):
        return None
    try:
        return {
            "x": int(block["x"]),
            "y": int(block["y"]),
            "width": int(block["width"]),
            "height": int(block["height"]),
        }
    except (KeyError, TypeError, ValueError):
        return None


def save_hub_open_times_geometry(
    x: int,
    y: int,
    width: int,
    height: int,
    config_path: Path | None = None,
) -> None:
    """Patch only this window's place and size. Tiny sizes are ignored."""
    if int(width) < MIN_WINDOW_WIDTH or int(height) < MIN_WINDOW_HEIGHT:
        return
    path = config_file_path(config_path)
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    settings = data.setdefault("settings", {})
    settings[GEOMETRY_SETTINGS_KEY] = {
        "x": int(x),
        "y": int(y),
        "width": int(width),
        "height": int(height),
    }
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")
