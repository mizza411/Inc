"""Super main hub window — 4-pillar launcher grid (Phase 2)."""

from __future__ import annotations

import logging
import queue
import threading
import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
from typing import Any, Callable, Dict, List, Optional

from inc_launcher.actions import run_action
from inc_launcher.config import INC_ROOT, list_pillars
from inc_launcher.recent import list_pinned, load_recent, record_recent

logger = logging.getLogger(__name__)

# Theme
SIDEBAR_BG = "#1e293b"
SIDEBAR_FG = "#e2e8f0"
SIDEBAR_ACTIVE = "#334155"
CONTENT_BG = "#f8fafc"
ACCENT = "#228be6"
CARD_BG = "#ffffff"
CARD_BORDER = "#e2e8f0"


class HubController:
    """Runs tkinter on a background thread; safe to call from pystray."""

    def __init__(self) -> None:
        self._thread: threading.Thread | None = None
        self._queue: queue.Queue | None = None
        self._ready = threading.Event()
        self._config: Dict[str, Any] = {}
        self._window: Optional["HubWindow"] = None
        self._root: tk.Tk | None = None

    def show(self, config: Dict[str, Any]) -> None:
        self._config = config
        if self._thread is None or not self._thread.is_alive():
            self._queue = queue.Queue()
            self._ready.clear()
            self._thread = threading.Thread(target=self._run_loop, daemon=True, name="inc-hub")
            self._thread.start()
            self._ready.wait(timeout=10)
        assert self._queue is not None
        self._queue.put("show")

    def _run_loop(self) -> None:
        self._root = tk.Tk()
        self._root.withdraw()
        self._root.title("Inc Launcher")
        self._ready.set()
        assert self._queue is not None
        while True:
            try:
                cmd = self._queue.get(timeout=0.15)
            except queue.Empty:
                try:
                    self._root.update()
                except tk.TclError:
                    break
                continue
            if cmd == "show":
                self._open_window()
            elif cmd == "hide":
                if self._window is not None:
                    self._window.withdraw()
            elif cmd == "quit":
                break
        try:
            self._root.destroy()
        except tk.TclError:
            pass

    def _open_window(self) -> None:
        if self._root is None:
            return
        if self._window is None or not self._window.winfo_exists():
            self._window = HubWindow(self._root, self._config, on_close=self._on_window_close)
        self._window.deiconify()
        self._window.lift()
        self._window.focus_force()

    def _on_window_close(self) -> None:
        if self._window is not None:
            self._window.withdraw()


