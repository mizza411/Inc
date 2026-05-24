"""Windows login startup for Inc Launcher (Phase 3)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from inc_launcher.config import INC_ROOT

SHORTCUT_NAME = "Inc Launcher.bat"


def startup_script_path() -> Path:
    appdata = os.environ.get("APPDATA")
    if not appdata:
        raise OSError("APPDATA is not set")
    return (
        Path(appdata)
        / "Microsoft"
        / "Windows"
        / "Start Menu"
        / "Programs"
        / "Startup"
        / SHORTCUT_NAME
    )


def is_login_startup_enabled() -> bool:
    return startup_script_path().is_file()


def set_login_startup(enabled: bool) -> None:
    path = startup_script_path()
    if enabled:
        pythonw = Path(sys.executable).with_name("pythonw.exe")
        if not pythonw.is_file():
            pythonw = Path(sys.executable)
        script = (
            "@echo off\r\n"
            f'cd /d "{INC_ROOT}"\r\n'
            f'"{pythonw}" -m inc_launcher.tray_app\r\n'
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(script, encoding="utf-8")
    elif path.is_file():
        path.unlink()
