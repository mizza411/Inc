"""While-running formulation catch-up after cloud B (section 19 Phase 7.11.1).

Fires the same catch-up chain once per local calendar day at/after 11:15
(default), without restarting the tray. Independent of Interval nudges.
"""

from __future__ import annotations

import json
import logging
import threading
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional, Set

from inc_launcher.config import PACKAGE_DIR, is_formulation_catchup_enabled
from inc_launcher.formulation_catchup import start_formulation_catchup_background

logger = logging.getLogger(__name__)

# After Automation B (11:00 WAT). Uses the PC local clock (expected WAT).
POST_B_HOUR = 11
POST_B_MINUTE = 15
POLL_SECONDS = 30
FIRED_STATE_FILE = PACKAGE_DIR / "formulation_catchup_schedule_fired.json"
MAX_FIRED_DAYS = 21

_scheduler: Optional["FormulationCatchupScheduler"] = None


def day_fire_key(when: datetime) -> str:
    return when.strftime("%Y-%m-%d")


def past_or_at_post_b(when: datetime, *, hour: int = POST_B_HOUR, minute: int = POST_B_MINUTE) -> bool:
    return (when.hour, when.minute) >= (hour, minute)


def load_fired_days(path: Path | None = None) -> Set[str]:
    state_path = path or FIRED_STATE_FILE
    if not state_path.is_file():
        return set()
    try:
        with state_path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        keys = data.get("fired", [])
        if not isinstance(keys, list):
            return set()
        return {str(k) for k in keys}
    except (OSError, json.JSONDecodeError, TypeError):
        return set()


def save_fired_days(keys: Set[str], path: Path | None = None) -> None:
    state_path = path or FIRED_STATE_FILE
    pruned = sorted(keys)[-MAX_FIRED_DAYS:]
    state_path.parent.mkdir(parents=True, exist_ok=True)
    with state_path.open("w", encoding="utf-8") as handle:
        json.dump({"fired": pruned}, handle, indent=2)


def mark_post_b_day_fired(
    when: datetime | None = None,
    path: Path | None = None,
) -> str:
    """Record today's post-B slot as done (e.g. tray-start catch-up already covers it)."""
    when = when or datetime.now()
    key = day_fire_key(when)
    state_path = path or FIRED_STATE_FILE
    fired = load_fired_days(state_path)
    if key not in fired:
        fired.add(key)
        save_fired_days(fired, state_path)
        logger.info("Formulation post-B day marked fired (start catch-up covers): %s", key)
    return key


def should_fire_post_b(
    when: datetime,
    fired: Set[str],
    *,
    enabled: bool,
    hour: int = POST_B_HOUR,
    minute: int = POST_B_MINUTE,
) -> bool:
    """True once per day at/after the post-B slot when catch-up is enabled."""
    if not enabled:
        return False
    if not past_or_at_post_b(when, hour=hour, minute=minute):
        return False
    return day_fire_key(when) not in fired


class FormulationCatchupScheduler:
    """Daemon poller: one catch-up per day at/after post-B time while tray is up."""

    def __init__(
        self,
        *,
        enabled_fn: Callable[[], bool],
        fire_fn: Callable[[], None],
        state_path: Path | None = None,
        hour: int = POST_B_HOUR,
        minute: int = POST_B_MINUTE,
        poll_seconds: int = POLL_SECONDS,
    ) -> None:
        self._enabled_fn = enabled_fn
        self._fire_fn = fire_fn
        self._state_path = state_path or FIRED_STATE_FILE
        self._hour = hour
        self._minute = minute
        self._poll_seconds = poll_seconds
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._fired = load_fired_days(self._state_path)
        self._lock = threading.Lock()

    def start(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._loop,
            daemon=True,
            name="formulation-catchup-schedule",
        )
        self._thread.start()
        logger.info(
            "Formulation catch-up schedule started (post-B %02d:%02d local, poll %ss)",
            self._hour,
            self._minute,
            self._poll_seconds,
        )

    def stop(self) -> None:
        self._stop.set()

    def tick(self, when: datetime | None = None) -> bool:
        """Run one check. Returns True if catch-up was started."""
        when = when or datetime.now()
        with self._lock:
            enabled = bool(self._enabled_fn())
            if not should_fire_post_b(
                when,
                self._fired,
                enabled=enabled,
                hour=self._hour,
                minute=self._minute,
            ):
                return False
            key = day_fire_key(when)
            try:
                self._fire_fn()
            except Exception:
                logger.exception("Formulation post-B catch-up fire failed")
                return False
            self._fired.add(key)
            try:
                save_fired_days(self._fired, self._state_path)
            except OSError as exc:
                logger.warning("Could not save catch-up schedule fired state: %s", exc)
            logger.info("Formulation post-B catch-up fired for %s", key)
            return True

    def _loop(self) -> None:
        # Wait before first tick so tray-start catch-up is not raced on boot.
        # Missed 11:15 while already up is still covered on the next poll.
        while not self._stop.wait(self._poll_seconds):
            try:
                self.tick()
            except Exception:
                logger.exception("Formulation catch-up schedule tick failed")


def start_formulation_catchup_schedule(
    *,
    config_path: Path | None = None,
    repo_root: Path | None = None,
    state_path: Path | None = None,
) -> FormulationCatchupScheduler:
    """Start the while-running post-B catch-up poller (singleton)."""
    global _scheduler
    if _scheduler is not None:
        return _scheduler

    def _enabled() -> bool:
        return is_formulation_catchup_enabled(config_path)

    def _fire() -> None:
        start_formulation_catchup_background(
            enabled=is_formulation_catchup_enabled(config_path),
            repo_root=repo_root,
        )

    _scheduler = FormulationCatchupScheduler(
        enabled_fn=_enabled,
        fire_fn=_fire,
        state_path=state_path,
    )
    _scheduler.start()
    return _scheduler


def stop_formulation_catchup_schedule() -> None:
    global _scheduler
    if _scheduler is not None:
        _scheduler.stop()
        _scheduler = None
