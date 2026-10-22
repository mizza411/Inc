"""AUTO-NAR-02 — deterministic S3 / S4 / both prompt selection."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Literal

Mode = Literal["s3", "s4", "both"]

_WEEKDAY_TO_KEY = {
    0: "mon",
    1: "tue",
    2: "wed",
    3: "thu",
    4: "fri",
    5: "sat",
    6: "sun",
}


@dataclass(frozen=True)
class DayPrompt:
    mode: Mode
    is_cadence_day: bool
    prompt_text: str
    day_key: str


def day_key_for(d: date) -> str:
    return _WEEKDAY_TO_KEY[d.weekday()]


def is_cadence_day(cfg: dict[str, Any], d: date) -> bool:
    return day_key_for(d) in cfg["cadence"]["days"]


def select_mode(cfg: dict[str, Any], d: date) -> Mode:
    rotate = cfg["rotate_mode"]
    if rotate == "both":
        return "both"
    if rotate == "s3_only":
        return "s3"
    if rotate == "s4_only":
        return "s4"

    # alternate_s3_s4: index among cadence days in the ISO week → even s3, odd s4
    days: list[str] = cfg["cadence"]["days"]
    key = day_key_for(d)
    if key not in days:
        # Off-cadence: still pick next alternate by weekday order for status previews
        ordered = sorted(range(7), key=lambda i: _WEEKDAY_TO_KEY[i])
        # Fall back: use weekday index parity
        return "s3" if d.weekday() % 2 == 0 else "s4"
    idx = days.index(key)
    # Stable across weeks: fold ISO week number so Mon of week N flips vs week N+1
    iso_week = d.isocalendar()[1]
    slot = (iso_week + idx) % 2
    return "s3" if slot == 0 else "s4"


def prompt_for_mode(cfg: dict[str, Any], mode: Mode) -> str:
    prompts = cfg["prompts"]
    if mode == "s3":
        return prompts["s3"]
    if mode == "s4":
        return prompts["s4"]
    return f"[S3] {prompts['s3']}\n[S4] {prompts['s4']}"


def day_prompt(cfg: dict[str, Any], d: date | None = None) -> DayPrompt:
    when = d or date.today()
    mode = select_mode(cfg, when)
    return DayPrompt(
        mode=mode,
        is_cadence_day=is_cadence_day(cfg, when),
        prompt_text=prompt_for_mode(cfg, mode),
        day_key=day_key_for(when),
    )


def parse_date(s: str | None) -> date:
    if not s:
        return date.today()
    return datetime.strptime(s, "%Y-%m-%d").date()
