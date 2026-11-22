"""Small main window for Paul Pearl/Upstream Drive (not Settings)."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Optional

from lifecycle_log import append_lifecycle
from menu_labels import (
    APP_TITLE,
    OPEN_NOTE_HOVER,
    OPEN_NOTE_MENU,
    OPEN_OFFER_HOVER,
    OPEN_OFFER_MENU,
    SETTINGS_HOVER,
    SETTINGS_MENU,
)
from open_offer_lines import open_offer_lines_docx
from open_paul_pearl_note import open_paul_pearl_note
from paths import PACKAGE_DIR
from schedule import load_schedule_bundle
from settings_ui import open_settings
from ui_geometry import bind_geometry_persist, place_on_screen

_main_win: Optional[tk.Toplevel] = None

HIDE_HOVER = "Hide this window and leave the tray running"
MAIN_DEFAULT_GEOMETRY = "440x300"


def _toast_hidden() -> None:
    try:
        from plyer import notification

        notification.notify(
            title=APP_TITLE,
            message="Window hidden. The tray icon is still running.",
            app_name=APP_TITLE,
            timeout=3,
        )
    except Exception:
        pass


def open_main(root: tk.Tk) -> None:
    """Show the main window on the tray UI thread."""
    global _main_win
    if _main_win is not None:
        try:
            if _main_win.winfo_exists():
                _main_win.deiconify()
                _main_win.lift()
                _main_win.focus_force()
                return
        except tk.TclError:
            _main_win = None

    win = tk.Toplevel(root)
    _main_win = win
    win.title(APP_TITLE)
    win.minsize(360, 240)
    place_on_screen(win, key="main_geometry", default=MAIN_DEFAULT_GEOMETRY)
    bind_geometry_persist(win, key="main_geometry")

    frame = ttk.Frame(win, padding=12)
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text=APP_TITLE, font=("", 12, "bold")).pack(anchor=tk.W)
    ttk.Label(
        frame,
        text="Main window. Opens with the offer sheet at tray start and at weekday slots.",
        wraplength=400,
    ).pack(anchor=tk.W, pady=(6, 10))

    bundle = load_schedule_bundle(str(PACKAGE_DIR))
    slots = ", ".join(bundle.schedule.slots) or "(none)"
    info = (
        f"Schedule enabled: {bundle.schedule.enabled}\n"
        f"Weekdays only: {bundle.schedule.weekdays_only}\n"
        f"Slots: {slots}"
    )
    ttk.Label(frame, text=info, justify=tk.LEFT).pack(anchor=tk.W, pady=(0, 12))

    row = ttk.Frame(frame)
    row.pack(fill=tk.X, pady=(0, 8))

    def on_offer() -> None:
        open_offer_lines_docx()

    def on_note() -> None:
        open_paul_pearl_note()

    def on_settings() -> None:
        open_settings(root)

    def hide_to_tray() -> None:
        win.withdraw()
        _toast_hidden()

    btn_offer = ttk.Button(row, text=OPEN_OFFER_MENU, command=on_offer)
    btn_offer.pack(side=tk.LEFT, padx=(0, 6))
    _Tooltip(btn_offer, OPEN_OFFER_HOVER)

    btn_note = ttk.Button(row, text=OPEN_NOTE_MENU, command=on_note)
    btn_note.pack(side=tk.LEFT, padx=(0, 6))
    _Tooltip(btn_note, OPEN_NOTE_HOVER)

    btn_settings = ttk.Button(row, text=SETTINGS_MENU, command=on_settings)
    btn_settings.pack(side=tk.LEFT, padx=(0, 6))
    _Tooltip(btn_settings, SETTINGS_HOVER)

    btn_hide = ttk.Button(win, text="Hide to tray", command=hide_to_tray)
    btn_hide.pack(pady=(0, 10))
    _Tooltip(btn_hide, HIDE_HOVER)

    win.bind("<Escape>", lambda _e: hide_to_tray())
    win.protocol("WM_DELETE_WINDOW", hide_to_tray)
    append_lifecycle("opened main window")


class _Tooltip:
    """Simple hover label for Tk controls."""

    def __init__(self, widget, text: str) -> None:
        self.widget = widget
        self.text = text
        self.tip: Optional[tk.Toplevel] = None
        widget.bind("<Enter>", self._show)
        widget.bind("<Leave>", self._hide)

    def _show(self, _event=None) -> None:
        if self.tip is not None:
            return
        tip = tk.Toplevel(self.widget)
        tip.wm_overrideredirect(True)
        tip.attributes("-topmost", True)
        x = self.widget.winfo_rootx() + 12
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
        tip.wm_geometry(f"+{x}+{y}")
        ttk.Label(tip, text=self.text, relief=tk.SOLID, padding=(6, 2)).pack()
        self.tip = tip

    def _hide(self, _event=None) -> None:
        if self.tip is None:
            return
        try:
            self.tip.destroy()
        except Exception:
            pass
        self.tip = None
