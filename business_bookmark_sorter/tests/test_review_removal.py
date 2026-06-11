"""Tests for post-file Chrome removal confirmation dialog."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import tkinter as tk

from business_bookmark_sorter.file_workflow import FileResult
from business_bookmark_sorter.queue_store import build_queue_item, load_routes_config, save_queue
from business_bookmark_sorter.review_ui import ReviewPanel

CONFIG = Path(__file__).resolve().parent.parent / "config" / "routes.json"


def _panel_with_hidden_root() -> ReviewPanel:
    root = tk.Tk()
    root.withdraw()
    panel = ReviewPanel.__new__(ReviewPanel)
    panel.root = root
    panel.config = load_routes_config(CONFIG)
    panel.dest_ids = ["leads", "other"]
    panel._last_sync = ""
    panel._toast_frame = None
    panel._toast_timer = None
    panel._stats = MagicMock()
    panel._sync_label = MagicMock()
    panel._title = MagicMock()
    panel._url = MagicMock()
    panel._folder = MagicMock()
    panel._suggest = MagicMock()
    panel._note = MagicMock()
    panel._status_msg = MagicMock()
    panel._dest_combo = MagicMock()
    panel._file_btn = MagicMock()
    panel._removal_btn = MagicMock()
    panel._item = None
    return panel


def test_ask_bookmark_removed_uses_yes_no_dialog():
    panel = _panel_with_hidden_root()
    with patch(
        "business_bookmark_sorter.review_ui.messagebox.askyesno",
        return_value=True,
    ) as ask:
        assert panel._ask_bookmark_removed("Example bookmark title") is True
        ask.assert_called_once()
        assert "removed" in ask.call_args[0][1].lower()
        assert ask.call_args[1]["default"] == tk.messagebox.NO
    panel.root.destroy()


def test_file_and_open_advances_when_user_says_yes(tmp_path, monkeypatch):
    from business_bookmark_sorter import queue_store as qs

    monkeypatch.setattr(qs, "QUEUE_PATH", tmp_path / "queue.json")
    config = load_routes_config(CONFIG)
    item = build_queue_item(
        {"type": "url", "title": "Test", "url": "https://example.com/t", "folder_path": ""},
        config,
    )
    save_queue({"version": 1, "items": [item]})

    panel = _panel_with_hidden_root()
    panel.config = config
    panel._dest_combo.get.return_value = "leads — My leads"
    panel._item = item
    panel._dest_from_combo = lambda: "leads"  # type: ignore[method-assign]
    panel._show_toast = MagicMock()  # type: ignore[method-assign]
    panel._update_stats_bar = MagicMock()  # type: ignore[method-assign]
    panel._display_item = MagicMock()  # type: ignore[method-assign]
    panel._advance_after_removal = MagicMock()  # type: ignore[method-assign]
    panel._show_removal_continue = MagicMock()  # type: ignore[method-assign]

    ok_result = FileResult(
        True,
        "ok",
        destination_id="leads",
        destination_label="My leads",
    )
    with patch("business_bookmark_sorter.review_ui.file_item", return_value=ok_result):
        with patch(
            "business_bookmark_sorter.review_ui.find_item",
            return_value={**item, "status": "filed", "filed_destination": "leads"},
        ):
            with patch.object(panel, "_ask_bookmark_removed", return_value=True):
                panel._file_and_open()

    panel._advance_after_removal.assert_called_once()
    panel._show_removal_continue.assert_not_called()
    panel.root.destroy()


def test_file_and_open_stays_when_user_says_not_yet(tmp_path, monkeypatch):
    from business_bookmark_sorter import queue_store as qs

    monkeypatch.setattr(qs, "QUEUE_PATH", tmp_path / "queue.json")
    config = load_routes_config(CONFIG)
    item = build_queue_item(
        {"type": "url", "title": "Test", "url": "https://example.com/t", "folder_path": ""},
        config,
    )
    save_queue({"version": 1, "items": [item]})

    panel = _panel_with_hidden_root()
    panel.config = config
    panel._item = item
    panel._dest_from_combo = lambda: "other"  # type: ignore[method-assign]
    panel._show_toast = MagicMock()  # type: ignore[method-assign]
    panel._update_stats_bar = MagicMock()  # type: ignore[method-assign]
    panel._display_item = MagicMock()  # type: ignore[method-assign]
    panel._advance_after_removal = MagicMock()  # type: ignore[method-assign]
    panel._show_removal_continue = MagicMock()  # type: ignore[method-assign]

    ok_result = FileResult(True, "ok", destination_id="other", destination_label="Other")
    filed = {**item, "status": "filed", "filed_destination": "other"}

    with patch("business_bookmark_sorter.review_ui.file_item", return_value=ok_result):
        with patch("business_bookmark_sorter.review_ui.find_item", return_value=filed):
            with patch.object(panel, "_ask_bookmark_removed", return_value=False):
                panel._file_and_open()

    panel._advance_after_removal.assert_not_called()
    panel._show_removal_continue.assert_called_once_with(True)
    assert panel._display_item.call_count >= 2
    panel.root.destroy()
