"""
Paul Pearl/Upstream Drive tray host — schedule + tray only (Inc home).
One product (renamed Upstream engagement).
Startup/schedule: offer_lines.docx. Extra menu: Paul Pearl note.
"""

from __future__ import annotations

import logging
import os
import subprocess
import sys
import threading
import tkinter as tk

import pystray
from PIL import Image, ImageDraw

from lifecycle_log import append_lifecycle
from menu_labels import (
    APP_TITLE,
    EXIT_HOVER,
    EXIT_MENU,
    OPEN_NOTE_HOVER,
    OPEN_NOTE_MENU,
    OPEN_OFFER_HOVER,
    OPEN_OFFER_MENU,
    RESTART_HOVER,
    RESTART_MENU,
    SETTINGS_HOVER,
    SETTINGS_MENU,
)
from open_offer_lines import maybe_open_on_startup, open_offer_lines_docx
from open_paul_pearl_note import open_paul_pearl_note
from paths import INC_ROOT, PACKAGE_DIR, resolve_offer_lines_docx
from schedule import load_schedule_bundle
from schedule_poll import install_schedule
from settings_ui import open_settings
from single_instance import notify_already_running, release, try_acquire

# Documented action text (pystray has no tooltip API on Windows).
_ = (OPEN_OFFER_HOVER, OPEN_NOTE_HOVER, SETTINGS_HOVER, RESTART_HOVER, EXIT_HOVER)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("paul_pearl")

LAUNCHER_NAME = "paul_pearl_engagement_tray_launcher.py"


def _tray_image() -> Image.Image:
    size = 64
    image = Image.new("RGB", (size, size), color="#0f3d2e")
    draw = ImageDraw.Draw(image)
    draw.rectangle([12, 12, 52, 52], fill="#2dd4a8")
    draw.text((18, 20), "PP", fill="#0f3d2e")
    return image


def _pythonw() -> str:
    pythonw = sys.executable.replace("python.exe", "pythonw.exe")
    if not os.path.isfile(pythonw):
        return sys.executable
    return pythonw


def _spawn_launcher() -> None:
    launcher = INC_ROOT / LAUNCHER_NAME
    subprocess.Popen(
        [_pythonw(), str(launcher), "--tray-restart"],
        cwd=str(INC_ROOT),
        close_fds=True,
    )


def _exit_app(app: tk.Tk, icon: pystray.Icon | None, *, reason: str) -> None:
    append_lifecycle(reason)
    append_lifecycle("shutting down")
    try:
        if icon is not None:
            icon.stop()
    except Exception:
        pass
    release()
    try:
        app.after(0, app.destroy)
    except Exception:
        pass


def main() -> int:
    restart_handoff = "--tray-restart" in sys.argv
    if not try_acquire():
        if restart_handoff:
            # Brief retry window during single-icon handoff
            import time

            for _ in range(20):
                time.sleep(0.15)
                if try_acquire():
                    break
            else:
                notify_already_running()
                return 0
        else:
            notify_already_running()
            return 0

    docx = resolve_offer_lines_docx()
    if docx is None:
        logger.error("offer_lines.docx missing — refusing to start tray")
        append_lifecycle("start refused — offer_lines.docx missing")
        release()
        return 1

    append_lifecycle("starting")

    app = tk.Tk()
    app.withdraw()
    app.title(APP_TITLE)

    bundle = load_schedule_bundle(str(PACKAGE_DIR))
    install_schedule(app)

    def on_startup() -> None:
        maybe_open_on_startup(enabled=bundle.startup_open_docx)

    app.after(800, on_startup)

    icon_holder: dict = {"icon": None}

    def tray_open(_icon=None, _item=None) -> None:
        app.after(0, open_offer_lines_docx)

    def tray_open_note(_icon=None, _item=None) -> None:
        app.after(0, open_paul_pearl_note)

    def tray_settings(_icon=None, _item=None) -> None:
        app.after(0, lambda: open_settings(app))

    def tray_restart(_icon=None, _item=None) -> None:
        """Shut down this icon/process, then start one replacement."""

        def handoff() -> None:
            append_lifecycle("Restart selected")
            append_lifecycle("shutting down")
            icon = icon_holder.get("icon")
            try:
                if icon is not None:
                    icon.stop()
            except Exception:
                pass
            release()
            _spawn_launcher()
            try:
                app.destroy()
            except Exception:
                pass

        app.after(0, handoff)

    def tray_exit(_icon=None, _item=None) -> None:
        _exit_app(app, icon_holder.get("icon"), reason="tray Exit selected")

    menu = pystray.Menu(
        pystray.MenuItem(OPEN_OFFER_MENU, tray_open, default=True),
        pystray.MenuItem(OPEN_NOTE_MENU, tray_open_note),
        pystray.MenuItem(SETTINGS_MENU, tray_settings),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(RESTART_MENU, tray_restart),
        pystray.MenuItem(EXIT_MENU, tray_exit),
    )
    icon = pystray.Icon("paul_pearl", _tray_image(), APP_TITLE, menu)
    icon_holder["icon"] = icon

    threading.Thread(target=icon.run, daemon=True).start()
    try:
        app.mainloop()
    finally:
        append_lifecycle("shutting down")
        try:
            icon.stop()
        except Exception:
            pass
        release()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
