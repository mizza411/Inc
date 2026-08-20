"""BB-TIMED-1 Phase 4 — removal skip flag + suggested dest pre-select."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from business_bookmark_sorter.queue_store import load_routes_config
from business_bookmark_sorter.review_ui import ReviewPanel

CONFIG = Path(__file__).resolve().parent.parent / "config" / "routes.json"


def _panel() -> ReviewPanel:
    # Avoid live Tk when a review window already holds the Tcl runtime (flaky on this PC).
    root = MagicMock()
    root.focus_get.return_value = None
    panel = ReviewPanel.__new__(ReviewPanel)
    panel.root = root
    panel.config = load_routes_config(CONFIG)
    panel.dest_ids = [
        k
        for k in panel.config.get("export_section_order", [])
        if k in panel.config.get("destinations", {})
        and k != "stay_in_chrome"
        and panel.config["destinations"][k].get("assignable", True) is not False
    ] or ["other", "leads"]
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


def test_ask_skips_dialog_when_session_flag_set():
    panel = _panel()
    panel._skip_removal_prompt = True
    with patch(
        "business_bookmark_sorter.review_ui.ask_bookmark_removed_dialog"
    ) as ask:
        assert panel._ask_bookmark_removed("Anything") is True
        ask.assert_not_called()


def test_ask_sets_flag_when_dont_ask_checked():
    panel = _panel()
    with patch(
        "business_bookmark_sorter.review_ui.ask_bookmark_removed_dialog",
        return_value=(True, True),
    ):
        assert panel._ask_bookmark_removed("T") is True
    assert panel._skip_removal_prompt is True


def test_display_item_shows_filing_as_from_suggested_destination():
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
    if "leads" not in panel.dest_ids:
        panel.dest_ids.append("leads")
    panel._display_item(item)
    call_kw = panel._filing_as.configure.call_args
    assert call_kw is not None
    shown = call_kw.kwargs.get("text") if call_kw.kwargs else call_kw[1].get("text")
    assert shown is not None and shown.startswith("Filing as:")
    assert "leads" in shown
