"""Pending formulation Word packs vs shown-ledger (task.md section 19 Phase 7.3).

Diffs on-disk ``business_ideas_YYYYMMDD.docx`` files against a local shown
ledger. Returns oldest-first pending paths. No fixed day lookback window.
Mark-shown helpers are here for 7.4, but opener wiring stays Phase 7.4/7.5.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List, Optional, Set

from inc_launcher.config import INC_ROOT, PACKAGE_DIR

OUTPUTS_REL = Path("agent-business-idea-runs") / "outputs"
DOCX_NAME_RE = re.compile(r"^business_ideas_(\d{8})\.docx$", re.IGNORECASE)
SHOWN_STATE_PATH = PACKAGE_DIR / "formulation_shown_state.json"

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PendingPack:
    """One unshown formulation .docx on disk."""

    date_key: str
    path: Path

    @property
    def filename(self) -> str:
        return self.path.name


def outputs_dir(repo_root: Optional[Path] = None) -> Path:
    root = Path(repo_root or INC_ROOT).resolve()
    return root / OUTPUTS_REL


def parse_date_key(path: Path) -> Optional[str]:
    match = DOCX_NAME_RE.match(path.name)
    return match.group(1) if match else None


def list_pack_docx(outputs: Path) -> List[PendingPack]:
    """All matching .docx under outputs, oldest date first."""
    if not outputs.is_dir():
        return []
    found: List[PendingPack] = []
    for path in outputs.iterdir():
        if not path.is_file():
            continue
        date_key = parse_date_key(path)
        if date_key is None:
            continue
        found.append(PendingPack(date_key=date_key, path=path.resolve()))
    found.sort(key=lambda p: p.date_key)
    return found


def load_shown_keys(state_path: Optional[Path] = None) -> Set[str]:
    path = Path(state_path or SHOWN_STATE_PATH)
    if not path.is_file():
        return set()
    try:
        with path.open(encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError, TypeError):
        logger.warning("Could not read shown-state %s — treating as empty", path)
        return set()
    shown = data.get("shown", [])
    if not isinstance(shown, list):
        return set()
    keys: Set[str] = set()
    for item in shown:
        if isinstance(item, str) and DOCX_NAME_RE.match(f"business_ideas_{item}.docx"):
            keys.add(item)
        elif isinstance(item, dict):
            key = item.get("date_key") or item.get("date")
            if isinstance(key, str) and re.fullmatch(r"\d{8}", key):
                keys.add(key)
    return keys


def save_shown_keys(keys: Iterable[str], state_path: Optional[Path] = None) -> None:
    path = Path(state_path or SHOWN_STATE_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    unique = sorted({k for k in keys if re.fullmatch(r"\d{8}", k)})
    payload = {
        "shown": unique,
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    with path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")


def mark_shown(date_key: str, state_path: Optional[Path] = None) -> Set[str]:
    """Record one pack as shown. Returns the full shown set afterward."""
    if not re.fullmatch(r"\d{8}", date_key):
        raise ValueError(f"Invalid date_key: {date_key!r}")
    keys = load_shown_keys(state_path)
    keys.add(date_key)
    save_shown_keys(keys, state_path)
    return keys


def list_pending_packs(
    repo_root: Optional[Path] = None,
    *,
    state_path: Optional[Path] = None,
    outputs: Optional[Path] = None,
) -> List[PendingPack]:
    """Packs on disk not yet in the shown ledger, oldest first."""
    out_dir = Path(outputs) if outputs is not None else outputs_dir(repo_root)
    shown = load_shown_keys(state_path)
    pending = [p for p in list_pack_docx(out_dir) if p.date_key not in shown]
    logger.info(
        "formulation pending: %s (shown ledger size %s)",
        len(pending),
        len(shown),
    )
    return pending


def pending_count(
    repo_root: Optional[Path] = None,
    *,
    state_path: Optional[Path] = None,
    outputs: Optional[Path] = None,
) -> int:
    return len(
        list_pending_packs(repo_root, state_path=state_path, outputs=outputs)
    )
