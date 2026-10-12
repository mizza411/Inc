"""Tests for section 19 Phase 7.11.1 post-B while-running catch-up schedule."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from inc_launcher.config import load_config
from inc_launcher.formulation_catchup_schedule import (
    FormulationCatchupScheduler,
    day_fire_key,
    mark_post_b_day_fired,
    past_or_at_post_b,
    should_fire_post_b,
)
from inc_launcher.tray_app import build_menu


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
        state_path=state,
        poll_seconds=60,
    )
    when = datetime(2026, 10, 12, 11, 15)
    assert sched.tick(when) is True
    assert calls["n"] == 1
    assert sched.tick(when) is False
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
        state_path=state,
    )
    assert sched.tick(datetime(2026, 10, 12, 16, 0)) is True
    assert calls["n"] == 1
    assert sched.tick(datetime(2026, 10, 12, 16, 30)) is False


def test_mark_post_b_day_fired_blocks_schedule_same_day(tmp_path: Path):
    state = tmp_path / "fired.json"
    when = datetime(2026, 10, 12, 16, 0)
    mark_post_b_day_fired(when, state)
    calls = {"n": 0}
    sched = FormulationCatchupScheduler(
        enabled_fn=lambda: True,
        fire_fn=lambda: calls.__setitem__("n", calls["n"] + 1),
        state_path=state,
    )
    assert sched.tick(when) is False
    assert calls["n"] == 0


def test_scheduler_skips_when_toggle_off(tmp_path: Path):
    state = tmp_path / "fired.json"
    calls = {"n": 0}
    sched = FormulationCatchupScheduler(
        enabled_fn=lambda: False,
        fire_fn=lambda: calls.__setitem__("n", calls["n"] + 1),
        state_path=state,
    )
    assert sched.tick(datetime(2026, 10, 12, 11, 15)) is False
    assert calls["n"] == 0


def test_tray_menu_shows_formulation_packs_auto_toggle():
    menu = build_menu(load_config())
    labels = [getattr(entry, "text", "") or "" for entry in menu]
    assert any("Open formulation packs auto" in label for label in labels)
