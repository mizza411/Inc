"""BB-TIMED-1 Phase 1.2 — Settings dialog helpers (no live display required)."""

from __future__ import annotations

from business_bookmark_sorter.session_settings import (
    MAX_SESSION_MINUTES,
    MIN_SESSION_MINUTES,
    SessionSettings,
    save_session_settings,
)
from business_bookmark_sorter.session_settings_ui import parse_minutes_input


def test_parse_minutes_input():
    assert parse_minutes_input("15") == 15
    assert parse_minutes_input(" 20 ") == 20
    assert parse_minutes_input("abc") is None
    assert parse_minutes_input("") is None


def test_apply_path_clamps_via_save(tmp_path, monkeypatch):
    path = tmp_path / "session_settings.json"
    monkeypatch.setattr(
        "business_bookmark_sorter.session_settings.SESSION_SETTINGS_PATH",
        path,
    )
    # Dialog Apply uses save_session_settings — clamp high
    saved = save_session_settings(
        SessionSettings(session_minutes=999, auto_open_links=True),
        path=path,
    )
    assert saved.session_minutes == MAX_SESSION_MINUTES
    saved_low = save_session_settings(
        SessionSettings(session_minutes=0, auto_open_links=False),
        path=path,
    )
    assert saved_low.session_minutes == MIN_SESSION_MINUTES
    assert saved_low.auto_open_links is False
