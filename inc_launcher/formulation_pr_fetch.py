"""Fetch today's formulation pack files from open formulation/auto-* branch (7.9.1).

Copies only ``agent-business-idea-runs/outputs/business_ideas_YYYYMMDD.{md,docx}``
via ``git show`` — never force-resets the working tree. Soft no-op when the
remote branch or files are missing. Skips overwrite when the local file is
newer than the remote blob commit time.
"""

from __future__ import annotations

import logging
import subprocess
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Callable, List, Optional, Tuple

from inc_launcher.config import INC_ROOT
from inc_launcher.formulation_pending import OUTPUTS_REL
from inc_launcher.formulation_repo_sync import (
    DEFAULT_REMOTE,
    LOG_PATH,
    GitRunner,
    _append_log,
    _default_runner,
    _run,
)

BRANCH_PREFIX = "formulation/auto-"

logger = logging.getLogger(__name__)

# cwd, ref, rel_posix -> (code, bytes, err_text)
BlobReader = Callable[[Path, str, str], Tuple[int, bytes, str]]


@dataclass(frozen=True)
class FetchResult:
    """Outcome of one formulation PR pack fetch attempt."""

    status: str
    detail: str
    date_key: str = ""
    branch: str = ""
    written: Tuple[str, ...] = field(default_factory=tuple)

    @property
    def ok_to_continue(self) -> bool:
        return True


def today_date_key(today: Optional[date] = None) -> str:
    return (today or date.today()).strftime("%Y%m%d")


def formulation_branch_name(date_key: str) -> str:
    return f"{BRANCH_PREFIX}{date_key}"


def pack_rel_paths(date_key: str) -> Tuple[Path, Path]:
    base = OUTPUTS_REL / f"business_ideas_{date_key}"
    return base.with_suffix(".md"), base.with_suffix(".docx")


def _remote_ref(remote: str, branch: str) -> str:
    return f"{remote}/{branch}"


def _default_blob_reader(cwd: Path, ref: str, rel_posix: str) -> Tuple[int, bytes, str]:
    completed = subprocess.run(
        ["git", "show", f"{ref}:{rel_posix}"],
        cwd=str(cwd),
        capture_output=True,
        check=False,
    )
    err = (completed.stderr or b"").decode("utf-8", errors="replace")
    return completed.returncode, completed.stdout or b"", err


def _parse_unix_ts(raw: str) -> Optional[int]:
    text = (raw or "").strip()
    if not text.isdigit():
        return None
    return int(text)


def _should_write_local(
    local_path: Path,
    remote_commit_ts: Optional[int],
) -> Tuple[bool, str]:
    if not local_path.is_file():
        return True, "missing"
    if local_path.stat().st_size == 0:
        return True, "empty"
    if remote_commit_ts is None:
        return False, "local_exists_no_remote_time"
    local_mtime = int(local_path.stat().st_mtime)
    if local_mtime > remote_commit_ts:
        return False, "local_newer"
    return True, "remote_same_or_newer"


def _fetch_miss_is_missing_branch(combined: str) -> bool:
    lowered = combined.lower()
    needles = (
        "couldn't find remote ref",
        "could not find remote ref",
        "does not exist",
        "not found",
        "no such ref",
    )
    return any(n in lowered for n in needles)


