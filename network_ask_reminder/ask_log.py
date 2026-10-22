"""AUTO-NAR-06 — append-only ask capture log (JSONL)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .paths import DATA_DIR, DEFAULT_LOG, PACKAGE_DIR


def resolve_log_path(cfg: dict[str, Any], override: Path | None = None) -> Path:
    if override is not None:
        return override
    rel = cfg["capture"]["log_path"]
    path = Path(rel)
    if not path.is_absolute():
        path = PACKAGE_DIR / path
    return path


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def append_ask(
    cfg: dict[str, Any],
    *,
    mode: str,
    notes: str,
    role: str = "",
    log_path: Path | None = None,
    when: datetime | None = None,
) -> dict[str, Any]:
    mode_n = mode.strip().lower()
    if mode_n not in ("s3", "s4"):
        raise ValueError("mode must be s3 or s4")
    notes_n = (notes or "").strip()
    if not notes_n:
        raise ValueError("notes must be non-empty")

    path = resolve_log_path(cfg, log_path)
    ensure_parent(path)
    stamp = when or datetime.now(timezone.utc)
    row = {
        "ts": stamp.isoformat(),
        "mode": mode_n,
        "role": (role or "").strip(),
        "notes": notes_n,
    }
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def read_asks(cfg: dict[str, Any], log_path: Path | None = None) -> list[dict[str, Any]]:
    path = resolve_log_path(cfg, log_path)
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def default_log_path() -> Path:
    return DEFAULT_LOG
