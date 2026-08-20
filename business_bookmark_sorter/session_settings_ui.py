"""Settings dialog for timed review sessions (BB-TIMED-1 Phase 1.2).

User changes session length here — not by editing JSON by hand.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable, Optional

from business_bookmark_sorter.session_settings import (
    MAX_SESSION_MINUTES,
    MIN_SESSION_MINUTES,
    SessionSettings,
    load_session_settings,
    save_session_settings,
)
from business_bookmark_sorter.ui_tooltips import bind_tooltip


def parse_minutes_input(raw: str) -> Optional[int]:
    """Return int minutes or None if not a number."""
    try:
        return int(str(raw).strip())
    except (TypeError, ValueError):
        return None


def open_session_settings_dialog(
    parent: tk.Misc,
    *,
    on_saved: Optional[Callable[[SessionSettings], None]] = None,
) -> None:
    """Modal Settings window. Saves via session_settings module on Apply."""
    current = load_session_settings()

    win = tk.Toplevel(parent)
    win.title("Session settings")
    win.transient(parent)
    win.resizable(False, False)
    win.attributes("-topmost", True)

    body = ttk.Frame(win, padding=12)
    body.pack(fill="both", expand=True)

    ttk.Label(
        body,
        text="Timed filing session",
        font=("Segoe UI", 11, "bold"),
    ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

    ttk.Label(body, text="Session length (minutes):").grid(
        row=1, column=0, sticky="w", pady=4
    )
    minutes_var = tk.StringVar(value=str(current.session_minutes))
    spin = ttk.Spinbox(
        body,
        from_=MIN_SESSION_MINUTES,
        to=MAX_SESSION_MINUTES,
        textvariable=minutes_var,
        width=8,
    )
    spin.grid(row=1, column=1, sticky="w", padx=(8, 0), pady=4)
    bind_tooltip(
        spin,
        f"How long each timed filing slot lasts ({MIN_SESSION_MINUTES}–{MAX_SESSION_MINUTES} min). "
        "Changed here only — do not edit session_settings.json by hand.",
    )

    auto_var = tk.BooleanVar(value=current.auto_open_links)
    auto_chk = ttk.Checkbutton(
        body,
        text="Auto-open current link in browser",
        variable=auto_var,
    )
    auto_chk.grid(row=2, column=0, columnspan=2, sticky="w", pady=8)
    bind_tooltip(
        auto_chk,
        "When on, showing a pending bookmark opens its URL once in the browser. "
        "Saved with session settings; default on.",
    )

    ttk.Label(
        body,
        text="Preferences are saved on this PC only (not committed to git).",
        foreground="#666",
        font=("Segoe UI", 8),
    ).grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 8))

    btn_row = ttk.Frame(body)
    btn_row.grid(row=4, column=0, columnspan=2, sticky="e", pady=(8, 0))

    def _close() -> None:
        win.destroy()

    def _apply() -> None:
        parsed = parse_minutes_input(minutes_var.get())
        if parsed is None:
            messagebox.showerror(
                "Invalid minutes",
                "Enter a whole number of minutes.",
                parent=win,
            )
            return
        saved = save_session_settings(
            SessionSettings(
                session_minutes=parsed,
                auto_open_links=bool(auto_var.get()),
            )
        )
        if on_saved is not None:
            on_saved(saved)
        messagebox.showinfo(
            "Settings saved",
            f"Session length: {saved.session_minutes} min.\n"
            f"Auto-open links: {'ON' if saved.auto_open_links else 'OFF'}.\n\n"
            "Timer uses this length starting now (Apply restarts the countdown).",
            parent=win,
        )
        _close()

    cancel_btn = ttk.Button(btn_row, text="Cancel", command=_close)
    cancel_btn.pack(side="right", padx=(6, 0))
    apply_btn = ttk.Button(btn_row, text="Apply", command=_apply)
    apply_btn.pack(side="right")
    bind_tooltip(apply_btn, "Save session length (and auto-open) for this PC.")

    win.protocol("WM_DELETE_WINDOW", _close)
    win.grab_set()
    win.focus_force()
    spin.focus_set()
