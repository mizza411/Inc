"""BB-TIMED-1 Phase 1.1 — session_settings load/save/clamp."""

from __future__ import annotations

import json

from business_bookmark_sorter.session_settings import (
    DEFAULT_SESSION_MINUTES,
    MAX_SESSION_MINUTES,
    MIN_SESSION_MINUTES,
    SessionSettings,
    default_settings,
    load_session_settings,
    save_session_settings,
)


def test_defaults():
    s = default_settings()
    assert s.session_minutes == DEFAULT_SESSION_MINUTES
    assert s.auto_open_links is True


def test_clamp_low_and_high():
    assert SessionSettings(session_minutes=0).clamped().session_minutes == MIN_SESSION_MINUTES
    assert (
        SessionSettings(session_minutes=999).clamped().session_minutes == MAX_SESSION_MINUTES
    )


def test_save_load_roundtrip(tmp_path):
    path = tmp_path / "session_settings.json"
    written = save_session_settings(
        SessionSettings(session_minutes=20, auto_open_links=False),
        path=path,
    )
    assert written.session_minutes == 20
    assert written.auto_open_links is False
    loaded = load_session_settings(path)
    assert loaded.session_minutes == 20
    assert loaded.auto_open_links is False


def test_missing_file_returns_defaults(tmp_path):
    path = tmp_path / "missing.json"
    loaded = load_session_settings(path)
    assert loaded.session_minutes == DEFAULT_SESSION_MINUTES
    assert loaded.auto_open_links is True


def test_corrupt_json_returns_defaults(tmp_path):
    path = tmp_path / "session_settings.json"
    path.write_text("{not-json", encoding="utf-8")
    loaded = load_session_settings(path)
    assert loaded.session_minutes == DEFAULT_SESSION_MINUTES


def test_invalid_minutes_clamped_on_load(tmp_path):
    path = tmp_path / "session_settings.json"
    path.write_text(
        json.dumps({"version": 1, "session_minutes": -5, "auto_open_links": True}),
        encoding="utf-8",
    )
    loaded = load_session_settings(path)
    assert loaded.session_minutes == MIN_SESSION_MINUTES


def test_rejects_bookmark_like_payload(tmp_path):
    path = tmp_path / "session_settings.json"
    path.write_text(
        json.dumps(
            {
                "session_minutes": 30,
                "url": "https://example.com/secret",
                "bookmarks": [],
            }
        ),
        encoding="utf-8",
    )
    loaded = load_session_settings(path)
    assert loaded.session_minutes == DEFAULT_SESSION_MINUTES
