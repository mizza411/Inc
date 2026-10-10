"""Unit tests for section 19 Phase 7.2 safe main sync (mocked git)."""

from __future__ import annotations

from pathlib import Path
from typing import List, Sequence, Tuple

from inc_launcher.formulation_repo_sync import (
    SyncResult,
    safe_pull_main,
    sync_commands_for_tests,
)


def _repo(tmp_path: Path) -> Path:
    root = tmp_path / "Inc"
    root.mkdir()
    (root / ".git").mkdir()
    return root


class ScriptedRunner:
    """Return canned (code, stdout, stderr) per git arg list."""

    def __init__(self, script: dict[tuple[str, ...], Tuple[int, str, str]]) -> None:
        self.script = script
        self.calls: List[List[str]] = []

    def __call__(self, args: Sequence[str], cwd: Path) -> Tuple[int, str, str]:
        self.calls.append(list(args))
        key = tuple(args)
        if key not in self.script:
            raise AssertionError(f"Unexpected git call: {args} cwd={cwd}")
        return self.script[key]


def test_skipped_not_git(tmp_path: Path):
    root = tmp_path / "not_a_repo"
    root.mkdir()
    log = tmp_path / "sync.log"

    result = safe_pull_main(root, runner=lambda *_: (0, "", ""), log_path=log)

    assert result.status == "skipped_not_git"
    assert result.ok_to_continue
    assert "skipped_not_git" in log.read_text(encoding="utf-8")


def test_skipped_dirty(tmp_path: Path):
    root = _repo(tmp_path)
    log = tmp_path / "sync.log"
    runner = ScriptedRunner(
        {
            ("git", "status", "--porcelain"): (0, " M README.md\n", ""),
        }
    )

    result = safe_pull_main(root, runner=runner, log_path=log)

    assert result.status == "skipped_dirty"
    assert result.ok_to_continue
    assert len(runner.calls) == 1


def test_skipped_wrong_branch(tmp_path: Path):
    root = _repo(tmp_path)
    runner = ScriptedRunner(
        {
            ("git", "status", "--porcelain"): (0, "", ""),
            ("git", "rev-parse", "--abbrev-ref", "HEAD"): (0, "feature/x\n", ""),
        }
    )

    result = safe_pull_main(root, runner=runner, log_path=tmp_path / "s.log")

    assert result.status == "skipped_wrong_branch"
    assert "feature/x" in result.detail
    assert result.ok_to_continue


def test_pulled_happy_path(tmp_path: Path):
    root = _repo(tmp_path)
    log = tmp_path / "sync.log"
    runner = ScriptedRunner(
        {
            ("git", "status", "--porcelain"): (0, "", ""),
            ("git", "rev-parse", "--abbrev-ref", "HEAD"): (0, "main\n", ""),
            ("git", "fetch", "origin", "main"): (0, "", ""),
            ("git", "pull", "--ff-only", "origin", "main"): (
                0,
                "Updating abc..def\nFast-forward\n",
                "",
            ),
        }
    )

    result = safe_pull_main(root, runner=runner, log_path=log)

    assert result.status == "pulled"
    assert result.ok_to_continue
    assert len(runner.calls) == 4
    assert "pulled:" in log.read_text(encoding="utf-8")


def test_already_up_to_date(tmp_path: Path):
    root = _repo(tmp_path)
    runner = ScriptedRunner(
        {
            ("git", "status", "--porcelain"): (0, "", ""),
            ("git", "rev-parse", "--abbrev-ref", "HEAD"): (0, "main\n", ""),
            ("git", "fetch", "origin", "main"): (0, "", ""),
            ("git", "pull", "--ff-only", "origin", "main"): (
                0,
                "Already up to date.\n",
                "",
            ),
        }
    )

    result = safe_pull_main(root, runner=runner, log_path=tmp_path / "s.log")

    assert result.status == "already_up_to_date"
    assert isinstance(result, SyncResult)


def test_pull_ff_only_failure(tmp_path: Path):
    root = _repo(tmp_path)
    runner = ScriptedRunner(
        {
            ("git", "status", "--porcelain"): (0, "", ""),
            ("git", "rev-parse", "--abbrev-ref", "HEAD"): (0, "main\n", ""),
            ("git", "fetch", "origin", "main"): (0, "", ""),
            ("git", "pull", "--ff-only", "origin", "main"): (
                1,
                "",
                "fatal: Not possible to fast-forward\n",
            ),
        }
    )

    result = safe_pull_main(root, runner=runner, log_path=tmp_path / "s.log")

    assert result.status == "failed"
    assert "fast-forward" in result.detail.lower()
    assert result.ok_to_continue  # still may open packs already on disk


def test_never_uses_force_reset_in_command_list():
    joined = " ".join(sync_commands_for_tests())
    assert "reset" not in joined
    assert "ff-only" in joined
