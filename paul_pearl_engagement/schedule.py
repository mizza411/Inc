"""Schedule bundle for Paul Pearl engagement — offer_lines.docx only."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Optional

from schedule_core import ScheduleConfig

CONFIG_FILENAME = "paul_pearl_schedule_config.json"
DEFAULT_SLOTS = ("10:00", "17:00")


@dataclass
class PaulPearlScheduleBundle:
    schedule: ScheduleConfig
    scheduled_open_docx: bool = True
    startup_open_docx: bool = True


def config_path(base_dir: Optional[str] = None) -> str:
    root = base_dir or os.path.dirname(os.path.abspath(__file__))
    return os.path.join(root, CONFIG_FILENAME)


def _bundle_from_dict(data: dict) -> PaulPearlScheduleBundle:
    return PaulPearlScheduleBundle(
        schedule=ScheduleConfig.from_dict(data),
        scheduled_open_docx=bool(data.get("scheduled_open_docx", True)),
        startup_open_docx=bool(data.get("startup_open_docx", True)),
    )


def load_schedule_bundle(base_dir: Optional[str] = None) -> PaulPearlScheduleBundle:
    path = config_path(base_dir)
    defaults = PaulPearlScheduleBundle(
        schedule=ScheduleConfig(
            slots=DEFAULT_SLOTS,
            show_window_on_scheduled=False,
            require_internet_for_scheduled=False,
            minimize_to_tray_after_scheduled=False,
        ),
    )
    if not os.path.isfile(path):
        return defaults
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return _bundle_from_dict(data)
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        pass
    return defaults


def scheduled_skip_message(
    slot: str,
    reason: str,
    *,
    cooldown_minutes: Optional[int] = None,
    remaining_seconds: Optional[int] = None,
) -> str:
    if reason == "busy":
        return f"Skipped Paul Pearl/Upstream Drive open {slot} — busy."
    if reason == "cooldown":
        mins = cooldown_minutes if cooldown_minutes is not None else "?"
        secs = remaining_seconds if remaining_seconds is not None else "?"
        return (
            f"Skipped Paul Pearl/Upstream Drive open {slot} — "
            f"cooldown ({mins}m, ~{secs}s left)."
        )
    if reason == "offline":
        return f"Skipped Paul Pearl/Upstream Drive open {slot} — offline."
    return f"Skipped Paul Pearl/Upstream Drive open {slot} — {reason}."
