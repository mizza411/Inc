"""Floating review panel — file, export, and open docx in one step."""



from __future__ import annotations



import tkinter as tk

import webbrowser

from tkinter import font as tkfont

from tkinter import messagebox

from tkinter import ttk

from typing import Any, Dict, List, Optional



from business_bookmark_sorter.export_markdown import export_filed_to_markdown, master_links_path

from business_bookmark_sorter.file_workflow import file_item

from business_bookmark_sorter.paths import CONFIG_PATH, default_chrome_bookmarks_path

from business_bookmark_sorter.queue_store import (

    count_by_status,

    load_queue,

    load_routes_config,

    next_pending,

    refresh_queue_from_sources,

)

from business_bookmark_sorter.review_actions import apply_skip, apply_stay_in_chrome, find_item
from business_bookmark_sorter.ui_tooltips import bind_tooltip





class ReviewPanel:

    def __init__(self) -> None:

        self.config = load_routes_config(CONFIG_PATH)

        self.dest_ids = self._assignable_destinations()

        self.root = tk.Tk()

        self.root.title("Business Bookmark Reviewer")

        self.root.geometry("780x480")

        self.root.attributes("-topmost", True)

        self._last_sync = ""

        self._toast_frame: tk.Frame | None = None

        self._toast_timer: str | None = None

        self._build()

        self._sync_queue(startup=True)

        self._load_current()



    def _assignable_destinations(self) -> List[str]:
        dests = self.config.get("destinations", {})
        order = self.config.get("export_section_order", [])
        keys = [k for k in order if k in dests] if order else list(dests.keys())
        assignable = [
            k
            for k in keys
            if k != "stay_in_chrome"
            and dests[k].get("label")
            and dests[k].get("assignable", True) is not False
        ]
        for k, v in dests.items():
            if (
                k not in assignable
                and k != "stay_in_chrome"
                and v.get("assignable", True) is not False
                and v.get("label")
            ):
                assignable.append(k)
        return assignable



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

        tk.Label(

            self.root,

            text="File & open doc: one Business Links doc (sections per category). Shift+click = re-export all.",

            font=("Segoe UI", 8),

            fg="#666",

        ).pack(anchor="w", padx=12)



        frame = tk.Frame(self.root)

        frame.pack(fill="both", expand=True, padx=12, pady=8)



        self._title = tk.Label(frame, text="", wraplength=720, justify="left", font=("Segoe UI", 11, "bold"))

        self._title.pack(anchor="w")

        self._url = tk.Label(frame, text="", wraplength=720, justify="left", fg="#06c", cursor="hand2")

        self._url.pack(anchor="w", pady=4)

        self._folder = tk.Label(frame, text="", wraplength=720, justify="left", fg="#666")

        self._folder.pack(anchor="w")

        self._suggest = tk.Label(frame, text="", wraplength=720, justify="left", fg="#333")

        self._suggest.pack(anchor="w", pady=6)

        self._note = tk.Label(frame, text="", wraplength=720, justify="left", fg="#a00")

        self._note.pack(anchor="w")



        dest_row = tk.Frame(self.root)

        dest_row.pack(fill="x", padx=12)

        assign_lbl = tk.Label(dest_row, text="Assign to:", font=("Segoe UI", 10))
        assign_lbl.pack(side="left")
        bind_tooltip(
            assign_lbl,
            "Category section in Business Links.md (e.g. Leads, Other). "
            "Other = system could not match a pillar, or you chose it on purpose.",
        )

        labels = [

            f"{did} — {self.config['destinations'][did].get('label', did)}"

            for did in self.dest_ids

        ]

        self._dest_var = tk.StringVar()

        self._dest_combo = ttk.Combobox(dest_row, values=labels, width=58, state="readonly")

        self._dest_combo.pack(side="left", padx=8)
        bind_tooltip(
            self._dest_combo,
            "Where this link will appear in the master document. "
            "Pick a pillar when it fits; pick Other when it does not (or you prefer Other).",
        )



        btn_row = tk.Frame(self.root)

        btn_row.pack(fill="x", padx=12, pady=12)



        open_btn = tk.Button(btn_row, text="Open URL", command=self._open_url, width=11)
        open_btn.pack(side="left", padx=3)
        bind_tooltip(open_btn, "Open this link in your browser. Does not file it or change the queue.")

        refresh_btn = tk.Button(btn_row, text="Refresh now", command=self._refresh_only, width=11)
        refresh_btn.pack(side="left", padx=3)
        bind_tooltip(
            refresh_btn,
            "Sync queue.json from Chrome now (new bookmarks, mark removed ones as gone).",
        )

        self._file_btn = tk.Button(

            btn_row,

            text="File & open doc",

            width=14,

            bg="#2d89ef",

            fg="white",

        )

        self._file_btn.pack(side="left", padx=3)

        self._file_btn.bind("<Button-1>", self._on_file_click)
        bind_tooltip(
            self._file_btn,
            "File this bookmark: save to queue, update Business Links.md/.docx, open the doc. "
            "Shift+click: re-export all filed links without filing the current item.",
        )

        self._removal_btn = tk.Button(
            btn_row,
            text="Bookmark removed — next",
            command=self._advance_after_removal,
            width=18,
            bg="#5cb85c",
            fg="white",
        )
        bind_tooltip(
            self._removal_btn,
            "You filed this link but have not confirmed Chrome removal yet. "
            "Delete the bookmark in Chrome, then click here to go to the next item.",
        )

        skip_btn = tk.Button(btn_row, text="Skip", command=self._skip, width=8)
        skip_btn.pack(side="left", padx=3)
        bind_tooltip(
            skip_btn,
            "Decide later — skip for now. Chrome bookmark stays. Not added to Business Links. "
            "May show up again if you re-import or reset status.",
        )

        stay_btn = tk.Button(
            btn_row,
            text="Stay in Chrome",
            command=self._stay,
            width=13,
            bg="#f0ad4e",
        )
        stay_btn.pack(side="left", padx=3)
        bind_tooltip(
            stay_btn,
            "Done reviewing — this is not an Inc link. Keep it in Chrome only; "
            "do not file to Business Links. Won't appear as pending again.",
        )

        quit_btn = tk.Button(btn_row, text="Quit", command=self.root.destroy, width=7)
        quit_btn.pack(side="right", padx=3)
        bind_tooltip(quit_btn, "Close the Business Bookmark Reviewer.")



        self._status_msg = tk.Label(self.root, text="", fg="#080", font=("Segoe UI", 9))

        self._status_msg.pack(anchor="w", padx=12, pady=(0, 8))



    def _current_item(self) -> Optional[Dict[str, Any]]:

        return getattr(self, "_item", None)



    def _hide_toast(self) -> None:

        if self._toast_frame is not None:

            self._toast_frame.destroy()

            self._toast_frame = None

        self._toast_timer = None



    def _show_toast(self, title: str, subtitle: str = "", *, success: bool = True) -> None:

        self._hide_toast()



        border = "#28a745" if success else "#dc3545"

        bg = "#d4edda" if success else "#f8d7da"

        fg = "#155724" if success else "#721c24"



        self._toast_frame = tk.Frame(self.root, bg=border, bd=0)

        inner = tk.Frame(self._toast_frame, bg=bg)

        inner.pack(fill="both", expand=True, padx=1, pady=1)



        tk.Label(

            inner,

            text=title,

            bg=bg,

            fg=fg,

            font=("Segoe UI", 11, "bold"),

            justify="left",

        ).pack(anchor="w", padx=14, pady=(10, 2))

        if subtitle:

            tk.Label(

                inner,

                text=subtitle,

                bg=bg,

                fg=fg,

                font=("Segoe UI", 9),

                justify="left",

            ).pack(anchor="w", padx=14, pady=(0, 10))



        self._toast_frame.place(relx=1.0, rely=0.0, anchor="ne", x=-14, y=14)

        self._toast_frame.lift()

        self._toast_timer = self.root.after(3200, self._hide_toast)



    def _sync_queue(self, startup: bool = False) -> None:

        try:

            queue = refresh_queue_from_sources(

                self.config,

                bookmarks_path=default_chrome_bookmarks_path(),

                merge_inbox=False,

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



    def _update_stats_bar(self, queue: Dict[str, Any]) -> None:
        counts = count_by_status(queue)
        pending = counts.get("pending", 0)
        self._stats.configure(
            text=f"Pending: {pending} | Filed: {counts.get('filed', 0)} | "
            f"Stay in Chrome: {counts.get('stay_in_chrome', 0)} | Skipped: {counts.get('skipped', 0)} | "
            f"Gone: {counts.get('gone_from_chrome', 0)}"
        )
        self._sync_label.configure(text=f"Last synced: {self._last_sync or 'not yet'}")

    def _display_item(self, item: Dict[str, Any], *, extra_note: str = "") -> None:
        self._item = item
        self._title.configure(text=item.get("title", "(no title)"))
        url = item.get("url") or "(folder — open in Chrome)"
        self._url.configure(text=url)
        self._folder.configure(text=f"Chrome path: {item.get('folder_path', '')}")
        filed = item.get("status") == "filed"
        if filed:
            dest = item.get("filed_destination", "")
            label = self.config.get("destinations", {}).get(dest, {}).get("label", dest)
            self._suggest.configure(text=f"Filed → {label}")
        else:
            self._suggest.configure(
                text=f"Suggest: {item.get('suggested_destination')} — {item.get('suggested_reason', '')}"
            )
        note = item.get("note") or ""
        if extra_note:
            note = f"{extra_note}\n{note}".strip() if note else extra_note
        self._note.configure(text=note)
        dest_pick = item.get("filed_destination") or item.get("suggested_destination", self.dest_ids[0])
        self._set_combo_dest(dest_pick)

    def _show_removal_continue(self, show: bool) -> None:
        if show:
            self._removal_btn.pack(side="left", padx=3, after=self._file_btn)
        else:
            self._removal_btn.pack_forget()

    def _ask_bookmark_removed(self, title: str) -> bool:
        short = (title or "this bookmark")[:100]
        return messagebox.askyesno(
            "Remove bookmark from Chrome?",
            f"Have you removed this bookmark from Chrome?\n\n{short}\n\n"
            "Yes = removed — go to next link\n"
            "No = not yet — stay on this link",
            parent=self.root,
            default=messagebox.NO,
            icon="question",
        )

    def _advance_after_removal(self) -> None:
        self._show_removal_continue(False)
        self._sync_queue(startup=False)
        self._load_current()

    def _load_current(self) -> None:
        self._show_removal_continue(False)
        queue = load_queue()
        self._update_stats_bar(queue)
        item = next_pending(queue)
        if not item:
            self._item = None
            self._title.configure(text="All pending items reviewed.")
            self._url.configure(text="")
            self._folder.configure(text="")
            self._suggest.configure(text="")
            self._note.configure(text="")
            return
        self._display_item(item)



    def _open_url(self) -> None:

        item = self._current_item()

        if item and item.get("url"):

            webbrowser.open(item["url"])



    def _on_file_click(self, event: tk.Event) -> str:

        if event.state & 0x0001:

            self._reexport_all()

        else:

            self._file_and_open()

        return "break"



    def _file_and_open(self) -> None:

        item = self._current_item()

        if not item:

            return

        dest = self._dest_from_combo()

        result = file_item(item["id"], dest, self.config)

        self._status_msg.configure(text=result.message, fg="#080" if result.ok else "#a00")

        if result.ok:

            md_name = result.md_path.name if result.md_path else ""

            docx_name = result.docx_path.name if result.docx_path else ""

            self._show_toast(
                "Filed & exported",
                f"Section: {result.destination_label}\n{md_name}"
                + (f"\nOpened {docx_name}" if docx_name else ""),
                success=True,
            )
            filed_id = item["id"]
            queue = load_queue()
            filed_item = find_item(queue, filed_id) or item
            self._update_stats_bar(queue)
            self._display_item(filed_item)
            if self._ask_bookmark_removed(filed_item.get("title", "")):
                self._advance_after_removal()
            else:
                self._show_removal_continue(True)
                self._display_item(
                    filed_item,
                    extra_note="Remove this bookmark in Chrome, then click "
                    '"Bookmark removed — next" or file again and choose Yes.',
                )
                self._status_msg.configure(
                    text="Waiting for Chrome removal — staying on this link.",
                    fg="#a60",
                )

        else:

            sub = result.message

            if result.md_path:

                sub += f"\nMarkdown: {result.md_path}"

            self._show_toast("Could not complete filing", sub, success=False)



    def _reexport_all(self) -> None:

        try:

            queue = load_queue()

            count, paths = export_filed_to_markdown(self.config, queue)

            master = paths[0] if paths else master_links_path(self.config)

            msg = f"Re-exported {count} link(s) to {master.name}"

            self._status_msg.configure(text=msg, fg="#080")

            self._show_toast("Full re-export done", msg, success=True)

        except Exception as exc:

            self._status_msg.configure(text=f"Re-export failed: {exc}", fg="#a00")

            self._show_toast("Re-export failed", str(exc), success=False)



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


