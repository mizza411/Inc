"""Tests for Phase 3: single instance, login startup, extra pillars."""

from pathlib import Path

import inc_launcher.startup as startup_mod
from inc_launcher.config import load_config, list_pillars
from inc_launcher.icon_loader import load_tray_icon
from inc_launcher.single_instance import ensure_single_instance


def test_config_has_automation_pillar():
    config = load_config()
    pillars = list_pillars(config)
    assert len(pillars) >= 5
    ids = [p["id"] for p in pillars]
    assert "automation" in ids


def test_settings_single_instance_flag():
    config = load_config()
    assert config.get("settings", {}).get("single_instance") is True


def test_load_tray_icon_default():
    config = load_config()
    img = load_tray_icon(config)
    assert img.size == (64, 64)


def test_login_startup_roundtrip(tmp_path, monkeypatch):
    startup_dir = tmp_path / "Startup"
    startup_dir.mkdir()
    script = startup_dir / startup_mod.SHORTCUT_NAME
    monkeypatch.setattr(startup_mod, "startup_script_path", lambda: script)

    startup_mod.set_login_startup(True)
    assert startup_mod.is_login_startup_enabled()
    assert "inc_launcher.tray_app" in script.read_text(encoding="utf-8")

    startup_mod.set_login_startup(False)
    assert not startup_mod.is_login_startup_enabled()


def test_ensure_single_instance_on_windows(monkeypatch):
    import sys

    if sys.platform != "win32":
        return

    import inc_launcher.single_instance as single_instance_mod

    class _FakeKernel32:
        def CreateMutexW(self, _a, _b, _name):
            return 1

        def GetLastError(self):
            return 0

    single_instance_mod._mutex_handle = None
    monkeypatch.setattr("ctypes.windll.kernel32", _FakeKernel32())
    assert ensure_single_instance() is True
