"""Tests for section 19 Phase 7.11.1–7.11.2 / 7.11.6 catch-up schedule + late retries."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from inc_launcher.config import load_config
from inc_launcher.formulation_catchup_schedule import (
    RETRY_INTERVAL_MINUTES,
    FormulationCatchupScheduler,
    day_fire_key,
    mark_post_b_day_fired,
    past_or_at_post_b,
    should_fire_post_b,
    should_retry_late_pack,
)
from inc_launcher.tray_app import build_menu


def test_default_retry_interval_is_fast_for_fetch_recovery():
    """7.11.6: default gap must stay short so a failed fetch is not a 45-min wait."""
    assert RETRY_INTERVAL_MINUTES == 10
    assert RETRY_INTERVAL_MINUTES < 45


def test_past_or_at_post_b_boundaries():
    assert past_or_at_post_b(datetime(2026, 10, 12, 11, 14)) is False
    assert past_or_at_post_b(datetime(2026, 10, 12, 11, 15)) is True
    assert past_or_at_post_b(datetime(2026, 10, 12, 16, 0)) is True


def test_should_fire_once_per_day_after_slot():
    when = datetime(2026, 10, 12, 11, 15)
    fired: set[str] = set()
    assert should_fire_post_b(when, fired, enabled=True) is True
    fired.add(day_fire_key(when))
    assert should_fire_post_b(when, fired, enabled=True) is False
    assert should_fire_post_b(datetime(2026, 10, 12, 16, 0), fired, enabled=True) is False


def test_should_not_fire_before_slot_or_when_disabled():
    early = datetime(2026, 10, 12, 10, 0)
    assert should_fire_post_b(early, set(), enabled=True) is False
    late = datetime(2026, 10, 12, 11, 15)
    assert should_fire_post_b(late, set(), enabled=False) is False


def test_scheduler_tick_fires_and_persists(tmp_path: Path):
    state = tmp_path / "fired.json"
    calls = {"n": 0}

    sched = FormulationCatchupScheduler(
        enabled_fn=lambda: True,
        fire_fn=lambda: calls.__setitem__("n", calls["n"] + 1),
        pack_shown_fn=lambda _when: True,
        state_path=state,
        poll_seconds=60,
        max_late_retries=0,
    )
    when = datetime(2026, 10, 12, 11, 15)
    assert sched.tick(when) == "primary"
    assert calls["n"] == 1
    assert sched.tick(when) == ""
    assert calls["n"] == 1
    assert state.is_file()
    text = state.read_text(encoding="utf-8")
    assert "2026-10-12" in text


def test_scheduler_tick_missed_slot_afternoon(tmp_path: Path):
    """Tray stayed up past 11:15: a later tick still fires once for that day."""
    state = tmp_path / "fired.json"
    calls = {"n": 0}
    sched = FormulationCatchupScheduler(
        enabled_fn=lambda: True,
        fire_fn=lambda: calls.__setitem__("n", calls["n"] + 1),
        pack_shown_fn=lambda _when: True,
        state_path=state,
        max_late_retries=0,
    )
    assert sched.tick(datetime(2026, 10, 12, 16, 0)) == "primary"
    assert calls["n"] == 1
    assert sched.tick(datetime(2026, 10, 12, 16, 30)) == ""


def test_mark_post_b_day_fired_blocks_primary_same_day(tmp_path: Path):
    state = tmp_path / "fired.json"
    when = datetime(2026, 10, 12, 16, 0)
    mark_post_b_day_fired(when, state)
    calls = {"n": 0}
    sched = FormulationCatchupScheduler(
        enabled_fn=lambda: True,
        fire_fn=lambda: calls.__setitem__("n", calls["n"] + 1),
        pack_shown_fn=lambda _when: True,
        state_path=state,
        max_late_retries=0,
    )
    assert sched.tick(when) == ""
    assert calls["n"] == 0


def test_scheduler_skips_when_toggle_off(tmp_path: Path):
    state = tmp_path / "fired.json"
    calls = {"n": 0}
    sched = FormulationCatchupScheduler(
        enabled_fn=lambda: False,
        fire_fn=lambda: calls.__setitem__("n", calls["n"] + 1),
        state_path=state,
    )
    assert sched.tick(datetime(2026, 10, 12, 11, 15)) == ""
    assert calls["n"] == 0


def test_should_retry_late_pack_rules():
    key = "2026-10-12"
    fired = {key}
    when = datetime(2026, 10, 12, 11, 30)
    assert (
        should_retry_late_pack(
            when,
            fired,
            {"count": 0, "last_at": "2026-10-12T11:15:00"},
            enabled=True,
            pack_shown=False,
            max_retries=8,
            interval_minutes=10,
        )
        is True
    )
    assert (
        should_retry_late_pack(
            when,
            fired,
            {"count": 0, "last_at": "2026-10-12T11:25:00"},
            enabled=True,
            pack_shown=False,
            max_retries=8,
            interval_minutes=10,
        )
        is False
    )
    assert (
        should_retry_late_pack(
            when,
            fired,
            {"count": 0, "last_at": "2026-10-12T11:15:00"},
            enabled=True,
            pack_shown=True,
            max_retries=8,
            interval_minutes=10,
        )
        is False
    )
    assert (
        should_retry_late_pack(
            when,
            fired,
            {"count": 8, "last_at": "2026-10-12T11:15:00"},
            enabled=True,
            pack_shown=False,
            max_retries=8,
            interval_minutes=10,
        )
        is False
    )
    assert (
        should_retry_late_pack(
            when,
            fired,
            {"count": 0, "last_at": "2026-10-12T11:15:00"},
            enabled=True,
            pack_shown=False,
            max_retries=0,
            interval_minutes=10,
        )
        is False
    )


def test_late_retry_after_primary_when_pack_unshown(tmp_path: Path):
    state = tmp_path / "fired.json"
    calls = {"n": 0}
    shown = {"ok": False}

    sched = FormulationCatchupScheduler(
        enabled_fn=lambda: True,
        fire_fn=lambda: calls.__setitem__("n", calls["n"] + 1),
        pack_shown_fn=lambda _when: shown["ok"],
        state_path=state,
        max_late_retries=3,
        retry_interval_minutes=10,
    )
    assert sched.tick(datetime(2026, 10, 12, 11, 15)) == "primary"
    assert calls["n"] == 1
    # Too soon (5 min < 10)
    assert sched.tick(datetime(2026, 10, 12, 11, 20)) == ""
    # Interval elapsed, still unshown (fetch-failure recovery path)
    assert sched.tick(datetime(2026, 10, 12, 11, 25)) == "retry"
    assert calls["n"] == 2
    shown["ok"] = True
    assert sched.tick(datetime(2026, 10, 12, 11, 35)) == ""
    assert calls["n"] == 2


def test_late_retry_cap(tmp_path: Path):
    state = tmp_path / "fired.json"
    calls = {"n": 0}
    sched = FormulationCatchupScheduler(
        enabled_fn=lambda: True,
        fire_fn=lambda: calls.__setitem__("n", calls["n"] + 1),
        pack_shown_fn=lambda _when: False,
        state_path=state,
        max_late_retries=2,
        retry_interval_minutes=30,
    )
    assert sched.tick(datetime(2026, 10, 12, 11, 15)) == "primary"
    assert sched.tick(datetime(2026, 10, 12, 11, 45)) == "retry"
    assert sched.tick(datetime(2026, 10, 12, 12, 15)) == "retry"
    assert sched.tick(datetime(2026, 10, 12, 12, 45)) == ""
    assert calls["n"] == 3  # 1 primary + 2 retries


def test_max_retries_zero_leaves_primary_only(tmp_path: Path):
    state = tmp_path / "fired.json"
    calls = {"n": 0}
    sched = FormulationCatchupScheduler(
        enabled_fn=lambda: True,
        fire_fn=lambda: calls.__setitem__("n", calls["n"] + 1),
        pack_shown_fn=lambda _when: False,
        state_path=state,
        max_late_retries=0,
        retry_interval_minutes=30,
    )
    assert sched.tick(datetime(2026, 10, 12, 11, 15)) == "primary"
    assert sched.tick(datetime(2026, 10, 12, 12, 0)) == ""
    assert calls["n"] == 1


def test_boot_mark_fired_still_allows_late_retry_if_unshown(tmp_path: Path):
    state = tmp_path / "fired.json"
    when = datetime(2026, 10, 12, 16, 0)
    mark_post_b_day_fired(when, state)
    calls = {"n": 0}
    sched = FormulationCatchupScheduler(
        enabled_fn=lambda: True,
        fire_fn=lambda: calls.__setitem__("n", calls["n"] + 1),
        pack_shown_fn=lambda _when: False,
        state_path=state,
        max_late_retries=2,
        retry_interval_minutes=0,
    )
    assert sched.tick(when) == "retry"
    assert calls["n"] == 1


def test_tray_menu_shows_formulation_packs_auto_toggle():
    menu = build_menu(load_config())
    labels = [getattr(entry, "text", "") or "" for entry in menu]
    assert any("Open formulation packs auto" in label for label in labels)
