"""HUB-OPEN-TIMES-1 Phase 1: patch-save the two Hub clocks on a temp config."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from inc_launcher.config import DEFAULT_CONFIG
from inc_launcher.hub_open_times import (
    HUB_OPEN_TIME_IDS,
    HubOpenTimeError,
    load_hub_open_times,
    load_hub_open_times_geometry,
    place_on_visible_screen,
    save_hub_open_time,
    save_hub_open_times_geometry,
)


def _copy_config(tmp_path: Path) -> Path:
    dest = tmp_path / "launcher_config.json"
    dest.write_text(DEFAULT_CONFIG.read_text(encoding="utf-8"), encoding="utf-8")
    return dest


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _item(data: dict, item_id: str) -> dict:
    for item in data["schedules"]["items"]:
        if item["id"] == item_id:
            return item
    raise AssertionError(item_id)


def test_live_config_has_only_the_two_hub_open_ids():
    rows = load_hub_open_times(DEFAULT_CONFIG)
    assert tuple(rows) == HUB_OPEN_TIME_IDS
    for row in rows.values():
        assert 0 <= row.hour <= 23
        assert 0 <= row.minute <= 59
        assert row.days


def test_save_changes_one_hub_row_and_leaves_the_rest(tmp_path: Path):
    path = _copy_config(tmp_path)
    before = _load(path)

    save_hub_open_time("daily_inc_hub", 10, 45, ["tue"], path)

    after = _load(path)
    assert _item(after, "daily_inc_hub")["time"] == "10:45"
    assert _item(after, "daily_inc_hub")["days"] == ["tue"]
    assert _item(after, "daily_inc_hub")["target"] == _item(before, "daily_inc_hub")["target"]
    assert _item(after, "network_ask_mwf") == _item(before, "network_ask_mwf")
    assert _item(after, "daily_task_md") == _item(before, "daily_task_md")
    assert _item(after, "youtube_status_sunday") == _item(before, "youtube_status_sunday")
    assert after["schedules"]["enabled"] == before["schedules"]["enabled"]
    assert after["pillars"] == before["pillars"]


def test_hour_24_is_refused_and_file_is_not_written(tmp_path: Path):
    path = _copy_config(tmp_path)
    before = path.read_bytes()
    with pytest.raises(HubOpenTimeError):
        save_hub_open_time("daily_inc_hub", 24, 0, ["mon"], path)
    assert path.read_bytes() == before


def test_zero_days_is_refused_and_file_is_not_written(tmp_path: Path):
    path = _copy_config(tmp_path)
    before = path.read_bytes()
    with pytest.raises(HubOpenTimeError):
        save_hub_open_time("network_ask_mwf", 9, 30, [], path)
    assert path.read_bytes() == before


def test_geometry_save_restores_and_leaves_clocks_alone(tmp_path: Path):
    path = _copy_config(tmp_path)
    before = _load(path)
    save_hub_open_times_geometry(120, 80, 640, 360, path)
    saved = load_hub_open_times_geometry(path)
    assert saved == {"x": 120, "y": 80, "width": 640, "height": 360}
    after = _load(path)
    assert _item(after, "daily_inc_hub") == _item(before, "daily_inc_hub")
    assert after["schedules"]["enabled"] == before["schedules"]["enabled"]
    assert after["settings"]["single_instance"] == before["settings"]["single_instance"]


def test_off_screen_spot_moves_back_onto_the_screen():
    assert place_on_visible_screen(-3000, -3000, 640, 360, 1920, 1080) == (40, 40, 640, 360)
    assert place_on_visible_screen(100, 80, 640, 360, 1920, 1080) == (100, 80, 640, 360)


def test_other_schedule_id_is_refused_and_file_is_not_written(tmp_path: Path):
    path = _copy_config(tmp_path)
    before = path.read_bytes()
    with pytest.raises(HubOpenTimeError):
        save_hub_open_time("daily_task_md", 8, 0, ["mon"], path)
    assert path.read_bytes() == before
