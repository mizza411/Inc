"""Post-file Chrome removal confirm (BB-TIMED-1 Phase 4).

Returns whether the user said they removed the bookmark, and whether
“Don’t ask again this session” was checked.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Tuple


def ask_bookmark_removed_dialog(
    parent: tk.Misc,
    title: str,
) -> Tuple[bool, bool]:
    """Modal Yes/No with optional don’t-ask-again.

    Returns (yes_removed, dont_ask_again).
    """
    short = (title or "this bookmark")[:100]
    result = {"yes": False, "dont_ask": False}

    win = tk.Toplevel(parent)
    win.title("Remove bookmark from Chrome?")
    win.transient(parent)
    win.resizable(False, False)
    win.attributes("-topmost", True)

    body = ttk.Frame(win, padding=12)
    body.pack(fill="both", expand=True)

    ttk.Label(
        body,
        text=(
            f"Have you removed this bookmark from Chrome?\n\n{short}\n\n"
            "Yes = removed — go to next link\n"
            "No = not yet — stay on this link"
        ),
        wraplength=420,
        justify="left",
    ).pack(anchor="w")

    dont_var = tk.BooleanVar(value=False)
    ttk.Checkbutton(
        body,
        text="Don’t ask again this session (assume Yes after filing)",
        variable=dont_var,
    ).pack(anchor="w", pady=(12, 8))

    btn_row = ttk.Frame(body)
    btn_row.pack(fill="x")

    def _finish(yes: bool) -> None:
        result["yes"] = yes
        result["dont_ask"] = bool(dont_var.get())
        win.destroy()

    ttk.Button(btn_row, text="No — not yet", command=lambda: _finish(False)).pack(
        side="right", padx=(6, 0)
    )
    ttk.Button(btn_row, text="Yes — removed", command=lambda: _finish(True)).pack(
        side="right"
    )

    win.protocol("WM_DELETE_WINDOW", lambda: _finish(False))
    win.grab_set()
    win.focus_force()
    win.wait_window()
    return result["yes"], result["dont_ask"]
