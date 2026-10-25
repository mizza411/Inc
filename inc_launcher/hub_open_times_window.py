"""Settings form for the Daily Hub open clock.

Not on the tray yet. The caller supplies the parent window. This file does not
create its own Tk root.
"""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import ttk

from inc_launcher.hub_open_times import (
    HUB_OPEN_TIME_IDS,
    MIN_WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
    HubOpenTimeError,
    load_hub_open_times,
    load_hub_open_times_geometry,
    place_on_visible_screen,
    save_hub_open_time,
    save_hub_open_times_geometry,
    validate_hub_open_time,
)
from inc_launcher.scheduled_nudges import DAY_NAMES

DEFAULT_GEOMETRY = "640x360"

ROW_TITLES = {
    "daily_inc_hub": "Daily Hub open",
}

DAY_CAPTIONS = {
    "mon": "Mon",
    "tue": "Tue",
    "wed": "Wed",
    "thu": "Thu",
    "fri": "Fri",
    "sat": "Sat",
    "sun": "Sun",
}

SAVE_HOVER_OK = "Save hub open times"
CANCEL_HOVER = "Close without saving hub open times"


def attach_hover_label(widget: tk.Misc, text_source) -> None:
    """Show a hover label. text_source is a string or a zero-arg callable."""
    tip: tk.Toplevel | None = None

    def _text() -> str:
        value = text_source() if callable(text_source) else text_source
        return str(value)

    def _show(_event: tk.Event) -> None:
        nonlocal tip
        if tip is not None:
            return
        tip = tk.Toplevel(widget)
        tip.wm_overrideredirect(True)
        try:
            tip.attributes("-topmost", True)
        except tk.TclError:
            pass
        tk.Label(
            tip,
            text=_text(),
            bg="#1e293b",
            fg="#f8fafc",
            font=("Segoe UI", 9),
            padx=8,
            pady=4,
        ).pack()
        x = widget.winfo_rootx() + 8
        y = widget.winfo_rooty() + widget.winfo_height() + 4
        tip.geometry(f"+{x}+{y}")

    def _hide(_event: tk.Event) -> None:
        nonlocal tip
        if tip is not None:
            try:
                tip.destroy()
            except tk.TclError:
                pass
            tip = None

    widget.bind("<Enter>", _show)
    widget.bind("<Leave>", _hide)


class _Row:
    def __init__(self, entry_id: str, hour: int, minute: int, days: tuple[str, ...]) -> None:
        self.entry_id = entry_id
        self.title = ROW_TITLES[entry_id]
        self.hour = tk.StringVar(value=str(hour))
        self.minute = tk.StringVar(value=str(minute))
        self.days = {name: tk.BooleanVar(value=name in days) for name in DAY_NAMES}

    def chosen_days(self) -> list[str]:
        return [name for name in DAY_NAMES if self.days[name].get()]

    def problem(self) -> str | None:
        try:
            validate_hub_open_time(int(self.hour.get()), int(self.minute.get()), self.chosen_days())
        except (HubOpenTimeError, ValueError) as exc:
            return f"{self.title}: {exc}"
        return None


