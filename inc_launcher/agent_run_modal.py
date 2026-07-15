"""Option B confirmation modal for agent formulation run (Phase 5.4)."""

from __future__ import annotations

import logging
import tkinter as tk
from typing import Any, Callable, Dict, Sequence

from inc_launcher.actions import run_action
from inc_launcher.config import INC_ROOT

logger = logging.getLogger(__name__)

MODAL_TITLE = "Ready for formulation agent run?"
BULLETS = (
    f"Opens Cursor at {INC_ROOT}",
    "Pastes prompt into chat (~8s)",
    "Skips 3, 4, 8, 10 per policy",
)


def bullets_for_item(item: Dict[str, Any]) -> tuple[str, ...]:
    custom = item.get("modal_bullets")
    if isinstance(custom, (list, tuple)) and custom:
        return tuple(str(x) for x in custom)
    return BULLETS


def title_for_item(item: Dict[str, Any]) -> str:
    custom = item.get("modal_title")
    if isinstance(custom, str) and custom.strip():
        return custom.strip()
    return MODAL_TITLE


class AgentRunModal(tk.Toplevel):
    """Hub-hosted confirmation before agent formulation orchestration."""

    def __init__(
        self,
        master: tk.Misc,
        item: Dict[str, Any],
        on_started: Callable[[], None] | None = None,
    ) -> None:
        super().__init__(master)
        self._item = item
        self._on_started = on_started
        self._bullets: Sequence[str] = bullets_for_item(item)
        self._modal_title = title_for_item(item)

        self.title(item.get("label") or "Agent formulation run")
        self.configure(bg="#ffffff")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        pad = {"padx": 20, "pady": 4}
        tk.Label(
            self,
            text=self._modal_title,
            bg="#ffffff",
            fg="#0f172a",
            font=("Segoe UI", 12, "bold"),
            anchor="w",
            justify="left",
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(20, 12))

        for row, line in enumerate(self._bullets, start=1):
            tk.Label(
                self,
                text=f"• {line}",
                bg="#ffffff",
                fg="#475569",
                font=("Segoe UI", 10),
                anchor="w",
                justify="left",
            ).grid(row=row, column=0, sticky="w", **pad)

        btn_frame = tk.Frame(self, bg="#ffffff")
        btn_frame.grid(row=len(self._bullets) + 1, column=0, sticky="e", padx=20, pady=(16, 20))

        tk.Button(
            btn_frame,
            text="Not now",
            command=self.destroy,
            font=("Segoe UI", 10),
            padx=12,
            pady=4,
        ).pack(side="right", padx=(8, 0))

        tk.Button(
            btn_frame,
            text="Start",
            command=self._on_start,
            font=("Segoe UI", 10, "bold"),
            bg="#228be6",
            fg="#ffffff",
            activebackground="#1c7ed6",
            activeforeground="#ffffff",
            padx=16,
            pady=4,
            cursor="hand2",
        ).pack(side="right")

        self.update_idletasks()
        self._center_on_parent(master)

    def _center_on_parent(self, master: tk.Misc) -> None:
        try:
            master.update_idletasks()
            px = master.winfo_rootx()
            py = master.winfo_rooty()
            pw = master.winfo_width()
            ph = master.winfo_height()
            w = self.winfo_width()
            h = self.winfo_height()
            x = px + max(0, (pw - w) // 2)
            y = py + max(0, (ph - h) // 2)
            self.geometry(f"+{x}+{y}")
        except tk.TclError:
            pass

    def _on_start(self) -> None:
        try:
            run_action(self._item, INC_ROOT)
            if self._on_started is not None:
                self._on_started()
        except Exception as exc:
            logger.exception("Agent formulation run failed: %s", exc)
        finally:
            self.destroy()


def show_agent_run_modal(
    master: tk.Misc,
    item: Dict[str, Any],
    on_started: Callable[[], None] | None = None,
) -> AgentRunModal:
    modal = AgentRunModal(master, item, on_started=on_started)
    modal.lift()
    modal.focus_force()
    return modal
