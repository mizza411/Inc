"""Weekday poll — opens offer_lines.docx only (no hub window required)."""

from __future__ import annotations

import logging
import time
from datetime import datetime
from typing import Optional, Set

from open_offer_lines import open_offer_lines_docx
from paths import PACKAGE_DIR
from schedule import (
    PaulPearlScheduleBundle,
    load_schedule_bundle,
    scheduled_skip_message,
)
from schedule_core import (
    POLL_INTERVAL_MS,
    check_internet_available,
    cooldown_remaining_seconds,
    due_slot,
    mark_slot_fired,
    slot_fired_key,
    within_scheduled_cooldown,
)

from menu_labels import APP_TITLE

logger = logging.getLogger(__name__)


def _show_toast(slot: str) -> None:
    try:
        from plyer import notification

        notification.notify(
            title=APP_TITLE,
            message=f"Opening offer lines ({slot})",
            app_name=APP_TITLE,
            timeout=4,
        )
    except Exception as exc:
        logger.debug("toast failed: %s", exc)


def install_schedule(app) -> None:
    app._schedule_fired_today: Set[str] = set()
    app._schedule_poll_after_id = None
    app._last_scheduled_run_finished_at: Optional[float] = None
    app._opening_docx = False
    app.schedule_bundle = load_schedule_bundle(str(PACKAGE_DIR))
    if app.schedule_bundle.schedule.enabled:
        app.after(1000, lambda: _poll_tick(app))


def _skip_reason(app, slot: str) -> Optional[str]:
    if getattr(app, "_opening_docx", False):
        return scheduled_skip_message(slot, "busy")
    bundle: PaulPearlScheduleBundle = app.schedule_bundle
    cooldown_s = bundle.schedule.scheduled_cooldown_seconds
    if within_scheduled_cooldown(app._last_scheduled_run_finished_at, cooldown_s):
        remaining = cooldown_remaining_seconds(
            app._last_scheduled_run_finished_at, cooldown_s
        )
        return scheduled_skip_message(
            slot,
            "cooldown",
            cooldown_minutes=bundle.schedule.scheduled_cooldown_minutes,
            remaining_seconds=remaining,
        )
    if bundle.schedule.require_internet_for_scheduled:
        if not check_internet_available(
            bundle.schedule.internet_check_timeout_seconds,
            bundle.schedule.internet_probe_urls,
        ):
            return scheduled_skip_message(slot, "offline")
    return None


def _open_slot(app, slot: str) -> None:
    bundle: PaulPearlScheduleBundle = app.schedule_bundle
    if not bundle.scheduled_open_docx:
        return
    app._opening_docx = True
    try:
        _show_toast(slot)
        result = open_offer_lines_docx()
        logger.info("scheduled open %s -> %s", slot, result)
    finally:
        app._opening_docx = False
        app._last_scheduled_run_finished_at = time.time()


def _poll_tick(app) -> None:
    try:
        app.schedule_bundle = load_schedule_bundle(str(PACKAGE_DIR))
        bundle = app.schedule_bundle
        if not bundle.schedule.enabled:
            return
        now = datetime.now()
        slot = due_slot(now, bundle.schedule, app._schedule_fired_today)
        if slot:
            key = slot_fired_key(now, slot)
            skip = _skip_reason(app, slot)
            if skip:
                logger.info("%s", skip)
            else:
                mark_slot_fired(app._schedule_fired_today, key)
                _open_slot(app, slot)
    except Exception as exc:
        logger.exception("schedule poll failed: %s", exc)
    finally:
        try:
            app._schedule_poll_after_id = app.after(
                POLL_INTERVAL_MS, lambda: _poll_tick(app)
            )
        except Exception:
            pass