class HubOpenTimesWindow(tk.Toplevel):
    """Daily Hub open, Save, and Cancel. Cancel does not write."""

    def __init__(self, master: tk.Misc, config_path: Path | None = None) -> None:
        super().__init__(master)
        self.title("Settings")
        self._config_path = config_path
        self._geometry_job: str | None = None
        self._apply_opening_geometry()
        self._save_hover = SAVE_HOVER_OK
        loaded = load_hub_open_times(config_path)
        self._rows = [
            _Row(entry_id, loaded[entry_id].hour, loaded[entry_id].minute, loaded[entry_id].days)
            for entry_id in HUB_OPEN_TIME_IDS
        ]
        self._build()
        self._refresh_save()
        self.bind("<Configure>", self._schedule_geometry_save)
        self.protocol("WM_DELETE_WINDOW", self.cancel)

    def _apply_opening_geometry(self) -> None:
        saved = load_hub_open_times_geometry(self._config_path)
        if not saved:
            self._opening_geometry = DEFAULT_GEOMETRY
            self.geometry(self._opening_geometry)
            return
        try:
            screen_width = int(self.winfo_screenwidth())
            screen_height = int(self.winfo_screenheight())
        except tk.TclError:
            screen_width, screen_height = 1920, 1080
        x, y, width, height = place_on_visible_screen(
            saved["x"],
            saved["y"],
            saved["width"],
            saved["height"],
            screen_width,
            screen_height,
        )
        self._opening_geometry = f"{width}x{height}+{x}+{y}"
        self.geometry(self._opening_geometry)

    def _schedule_geometry_save(self, _event: tk.Event) -> None:
        if self._geometry_job is not None:
            try:
                self.after_cancel(self._geometry_job)
            except tk.TclError:
                pass
        self._geometry_job = self.after(400, self._write_geometry)

    def _write_geometry(self) -> None:
        self._geometry_job = None
        try:
            if not self.winfo_exists():
                return
            width = int(self.winfo_width())
            height = int(self.winfo_height())
            if width < MIN_WINDOW_WIDTH or height < MIN_WINDOW_HEIGHT:
                return
            save_hub_open_times_geometry(
                int(self.winfo_x()),
                int(self.winfo_y()),
                width,
                height,
                self._config_path,
            )
        except tk.TclError:
            return

    def _cancel_geometry_job(self) -> None:
        if self._geometry_job is None:
            return
        try:
            self.after_cancel(self._geometry_job)
        except tk.TclError:
            pass
        self._geometry_job = None

    def _build(self) -> None:
        for row in self._rows:
            frame = ttk.LabelFrame(self, text=row.title)
            frame.pack(fill="x", padx=12, pady=8)
            clocks = ttk.Frame(frame)
            clocks.pack(fill="x", padx=8, pady=4)
            ttk.Label(clocks, text="Hour").pack(side="left")
            hour = ttk.Spinbox(clocks, from_=0, to=23, width=4, textvariable=row.hour, command=self._refresh_save)
            hour.pack(side="left", padx=(4, 12))
            hour.bind("<KeyRelease>", lambda _e: self._refresh_save())
            ttk.Label(clocks, text="Minute").pack(side="left")
            minute = ttk.Spinbox(
                clocks, from_=0, to=59, width=4, textvariable=row.minute, command=self._refresh_save
            )
            minute.pack(side="left", padx=(4, 0))
            minute.bind("<KeyRelease>", lambda _e: self._refresh_save())
            days = ttk.Frame(frame)
            days.pack(fill="x", padx=8, pady=4)
            for name in DAY_NAMES:
                ttk.Checkbutton(
                    days,
                    text=DAY_CAPTIONS[name],
                    variable=row.days[name],
                    command=self._refresh_save,
                ).pack(side="left", padx=2)

        buttons = ttk.Frame(self)
        buttons.pack(fill="x", padx=12, pady=12)
        save_wrap = ttk.Frame(buttons)
        save_wrap.pack(side="left")
        self.save_button = ttk.Button(save_wrap, text="Save", command=self.save)
        self.save_button.pack()
        attach_hover_label(save_wrap, lambda: self._save_hover)
        cancel = ttk.Button(buttons, text="Cancel", command=self.cancel)
        cancel.pack(side="left", padx=8)
        attach_hover_label(cancel, CANCEL_HOVER)

    def problems(self) -> list[str]:
        found = []
        for row in self._rows:
            problem = row.problem()
            if problem:
                found.append(problem)
        return found

    def _refresh_save(self) -> None:
        found = self.problems()
        if found:
            self._save_hover = " ".join(found)
            self.save_button.configure(state=tk.DISABLED)
        else:
            self._save_hover = SAVE_HOVER_OK
            self.save_button.configure(state=tk.NORMAL)

    def save(self) -> None:
        found = self.problems()
        if found:
            self._refresh_save()
            return
        for row in self._rows:
            save_hub_open_time(
                row.entry_id,
                int(row.hour.get()),
                int(row.minute.get()),
                row.chosen_days(),
                self._config_path,
            )
        self._cancel_geometry_job()
        self.destroy()

    def cancel(self) -> None:
        self._cancel_geometry_job()
        self.destroy()
