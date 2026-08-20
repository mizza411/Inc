"""BB-TIMED-1 v1 automated sign-off — covers former MANUAL §§I–L + config M/N.

No live owner clicks. Fake clock / mocks / config reads only.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from business_bookmark_sorter.auto_open import LinkAutoOpener
from business_bookmark_sorter.paths import INC_ROOT, SESSION_SETTINGS_PATH
from business_bookmark_sorter.queue_store import load_routes_config
from business_bookmark_sorter.review_ui import ReviewPanel
from business_bookmark_sorter.session_settings import (
    SessionSettings,
    load_session_settings,
    save_session_settings,
)
from business_bookmark_sorter.session_timer import SessionTimer, format_remaining
from inc_launcher.config import load_config
from inc_launcher.scheduled_nudges import (
    day_name,
    entries_due_now,
    load_schedule_settings,
    resolve_schedule_target,
)
from datetime import datetime

CONFIG = Path(__file__).resolve().parent.parent / "config" / "routes.json"
PR_CONFIG = Path(r"C:\dev\project_reminder\launcher_config.json")


class FakeClock:
    def __init__(self, start: float = 0.0) -> None:
        self.t = start

    def __call__(self) -> float:
        return self.t

    def advance(self, seconds: float) -> None:
        self.t += seconds


def _panel() -> ReviewPanel:
    root = MagicMock()
    root.focus_get.return_value = None
    panel = ReviewPanel.__new__(ReviewPanel)
    panel.root = root
    panel.config = load_routes_config(CONFIG)
    panel.dest_ids = ["leads", "other"]
    panel._last_sync = ""
    panel._toast_frame = None
    panel._toast_timer = None
    panel._tick_job = None
    panel._session_settings = SessionSettings(session_minutes=1, auto_open_links=True)
    panel._auto_opener = LinkAutoOpener(open_url=lambda _u: None)
    panel._skip_removal_prompt = False
    panel._session_ended = False
    clock = FakeClock()
    panel._timer = SessionTimer(60, clock=clock)
    panel._fake_clock = clock
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


# --- §I Settings (UI Apply path = save_session_settings) ---


def test_signoff_I_settings_roundtrip(tmp_path, monkeypatch):
    path = tmp_path / "session_settings.json"
    monkeypatch.setattr(
        "business_bookmark_sorter.session_settings.SESSION_SETTINGS_PATH",
        path,
    )
    save_session_settings(SessionSettings(session_minutes=2, auto_open_links=False))
    loaded = load_session_settings()
    assert loaded.session_minutes == 2
    assert loaded.auto_open_links is False
    raw = json.loads(path.read_text(encoding="utf-8"))
    assert "url" not in raw and "bookmarks" not in raw


# --- §J Timer stop-nagging ---


def test_signoff_J_timer_blocks_advance_after_expiry():
    panel = _panel()
    panel._timer.start()
    panel._fake_clock.advance(61)
    assert panel._timer.is_expired()
    with patch.object(panel, "_update_timer_label"):
        assert panel._session_allows_advance() is False
    assert panel._session_ended is True


def test_signoff_J_extend_allows_advance_again():
    panel = _panel()
    panel._timer.start()
    panel._fake_clock.advance(61)
    panel._session_ended = True
    with patch.object(panel, "_update_timer_label"), patch.object(
        panel, "_schedule_tick"
    ):
        panel._extend_session()
    assert panel._session_ended is False
    assert not panel._timer.is_expired()
    assert panel._session_allows_advance() is True


def test_signoff_J_format_remaining_readable():
    assert format_remaining(90) == "1:30"


# --- §K Auto-open ---


def test_signoff_K_auto_open_one_url_per_id():
    opened: list[str] = []
    opener = LinkAutoOpener(open_url=opened.append)
    assert opener.maybe_open(item_id="1", url="https://a.example", enabled=True)
    assert opener.maybe_open(item_id="1", url="https://a.example", enabled=True) is False
    assert opened == ["https://a.example"]


def test_signoff_K_auto_open_off():
    opened: list[str] = []
    opener = LinkAutoOpener(open_url=opened.append)
    assert opener.maybe_open(item_id="2", url="https://b.example", enabled=False) is False
    assert opened == []


def test_signoff_K_display_calls_auto_open_when_pending():
    panel = _panel()
    opened: list[str] = []
    panel._auto_opener = LinkAutoOpener(open_url=opened.append)
    panel._session_settings = SessionSettings(session_minutes=15, auto_open_links=True)
    item = {
        "id": "item-k",
        "type": "url",
        "title": "T",
        "url": "https://k.example",
        "folder_path": "",
        "status": "pending",
        "suggested_destination": "other",
        "suggested_reason": "none",
    }
    panel._display_item(item)
    assert opened == ["https://k.example"]
    panel._display_item(item)
    assert opened == ["https://k.example"]


# --- §L Minimal confirm ---


def test_signoff_L_enter_files_when_not_in_entry():
    panel = _panel()
    panel.root.focus_get = MagicMock(return_value=None)  # type: ignore[method-assign]
    filed = MagicMock()
    panel._file_and_open = filed  # type: ignore[method-assign]
    assert panel._on_enter_file() == "break"
    filed.assert_called_once()


def test_signoff_L_enter_skipped_when_focus_on_entry():
    """Settings/spinboxes still swallow Enter; Assign Combobox is gone (Phase 1)."""
    panel = _panel()
    focus = MagicMock()
    focus.winfo_class.return_value = "TEntry"
    panel.root.focus_get = MagicMock(return_value=focus)  # type: ignore[method-assign]
    filed = MagicMock()
    panel._file_and_open = filed  # type: ignore[method-assign]
    assert panel._on_enter_file() == ""
    filed.assert_not_called()


def test_signoff_L_enter_files_even_if_legacy_combobox_focus():
    """No Assign combo — Enter files even if focus class were TCombobox."""
    panel = _panel()
    focus = MagicMock()
    focus.winfo_class.return_value = "TCombobox"
    panel.root.focus_get = MagicMock(return_value=focus)  # type: ignore[method-assign]
    filed = MagicMock()
    panel._file_and_open = filed  # type: ignore[method-assign]
    assert panel._on_enter_file() == "break"
    filed.assert_called_once()


def test_signoff_L_removal_dont_ask_again():
    panel = _panel()
    with patch(
        "business_bookmark_sorter.review_ui.ask_bookmark_removed_dialog",
        return_value=(True, True),
    ):
        assert panel._ask_bookmark_removed("x") is True
    assert panel._skip_removal_prompt is True
    with patch(
        "business_bookmark_sorter.review_ui.ask_bookmark_removed_dialog"
    ) as ask:
        assert panel._ask_bookmark_removed("y") is True
        ask.assert_not_called()


# --- §M schedule config (clock fire needs live tray — config proven here) ---


def test_signoff_M_weekday_1100_targets_bookmark_review():
    config = load_config()
    settings = load_schedule_settings(config)
    entry = next(e for e in settings.entries if e.id == "bookmark_review_weekdays")
    assert entry.hour == 11 and entry.minute == 0
    assert entry.target == "bookmark_review"
    resolved = resolve_schedule_target(config, "bookmark_review")
    assert resolved is not None
    assert "business_bookmark_sorter review" in resolved["command"]
    monday = datetime(2026, 6, 1, 11, 0)
    assert day_name(monday) == "mon"
    due = entries_due_now(settings, {**config, "schedules": {**config["schedules"], "enabled": True}}, monday, set())
    assert [e.id for e in due] == ["bookmark_review_weekdays"]


# --- §N PR boot config ---


def test_signoff_N_pr_boot_application_entry():
    data = json.loads(PR_CONFIG.read_text(encoding="utf-8"))
    entry = data["applications"]["inc_business_bookmark_review"]
    assert entry["enabled"] is True
    assert "business_bookmark_sorter review" in entry["arguments"]
    assert Path(entry["working_dir"]).resolve() == INC_ROOT.resolve()
    assert "bookmark_sorter" in data["scripts"]


def test_signoff_process_smoke_cli_help():
    import subprocess
    import sys

    result = subprocess.run(
        [sys.executable, "-m", "business_bookmark_sorter", "--help"],
        cwd=str(INC_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "review" in result.stdout
