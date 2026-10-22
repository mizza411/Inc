"""AUTO-NAR-07 — last-asked / streak / next mode status."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from typing import Any

from .ask_log import read_asks
from .rotate import day_prompt

_DAY_KEYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


@dataclass(frozen=True)
class StatusReport:
    ask_count: int
    last_ts: str | None
    last_mode: str | None
    days_since_last: int | None
    streak_cadence_hits: int
    today_mode: str
    today_is_cadence: bool
    today_prompt: str


def _parse_ts(ts: str) -> datetime:
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    return datetime.fromisoformat(ts)


def _ask_date(row: dict[str, Any]) -> date | None:
    ts = row.get("ts")
    if not isinstance(ts, str):
        return None
    try:
        return _parse_ts(ts).astimezone(timezone.utc).date()
    except ValueError:
        return None


def _streak_cadence_hits(
    cadence_days: set[str],
    asked_dates: set[date],
    today: date,
) -> int:
    """Count consecutive past cadence days (skipping unfinished today) with a log."""
    streak = 0
    cursor = today
    for _ in range(120):
        key = _DAY_KEYS[cursor.weekday()]
        if key in cadence_days:
            if cursor == today and cursor not in asked_dates:
                cursor -= timedelta(days=1)
                continue
            if cursor in asked_dates:
                streak += 1
            else:
                break
        cursor -= timedelta(days=1)
    return streak


def compute_status(
    cfg: dict[str, Any],
    *,
    today: date | None = None,
    log_path=None,
) -> StatusReport:
    when = today or date.today()
    rows = read_asks(cfg, log_path)
    last_ts = None
    last_mode = None
    days_since = None
    if rows:
        last = rows[-1]
        last_ts = last.get("ts") if isinstance(last.get("ts"), str) else None
        last_mode = last.get("mode") if isinstance(last.get("mode"), str) else None
        last_d = _ask_date(last)
        if last_d is not None:
            days_since = (when - last_d).days

    asked_dates = {d for d in (_ask_date(r) for r in rows) if d is not None}
    streak = _streak_cadence_hits(set(cfg["cadence"]["days"]), asked_dates, when)
    dp = day_prompt(cfg, when)
    return StatusReport(
        ask_count=len(rows),
        last_ts=last_ts,
        last_mode=last_mode,
        days_since_last=days_since,
        streak_cadence_hits=streak,
        today_mode=dp.mode,
        today_is_cadence=dp.is_cadence_day,
        today_prompt=dp.prompt_text,
    )


def format_status(report: StatusReport) -> str:
    return "\n".join(
        [
            f"asks_logged: {report.ask_count}",
            f"last_ts: {report.last_ts or '(none)'}",
            f"last_mode: {report.last_mode or '(none)'}",
            f"days_since_last: {report.days_since_last if report.days_since_last is not None else '(n/a)'}",
            f"streak_cadence_hits: {report.streak_cadence_hits}",
            f"today_mode: {report.today_mode}",
            f"today_is_cadence_day: {report.today_is_cadence}",
            f"today_prompt: {report.today_prompt}",
        ]
    )
