"""Networking window. A Toplevel on the hub, not a second Tk root."""

from __future__ import annotations

import json
import tkinter as tk
from tkinter import ttk
from pathlib import Path

from inc_launcher.config import INC_ROOT, config_file_path, load_config
from inc_launcher.hub_open_times import place_on_visible_screen
from inc_launcher.networking_rows import NO_PERSON, NetworkingRow, list_networking_rows

GEOMETRY_KEY = "networking_window"
DEFAULT_WIDTH = 520
DEFAULT_HEIGHT = 420
INTRO = "People to speak with about the prospective businesses just checked."
EMPTY = "No prospective businesses are listed yet."
CLOSE_HOVER = "Close the Networking window"


def load_networking_geometry(config_path: Path | None = None) -> dict[str, int] | None:
    config = load_config(config_path)
    block = (config.get("settings") or {}).get(GEOMETRY_KEY)
    if not isinstance(block, dict):
        return None
    try:
        return {
            "x": int(block["x"]),
            "y": int(block["y"]),
            "width": int(block["width"]),
            "height": int(block["height"]),
        }
    except (KeyError, TypeError, ValueError):
        return None


def save_networking_geometry(
    x: int,
    y: int,
    width: int,
    height: int,
    config_path: Path | None = None,
) -> None:
    """Patch only this window's place and size."""
    if int(width) < 320 or int(height) < 200:
        return
    path = config_file_path(config_path)
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    settings = data.setdefault("settings", {})
    settings[GEOMETRY_KEY] = {
        "x": int(x),
        "y": int(y),
        "width": int(width),
        "height": int(height),
    }
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


