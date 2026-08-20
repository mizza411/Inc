"""Local session settings for timed bookmark review (BB-TIMED-1).

Persisted under data/ (gitignored). User changes these via the review Settings UI —
never by hand-editing JSON. No Chrome URLs or bookmark titles are stored here.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from business_bookmark_sorter.paths import SESSION_SETTINGS_PATH

DEFAULT_SESSION_MINUTES = 15
MIN_SESSION_MINUTES = 1
MAX_SESSION_MINUTES = 180
DEFAULT_AUTO_OPEN = True


@dataclass
class SessionSettings:
    """Review-session preferences (duration + future toggles)."""

    session_minutes: int = DEFAULT_SESSION_MINUTES
    auto_open_links: bool = DEFAULT_AUTO_OPEN

    def clamped(self) -> "SessionSettings":
        minutes = int(self.session_minutes)
        if minutes < MIN_SESSION_MINUTES:
            minutes = MIN_SESSION_MINUTES
        elif minutes > MAX_SESSION_MINUTES:
            minutes = MAX_SESSION_MINUTES
        return SessionSettings(
            session_minutes=minutes,
            auto_open_links=bool(self.auto_open_links),
        )


def default_settings() -> SessionSettings:
    return SessionSettings().clamped()


def _from_dict(raw: Dict[str, Any]) -> SessionSettings:
    minutes = raw.get("session_minutes", DEFAULT_SESSION_MINUTES)
    try:
        minutes_int = int(minutes)
    except (TypeError, ValueError):
        minutes_int = DEFAULT_SESSION_MINUTES
    auto_open = raw.get("auto_open_links", DEFAULT_AUTO_OPEN)
    if not isinstance(auto_open, bool):
        auto_open = bool(auto_open)
    return SessionSettings(
        session_minutes=minutes_int,
        auto_open_links=auto_open,
    ).clamped()


def load_session_settings(path: Optional[Path] = None) -> SessionSettings:
    """Load settings from disk, or defaults if missing/corrupt."""
    p = path or SESSION_SETTINGS_PATH
    if not p.is_file():
        return default_settings()
    try:
        with p.open(encoding="utf-8") as f:
            raw = json.load(f)
    except (OSError, json.JSONDecodeError):
        return default_settings()
    if not isinstance(raw, dict):
        return default_settings()
    # Reject accidental bookmark dumps — settings must stay small prefs only
    forbidden = ("url", "urls", "bookmarks", "items", "chrome")
    if any(k in raw for k in forbidden):
        return default_settings()
    return _from_dict(raw)


def save_session_settings(
    settings: SessionSettings,
    path: Optional[Path] = None,
) -> SessionSettings:
    """Write clamped settings to disk. Returns what was written."""
    p = path or SESSION_SETTINGS_PATH
    clean = settings.clamped()
    p.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": 1,
        **asdict(clean),
    }
    with p.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return clean
