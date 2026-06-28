"""Phase 4 interval nudges — schedule parsing and due-time logic (no tray wiring in 4.1)."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, FrozenSet, Iterable, List, Mapping, MutableSet, Optional, Tuple

from inc_launcher.config import list_global_actions, list_pillars

logger = logging.getLogger(__name__)

DAY_NAMES: Tuple[str, ...] = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
HUB_TARGET = "hub"


@dataclass(frozen=True)
class ScheduleEntry:
    id: str
    hour: int
    minute: int
    days: FrozenSet[str]
    target: str
    skip_when: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class ScheduleSettings:
    enabled: bool
    entries: Tuple[ScheduleEntry, ...]


def parse_time(value: str) -> Tuple[int, int]:
    """Parse HH:MM (24-hour) into hour and minute."""
    parts = value.strip().split(":")
    if len(parts) != 2:
        raise ValueError(f"Invalid time (expected HH:MM): {value!r}")
    hour, minute = int(parts[0]), int(parts[1])
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ValueError(f"Time out of range: {value!r}")
    return hour, minute


def parse_days(values: Iterable[str]) -> FrozenSet[str]:
    days = frozenset(day.strip().lower() for day in values)
    unknown = days - set(DAY_NAMES)
    if unknown:
        raise ValueError(f"Unknown day names: {sorted(unknown)}")
    return days


def day_name(when: datetime) -> str:
    return DAY_NAMES[when.weekday()]


def fire_key(entry_id: str, when: datetime) -> str:
    return f"{entry_id}:{when.strftime('%Y-%m-%d %H:%M')}"


def load_schedule_settings(config: Mapping[str, Any]) -> ScheduleSettings:
    block = config.get("schedules") or {}
    enabled = bool(block.get("enabled", False))
    raw_items = block.get("items") or []
    entries: List[ScheduleEntry] = []
    for raw in raw_items:
        hour, minute = parse_time(str(raw["time"]))
        entries.append(
            ScheduleEntry(
                id=str(raw["id"]),
                hour=hour,
                minute=minute,
                days=parse_days(raw.get("days") or []),
                target=str(raw["target"]),
                skip_when=raw.get("skip_when"),
            )
        )
    return ScheduleSettings(enabled=enabled, entries=tuple(entries))


def iter_menu_items(config: Mapping[str, Any]) -> Iterable[Dict[str, Any]]:
    for item in list_global_actions(config):
        yield item
    for pillar in list_pillars(config):
        for item in pillar.get("items", []):
            yield item


def find_menu_item_by_id(config: Mapping[str, Any], item_id: str) -> Optional[Dict[str, Any]]:
    for item in iter_menu_items(config):
        if item.get("id") == item_id:
            return dict(item)
    return None


def resolve_schedule_target(config: Mapping[str, Any], target: str) -> Optional[Dict[str, Any]]:
    """Return an action dict for a schedule target id, or hub pseudo-action."""
    if target == HUB_TARGET:
        return {"action": HUB_TARGET, "label": "Open Inc Hub"}
    item = find_menu_item_by_id(config, target)
    if item is None:
        logger.warning("Schedule target not found in menu config: %s", target)
    return item


def should_skip_entry(entry: ScheduleEntry, config: Mapping[str, Any]) -> bool:
    if not entry.skip_when:
        return False
    setting = entry.skip_when.get("setting")
    if not setting:
        return False
    settings = config.get("settings") or {}
    actual = settings.get(setting)
    expected = entry.skip_when.get("equals")
    return actual == expected


def entries_due_now(
    settings: ScheduleSettings,
    config: Mapping[str, Any],
    when: datetime,
    already_fired: MutableSet[str],
) -> List[ScheduleEntry]:
    """Return schedule entries that should fire at `when` (same calendar minute)."""
    if not settings.enabled:
        return []

    due: List[ScheduleEntry] = []
    today = day_name(when)
    for entry in settings.entries:
        if today not in entry.days:
            continue
        if when.hour != entry.hour or when.minute != entry.minute:
            continue
        if should_skip_entry(entry, config):
            continue
        key = fire_key(entry.id, when)
        if key in already_fired:
            continue
        due.append(entry)
    return due


def validate_schedule_targets(config: Mapping[str, Any]) -> List[str]:
    """Return list of unresolved target ids (empty if all valid)."""
    settings = load_schedule_settings(config)
    missing: List[str] = []
    for entry in settings.entries:
        if entry.target == HUB_TARGET:
            continue
        if find_menu_item_by_id(config, entry.target) is None:
            missing.append(entry.target)
    return missing
