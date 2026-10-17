"""INC-TRAY-RESTART-1 Phase 1b: exit_before_spawn handoff wiring."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

from inc_launcher.single_instance import BYPASS_FLAG, bypass_requested
from inc_launcher.tray_app import _on_restart_menu
from inc_launcher.tray_process_restart import (
    build_relaunch_command,
    restart_tray_process,
)


def test_bypass_flag_constant_and_parser():
    assert BYPASS_FLAG == "--tray-restart"
    assert bypass_requested(["--tray-restart"]) is True
    assert bypass_requested(["--other"]) is False


def test_module_relaunch_includes_bypass_flag():
    cmd = build_relaunch_command(
        module="inc_launcher.tray_app",
        extra_args=(BYPASS_FLAG,),
        executable="python.exe",
    )
    assert cmd is not None
    assert "-m" in cmd
    assert "inc_launcher.tray_app" in cmd
    assert BYPASS_FLAG in cmd


def test_exit_before_spawn_order(tmp_path: Path):
    order: list[str] = []
    script = tmp_path / "dummy_tray.py"
    script.write_text("# dummy\n", encoding="utf-8")

    def before() -> None:
        order.append("before")

    def popen(cmd, **_kwargs):
        order.append("spawn")
        assert BYPASS_FLAG in cmd
        return MagicMock()

    def exit_fn(code: int) -> None:
        order.append(f"exit:{code}")

    ok, _msg = restart_tray_process(
        script=script,
        app_name="Inc Launcher",
        extra_args=(BYPASS_FLAG,),
        before_exit=before,
        popen=popen,
        exit_fn=exit_fn,
        exit_before_spawn=True,
    )
    assert ok is True
    assert order == ["before", "spawn", "exit:0"]


def test_on_restart_menu_uses_exit_before_spawn(monkeypatch):
    captured: dict = {}

    def fake_restart(**kwargs):
        captured.update(kwargs)
        return True, "ok"

    monkeypatch.setattr(
        "inc_launcher.tray_process_restart.restart_tray_process",
        fake_restart,
    )
    icon = MagicMock()
    _on_restart_menu(icon, None)
    assert captured.get("exit_before_spawn") is True
    assert captured.get("module") == "inc_launcher.tray_app"
    assert BYPASS_FLAG in tuple(captured.get("extra_args") or ())
    assert callable(captured.get("before_exit"))
