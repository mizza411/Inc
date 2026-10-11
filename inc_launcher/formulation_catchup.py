"""Tray-start formulation catch-up: sync, PR-fetch, then open pending packs.

Section 19 Phase 7.5 + 7.9.1 (fetch from formulation/auto-* when needed).
"""

from __future__ import annotations

import logging
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

from inc_launcher.config import INC_ROOT
from inc_launcher.formulation_docx_opener import OpenBatchResult, open_pending_packs
from inc_launcher.formulation_pr_fetch import FetchResult, fetch_today_formulation_pack
from inc_launcher.formulation_repo_sync import SyncResult, safe_pull_main

logger = logging.getLogger(__name__)


@dataclass
class CatchupResult:
    skipped: bool
    skip_reason: str = ""
    sync: Optional[SyncResult] = None
    fetch: Optional[FetchResult] = None
    open_batch: Optional[OpenBatchResult] = None


def run_formulation_catchup(
    repo_root: Optional[Path] = None,
    *,
    enabled: bool = True,
    sync_fn: Optional[Callable[..., SyncResult]] = None,
    fetch_fn: Optional[Callable[..., FetchResult]] = None,
    open_fn: Optional[Callable[..., OpenBatchResult]] = None,
) -> CatchupResult:
    """Safe pull of main, fetch today's pack from formulation PR if needed, open.

    Never raises.
    """
    if not enabled:
        logger.info("formulation catch-up skipped (disabled)")
        return CatchupResult(skipped=True, skip_reason="disabled")

    root = Path(repo_root or INC_ROOT)
    sync_impl = sync_fn or safe_pull_main
    fetch_impl = fetch_fn or fetch_today_formulation_pack
    open_impl = open_fn or open_pending_packs

    try:
        sync_result = sync_impl(root)
    except Exception as exc:  # noqa: BLE001
        logger.exception("formulation sync failed: %s", exc)
        sync_result = SyncResult(status="failed", detail=str(exc))

    try:
        fetch_result = fetch_impl(root)
    except Exception as exc:  # noqa: BLE001
        logger.exception("formulation pr fetch failed: %s", exc)
        fetch_result = FetchResult(status="failed", detail=str(exc))

    try:
        open_batch = open_impl(root)
    except Exception as exc:  # noqa: BLE001
        logger.exception("formulation open failed: %s", exc)
        open_batch = OpenBatchResult()

    logger.info(
        "formulation catch-up done sync=%s fetch=%s opened=%s failed=%s",
        sync_result.status,
        fetch_result.status,
        open_batch.opened_count,
        open_batch.failed_count,
    )
    return CatchupResult(
        skipped=False,
        sync=sync_result,
        fetch=fetch_result,
        open_batch=open_batch,
    )


def start_formulation_catchup_background(
    *,
    enabled: bool,
    repo_root: Optional[Path] = None,
) -> None:
    """Fire-and-forget catch-up so tray UI is not blocked."""

    def _worker() -> None:
        try:
            run_formulation_catchup(repo_root, enabled=enabled)
        except Exception as exc:  # noqa: BLE001
            logger.exception("formulation catch-up background failed: %s", exc)

    thread = threading.Thread(
        target=_worker,
        name="formulation-catchup",
        daemon=True,
    )
    thread.start()
