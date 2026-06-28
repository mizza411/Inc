"""Automated equivalents for inc_launcher/MANUAL_TEST.md Phase 4 sign-off."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import inc_launcher.nudge_scheduler as scheduler_mod
import inc_launcher.tray_app as tray_mod
from inc_launcher.config import (
    is_interval_nudges_enabled,
    load_config,
    set_interval_nudges_enabled,
)
from inc_launcher.nudge_scheduler import (
    NudgeScheduler,
    start_nudge_scheduler,
    stop_nudge_scheduler,
)
from inc_launcher.tests.test_phase4_toggle import _write_disabled_config_copy
from inc_launcher.tray_app import build_menu


def _enabled_config_copy(source: Path, dest: Path) -> None:
    data = json.loads(source.read_text(encoding="utf-8"))
    data.setdefault("schedules", {})["enabled"] = True
    dest.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def test_manual_a_toggle_flips_config_and_refreshes_menu(tmp_path):
    """MANUAL A: Interval nudges toggle updates JSON and tray menu object."""
    source = Path(__file__).resolve().parent.parent / "launcher_config.json"
    config_path = tmp_path / "launcher_config.json"
    _write_disabled_config_copy(source, config_path)

    tray_mod._config_path = config_path
    tray_mod._hub_config = load_config(config_path)

    class _FakeIcon:
        def __init__(self) -> None:
            self.menu = None

    icon = _FakeIcon()
    tray_mod._tray_icon = icon

    assert is_interval_nudges_enabled(config_path) is False
    tray_mod._toggle_interval_nudges()
    assert is_interval_nudges_enabled(config_path) is True
    assert icon.menu is not None

    tray_mod._toggle_interval_nudges()
    assert is_interval_nudges_enabled(config_path) is False
    assert icon.menu is not None

    tray_mod._tray_icon = None
    tray_mod._config_path = None


def test_manual_a_build_menu_with_nudges_on_and_off(tmp_path):
    """MANUAL A: Tray menu builds for both enabled states."""
    source = Path(__file__).resolve().parent.parent / "launcher_config.json"
    config_path = tmp_path / "launcher_config.json"
    _write_disabled_config_copy(source, config_path)

    tray_mod._config_path = config_path
    try:
        assert build_menu(load_config(config_path)) is not None
        set_interval_nudges_enabled(True, config_path)
        assert build_menu(load_config(config_path)) is not None
    finally:
        tray_mod._config_path = None


def test_manual_b_approved_schedule_fires_task_and_hub(tmp_path, monkeypatch):
    """MANUAL B: 09:00 task.md and 09:15 hub fire once on a Saturday."""
    state_file = tmp_path / "schedule_fired.json"
    monkeypatch.setattr(scheduler_mod, "FIRED_STATE_FILE", state_file)

    source = Path(__file__).resolve().parent.parent / "launcher_config.json"
    config_path = tmp_path / "launcher_config.json"
    _enabled_config_copy(source, config_path)

    fired: list[str] = []

    scheduler = NudgeScheduler(
        config_path=config_path,
        open_hub=lambda _config: fired.append("hub"),
        run_menu_action=lambda item: fired.append(item.get("id", "")),
        poll_seconds=999,
    )

    sat_9 = datetime(2026, 5, 30, 9, 0)
    assert scheduler.tick(sat_9) == ["daily_task_md"]
    assert fired == ["open_task_md"]
    assert scheduler.tick(sat_9) == []

    sat_915 = datetime(2026, 5, 30, 9, 15)
    assert scheduler.tick(sat_915) == ["daily_inc_hub"]
    assert fired == ["open_task_md", "hub"]


def test_manual_b_mwf_problem_id_and_sunday_youtube(tmp_path, monkeypatch):
    """MANUAL B: Mon 10:00 live URL; Sun 18:00 YouTube status when ops active."""
    state_file = tmp_path / "schedule_fired.json"
    monkeypatch.setattr(scheduler_mod, "FIRED_STATE_FILE", state_file)

    source = Path(__file__).resolve().parent.parent / "launcher_config.json"
    config_path = tmp_path / "launcher_config.json"
    _enabled_config_copy(source, config_path)

    fired: list[str] = []

    scheduler = NudgeScheduler(
        config_path=config_path,
        open_hub=lambda _config: None,
        run_menu_action=lambda item: fired.append(item.get("id", "")),
        poll_seconds=999,
    )

    monday = datetime(2026, 6, 1, 10, 0)
    assert scheduler.tick(monday) == ["problem_id_live_mwf"]
    assert fired == ["problem_id_live"]

    sunday = datetime(2026, 5, 31, 18, 0)
    assert scheduler.tick(sunday) == ["youtube_status_sunday"]
    assert fired == ["problem_id_live", "youtube_status"]


def test_manual_c_disabled_schedule_never_fires(tmp_path, monkeypatch):
    """MANUAL C: schedules.enabled false → no auto actions."""
    state_file = tmp_path / "schedule_fired.json"
    monkeypatch.setattr(scheduler_mod, "FIRED_STATE_FILE", state_file)

    source = Path(__file__).resolve().parent.parent / "launcher_config.json"
    config_path = tmp_path / "launcher_config.json"
    _write_disabled_config_copy(source, config_path)

    fired: list[str] = []
    scheduler = NudgeScheduler(
        config_path=config_path,
        open_hub=lambda _config: fired.append("hub"),
        run_menu_action=lambda _item: fired.append("action"),
        poll_seconds=999,
    )
    when = datetime(2026, 5, 30, 9, 0)
    assert scheduler.tick(when) == []
    assert fired == []


def test_manual_e_scheduler_start_stop_lifecycle():
    """MANUAL E: Scheduler thread starts with tray wiring and stops cleanly."""
    events: list[str] = []

    scheduler = start_nudge_scheduler(
        None,
        open_hub=lambda _config: events.append("hub"),
        run_menu_action=lambda _item: events.append("action"),
    )
    assert scheduler._thread is not None
    assert scheduler._thread.is_alive()

    stop_nudge_scheduler()
    scheduler._thread.join(timeout=5)
    assert not scheduler._thread.is_alive()

