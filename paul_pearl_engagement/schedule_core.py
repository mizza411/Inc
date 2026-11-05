"""Weekday slot helpers (vendored for Inc — no project_reminder import)."""

from __future__ import annotations

import socket
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Sequence, Set, Tuple

DEFAULT_SLOTS = ("10:00", "17:00")
DEFAULT_COOLDOWN_MINUTES = 25
DEFAULT_INTERNET_CHECK_TIMEOUT_SECONDS = 5.0
DEFAULT_INTERNET_PROBE_URLS = (
    "https://www.google.com/generate_204",
)
POLL_INTERVAL_MS = 30_000


@dataclass
class ScheduleConfig:
    enabled: bool = True
    weekdays_only: bool = True
    slots: Tuple[str, ...] = DEFAULT_SLOTS
    show_window_on_scheduled: bool = False
    minimize_to_tray_after_scheduled: bool = False
    scheduled_cooldown_minutes: int = DEFAULT_COOLDOWN_MINUTES
    require_internet_for_scheduled: bool = False
    internet_check_timeout_seconds: float = DEFAULT_INTERNET_CHECK_TIMEOUT_SECONDS
    internet_probe_urls: Tuple[str, ...] = DEFAULT_INTERNET_PROBE_URLS

    @property
    def scheduled_cooldown_seconds(self) -> float:
        return max(0, int(self.scheduled_cooldown_minutes)) * 60.0

    @classmethod
    def from_dict(cls, data: dict) -> "ScheduleConfig":
        try:
            scheduled_cooldown_minutes = int(
                data.get("scheduled_cooldown_minutes", DEFAULT_COOLDOWN_MINUTES)
            )
        except (TypeError, ValueError):
            scheduled_cooldown_minutes = DEFAULT_COOLDOWN_MINUTES
        scheduled_cooldown_minutes = max(0, scheduled_cooldown_minutes)
        try:
            internet_check_timeout_seconds = float(
                data.get(
                    "internet_check_timeout_seconds",
                    DEFAULT_INTERNET_CHECK_TIMEOUT_SECONDS,
                )
            )
        except (TypeError, ValueError):
            internet_check_timeout_seconds = DEFAULT_INTERNET_CHECK_TIMEOUT_SECONDS
        internet_check_timeout_seconds = max(1.0, internet_check_timeout_seconds)
        raw_probes = data.get("internet_probe_urls")
        probe_urls: List[str] = []
        if isinstance(raw_probes, list):
            for item in raw_probes:
                text = str(item).strip()
                if text.startswith("http://") or text.startswith("https://"):
                    probe_urls.append(text)
        if not probe_urls:
            probe_urls = list(DEFAULT_INTERNET_PROBE_URLS)
        raw_slots = data.get("slots", list(DEFAULT_SLOTS))
        slots: List[str] = []
        if isinstance(raw_slots, list):
            for item in raw_slots:
                normalized = normalize_slot(str(item))
                if normalized:
                    slots.append(normalized)
        if not slots:
            slots = list(DEFAULT_SLOTS)
        return cls(
            enabled=bool(data.get("enabled", True)),
            weekdays_only=bool(data.get("weekdays_only", True)),
            slots=tuple(slots),
            show_window_on_scheduled=bool(data.get("show_window_on_scheduled", False)),
            minimize_to_tray_after_scheduled=bool(
                data.get("minimize_to_tray_after_scheduled", False)
            ),
            scheduled_cooldown_minutes=scheduled_cooldown_minutes,
            require_internet_for_scheduled=bool(
                data.get("require_internet_for_scheduled", False)
            ),
            internet_check_timeout_seconds=internet_check_timeout_seconds,
            internet_probe_urls=tuple(probe_urls),
        )


def normalize_slot(value: str) -> Optional[str]:
    text = (value or "").strip()
    if not text:
        return None
    parts = text.split(":")
    if len(parts) != 2:
        return None
    try:
        hour = int(parts[0])
        minute = int(parts[1])
    except ValueError:
        return None
    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        return None
    return f"{hour:02d}:{minute:02d}"


def parse_slot(slot: str) -> Tuple[int, int]:
    normalized = normalize_slot(slot)
    if not normalized:
        raise ValueError(f"Invalid slot: {slot!r}")
    hour, minute = normalized.split(":")
    return int(hour), int(minute)


def is_weekday(now: datetime, weekdays_only: bool) -> bool:
    if not weekdays_only:
        return True
    return now.weekday() < 5


def slot_fired_key(now: datetime, slot: str) -> str:
    return f"{now.date().isoformat()}:{normalize_slot(slot) or slot}"


def prune_fired_keys(fired: Set[str], today_iso: str) -> None:
    stale = [k for k in fired if not k.startswith(f"{today_iso}:")]
    for key in stale:
        fired.discard(key)


def due_slot(
    now: datetime,
    config: ScheduleConfig,
    fired_today: Set[str],
) -> Optional[str]:
    if not config.enabled:
        return None
    if not is_weekday(now, config.weekdays_only):
        return None
    today_iso = now.date().isoformat()
    prune_fired_keys(fired_today, today_iso)
    for slot in config.slots:
        try:
            hour, minute = parse_slot(slot)
        except ValueError:
            continue
        if now.hour != hour or now.minute != minute:
            continue
        key = slot_fired_key(now, slot)
        if key in fired_today:
            continue
        return normalize_slot(slot) or slot
    return None


def mark_slot_fired(fired_today: Set[str], key: str) -> None:
    fired_today.add(key)


def _probe_url_reachable(url: str, timeout: float, *, use_head: bool) -> bool:
    try:
        if use_head:
            request = urllib.request.Request(
                url,
                method="HEAD",
                headers={"User-Agent": "PaulPearlEngagement/1.0"},
            )
        else:
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "PaulPearlEngagement/1.0"},
            )
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = getattr(response, "status", 200)
            return 200 <= status < 400
    except urllib.error.HTTPError as exc:
        return bool(exc.code and exc.code < 500)
    except (urllib.error.URLError, OSError, ValueError, socket.timeout):
        return False


def check_internet_available(
    timeout_seconds: float = DEFAULT_INTERNET_CHECK_TIMEOUT_SECONDS,
    probe_urls: Optional[Sequence[str]] = None,
) -> bool:
    urls = tuple(probe_urls) if probe_urls else DEFAULT_INTERNET_PROBE_URLS
    timeout = max(1.0, float(timeout_seconds))
    for url in urls:
        if _probe_url_reachable(url, timeout, use_head=True):
            return True
        if _probe_url_reachable(url, timeout, use_head=False):
            return True
    try:
        socket.create_connection(("1.1.1.1", 443), timeout=timeout)
        return True
    except OSError:
        return False


def within_scheduled_cooldown(
    last_scheduled_finish_epoch: Optional[float],
    cooldown_seconds: float,
    now_epoch: Optional[float] = None,
) -> bool:
    if cooldown_seconds <= 0 or last_scheduled_finish_epoch is None:
        return False
    now = now_epoch if now_epoch is not None else time.time()
    return (now - last_scheduled_finish_epoch) < cooldown_seconds


def cooldown_remaining_seconds(
    last_scheduled_finish_epoch: Optional[float],
    cooldown_seconds: float,
    now_epoch: Optional[float] = None,
) -> int:
    if not within_scheduled_cooldown(
        last_scheduled_finish_epoch, cooldown_seconds, now_epoch
    ):
        return 0
    now = now_epoch if now_epoch is not None else time.time()
    remaining = cooldown_seconds - (now - last_scheduled_finish_epoch)
    return max(0, int(remaining))
