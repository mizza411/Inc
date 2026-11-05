"""Paul Pearl/Upstream Drive Settings stub — real schedule fields can expand later."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Optional

from menu_labels import APP_TITLE, SETTINGS_HOVER
from paths import PACKAGE_DIR
from schedule import load_schedule_bundle
from ui_geometry import bind_geometry_persist, place_on_screen

_settings_win: Optional[tk.Toplevel] = None


def open_settings(root: tk.Tk) -> None:
    """Show Settings as a Toplevel on the tray UI thread (stub)."""
    global _settings_win
    if _settings_win is not None:
        try:
            if _settings_win.winfo_exists():
                _settings_win.lift()
                _settings_win.focus_force()
                return
        except tk.TclError:
            _settings_win = None

    win = tk.Toplevel(root)
    _settings_win = win
    win.title(f"{APP_TITLE} — Settings")
    win.minsize(360, 220)
    place_on_screen(win)
    bind_geometry_persist(win)

    frame = ttk.Frame(win, padding=12)
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text=APP_TITLE, font=("", 12, "bold")).pack(anchor=tk.W)
    ttk.Label(
        frame,
        text=(
            "Stub Settings. Change schedule later here — do not hand-edit the JSON "
            "for day-to-day use."
        ),
        wraplength=380,
    ).pack(anchor=tk.W, pady=(6, 10))

    bundle = load_schedule_bundle(str(PACKAGE_DIR))
    slots = ", ".join(bundle.schedule.slots) or "(none)"
    info = (
        f"Schedule enabled: {bundle.schedule.enabled}\n"
        f"Weekdays only: {bundle.schedule.weekdays_only}\n"
        f"Slots: {slots}\n"
        f"Open on startup: {bundle.startup_open_docx}\n"
        f"Open on schedule: {bundle.scheduled_open_docx}"
    )
    ttk.Label(frame, text=info, justify=tk.LEFT).pack(anchor=tk.W, pady=(0, 12))

    btn = ttk.Button(win, text="Close", command=win.destroy)
    btn.pack(pady=(0, 10))
    try:
        # Tk tooltip stand-in: balloon via title on some themes; also set takefocus.
        btn.configure(takefocus=True)
        _Tooltip(btn, "Close Settings")
    except Exception:
        pass

    win.bind("<Escape>", lambda _e: win.destroy())
    win.protocol("WM_DELETE_WINDOW", win.destroy)


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


# Re-export hover for smoke / docs
SETTINGS_ACTION = SETTINGS_HOVER