class NetworkingWindow(tk.Toplevel):
    def __init__(
        self,
        master: tk.Misc,
        *,
        config_path: Path | None = None,
        prospects_dir: Path | None = None,
    ) -> None:
        super().__init__(master)
        self._config_path = config_path
        self._geom_job: str | None = None
        self._card_canvas: tk.Canvas | None = None
        self._card_scrollbar: ttk.Scrollbar | None = None
        self._cards_fit = False
        self._closing = False
        self.title("Networking")
        self.minsize(360, 240)
        self.configure(bg="#f8fafc")
        self.transient(master)
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.bind("<Escape>", lambda _event: self.close())

        header = tk.Frame(self, bg="#1e293b", padx=16, pady=12)
        header.pack(fill="x")
        tk.Label(
            header,
            text="Networking",
            bg="#1e293b",
            fg="#f8fafc",
            font=("Segoe UI", 13, "bold"),
            anchor="w",
        ).pack(fill="x")

        body = tk.Frame(self, bg="#f8fafc", padx=16, pady=12)
        body.pack(fill="both", expand=True)
        tk.Label(
            body,
            text=INTRO,
            bg="#f8fafc",
            fg="#334155",
            font=("Segoe UI", 10),
            anchor="w",
            justify="left",
            wraplength=460,
        ).pack(fill="x", pady=(0, 8))

        folder = prospects_dir or (INC_ROOT / "Prospect-Businesses")
        rows = list_networking_rows(folder)
        close_btn = tk.Button(
            body,
            text="Close",
            command=self.close,
            font=("Segoe UI", 10),
            bg="#228be6",
            fg="#ffffff",
            activebackground="#1c7ed6",
            activeforeground="#ffffff",
            padx=14,
            pady=4,
            cursor="hand2",
        )
        self._hover(close_btn, CLOSE_HOVER)
        close_btn.focus_set()
        if not rows:
            tk.Label(
                body,
                text=EMPTY,
                bg="#f8fafc",
                fg="#64748b",
                font=("Segoe UI", 10),
                anchor="w",
            ).pack(fill="x")
            close_btn.pack(anchor="e", pady=(12, 0))
        else:
            # Bottom first, so a tall card list cannot push Close off the window.
            close_btn.pack(side="bottom", anchor="e", pady=(12, 0))
            self._mount_card_scroller(body, rows)

        self._apply_saved_geometry()
        self.bind("<Configure>", self._on_configure)
        # Child events reach this toplevel before the hub's whole-app wheel bind.
        self.bind("<MouseWheel>", self._on_mousewheel)
        self.bind("<Prior>", self._on_page_key)
        self.bind("<Next>", self._on_page_key)

    def _mount_card_scroller(self, body: tk.Frame, rows: list[NetworkingRow]) -> None:
        """Cards live in a canvas. Header, intro, and Close stay outside it."""
        list_frame = tk.Frame(body, bg="#f8fafc")
        list_frame.pack(fill="both", expand=True)
        canvas = tk.Canvas(
            list_frame,
            bg="#f8fafc",
            highlightthickness=0,
            borderwidth=0,
        )
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        cards = tk.Frame(canvas, bg="#f8fafc")
        window_id = canvas.create_window((0, 0), window=cards, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def _sync_region(_event: tk.Event) -> None:
            bbox = canvas.bbox("all")
            if bbox is not None:
                canvas.configure(scrollregion=bbox)
            self._apply_card_fit()

        def _fit_width(event: tk.Event) -> None:
            if event.width > 1:
                canvas.itemconfigure(window_id, width=event.width)
            self._apply_card_fit()

        self._card_canvas = canvas
        self._card_scrollbar = scrollbar
        cards.bind("<Configure>", _sync_region)
        canvas.bind("<Configure>", _fit_width)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for row in rows:
            line = tk.Frame(
                cards,
                bg="#ffffff",
                highlightbackground="#e2e8f0",
                highlightthickness=1,
            )
            line.pack(fill="x", pady=4)
            tk.Label(
                line,
                text=row.business,
                bg="#ffffff",
                fg="#0f172a",
                font=("Segoe UI", 10, "bold"),
                anchor="w",
            ).pack(fill="x", padx=10, pady=(8, 0))
            tk.Label(
                line,
                text=row.person,
                bg="#ffffff",
                fg="#475569" if row.person != NO_PERSON else "#94a3b8",
                font=("Segoe UI", 10),
                anchor="w",
            ).pack(fill="x", padx=10, pady=(0, 8))
        canvas.after_idle(self._apply_card_fit)

    def _apply_card_fit(self) -> None:
        """A short card list does not scroll. A tall one does."""
        canvas = self._card_canvas
        bar = self._card_scrollbar
        if canvas is None or bar is None:
            return
        try:
            if not canvas.winfo_exists():
                return
            view_h = canvas.winfo_height()
            bbox = canvas.bbox("all")
        except tk.TclError:
            return
        if bbox is None or view_h <= 1:
            return
        fits = (bbox[3] - bbox[1]) <= view_h
        self._cards_fit = fits
        if fits:
            canvas.yview_moveto(0)
            bar.state(["disabled"])
        else:
            bar.state(["!disabled"])

    def _on_mousewheel(self, event: tk.Event) -> str:
        """One notch moves the cards. Header and Close are outside the canvas."""
        canvas = self._card_canvas
        if canvas is not None:
            try:
                alive = canvas.winfo_exists()
            except tk.TclError:
                alive = False
            delta = int(getattr(event, "delta", 0) or 0)
            if alive and delta != 0 and not self._cards_fit:
                steps = int(-delta / 120)
                if steps == 0:
                    steps = -1 if delta > 0 else 1
                canvas.yview_scroll(steps, "units")
        return "break"

    def _on_page_key(self, event: tk.Event) -> str:
        """Page Down and Page Up move the cards. A short list stays still."""
        canvas = self._card_canvas
        if canvas is None or self._cards_fit:
            return "break"
        try:
            alive = canvas.winfo_exists()
        except tk.TclError:
            alive = False
        if not alive:
            return "break"
        key = str(getattr(event, "keysym", ""))
        if key == "Next":
            canvas.yview_scroll(1, "pages")
        elif key == "Prior":
            canvas.yview_scroll(-1, "pages")
        return "break"

    def close(self) -> None:
        self._persist_geometry()
        self.destroy()

    def destroy(self) -> None:
        self._closing = True
        self._cancel_geom_job()
        try:
            super().destroy()
        except tk.TclError:
            pass

    def _cancel_geom_job(self) -> None:
        job = self._geom_job
        self._geom_job = None
        if job is None:
            return
        try:
            self.after_cancel(job)
        except tk.TclError:
            pass

    def _apply_saved_geometry(self) -> None:
        saved = load_networking_geometry(self._config_path)
        if saved is None:
            self.geometry(f"{DEFAULT_WIDTH}x{DEFAULT_HEIGHT}")
            return
        x, y, width, height = place_on_visible_screen(
            saved["x"],
            saved["y"],
            saved["width"],
            saved["height"],
            self.winfo_screenwidth(),
            self.winfo_screenheight(),
        )
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _on_configure(self, _event: tk.Event) -> None:
        if self._closing:
            return
        if self._geom_job is not None:
            try:
                self.after_cancel(self._geom_job)
            except tk.TclError:
                pass
        self._geom_job = self.after(400, self._persist_geometry)

    def _persist_geometry(self) -> None:
        if not self.winfo_exists():
            return
        try:
            save_networking_geometry(
                self.winfo_x(),
                self.winfo_y(),
                self.winfo_width(),
                self.winfo_height(),
                self._config_path,
            )
        except (OSError, json.JSONDecodeError, tk.TclError):
            return

    def _hover(self, widget: tk.Misc, text: str) -> None:
        tip: tk.Toplevel | None = None

        def show(_event: tk.Event) -> None:
            nonlocal tip
            if tip is not None:
                return
            tip = tk.Toplevel(self)
            tip.wm_overrideredirect(True)
            try:
                tip.attributes("-topmost", True)
            except tk.TclError:
                pass
            tk.Label(
                tip,
                text=text,
                bg="#1e293b",
                fg="#f8fafc",
                font=("Segoe UI", 9),
                padx=8,
                pady=4,
            ).pack()
            tip.geometry(f"+{widget.winfo_rootx() + 8}+{widget.winfo_rooty() + widget.winfo_height() + 4}")

        def hide(_event: tk.Event) -> None:
            nonlocal tip
            if tip is not None:
                try:
                    tip.destroy()
                except tk.TclError:
                    pass
                tip = None

        widget.bind("<Enter>", show)
        widget.bind("<Leave>", hide)
