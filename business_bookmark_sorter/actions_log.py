"""Audit log for review actions (Phase 2)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from business_bookmark_sorter.paths import DATA_DIR

ACTIONS_PATH = DATA_DIR / "actions.log"


def log_action(event: Dict[str, Any]) -> None:
    ACTIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
    event = dict(event)
    event["at"] = datetime.now(timezone.utc).isoformat()
    with ACTIONS_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
