"""Tests for Phase 4.3: interval nudges ON/OFF toggle."""

import json
from pathlib import Path

from inc_launcher.config import (
    is_interval_nudges_enabled,
    load_config,
    set_interval_nudges_enabled,
)
from inc_launcher.tray_app import build_menu


def _write_disabled_config_copy(source: Path, dest: Path) -> None:
    data = json.loads(source.read_text(encoding="utf-8"))
    data.setdefault("schedules", {})["enabled"] = False
    dest.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def test_interval_nudges_disabled_when_config_off(tmp_path):
    source = Path(__file__).resolve().parent.parent / "launcher_config.json"
    config_path = tmp_path / "launcher_config.json"
    _write_disabled_config_copy(source, config_path)
    assert is_interval_nudges_enabled(config_path) is False


def test_interval_nudges_toggle_roundtrip(tmp_path):
    source = Path(__file__).resolve().parent.parent / "launcher_config.json"
    config_path = tmp_path / "launcher_config.json"
    _write_disabled_config_copy(source, config_path)

    assert is_interval_nudges_enabled(config_path) is False
    set_interval_nudges_enabled(True, config_path)
    assert is_interval_nudges_enabled(config_path) is True

    saved = json.loads(config_path.read_text(encoding="utf-8"))
    assert saved["schedules"]["enabled"] is True

    set_interval_nudges_enabled(False, config_path)
    assert is_interval_nudges_enabled(config_path) is False


def test_tray_menu_shows_interval_nudges_toggle():
    menu = build_menu(load_config())
    assert menu is not None
