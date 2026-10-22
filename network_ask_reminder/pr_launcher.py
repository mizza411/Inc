"""AUTO-NAR-04 — validate additive project_reminder launcher entry (no auto_launcher edit)."""

from __future__ import annotations

import json
from pathlib import Path

from .build_docx import PLAYBOOK_DOCX, MIN_DOCX_BYTES

LAUNCHER_KEY = "ask_people_ask_owners_playbook"
DEFAULT_PR_LAUNCHER = Path(r"C:\dev\project_reminder\launcher_config.json")


def expected_docx_path() -> Path:
    # Prefer stable C:\dev\Inc path when available (junction-friendly machines)
    preferred = Path(r"C:\dev\Inc\network_ask_reminder\ask_people_ask_owners_playbook.docx")
    if preferred.is_file():
        return preferred
    return PLAYBOOK_DOCX.resolve()


def validate_pr_launcher(config_path: Path | None = None) -> list[str]:
    """Return error strings; empty = pass."""
    errors: list[str] = []
    path = config_path or DEFAULT_PR_LAUNCHER
    if not path.is_file():
        return [f"launcher_config not found: {path}"]

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid JSON in {path}: {exc}"]

    apps = data.get("applications")
    if not isinstance(apps, dict):
        return ["applications must be an object"]

    entry = apps.get(LAUNCHER_KEY)
    if not isinstance(entry, dict):
        errors.append(f"missing applications.{LAUNCHER_KEY}")
        return errors

    if entry.get("is_document") is not True:
        errors.append(f"{LAUNCHER_KEY}.is_document must be true")
    if entry.get("enabled") is not True:
        errors.append(f"{LAUNCHER_KEY}.enabled must be true")

    raw_path = entry.get("path")
    if not isinstance(raw_path, str) or not raw_path.strip():
        errors.append(f"{LAUNCHER_KEY}.path missing")
    else:
        docx = Path(raw_path)
        if not docx.is_file():
            errors.append(f"docx path does not exist: {docx}")
        else:
            if docx.resolve() != expected_docx_path():
                # Allow same file via different path spelling if resolve matches fail on case
                if docx.name != PLAYBOOK_DOCX.name:
                    errors.append(f"path should point at {PLAYBOOK_DOCX.name}")
            if docx.stat().st_size < MIN_DOCX_BYTES:
                errors.append(f"docx too small: {docx}")

    # Regression anchors — unrelated keys still present
    for key in ("abuja_oldies_night_playbook", "agric_agrictech_ideas_ng"):
        if key not in apps:
            errors.append(f"regression: missing unrelated key {key}")

    return errors


def suggested_entry() -> dict:
    return {
        "path": str(expected_docx_path()),
        "enabled": True,
        "launch_delay": 2,
        "restart_on_crash": False,
        "is_document": True,
    }
