"""BB-LINKS-UX-1 Phase 1 — no Assign picker; suggest → other."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from business_bookmark_sorter.queue_store import load_routes_config
from business_bookmark_sorter.review_actions import resolve_file_destination
from business_bookmark_sorter.review_ui import ReviewPanel

CONFIG = Path(__file__).resolve().parent.parent / "config" / "routes.json"


def test_resolve_uses_suggested_destination():
    config = load_routes_config(CONFIG)
    item = {"status": "pending", "suggested_destination": "leads"}
    assert resolve_file_destination(item, config) == "leads"


def test_resolve_falls_back_to_other():
    config = load_routes_config(CONFIG)
    item = {"status": "pending", "suggested_destination": None}
    assert resolve_file_destination(item, config) == "other"


def test_resolve_rejects_stay_in_chrome_suggest():
    config = load_routes_config(CONFIG)
    item = {"status": "pending", "suggested_destination": "stay_in_chrome"}
    assert resolve_file_destination(item, config) == "other"


def test_resolve_prefers_filed_destination_when_filed():
    config = load_routes_config(CONFIG)
    item = {
        "status": "filed",
        "filed_destination": "started",
        "suggested_destination": "other",
    }
    assert resolve_file_destination(item, config) == "started"


def _panel() -> ReviewPanel:
    root = MagicMock()
    root.focus_get.return_value = None
    panel = ReviewPanel.__new__(ReviewPanel)
    panel.root = root
    panel.config = load_routes_config(CONFIG)
    panel.dest_ids = ["other", "leads", "started"]
    panel._last_sync = ""
    panel._toast_frame = None
    panel._toast_timer = None
    panel._session_settings = MagicMock(auto_open_links=False)
    panel._auto_opener = MagicMock()
    panel._skip_removal_prompt = False
    panel._stats = MagicMock()
    panel._sync_label = MagicMock()
    panel._timer_label = MagicMock()
    panel._title = MagicMock()
    panel._url = MagicMock()
    panel._folder = MagicMock()
    panel._suggest = MagicMock()
    panel._note = MagicMock()
    panel._status_msg = MagicMock()
    panel._filing_as = MagicMock()
    panel._file_btn = MagicMock()
    panel._removal_btn = MagicMock()
    panel._item = None
    return panel


def test_build_has_no_assign_to_control():
    """Source + construct path: no Assign label; Filing as present."""
    ui_src = Path(__file__).resolve().parent.parent / "review_ui.py"
    text = ui_src.read_text(encoding="utf-8")
    assert 'text="Assign to:"' not in text
    assert "ttk.Combobox" not in text
    assert "_dest_combo" not in text
    assert "Filing as:" in text
    assert "resolve_file_destination" in text


def test_display_item_sets_filing_as_from_suggest():
    panel = _panel()
    item = {
        "id": "x",
        "type": "url",
        "title": "T",
        "url": "https://example.com",
        "folder_path": "",
        "status": "pending",
        "suggested_destination": "leads",
        "suggested_reason": "keyword",
    }
    panel._display_item(item)
    call_kw = panel._filing_as.configure.call_args
    assert call_kw is not None
    shown = call_kw.kwargs.get("text") if call_kw.kwargs else call_kw[1].get("text")
    assert shown is not None
    assert shown.startswith("Filing as:")
    assert "leads" in shown


def test_file_and_open_uses_resolve_not_combo(tmp_path, monkeypatch):
    from business_bookmark_sorter import queue_store as qs
    from business_bookmark_sorter.file_workflow import FileResult
    from business_bookmark_sorter.queue_store import build_queue_item, save_queue

    monkeypatch.setattr(qs, "QUEUE_PATH", tmp_path / "queue.json")
    config = load_routes_config(CONFIG)
    item = build_queue_item(
        {
            "type": "url",
            "title": "Test",
            "url": "https://example.com/phase1",
            "folder_path": "",
        },
        config,
    )
    item["suggested_destination"] = "other"
    save_queue({"version": 1, "items": [item]})

    panel = _panel()
    panel.config = config
    panel._item = item
    panel._filing_as = MagicMock()
    panel._show_toast = MagicMock()  # type: ignore[method-assign]
    panel._update_stats_bar = MagicMock()  # type: ignore[method-assign]
    panel._display_item = MagicMock()  # type: ignore[method-assign]
    panel._advance_after_removal = MagicMock()  # type: ignore[method-assign]
    panel._show_removal_continue = MagicMock()  # type: ignore[method-assign]

    captured: list[str] = []

    def fake_file(item_id, dest, cfg):
        captured.append(dest)
        return FileResult(True, "ok", destination_id=dest, destination_label="Other")

    with patch("business_bookmark_sorter.review_ui.file_item", side_effect=fake_file):
        with patch(
            "business_bookmark_sorter.review_ui.find_item",
            return_value={**item, "status": "filed", "filed_destination": "other"},
        ):
            with patch.object(panel, "_ask_bookmark_removed", return_value=True):
                panel._file_and_open()

    assert captured == ["other"]
    panel._advance_after_removal.assert_called_once()