def fetch_today_formulation_pack(
    repo_root: Optional[Path] = None,
    *,
    date_key: Optional[str] = None,
    remote: str = DEFAULT_REMOTE,
    runner: Optional[GitRunner] = None,
    blob_reader: Optional[BlobReader] = None,
    log_path: Optional[Path] = None,
    today: Optional[date] = None,
) -> FetchResult:
    """Fetch today's pack files from ``origin/formulation/auto-YYYYMMDD`` if present."""
    root = Path(repo_root or INC_ROOT).resolve()
    run = runner or _default_runner
    read_blob = blob_reader or _default_blob_reader
    log_file = Path(log_path) if log_path is not None else LOG_PATH
    key = date_key or today_date_key(today)
    branch = formulation_branch_name(key)
    ref = _remote_ref(remote, branch)

    if not (root / ".git").exists():
        result = FetchResult(
            status="skipped_not_git",
            detail=f"No .git under {root}",
            date_key=key,
            branch=branch,
        )
        _append_log(log_file, f"pr_fetch {result.status}: {result.detail}")
        logger.info("pr_fetch %s - %s", result.status, result.detail)
        return result

    code, out, err = _run(run, root, ["git", "fetch", remote, branch])
    if code != 0:
        combined = f"{err or out}".strip()
        if _fetch_miss_is_missing_branch(combined):
            result = FetchResult(
                status="skipped_no_branch",
                detail=f"No remote branch {remote}/{branch}",
                date_key=key,
                branch=branch,
            )
        else:
            result = FetchResult(
                status="failed",
                detail=f"git fetch failed: {combined}",
                date_key=key,
                branch=branch,
            )
        _append_log(log_file, f"pr_fetch {result.status}: {result.detail}")
        logger.info("pr_fetch %s - %s", result.status, result.detail)
        return result

    written: List[str] = []
    skipped_reasons: List[str] = []

    for rel in pack_rel_paths(key):
        rel_posix = rel.as_posix()
        local_path = root / rel
        code, raw, show_err = read_blob(root, ref, rel_posix)
        if code != 0 or raw is None:
            skipped_reasons.append(f"{rel.name}: missing_on_remote")
            if show_err:
                logger.debug("pr_fetch show %s: %s", rel_posix, show_err.strip())
            continue

        code, ts_out, ts_err = _run(
            run,
            root,
            ["git", "log", "-1", "--format=%ct", ref, "--", rel_posix],
        )
        remote_ts = _parse_unix_ts(ts_out) if code == 0 else None
        if remote_ts is None and ts_err:
            logger.debug("pr_fetch no commit time for %s: %s", rel_posix, ts_err)

        ok_write, reason = _should_write_local(local_path, remote_ts)
        if not ok_write:
            skipped_reasons.append(f"{rel.name}:{reason}")
            continue

        try:
            local_path.parent.mkdir(parents=True, exist_ok=True)
            local_path.write_bytes(raw)
            written.append(rel.name)
        except OSError as exc:
            result = FetchResult(
                status="failed",
                detail=f"write failed for {rel.name}: {exc}",
                date_key=key,
                branch=branch,
                written=tuple(written),
            )
            _append_log(log_file, f"pr_fetch {result.status}: {result.detail}")
            logger.warning("pr_fetch %s - %s", result.status, result.detail)
            return result

    if written:
        result = FetchResult(
            status="fetched",
            detail=f"Wrote {', '.join(written)} from {ref}",
            date_key=key,
            branch=branch,
            written=tuple(written),
        )
    elif skipped_reasons and all("missing_on_remote" in s for s in skipped_reasons):
        result = FetchResult(
            status="skipped_no_files",
            detail=f"Branch {ref} has no pack files for {key}",
            date_key=key,
            branch=branch,
        )
    elif skipped_reasons:
        result = FetchResult(
            status="skipped_local_newer_or_present",
            detail="; ".join(skipped_reasons),
            date_key=key,
            branch=branch,
        )
    else:
        result = FetchResult(
            status="skipped_no_files",
            detail=f"Nothing to fetch from {ref}",
            date_key=key,
            branch=branch,
        )

    _append_log(log_file, f"pr_fetch {result.status}: {result.detail}")
    logger.info("pr_fetch %s - %s", result.status, result.detail)
    return result


def fetch_commands_for_tests() -> List[str]:
    return [
        "fetch origin formulation/auto-YYYYMMDD",
        "show origin/formulation/auto-YYYYMMDD:…/business_ideas_YYYYMMDD.md|.docx",
        "log -1 --format=%ct …",
    ]