class HubWindow(tk.Toplevel):
    """Hub UI: sidebar pillars + launcher grid."""

    def __init__(
        self,
        master: tk.Tk,
        config: Dict[str, Any],
        on_close: Callable[[], None] | None = None,
    ) -> None:
        super().__init__(master)
        self.config_data = config
        self._on_close = on_close
        self._active_pillar_id: str | None = None
        self._sidebar_buttons: Dict[str, tk.Button] = {}

        self.title(config.get("app_name", "Inc Launcher"))
        self.geometry("920x560")
        self.minsize(720, 480)
        self.configure(bg=CONTENT_BG)
        self.protocol("WM_DELETE_WINDOW", self._handle_close)

        self._build_layout()
        pillars = list_pillars(config)
        if pillars:
            self._select_pillar(pillars[0].get("id", ""))

    def _build_layout(self) -> None:
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        sidebar = tk.Frame(self, bg=SIDEBAR_BG, width=240)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        title_font = tkfont.Font(family="Segoe UI", size=13, weight="bold")
        tk.Label(
            sidebar,
            text="Inc Hub",
            bg=SIDEBAR_BG,
            fg="#ffffff",
            font=title_font,
            anchor="w",
        ).pack(fill="x", padx=16, pady=(16, 8))

        tk.Label(
            sidebar,
            text="Four pillars",
            bg=SIDEBAR_BG,
            fg="#94a3b8",
            font=("Segoe UI", 9),
            anchor="w",
        ).pack(fill="x", padx=16, pady=(0, 8))

        for pillar in list_pillars(self.config_data):
            pid = pillar.get("id", "")
            btn = tk.Button(
                sidebar,
                text=pillar.get("label", pid),
                bg=SIDEBAR_BG,
                fg=SIDEBAR_FG,
                activebackground=SIDEBAR_ACTIVE,
                activeforeground="#ffffff",
                relief="flat",
                anchor="w",
                padx=16,
                pady=10,
                font=("Segoe UI", 10),
                cursor="hand2",
                command=lambda p=pid: self._select_pillar(p),
            )
            btn.pack(fill="x")
            self._sidebar_buttons[pid] = btn

        tk.Frame(sidebar, bg=SIDEBAR_BG, height=1).pack(fill="x", pady=12)

        tk.Button(
            sidebar,
            text="Open Inc workspace",
            bg=SIDEBAR_BG,
            fg=SIDEBAR_FG,
            activebackground=SIDEBAR_ACTIVE,
            activeforeground="#ffffff",
            relief="flat",
            anchor="w",
            padx=16,
            pady=8,
            font=("Segoe UI", 9),
            cursor="hand2",
            command=lambda: self._run_item({"label": "Inc workspace", "action": "folder", "path": "."}),
        ).pack(fill="x")

        # Content area with scroll
        content_outer = tk.Frame(self, bg=CONTENT_BG)
        content_outer.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        content_outer.rowconfigure(1, weight=1)
        content_outer.columnconfigure(0, weight=1)

        self._header = tk.Label(
            content_outer,
            text="",
            bg=CONTENT_BG,
            fg="#0f172a",
            font=("Segoe UI", 16, "bold"),
            anchor="w",
        )
        self._header.grid(row=0, column=0, sticky="ew", padx=24, pady=(20, 4))

        self._subtitle = tk.Label(
            content_outer,
            text="",
            bg=CONTENT_BG,
            fg="#64748b",
            font=("Segoe UI", 10),
            anchor="w",
        )
        self._subtitle.grid(row=0, column=0, sticky="ew", padx=24, pady=(44, 12))

        canvas = tk.Canvas(content_outer, bg=CONTENT_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_outer, orient="vertical", command=canvas.yview)
        self._grid_frame = tk.Frame(canvas, bg=CONTENT_BG)
        self._grid_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=self._grid_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.grid(row=1, column=0, sticky="nsew", padx=(24, 0), pady=(0, 24))
        scrollbar.grid(row=1, column=1, sticky="ns", pady=(0, 24))

        def _on_mousewheel(event: tk.Event) -> None:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def _select_pillar(self, pillar_id: str) -> None:
        self._active_pillar_id = pillar_id
        for pid, btn in self._sidebar_buttons.items():
            if pid == pillar_id:
                btn.configure(bg=SIDEBAR_ACTIVE, fg="#ffffff")
            else:
                btn.configure(bg=SIDEBAR_BG, fg=SIDEBAR_FG)
        self._render_content()

    def _render_content(self) -> None:
        for child in self._grid_frame.winfo_children():
            child.destroy()

        pillar = self._find_pillar(self._active_pillar_id)
        if pillar is None:
            return

        self._header.configure(text=pillar.get("label", ""))
        items = pillar.get("items", [])
        self._subtitle.configure(text=f"{len(items)} launcher(s)")

        row = 0
        pinned = [p for p in list_pinned(self.config_data) if p.get("pillar_id") == self._active_pillar_id]
        recent = [r for r in load_recent() if r.get("pillar_id") == self._active_pillar_id]

        if pinned:
            row = self._add_section("Pinned", pinned, row, show_pillar=False)
        if recent:
            row = self._add_section("Recently opened", recent[:5], row, show_pillar=False)
        row = self._add_section("All launchers", items, row, show_pillar=False)

    def _add_section(
        self,
        title: str,
        items: List[Dict[str, Any]],
        start_row: int,
        show_pillar: bool,
    ) -> int:
        if not items:
            return start_row

        tk.Label(
            self._grid_frame,
            text=title,
            bg=CONTENT_BG,
            fg="#475569",
            font=("Segoe UI", 11, "bold"),
            anchor="w",
        ).grid(row=start_row, column=0, columnspan=3, sticky="w", pady=(12 if start_row else 0, 8), padx=4)

        card_row = start_row + 1
        col = 0
        for item in items:
            self._add_card(item, card_row, col, show_pillar)
            col += 1
            if col >= 3:
                col = 0
                card_row += 1
        if col != 0:
            card_row += 1
        return card_row

    def _add_card(self, item: Dict[str, Any], row: int, col: int, show_pillar: bool) -> None:
        frame = tk.Frame(
            self._grid_frame,
            bg=CARD_BG,
            highlightbackground=CARD_BORDER,
            highlightthickness=1,
            padx=12,
            pady=12,
        )
        frame.grid(row=row, column=col, sticky="nsew", padx=6, pady=6)
        self._grid_frame.columnconfigure(col, weight=1)

        action = item.get("action", "")
        icon = {"folder": "📁", "file": "📄", "url": "🔗", "command": "▶", "cursor": "⌨"}.get(action, "•")

        tk.Label(
            frame,
            text=icon,
            bg=CARD_BG,
            font=("Segoe UI", 18),
        ).pack(anchor="w")

        tk.Label(
            frame,
            text=item.get("label", "Untitled"),
            bg=CARD_BG,
            fg="#0f172a",
            font=("Segoe UI", 10, "bold"),
            wraplength=220,
            justify="left",
        ).pack(anchor="w", pady=(4, 2))

        tk.Label(
            frame,
            text=action,
            bg=CARD_BG,
            fg="#64748b",
            font=("Segoe UI", 8),
        ).pack(anchor="w")

        if show_pillar and item.get("pillar_label"):
            tk.Label(
                frame,
                text=item["pillar_label"],
                bg=CARD_BG,
                fg="#94a3b8",
                font=("Segoe UI", 8),
            ).pack(anchor="w", pady=(2, 0))

        for widget in (frame, *frame.winfo_children()):
            widget.bind("<Button-1>", lambda _e, i=item: self._run_item(i))
            widget.configure(cursor="hand2")

    def _find_pillar(self, pillar_id: str | None) -> Dict[str, Any] | None:
        for pillar in list_pillars(self.config_data):
            if pillar.get("id") == pillar_id:
                return pillar
        return None

    def _run_item(self, item: Dict[str, Any]) -> None:
        try:
            run_action(item, INC_ROOT)
            record_recent(item, self._active_pillar_id)
            self._render_content()
        except Exception as exc:
            logger.exception("Hub action failed for %s: %s", item.get("label"), exc)

    def _handle_close(self) -> None:
        if self._on_close:
            self._on_close()
        else:
            self.withdraw()


_hub_controller: HubController | None = None


def show_hub(config: Dict[str, Any]) -> None:
    """Open or focus the super main hub window."""
    global _hub_controller
    if _hub_controller is None:
        _hub_controller = HubController()
    _hub_controller.show(config)
