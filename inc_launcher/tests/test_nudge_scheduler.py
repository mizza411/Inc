"""Tests for Phase 4.2: background nudge scheduler."""

import json
from datetime import datetime, timedelta

import inc_launcher.nudge_scheduler as scheduler_mod
from inc_launcher.config import load_config
from inc_launcher.nudge_scheduler import (
    NudgeScheduler,
    load_fired_keys,
    prune_fired_keys,
    save_fired_keys,
)
from inc_launcher.scheduled_nudges import DAY_NAMES, load_schedule_settings


def test_prune_fired_keys_drops_old_entries():
    keys = {
        "daily_task_md:2020-01-01 09:00",
        "daily_inc_hub:2099-06-01 09:15",
    }
    pruned = prune_fired_keys(keys)
    assert "daily_task_md:2020-01-01 09:00" not in pruned
    assert "daily_inc_hub:2099-06-01 09:15" in pruned


def test_fired_state_roundtrip(tmp_path, monkeypatch):
    state_file = tmp_path / "schedule_fired.json"
    monkeypatch.setattr(scheduler_mod, "FIRED_STATE_FILE", state_file)

    save_fired_keys({"daily_task_md:2099-01-01 09:00"})
    assert load_fired_keys() == {"daily_task_md:2099-01-01 09:00"}


def test_scheduler_tick_disabled_does_not_fire(tmp_path, monkeypatch):
    state_file = tmp_path / "schedule_fired.json"
    monkeypatch.setattr(scheduler_mod, "FIRED_STATE_FILE", state_file)

    config = dict(load_config())
    schedules = dict(config["schedules"])
    schedules["enabled"] = False
    config["schedules"] = schedules
    config_path = tmp_path / "launcher_config.json"
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")

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


def test_scheduler_tick_fires_due_entry_once(tmp_path, monkeypatch):
    state_file = tmp_path / "schedule_fired.json"
    monkeypatch.setattr(scheduler_mod, "FIRED_STATE_FILE", state_file)

    config = dict(load_config())
    schedules = dict(config["schedules"])
    schedules["enabled"] = True
    config["schedules"] = schedules
    config_path = tmp_path / "launcher_config.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")

    fired: list[str] = []

    scheduler = NudgeScheduler(
        config_path=config_path,
        open_hub=lambda _config: fired.append("hub"),
        run_menu_action=lambda item: fired.append(item.get("id", item.get("label"))),
        poll_seconds=999,
    )
    when = datetime(2026, 5, 30, 9, 0)

    assert scheduler.tick(when) == ["daily_task_md"]
    assert fired == ["open_task_md"]
    assert scheduler.tick(when) == []
    assert fired == ["open_task_md"]


def test_scheduler_tick_fires_daily_hub_at_its_saved_clock(tmp_path, monkeypatch):
    state_file = tmp_path / "schedule_fired.json"
    monkeypatch.setattr(scheduler_mod, "FIRED_STATE_FILE", state_file)

    config = dict(load_config())
    schedules = dict(config["schedules"])
    schedules["enabled"] = True
    config["schedules"] = schedules
    config_path = tmp_path / "launcher_config.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")

    hub = next(entry for entry in load_schedule_settings(config).entries if entry.id == "daily_inc_hub")
    day = min(hub.days, key=DAY_NAMES.index)
    when = datetime(2026, 10, 26, hub.hour, hub.minute) + timedelta(days=DAY_NAMES.index(day))

    fired: list[str] = []

    scheduler = NudgeScheduler(
        config_path=config_path,
        open_hub=lambda _config: fired.append("hub"),
        run_menu_action=lambda _item: fired.append("action"),
        poll_seconds=999,
    )

    assert scheduler.tick(when) == ["daily_inc_hub"]
    assert fired == ["hub"]
