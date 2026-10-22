"""AUTO-NAR-01 — load and validate cadence config."""

from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any

from .paths import CONFIG_EXAMPLE, CONFIG_LOCAL

VALID_DAYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
VALID_ROTATE = (
    "alternate_s3_s4",
    "both",
    "s3_only",
    "s4_only",
)
TIME_RE = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")


class ConfigError(ValueError):
    """Invalid network_ask_reminder config."""


def resolve_config_path(override: Path | None = None) -> Path:
    if override is not None:
        return override
    if CONFIG_LOCAL.is_file():
        return CONFIG_LOCAL
    return CONFIG_EXAMPLE


def load_raw(path: Path | None = None) -> dict[str, Any]:
    cfg_path = resolve_config_path(path)
    if not cfg_path.is_file():
        raise ConfigError(f"Config not found: {cfg_path}")
    with cfg_path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ConfigError("Config root must be a JSON object")
    return data


def validate_config(data: dict[str, Any]) -> dict[str, Any]:
    """Return a normalized deep copy or raise ConfigError."""
    cfg = deepcopy(data)

    if cfg.get("version") != 1:
        raise ConfigError("version must be 1")

    tz = cfg.get("timezone")
    if not isinstance(tz, str) or not tz.strip():
        raise ConfigError("timezone must be a non-empty string")

    cadence = cfg.get("cadence")
    if not isinstance(cadence, dict):
        raise ConfigError("cadence must be an object")
    days = cadence.get("days")
    if not isinstance(days, list) or not days:
        raise ConfigError("cadence.days must be a non-empty list")
    norm_days: list[str] = []
    for d in days:
        if not isinstance(d, str):
            raise ConfigError("cadence.days entries must be strings")
        key = d.strip().lower()[:3]
        if key not in VALID_DAYS:
            raise ConfigError(f"invalid day: {d!r}")
        if key not in norm_days:
            norm_days.append(key)
    cadence["days"] = norm_days

    local_time = cadence.get("local_time")
    if not isinstance(local_time, str) or not TIME_RE.match(local_time):
        raise ConfigError("cadence.local_time must be HH:MM (24h)")

    rotate = cfg.get("rotate_mode")
    if rotate not in VALID_ROTATE:
        raise ConfigError(f"rotate_mode must be one of {VALID_ROTATE}")

    surfaces = cfg.get("surfaces")
    if not isinstance(surfaces, dict):
        raise ConfigError("surfaces must be an object")
    for key in ("inc_hub", "project_reminder_docx", "task_reminder_seed"):
        if key not in surfaces or not isinstance(surfaces[key], bool):
            raise ConfigError(f"surfaces.{key} must be a boolean")

    quiet = cfg.get("quiet_hours")
    if not isinstance(quiet, dict):
        raise ConfigError("quiet_hours must be an object")
    for key in ("start", "end"):
        val = quiet.get(key)
        if not isinstance(val, str) or not TIME_RE.match(val):
            raise ConfigError(f"quiet_hours.{key} must be HH:MM")

    prompts = cfg.get("prompts")
    if not isinstance(prompts, dict):
        raise ConfigError("prompts must be an object")
    for key in ("s3", "s4"):
        val = prompts.get(key)
        if not isinstance(val, str) or not val.strip():
            raise ConfigError(f"prompts.{key} must be a non-empty string")

    capture = cfg.get("capture")
    if not isinstance(capture, dict):
        raise ConfigError("capture must be an object")
    log_path = capture.get("log_path")
    if not isinstance(log_path, str) or not log_path.strip():
        raise ConfigError("capture.log_path must be a non-empty string")
    pointers = capture.get("pointers")
    if not isinstance(pointers, dict):
        raise ConfigError("capture.pointers must be an object")
    for key in ("strategy3", "strategy4", "problem_id"):
        val = pointers.get(key)
        if not isinstance(val, str) or not val.strip():
            raise ConfigError(f"capture.pointers.{key} must be a non-empty string")

    return cfg


def load_config(path: Path | None = None) -> dict[str, Any]:
    return validate_config(load_raw(path))
