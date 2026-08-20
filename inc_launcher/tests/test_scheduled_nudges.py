"""Tests for Phase 4.1: schedule config parsing and due-time logic."""

from datetime import datetime

from inc_launcher.config import load_config
from inc_launcher.scheduled_nudges import (
    HUB_TARGET,
    ScheduleSettings,
    day_name,
    entries_due_now,
    fire_key,
    load_schedule_settings,
    parse_days,
    parse_time,
    resolve_schedule_target,
    validate_schedule_targets,
)


def test_parse_time_and_days():
    assert parse_time("09:00") == (9, 0)
    assert parse_time("18:00") == (18, 0)
    assert parse_days(["mon", "wed", "fri"]) == frozenset({"mon", "wed", "fri"})


def test_load_schedule_settings_from_repo_config():
    config = load_config()
    settings = load_schedule_settings(config)
    assert isinstance(settings, ScheduleSettings)
    assert isinstance(settings.enabled, bool)
    assert len(settings.entries) == 6
    ids = [entry.id for entry in settings.entries]
    assert ids == [
        "daily_task_md",
        "daily_inc_hub",
        "problem_id_live_mwf",
        "network_ask_mwf",
        "bookmark_review_weekdays",
        "youtube_status_sunday",
    ]


def test_validate_schedule_targets_all_resolve():
    config = load_config()
    assert validate_schedule_targets(config) == []


def test_resolve_hub_and_menu_targets():
    config = load_config()
    hub = resolve_schedule_target(config, HUB_TARGET)
    assert hub is not None
    assert hub["action"] == HUB_TARGET

    task = resolve_schedule_target(config, "open_task_md")
    assert task is not None
    assert task["action"] == "file"
    assert task["path"] == ".cursor/rules/task.md"

    review = resolve_schedule_target(config, "bookmark_review")
    assert review is not None
    assert review["action"] == "command"
    assert "business_bookmark_sorter review" in review["command"]


def test_bookmark_review_due_weekday_1100():
    config = load_config()
    config = dict(config)
    schedules = dict(config["schedules"])
    schedules["enabled"] = True
    config["schedules"] = schedules
    settings = load_schedule_settings(config)
    monday = datetime(2026, 6, 1, 11, 0)
    assert day_name(monday) == "mon"
    due = entries_due_now(settings, config, monday, set())
    assert [entry.id for entry in due] == ["bookmark_review_weekdays"]
    saturday = datetime(2026, 5, 30, 11, 0)
    assert day_name(saturday) == "sat"
    assert entries_due_now(settings, config, saturday, set()) == []


def test_entries_due_when_disabled():
    config = load_config()
    config = dict(config)
    schedules = dict(config["schedules"])
    schedules["enabled"] = False
    config["schedules"] = schedules
    settings = load_schedule_settings(config)
    fired: set[str] = set()
    when = datetime(2026, 5, 30, 9, 0)
    assert entries_due_now(settings, config, when, fired) == []


def test_entries_due_when_enabled_weekday_morning():
    config = load_config()
    config = dict(config)
    schedules = dict(config["schedules"])
    schedules["enabled"] = True
    config["schedules"] = schedules

    settings = load_schedule_settings(config)
    fired: set[str] = set()
    # 2026-05-30 is a Saturday
    when = datetime(2026, 5, 30, 9, 0)
    due = entries_due_now(settings, config, when, fired)
    assert [entry.id for entry in due] == ["daily_task_md"]

    fired.add(fire_key("daily_task_md", when))
    assert entries_due_now(settings, config, when, fired) == []


def test_entries_due_monday_hub_and_mwf_problem_id():
    config = load_config()
    config = dict(config)
    schedules = dict(config["schedules"])
    schedules["enabled"] = True
    config["schedules"] = schedules
    settings = load_schedule_settings(config)
    fired: set[str] = set()

    monday = datetime(2026, 6, 1, 10, 0)  # Monday
    assert day_name(monday) == "mon"
    due = entries_due_now(settings, config, monday, fired)
    assert [entry.id for entry in due] == ["problem_id_live_mwf"]


def test_youtube_sunday_skipped_when_ops_inactive():
    config = load_config()
    config = dict(config)
    settings_block = dict(config["settings"])
    settings_block["youtube_ops_active"] = False
    config["settings"] = settings_block
    schedules = dict(config["schedules"])
    schedules["enabled"] = True
    config["schedules"] = schedules

    settings = load_schedule_settings(config)
    sunday = datetime(2026, 5, 31, 18, 0)
    assert day_name(sunday) == "sun"
    assert entries_due_now(settings, config, sunday, set()) == []
