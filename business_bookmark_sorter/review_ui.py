"""Floating review panel — Batch Link Reviewer-style (Phase 2)."""

from __future__ import annotations

import tkinter as tk
import webbrowser
from tkinter import font as tkfont
from tkinter import ttk
from typing import Any, Dict, List, Optional

from business_bookmark_sorter.paths import CONFIG_PATH, default_chrome_bookmarks_path
from business_bookmark_sorter.queue_store import (
    count_by_status,
    load_queue,
    load_routes_config,
    next_pending,
    refresh_queue_from_sources,
)
from business_bookmark_sorter.review_actions import apply_file, apply_skip, apply_stay_in_chrome


class ReviewPanel:
    def __init__(self) -> None:
        self.config = load_routes_config(CONFIG_PATH)
        self.dest_ids = self._fileable_destinations()
        self.root = tk.Tk()
        self.root.title("Business Bookmark Reviewer")
        self.root.geometry("720x420")
        self.root.attributes("-topmost", True)
        self._last_sync = ""
        self._build()
        self._sync_queue(startup=True)
        self._load_current()

    def _fileable_destinations(self) -> List[str]:
        dests = self.config.get("destinations", {})
        return [k for k, v in dests.items() if v.get("links_file") and k != "stay_in_chrome"]

    def _build(self) -> None:
        header = tk.Label(
            self.root,
            text="Business Bookmark Reviewer",
            font=tkfont.Font(family="Segoe UI", size=14, weight="bold"),
        )
        header.pack(anchor="w", padx=12, pady=(12, 4))

        self._stats = tk.Label(self.root, text="", font=("Segoe UI", 9), fg="#555")
        self._stats.pack(anchor="w", padx=12)
        self._sync_label = tk.Label(self.root, text="", font=("Segoe UI", 9), fg="#777")
        self._sync_label.pack(anchor="w", padx=12)

        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=12, pady=8)

        self._title = tk.Label(frame, text="", wraplength=680, justify="left", font=("Segoe UI", 11, "bold"))
        self._title.pack(anchor="w")
        self._url = tk.Label(frame, text="", wraplength=680, justify="left", fg="#06c", cursor="hand2")
        self._url.pack(anchor="w", pady=4)
        self._folder = tk.Label(frame, text="", wraplength=680, justify="left", fg="#666")
        self._folder.pack(anchor="w")
        self._suggest = tk.Label(frame, text="", wraplength=680, justify="left", fg="#333")
        self._suggest.pack(anchor="w", pady=6)
        self._note = tk.Label(frame, text="", wraplength=680, justify="left", fg="#a00")
        self._note.pack(anchor="w")

        dest_row = tk.Frame(self.root)
        dest_row.pack(fill="x", padx=12)
        tk.Label(dest_row, text="File to:", font=("Segoe UI", 10)).pack(side="left")
        labels = [
            f"{did} — {self.config['destinations'][did].get('label', did)}"
            for did in self.dest_ids
        ]
        self._dest_var = tk.StringVar()
        self._dest_combo = ttk.Combobox(dest_row, values=labels, width=55, state="readonly")
        self._dest_combo.pack(side="left", padx=8)

        btn_row = tk.Frame(self.root)
        btn_row.pack(fill="x", padx=12, pady=12)

        tk.Button(btn_row, text="Open URL", command=self._open_url, width=12).pack(side="left", padx=4)
        tk.Button(btn_row, text="Refresh now", command=self._refresh_only, width=12).pack(side="left", padx=4)
        tk.Button(
            btn_row,
            text="File here",
            command=self._file_here,
            width=12,
            bg="#2d89ef",
            fg="white",
        ).pack(side="left", padx=4)
        tk.Button(btn_row, text="Skip", command=self._skip, width=10).pack(side="left", padx=4)
        tk.Button(
            btn_row,
            text="Stay in Chrome",
            command=self._stay,
            width=14,
            bg="#f0ad4e",
        ).pack(side="left", padx=4)
        tk.Button(btn_row, text="Quit", command=self.root.destroy, width=8).pack(side="right", padx=4)

        self._status_msg = tk.Label(self.root, text="", fg="#080", font=("Segoe UI", 9))
        self._status_msg.pack(anchor="w", padx=12, pady=(0, 8))

    def _current_item(self) -> Optional[Dict[str, Any]]:
        return getattr(self, "_item", None)

    def _sync_queue(self, startup: bool = False) -> None:
        try:
            queue = refresh_queue_from_sources(
                self.config,
                bookmarks_path=default_chrome_bookmarks_path(),
                merge_inbox=True,
            )
            self._last_sync = queue.get("last_sync_at", "")
            extra = queue.get("_added_on_sync", 0)
            prefix = "Startup sync complete" if startup else "Synced"
            self._status_msg.configure(text=f"{prefix}: +{extra} new from Chrome", fg="#080")
        except Exception as exc:
            self._status_msg.configure(text=f"Sync warning: {exc}", fg="#a00")

    def _refresh_only(self) -> None:
        self._sync_queue(startup=False)
        self._load_current()

    def _dest_from_combo(self) -> str:
        val = self._dest_var.get() or self._dest_combo.get()
        return val.split(" — ", 1)[0].strip() if val else self.dest_ids[0]

    def _set_combo_dest(self, dest_id: str) -> None:
        for i, did in enumerate(self.dest_ids):
            if did == dest_id:
                self._dest_combo.current(i)
                return
        if self.dest_ids:
            self._dest_combo.current(0)

    def _load_current(self) -> None:
        queue = load_queue()
        counts = count_by_status(queue)
        pending = counts.get("pending", 0)
        self._stats.configure(
            text=f"Pending: {pending} | Filed: {counts.get('filed', 0)} | "
            f"Stay in Chrome: {counts.get('stay_in_chrome', 0)} | Skipped: {counts.get('skipped', 0)} | "
            f"Gone: {counts.get('gone_from_chrome', 0)}"
        )
        self._sync_label.configure(text=f"Last synced: {self._last_sync or 'not yet'}")

        item = next_pending(queue)
        self._item = item
        if not item:
            self._title.configure(text="All pending items reviewed.")
            self._url.configure(text="")
            self._folder.configure(text="")
            self._suggest.configure(text="")
            self._note.configure(text="")
            return

        self._title.configure(text=item.get("title", "(no title)"))
        url = item.get("url") or "(folder — open in Chrome)"
        self._url.configure(text=url)
        self._folder.configure(text=f"Chrome path: {item.get('folder_path', '')}")
        self._suggest.configure(
            text=f"Suggest: {item.get('suggested_destination')} — {item.get('suggested_reason', '')}"
        )
        self._note.configure(text=item.get("note") or "")
        self._set_combo_dest(item.get("suggested_destination", self.dest_ids[0]))

    def _open_url(self) -> None:
        item = self._current_item()
        if item and item.get("url"):
            webbrowser.open(item["url"])

    def _file_here(self) -> None:
        item = self._current_item()
        if not item:
            return
        dest = self._dest_from_combo()
        ok, msg = apply_file(item["id"], dest, self.config)
        self._status_msg.configure(text=msg, fg="#080" if ok else "#a00")
        if ok:
            self._sync_queue(startup=False)
            self._load_current()

    def _skip(self) -> None:
        item = self._current_item()
        if not item:
            return
        ok, msg = apply_skip(item["id"])
        self._status_msg.configure(text=msg, fg="#080" if ok else "#a00")
        if ok:
            self._sync_queue(startup=False)
            self._load_current()

    def _stay(self) -> None:
        item = self._current_item()
        if not item:
            return
        ok, msg = apply_stay_in_chrome(item["id"])
        self._status_msg.configure(text=msg, fg="#080" if ok else "#a00")
        if ok:
            self._sync_queue(startup=False)
            self._load_current()

    def run(self) -> None:
        self.root.mainloop()


def run_review_panel() -> None:
    ReviewPanel().run()
