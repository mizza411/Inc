"""While-running formulation catch-up after cloud B (section 19 Phase 7.11).

7.11.1: once per local day at/after 11:15.
7.11.2: if today's pack is still not shown, capped soft retries every
RETRY_INTERVAL_MINUTES until shown or end of day. MAX_LATE_RETRIES=0
disables retries only (primary 11:15 still runs).
"""

from __future__ import annotations

import json
import logging
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Set

from inc_launcher.config import INC_ROOT, PACKAGE_DIR, is_formulation_catchup_enabled
from inc_launcher.formulation_catchup import start_formulation_catchup_background
from inc_launcher.formulation_pending import load_shown_keys

logger = logging.getLogger(__name__)

# After Automation B (11:00 WAT). Uses the PC local clock (expected WAT).
POST_B_HOUR = 11
POST_B_MINUTE = 15
POLL_SECONDS = 30
FIRED_STATE_FILE = PACKAGE_DIR / "formulation_catchup_schedule_fired.json"
MAX_FIRED_DAYS = 21

# 7.11.2 — late pack retries (0 = off, leaves 7.11.1 alone)
RETRY_INTERVAL_MINUTES = 45
MAX_LATE_RETRIES = 8
LATE_RETRY_END_HOUR = 23

_scheduler: Optional["FormulationCatchupScheduler"] = None

PackShownFn = Callable[[datetime], bool]


def day_fire_key(when: datetime) -> str:
    return when.strftime("%Y-%m-%d")


def today_pack_date_key(when: datetime) -> str:
    return when.strftime("%Y%m%d")


def past_or_at_post_b(when: datetime, *, hour: int = POST_B_HOUR, minute: int = POST_B_MINUTE) -> bool:
    return (when.hour, when.minute) >= (hour, minute)


def default_today_pack_shown(when: datetime) -> bool:
    """True when today's formulation pack date is already in the shown ledger."""
    return today_pack_date_key(when) in load_shown_keys()


def load_schedule_state(path: Path | None = None) -> Dict[str, Any]:
    state_path = path or FIRED_STATE_FILE
    if not state_path.is_file():
        return {"fired": [], "retries": {}}
    try:
        with state_path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, dict):
            return {"fired": [], "retries": {}}
        fired = data.get("fired", [])
        retries = data.get("retries", {})
        if not isinstance(fired, list):
            fired = []
        if not isinstance(retries, dict):
            retries = {}
        return {"fired": [str(k) for k in fired], "retries": retries}
    except (OSError, json.JSONDecodeError, TypeError):
        return {"fired": [], "retries": {}}


def load_fired_days(path: Path | None = None) -> Set[str]:
    return set(load_schedule_state(path).get("fired") or [])


def save_schedule_state(state: Dict[str, Any], path: Path | None = None) -> None:
    state_path = path or FIRED_STATE_FILE
    fired = sorted(str(k) for k in (state.get("fired") or []))[-MAX_FIRED_DAYS:]
    retries_in = state.get("retries") or {}
    retries_out: Dict[str, Any] = {}
    if isinstance(retries_in, dict):
        for key in fired:
            if key in retries_in:
                retries_out[key] = retries_in[key]
    state_path.parent.mkdir(parents=True, exist_ok=True)
    with state_path.open("w", encoding="utf-8") as handle:
        json.dump({"fired": fired, "retries": retries_out}, handle, indent=2)


def save_fired_days(keys: Set[str], path: Path | None = None) -> None:
    state = load_schedule_state(path)
    state["fired"] = sorted(keys)
    save_schedule_state(state, path)


def mark_post_b_day_fired(
    when: datetime | None = None,
    path: Path | None = None,
) -> str:
    """Record today's post-B primary slot as done (e.g. tray-start catch-up covers it)."""
    when = when or datetime.now()
    key = day_fire_key(when)
    state_path = path or FIRED_STATE_FILE
    state = load_schedule_state(state_path)
    fired = set(state.get("fired") or [])
    if key not in fired:
        fired.add(key)
        state["fired"] = sorted(fired)
        save_schedule_state(state, state_path)
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
    """True once per day at/after the post-B slot when catch-up is enabled (7.11.1)."""
    if not enabled:
        return False
    if not past_or_at_post_b(when, hour=hour, minute=minute):
        return False
    return day_fire_key(when) not in fired


def should_retry_late_pack(
    when: datetime,
    fired: Set[str],
    retry_info: Dict[str, Any] | None,
    *,
    enabled: bool,
    pack_shown: bool,
    max_retries: int = MAX_LATE_RETRIES,
    interval_minutes: int = RETRY_INTERVAL_MINUTES,
    end_hour: int = LATE_RETRY_END_HOUR,
    hour: int = POST_B_HOUR,
    minute: int = POST_B_MINUTE,
) -> bool:
    """True when 7.11.1 already ran today but today's pack is still unshown."""
    if not enabled or max_retries <= 0:
        return False
    if not past_or_at_post_b(when, hour=hour, minute=minute):
        return False
    if when.hour > end_hour:
        return False
    key = day_fire_key(when)
    if key not in fired:
        return False
    if pack_shown:
        return False
    info = retry_info or {}
    count = int(info.get("count") or 0)
    if count >= max_retries:
        return False
    last_raw = info.get("last_at")
    if last_raw:
        try:
            last_at = datetime.fromisoformat(str(last_raw))
        except ValueError:
            last_at = None
        if last_at is not None and when < last_at + timedelta(minutes=interval_minutes):
            return False
    return True


