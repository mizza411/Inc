"""Safe git sync of Inc main for formulation pack catch-up (task.md section 19 Phase 7.2).

Pulls origin/main with ff-only when the working tree is clean. Soft-skips on dirty
tree, wrong branch, or pull conflict. Never force-resets. Tray wiring is Phase 7.5.
"""

from __future__ import annotations

import logging
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, List, Optional, Sequence, Tuple

from inc_launcher.config import INC_ROOT, PACKAGE_DIR

DEFAULT_BRANCH = "main"
DEFAULT_REMOTE = "origin"
LOG_PATH = PACKAGE_DIR / "formulation_sync.log"

GitRunner = Callable[[Sequence[str], Path], Tuple[int, str, str]]

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SyncResult:
    """Outcome of one safe_pull_main attempt."""

    status: str
    detail: str
    branch: str = DEFAULT_BRANCH

    @property
    def ok_to_continue(self) -> bool:
        """Always True — sync never raises. Callers may open local packs after any status."""
        return True


def _default_runner(args: Sequence[str], cwd: Path) -> Tuple[int, str, str]:
    completed = subprocess.run(
        list(args),
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    return completed.returncode, completed.stdout or "", completed.stderr or ""


def _append_log(log_path: Path, line: str) -> None:
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(f"{stamp} {line}\n")
    except OSError as exc:
        logger.warning("Could not write sync log %s: %s", log_path, exc)


def _run(
    runner: GitRunner,
    cwd: Path,
    args: Sequence[str],
) -> Tuple[int, str, str]:
    return runner(args, cwd)


def safe_pull_main(
    repo_root: Optional[Path] = None,
    *,
    branch: str = DEFAULT_BRANCH,
    remote: str = DEFAULT_REMOTE,
    runner: Optional[GitRunner] = None,
    log_path: Optional[Path] = None,
) -> SyncResult:
    """Fetch and fast-forward pull ``remote/branch`` when safe.

    Soft outcomes (no exception): skipped_dirty, skipped_wrong_branch,
    skipped_not_git, failed (non-zero git). Never ``git reset --hard``.
    """
    root = Path(repo_root or INC_ROOT).resolve()
    run = runner or _default_runner
    log_file = Path(log_path) if log_path is not None else LOG_PATH

    if not (root / ".git").exists():
        result = SyncResult(
            status="skipped_not_git",
            detail=f"No .git under {root}",
            branch=branch,
        )
        _append_log(log_file, f"{result.status}: {result.detail}")
        logger.info("%s — %s", result.status, result.detail)
        return result

    code, out, err = _run(run, root, ["git", "status", "--porcelain"])
    if code != 0:
        result = SyncResult(
            status="failed",
            detail=f"git status failed: {(err or out).strip()}",
            branch=branch,
        )
        _append_log(log_file, f"{result.status}: {result.detail}")
        logger.warning("%s — %s", result.status, result.detail)
        return result

    if out.strip():
        result = SyncResult(
            status="skipped_dirty",
            detail="Working tree not clean — pull skipped (no force)",
            branch=branch,
        )
        _append_log(log_file, f"{result.status}: {result.detail}")
        logger.info("%s — %s", result.status, result.detail)
        return result

    code, out, err = _run(run, root, ["git", "rev-parse", "--abbrev-ref", "HEAD"])
    if code != 0:
        result = SyncResult(
            status="failed",
            detail=f"git rev-parse failed: {(err or out).strip()}",
            branch=branch,
        )
        _append_log(log_file, f"{result.status}: {result.detail}")
        logger.warning("%s — %s", result.status, result.detail)
        return result

    current = (out or "").strip()
    if current != branch:
        result = SyncResult(
            status="skipped_wrong_branch",
            detail=f"On '{current}', need '{branch}' — pull skipped",
            branch=branch,
        )
        _append_log(log_file, f"{result.status}: {result.detail}")
        logger.info("%s — %s", result.status, result.detail)
        return result

    code, out, err = _run(run, root, ["git", "fetch", remote, branch])
    if code != 0:
        result = SyncResult(
            status="failed",
            detail=f"git fetch failed: {(err or out).strip()}",
            branch=branch,
        )
        _append_log(log_file, f"{result.status}: {result.detail}")
        logger.warning("%s — %s", result.status, result.detail)
        return result

    code, out, err = _run(
        run,
        root,
        ["git", "pull", "--ff-only", remote, branch],
    )
    combined = f"{out}\n{err}".strip()
    if code != 0:
        result = SyncResult(
            status="failed",
            detail=f"git pull --ff-only failed: {combined}",
            branch=branch,
        )
        _append_log(log_file, f"{result.status}: {result.detail}")
        logger.warning("%s — %s", result.status, result.detail)
        return result

    lowered = combined.lower()
    if "already up to date" in lowered or "already up-to-date" in lowered:
        status = "already_up_to_date"
        detail = "Already up to date"
    else:
        status = "pulled"
        detail = combined or f"Pulled {remote}/{branch}"

    result = SyncResult(status=status, detail=detail, branch=branch)
    _append_log(log_file, f"{result.status}: {result.detail}")
    logger.info("%s — %s", result.status, result.detail)
    return result


def sync_commands_for_tests() -> List[str]:
    """Document the git subcommands used (for static asserts / docs)."""
    return [
        "status --porcelain",
        "rev-parse --abbrev-ref HEAD",
        f"fetch {DEFAULT_REMOTE} {DEFAULT_BRANCH}",
        f"pull --ff-only {DEFAULT_REMOTE} {DEFAULT_BRANCH}",
    ]
