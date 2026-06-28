"""Background interval nudge scheduler (Phase 4.2)."""

from __future__ import annotations

import json
import logging
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set

from inc_launcher.config import PACKAGE_DIR, load_config
from inc_launcher.scheduled_nudges import (
    HUB_TARGET,
    ScheduleEntry,
    entries_due_now,
    fire_key,
    load_schedule_settings,
    resolve_schedule_target,
)

logger = logging.getLogger(__name__)

FIRED_STATE_FILE = PACKAGE_DIR / "schedule_fired.json"
POLL_SECONDS = 30
MAX_FIRED_AGE_DAYS = 14

_scheduler: Optional["NudgeScheduler"] = None


def load_fired_keys() -> Set[str]:
    if not FIRED_STATE_FILE.is_file():
        return set()
    try:
        with FIRED_STATE_FILE.open(encoding="utf-8") as handle:
            data = json.load(handle)
        keys = data.get("fired", [])
        if not isinstance(keys, list):
            return set()
        return prune_fired_keys(set(str(key) for key in keys))
    except (OSError, json.JSONDecodeError, TypeError):
        return set()


def prune_fired_keys(keys: Set[str]) -> Set[str]:
    cutoff = datetime.now() - timedelta(days=MAX_FIRED_AGE_DAYS)
    kept: Set[str] = set()
    for key in keys:
        try:
            timestamp = key.split(":", 1)[1]
            fired_at = datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
        except (IndexError, ValueError):
            kept.add(key)
            continue
        if fired_at >= cutoff:
            kept.add(key)
    return kept


def save_fired_keys(keys: Set[str]) -> None:
    pruned = prune_fired_keys(keys)
    FIRED_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with FIRED_STATE_FILE.open("w", encoding="utf-8") as handle:
        json.dump({"fired": sorted(pruned)}, handle, indent=2)


def execute_nudge(
    entry: ScheduleEntry,
    config: Dict[str, Any],
    *,
    open_hub: Callable[[Dict[str, Any]], None],
    run_menu_action: Callable[[Dict[str, Any]], None],
) -> bool:
    action = resolve_schedule_target(config, entry.target)
    if action is None:
        return False
    try:
        if action.get("action") == HUB_TARGET:
            open_hub(config)
        else:
            run_menu_action(action)
        logger.info("Scheduled nudge fired: %s (%s)", entry.id, entry.target)
        return True
    except Exception:
        logger.exception("Scheduled nudge failed: %s", entry.id)
        return False


class NudgeScheduler:
    """Polls schedule config and fires due nudges from a daemon thread."""

    def __init__(
        self,
        config_path: Path | None = None,
        *,
        open_hub: Callable[[Dict[str, Any]], None],
        run_menu_action: Callable[[Dict[str, Any]], None],
        poll_seconds: int = POLL_SECONDS,
    ) -> None:
        self._config_path = config_path
        self._open_hub = open_hub
        self._run_menu_action = run_menu_action
        self._poll_seconds = poll_seconds
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._fired = load_fired_keys()
        self._lock = threading.Lock()

    def start(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._loop,
            daemon=True,
            name="inc-nudge-scheduler",
        )
        self._thread.start()
        settings = load_schedule_settings(load_config(self._config_path))
        state = "enabled" if settings.enabled else "disabled"
        logger.info("Nudge scheduler started (%s; poll every %ss)", state, self._poll_seconds)

    def stop(self) -> None:
        self._stop.set()

    def tick(self, when: datetime | None = None) -> List[str]:
        """Run one schedule check. Returns ids of entries fired."""
        when = when or datetime.now()
        config = load_config(self._config_path)
        settings = load_schedule_settings(config)
        fired_ids: List[str] = []

        with self._lock:
            due = entries_due_now(settings, config, when, self._fired)
            for entry in due:
                key = fire_key(entry.id, when)
                if execute_nudge(
                    entry,
                    config,
                    open_hub=self._open_hub,
                    run_menu_action=self._run_menu_action,
                ):
                    self._fired.add(key)
                    fired_ids.append(entry.id)
            if fired_ids:
                save_fired_keys(self._fired)
        return fired_ids

    def _loop(self) -> None:
        while not self._stop.wait(self._poll_seconds):
            try:
                self.tick()
            except Exception:
                logger.exception("Nudge scheduler tick failed")


def start_nudge_scheduler(
    config_path: Path | None,
    *,
    open_hub: Callable[[Dict[str, Any]], None],
    run_menu_action: Callable[[Dict[str, Any]], None],
) -> NudgeScheduler:
    global _scheduler
    if _scheduler is None:
        _scheduler = NudgeScheduler(
            config_path,
            open_hub=open_hub,
            run_menu_action=run_menu_action,
        )
        _scheduler.start()
    return _scheduler


def stop_nudge_scheduler() -> None:
    global _scheduler
    if _scheduler is not None:
        _scheduler.stop()
        _scheduler = None
