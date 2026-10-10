"""Open pending formulation .docx packs (task.md section 19 Phase 7.4).

Launches each unshown pack with the OS default handler (Word on Windows).
Marks shown only after a successful launch. Opens all pending (7.0 / 7.R4).
Tray wiring is Phase 7.5.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, List, Optional, Sequence

from inc_launcher.config import INC_ROOT, PACKAGE_DIR
from inc_launcher.formulation_pending import (
    PendingPack,
    list_pending_packs,
    mark_shown,
)

LOG_PATH = PACKAGE_DIR / "formulation_opener.log"
OpenFn = Callable[[Path], None]

logger = logging.getLogger(__name__)


@dataclass
class OpenAttempt:
    date_key: str
    path: Path
    opened: bool
    detail: str = ""


@dataclass
class OpenBatchResult:
    attempts: List[OpenAttempt] = field(default_factory=list)

    @property
    def opened_count(self) -> int:
        return sum(1 for a in self.attempts if a.opened)

    @property
    def failed_count(self) -> int:
        return sum(1 for a in self.attempts if not a.opened)


def _default_open(path: Path) -> None:
    if not path.is_file():
        raise FileNotFoundError(str(path))
    os.startfile(str(path))  # noqa: S606 — default .docx app (Word)


def _append_log(log_path: Path, line: str) -> None:
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(f"{stamp} {line}\n")
    except OSError as exc:
        logger.warning("Could not write opener log %s: %s", log_path, exc)


def open_pack_path(
    path: Path,
    *,
    open_fn: Optional[OpenFn] = None,
) -> None:
    """Open one .docx path. Raises on failure."""
    opener = open_fn or _default_open
    opener(Path(path))


def open_pending_packs(
    repo_root: Optional[Path] = None,
    *,
    state_path: Optional[Path] = None,
    outputs: Optional[Path] = None,
    packs: Optional[Sequence[PendingPack]] = None,
    open_fn: Optional[OpenFn] = None,
    log_path: Optional[Path] = None,
) -> OpenBatchResult:
    """Open all pending packs oldest-first. Mark shown only after success."""
    root = Path(repo_root or INC_ROOT)
    log_file = Path(log_path) if log_path is not None else LOG_PATH
    pending: List[PendingPack]
    if packs is not None:
        pending = list(packs)
    else:
        pending = list_pending_packs(
            root, state_path=state_path, outputs=outputs
        )

    result = OpenBatchResult()
    if not pending:
        _append_log(log_file, "no_pending: nothing to open")
        logger.info("formulation opener: no pending packs")
        return result

    for pack in pending:
        try:
            open_pack_path(pack.path, open_fn=open_fn)
            mark_shown(pack.date_key, state_path)
            attempt = OpenAttempt(
                date_key=pack.date_key,
                path=pack.path,
                opened=True,
                detail="opened and marked shown",
            )
            logger.info("Opened formulation pack %s", pack.path)
        except Exception as exc:  # noqa: BLE001 — soft-fail one pack, continue
            attempt = OpenAttempt(
                date_key=pack.date_key,
                path=pack.path,
                opened=False,
                detail=str(exc),
            )
            logger.warning(
                "Failed to open formulation pack %s: %s",
                pack.path,
                exc,
            )
        result.attempts.append(attempt)
        _append_log(
            log_file,
            f"{'opened' if attempt.opened else 'failed'} {pack.date_key} "
            f"{pack.path.name}: {attempt.detail}",
        )

    _append_log(
        log_file,
        f"batch_done opened={result.opened_count} failed={result.failed_count}",
    )
    return result