class FormulationCatchupScheduler:
    """Daemon poller: post-B catch-up + optional late-pack retries while tray is up."""

    def __init__(
        self,
        *,
        enabled_fn: Callable[[], bool],
        fire_fn: Callable[[], None],
        pack_shown_fn: PackShownFn | None = None,
        state_path: Path | None = None,
        hour: int = POST_B_HOUR,
        minute: int = POST_B_MINUTE,
        poll_seconds: int = POLL_SECONDS,
        max_late_retries: int = MAX_LATE_RETRIES,
        retry_interval_minutes: int = RETRY_INTERVAL_MINUTES,
        retry_end_hour: int = LATE_RETRY_END_HOUR,
    ) -> None:
        self._enabled_fn = enabled_fn
        self._fire_fn = fire_fn
        self._pack_shown_fn = pack_shown_fn or default_today_pack_shown
        self._state_path = state_path or FIRED_STATE_FILE
        self._hour = hour
        self._minute = minute
        self._poll_seconds = poll_seconds
        self._max_late_retries = max_late_retries
        self._retry_interval_minutes = retry_interval_minutes
        self._retry_end_hour = retry_end_hour
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        state = load_schedule_state(self._state_path)
        self._fired = set(state.get("fired") or [])
        self._retries: Dict[str, Any] = dict(state.get("retries") or {})
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
            "Formulation catch-up schedule started (post-B %02d:%02d local, "
            "poll %ss, late_retries max=%s every %smin)",
            self._hour,
            self._minute,
            self._poll_seconds,
            self._max_late_retries,
            self._retry_interval_minutes,
        )

    def stop(self) -> None:
        self._stop.set()

    def _persist(self) -> None:
        save_schedule_state(
            {"fired": sorted(self._fired), "retries": self._retries},
            self._state_path,
        )

    def tick(self, when: datetime | None = None) -> str:
        """Run one check. Returns 'primary', 'retry', or '' if nothing fired."""
        when = when or datetime.now()
        with self._lock:
            enabled = bool(self._enabled_fn())
            key = day_fire_key(when)

            if should_fire_post_b(
                when,
                self._fired,
                enabled=enabled,
                hour=self._hour,
                minute=self._minute,
            ):
                try:
                    self._fire_fn()
                except Exception:
                    logger.exception("Formulation post-B catch-up fire failed")
                    return ""
                self._fired.add(key)
                self._retries.setdefault(key, {"count": 0, "last_at": when.isoformat(timespec="seconds")})
                self._retries[key]["last_at"] = when.isoformat(timespec="seconds")
                try:
                    self._persist()
                except OSError as exc:
                    logger.warning("Could not save catch-up schedule state: %s", exc)
                logger.info("Formulation post-B catch-up fired for %s", key)
                return "primary"

            pack_shown = False
            try:
                pack_shown = bool(self._pack_shown_fn(when))
            except Exception:
                logger.exception("pack_shown_fn failed — treating as not shown")

            retry_info = self._retries.get(key) if isinstance(self._retries.get(key), dict) else {}
            if should_retry_late_pack(
                when,
                self._fired,
                retry_info,
                enabled=enabled,
                pack_shown=pack_shown,
                max_retries=self._max_late_retries,
                interval_minutes=self._retry_interval_minutes,
                end_hour=self._retry_end_hour,
                hour=self._hour,
                minute=self._minute,
            ):
                try:
                    self._fire_fn()
                except Exception:
                    logger.exception("Formulation late-pack retry fire failed")
                    return ""
                count = int(retry_info.get("count") or 0) + 1
                self._retries[key] = {
                    "count": count,
                    "last_at": when.isoformat(timespec="seconds"),
                }
                try:
                    self._persist()
                except OSError as exc:
                    logger.warning("Could not save catch-up schedule state: %s", exc)
                logger.info(
                    "Formulation late-pack retry %s/%s for %s",
                    count,
                    self._max_late_retries,
                    key,
                )
                return "retry"

            return ""

    def _loop(self) -> None:
        # Wait before first tick so tray-start catch-up is not raced on boot.
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
    max_late_retries: int = MAX_LATE_RETRIES,
) -> FormulationCatchupScheduler:
    """Start the while-running post-B catch-up poller (singleton)."""
    global _scheduler
    if _scheduler is not None:
        return _scheduler

    root = Path(repo_root or INC_ROOT)

    def _enabled() -> bool:
        return is_formulation_catchup_enabled(config_path)

    def _fire() -> None:
        start_formulation_catchup_background(
            enabled=is_formulation_catchup_enabled(config_path),
            repo_root=root,
        )

    _scheduler = FormulationCatchupScheduler(
        enabled_fn=_enabled,
        fire_fn=_fire,
        state_path=state_path,
        max_late_retries=max_late_retries,
    )
    _scheduler.start()
    return _scheduler


def stop_formulation_catchup_schedule() -> None:
    global _scheduler
    if _scheduler is not None:
        _scheduler.stop()
        _scheduler = None
