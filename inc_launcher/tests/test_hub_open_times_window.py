"""HUB-OPEN-TIMES-1 Phase 2: Settings form without a tray menu row."""

from __future__ import annotations

import json
from pathlib import Path

from inc_launcher.config import DEFAULT_CONFIG
from inc_launcher.hub_open_times import place_on_visible_screen, save_hub_open_times_geometry
from inc_launcher.hub_open_times_window import DEFAULT_GEOMETRY, CANCEL_HOVER, HubOpenTimesWindow
from inc_launcher.scheduled_nudges import DAY_NAMES


def _copy_config(tmp_path: Path) -> Path:
    dest = tmp_path / "launcher_config.json"
    dest.write_text(DEFAULT_CONFIG.read_text(encoding="utf-8"), encoding="utf-8")
    return dest


def _item(path: Path, item_id: str) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    for item in data["schedules"]["items"]:
        if item["id"] == item_id:
            return item
    raise AssertionError(item_id)


def test_form_uses_default_size_and_two_rows(tk_root, tmp_path: Path):
    path = _copy_config(tmp_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    data.get("settings", {}).pop("hub_open_times_window", None)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    win = HubOpenTimesWindow(tk_root, path)
    win.withdraw()
    # A withdrawn test root reports 1x1. The form still asks for the default size.
    assert win._opening_geometry == DEFAULT_GEOMETRY
    assert len(win._rows) == 2
    assert win._rows[0].title == "Daily Hub open"
    assert win._rows[1].title == "Ask window, which also opens Hub"
    assert tuple(win._rows[0].days) == DAY_NAMES
    win.cancel()


def test_cancel_does_not_write(tk_root, tmp_path: Path):
    path = _copy_config(tmp_path)
    before = path.read_bytes()
    win = HubOpenTimesWindow(tk_root, path)
    win.withdraw()
    win._rows[0].hour.set("11")
    win.cancel()
    assert path.read_bytes() == before
    assert not win.winfo_exists()


def test_save_disabled_until_a_day_is_ticked(tk_root, tmp_path: Path):
    path = _copy_config(tmp_path)
    before = path.read_bytes()
    win = HubOpenTimesWindow(tk_root, path)
    win.withdraw()
    for name in DAY_NAMES:
        win._rows[0].days[name].set(False)
    win._refresh_save()
    assert str(win.save_button.cget("state")) == "disabled"
    assert "at least one day" in win._save_hover.lower()
    win.save()
    assert path.read_bytes() == before
    win.cancel()


def test_save_writes_both_rows_through_the_phase_1_writer(tk_root, tmp_path: Path):
    path = _copy_config(tmp_path)
    ask_time = _item(path, "network_ask_mwf")["time"]
    task_time = _item(path, "daily_task_md")["time"]
    win = HubOpenTimesWindow(tk_root, path)
    win.withdraw()
    win._rows[0].hour.set("11")
    win._rows[0].minute.set("5")
    win.save()
    assert _item(path, "daily_inc_hub")["time"] == "11:05"
    assert _item(path, "network_ask_mwf")["time"] == ask_time
    assert _item(path, "daily_task_md")["time"] == task_time
    assert not win.winfo_exists()


def test_next_open_restores_a_saved_spot(tk_root, tmp_path: Path):
    path = _copy_config(tmp_path)
    save_hub_open_times_geometry(100, 80, 640, 360, path)
    win = HubOpenTimesWindow(tk_root, path)
    x, y, width, height = place_on_visible_screen(
        100,
        80,
        640,
        360,
        int(win.winfo_screenwidth()),
        int(win.winfo_screenheight()),
    )
    assert win._opening_geometry == f"{width}x{height}+{x}+{y}"
    win.withdraw()
    win.cancel()


def test_cancel_hover_text_is_present():
    assert CANCEL_HOVER == "Close without saving hub open times"
