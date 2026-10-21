"""Super main hub window — 4-pillar launcher grid (Phase 2)."""

from __future__ import annotations

import logging
import queue
import threading
import tkinter as tk
from pathlib import Path
from tkinter import font as tkfont
from tkinter import ttk
from typing import Any, Callable, Dict, List, Optional

from inc_launcher.actions import run_action
from inc_launcher.agent_run_modal import show_agent_run_modal
from inc_launcher.config import INC_ROOT, list_pillars
from inc_launcher.option_b_actions import prepare_option_b_item, uses_option_b_modal
from inc_launcher.recent import list_pinned, load_recent, record_recent
from inc_launcher.scheduled_nudges import find_menu_item_by_id

logger = logging.getLogger(__name__)

NETWORK_ASK_ITEM_ID = "network_ask_remind"
PROSPECT_ESTABLISHED_ITEM_ID = "prospect_businesses_folder_established"

PROSPECT_NUDGE_TITLE = "Check your prospective businesses?"
PROSPECT_NUDGE_BULLETS = (
    "On My Established business ideas, open All launchers",
    "Click Prospect Businesses folder (beside Started Businesses)",
    "That shortlist is not Started businesses yet",
)


def resolve_network_ask_item(config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Return the Ask people/owners card from Hub config, or None."""
    item = find_menu_item_by_id(config, NETWORK_ASK_ITEM_ID)
    if item is None:
        return None
    if item.get("action") != "network_ask":
        return None
    return item


def resolve_prospect_established_item(config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Return Established All-launchers Prospect folder card, or None."""
    for pillar in list_pillars(config):
        if pillar.get("id") != "established":
            continue
        for item in pillar.get("items", []):
            if item.get("id") == PROSPECT_ESTABLISHED_ITEM_ID:
                return dict(item)
    return None


def build_prospect_nudge_item(config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Option B-shaped item that opens Prospect-Businesses/ from the nudge."""
    base = resolve_prospect_established_item(config)
    if base is None:
        return None
    return {
        **base,
        "modal_title": PROSPECT_NUDGE_TITLE,
        "modal_bullets": list(PROSPECT_NUDGE_BULLETS),
        "modal_start_label": "Open folder",
        "modal_start_hover": "Open the Prospect Businesses folder",
    }

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
        self._pending_agent_run: Dict[str, Any] | None = None
        self._times_window: tk.Toplevel | None = None

    def show(self, config: Dict[str, Any]) -> None:
        """Open Hub and always pair the Ask people/owners Option B modal (1a)."""
        self._config = config
        if self._thread is None or not self._thread.is_alive():
            self._queue = queue.Queue()
            self._ready.clear()
            self._thread = threading.Thread(target=self._run_loop, daemon=True, name="inc-hub")
            self._thread.start()
            self._ready.wait(timeout=10)
        assert self._queue is not None
        self._queue.put("show")
        # NET-ASK-ALWAYS-SHOW-1 Phase 1a: Hub open ⇒ Ask modal (copy may be off-cadence preview).
        self._queue.put("always_show_network_ask")

    def prompt_agent_run(self, config: Dict[str, Any], item: Dict[str, Any]) -> None:
        """Open Hub and show Option B modal (tray or external callers).

        Does not also force Ask on top when the item is agent_run (avoids two grabs).
        network_ask items already are the Ask modal.
        """
        self._config = config
        self._pending_agent_run = item
        if self._thread is None or not self._thread.is_alive():
            self._queue = queue.Queue()
            self._ready.clear()
            self._thread = threading.Thread(target=self._run_loop, daemon=True, name="inc-hub")
            self._thread.start()
            self._ready.wait(timeout=10)
        assert self._queue is not None
        self._queue.put("show_agent_run")

    def show_hub_open_times(self, config: Dict[str, Any]) -> None:
        """Queue the Hub open times form on this Hub thread. Does not create a Tk root."""
        self._config = config
        if self._thread is None or not self._thread.is_alive():
            self._queue = queue.Queue()
            self._ready.clear()
            self._thread = threading.Thread(target=self._run_loop, daemon=True, name="inc-hub")
            self._thread.start()
            self._ready.wait(timeout=10)
        assert self._queue is not None
        self._queue.put("show_hub_open_times")

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
            elif cmd == "always_show_network_ask":
                self._open_network_ask_modal()
            elif cmd == "show_agent_run":
                self._open_window()
                if self._window is not None and self._pending_agent_run is not None:
                    item = self._pending_agent_run
                    self._pending_agent_run = None
                    self._window.show_agent_run_for_item(item)
            elif cmd == "show_hub_open_times":
                self._open_hub_open_times()
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

    def _open_network_ask_modal(self) -> None:
        """Show Ask Option B with Hub (always-show). Soft no-op if card missing."""
        self._open_window()
        if self._window is None:
            return
        item = resolve_network_ask_item(self._config)
        if item is None:
            logger.warning(
                "Always-show Ask skipped: no menu item id=%s",
                NETWORK_ASK_ITEM_ID,
            )
            return
        # After Ask dismiss: Prospect nudge (Established All launchers).
        self._window.show_agent_run_for_item(
            item,
            on_closed=self._window.schedule_prospect_nudge_after_ask,
        )

    def _open_hub_open_times(self) -> None:
        """Open the times form on the existing Hub root."""
        if self._root is None:
            return
        if self._times_window is not None:
            try:
                if self._times_window.winfo_exists():
                    self._times_window.deiconify()
                    self._times_window.lift()
                    self._times_window.focus_force()
                    return
            except tk.TclError:
                self._times_window = None
        from inc_launcher.hub_open_times_window import HubOpenTimesWindow

        path_text = self._config.get("_config_path")
        path = Path(path_text) if path_text else None
        self._times_window = HubOpenTimesWindow(self._root, path)
        self._times_window.deiconify()
        self._times_window.lift()

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

        pillar_count = len(list_pillars(self.config_data))
        tk.Label(
            sidebar,
            text=f"{pillar_count} pillars",
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

        restore_ask = tk.Button(
            sidebar,
            text="Show Ask reminder",
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
            command=self._restore_network_ask,
        )
        restore_ask.pack(fill="x")
        self._attach_hover_label(restore_ask, "Show the Ask people / owners window again")

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
        content_outer.rowconfigure(2, weight=1)
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
        self._subtitle.grid(row=1, column=0, sticky="ew", padx=24, pady=(0, 8))

        canvas = tk.Canvas(content_outer, bg=CONTENT_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_outer, orient="vertical", command=canvas.yview)
        self._grid_frame = tk.Frame(canvas, bg=CONTENT_BG)
        self._grid_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=self._grid_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.grid(row=2, column=0, sticky="nsew", padx=(24, 0), pady=(0, 24))
        scrollbar.grid(row=2, column=1, sticky="ns", pady=(0, 24))

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
        icon = {
            "folder": "📁",
            "file": "📄",
            "url": "🔗",
            "command": "▶",
            "cursor": "⌨",
            "agent_run": "🤖",
            "network_ask": "💬",
        }.get(action, "•")

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
            if uses_option_b_modal(item.get("action")):
                prepared = prepare_option_b_item(item)
                show_agent_run_modal(
                    self,
                    prepared,
                    on_started=lambda: self._after_option_b_started(prepared),
                )
                return
            run_action(item, INC_ROOT)
            record_recent(item, self._active_pillar_id)
            self._render_content()
        except Exception as exc:
            logger.exception("Hub action failed for %s: %s", item.get("label"), exc)

    def show_agent_run_for_item(
        self,
        item: Dict[str, Any],
        on_closed: Callable[[], None] | None = None,
    ) -> None:
        """Show Option B modal when Hub was opened from tray / schedule."""
        prepared = prepare_option_b_item(item)
        show_agent_run_modal(
            self,
            prepared,
            on_started=lambda: self._after_option_b_started(prepared),
            on_closed=on_closed,
        )

    def schedule_prospect_nudge_after_ask(self) -> None:
        """Queue Prospect nudge after Ask grab releases (same Hub session)."""
        try:
            self.after(0, self.show_prospect_folder_nudge)
        except tk.TclError:
            logger.warning("Prospect nudge skipped: Hub no longer available")

    def show_prospect_folder_nudge(self) -> None:
        """Guide owner to Established → All launchers → Prospect Businesses folder."""
        if not self.winfo_exists():
            return
        nudge = build_prospect_nudge_item(self.config_data)
        if nudge is None:
            logger.warning(
                "Prospect nudge skipped: no menu item id=%s",
                PROSPECT_ESTABLISHED_ITEM_ID,
            )
            return
        self._select_pillar("established")
        self.deiconify()
        self.lift()
        # No on_closed chain (avoid loops). Start opens the folder via run_action.
        show_agent_run_modal(
            self,
            nudge,
            on_started=lambda: self._after_option_b_started(nudge),
        )

    def _restore_network_ask(self) -> None:
        """Phase 1b: bring Ask modal back after dismiss (Hub sidebar)."""
        item = resolve_network_ask_item(self.config_data)
        if item is None:
            logger.warning("Restore Ask skipped: no menu item id=%s", NETWORK_ASK_ITEM_ID)
            return
        self.show_agent_run_for_item(
            item,
            on_closed=self.schedule_prospect_nudge_after_ask,
        )

    def _attach_hover_label(self, widget: tk.Misc, text: str) -> None:
        tip: tk.Toplevel | None = None

        def _show(_event: tk.Event) -> None:
            nonlocal tip
            if tip is not None:
                return
            tip = tk.Toplevel(self)
            tip.wm_overrideredirect(True)
            tip.attributes("-topmost", True)
            tk.Label(
                tip,
                text=text,
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

    def _after_option_b_started(self, item: Dict[str, Any]) -> None:
        record_recent(item, self._active_pillar_id)
        self._render_content()

    # Compat name used by older tests / call sites
    _after_agent_run_started = _after_option_b_started

    def _handle_close(self) -> None:
        if self._on_close:
            self._on_close()
        else:
            self.withdraw()


_hub_controller: HubController | None = None


def show_hub_open_times(config: Dict[str, Any]) -> None:
    """Open Hub open times on the running Hub thread."""
    global _hub_controller
    if _hub_controller is None:
        _hub_controller = HubController()
    _hub_controller.show_hub_open_times(config)


def show_hub(config: Dict[str, Any]) -> None:
    """Open or focus the super main hub window."""
    global _hub_controller
    if _hub_controller is None:
        _hub_controller = HubController()
    _hub_controller.show(config)


def open_hub_with_option_b(config: Dict[str, Any], item: Dict[str, Any]) -> None:
    """Open Hub and show Option B confirmation modal (agent_run or network_ask)."""
    global _hub_controller
    if _hub_controller is None:
        _hub_controller = HubController()
    _hub_controller.prompt_agent_run(config, prepare_option_b_item(item))


def restore_network_ask(config: Dict[str, Any]) -> bool:
    """Phase 1b: open Hub + Ask modal again after dismiss. Returns False if card missing."""
    item = resolve_network_ask_item(config)
    if item is None:
        logger.warning("Restore Ask skipped: no menu item id=%s", NETWORK_ASK_ITEM_ID)
        return False
    open_hub_with_option_b(config, item)
    return True


def open_hub_with_agent_run(config: Dict[str, Any], item: Dict[str, Any]) -> None:
    """Compat alias for open_hub_with_option_b."""
    open_hub_with_option_b(config, item)
