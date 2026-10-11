"""Unit tests for section 19 Phase 7.9.1 formulation PR pack fetch."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

from inc_launcher.formulation_pending import OUTPUTS_REL
from inc_launcher.formulation_pr_fetch import (
    fetch_commands_for_tests,
    fetch_today_formulation_pack,
    formulation_branch_name,
    pack_rel_paths,
)


def _repo(tmp_path: Path) -> Path:
    root = tmp_path / "Inc"
    root.mkdir()
    (root / ".git").mkdir()
    return root


class ScriptedRunner:
    def __init__(self, script: Dict[tuple[str, ...], Tuple[int, str, str]]) -> None:
        self.script = script
        self.calls: List[List[str]] = []

    def __call__(self, args: Sequence[str], cwd: Path) -> Tuple[int, str, str]:
        self.calls.append(list(args))
        key = tuple(args)
        if key not in self.script:
            raise AssertionError(f"Unexpected git call: {args}")
        return self.script[key]


def test_skipped_not_git(tmp_path: Path):
    root = tmp_path / "not_repo"
    root.mkdir()
    log = tmp_path / "sync.log"
    result = fetch_today_formulation_pack(
        root, date_key="20261012", runner=lambda *_: (0, "", ""), log_path=log
    )
    assert result.status == "skipped_not_git"
    assert "pr_fetch skipped_not_git" in log.read_text(encoding="utf-8")


def test_skipped_no_branch(tmp_path: Path):
    root = _repo(tmp_path)
    runner = ScriptedRunner(
        {
            ("git", "fetch", "origin", "formulation/auto-20261012"): (
                1,
                "",
                "fatal: couldn't find remote ref formulation/auto-20261012\n",
            ),
        }
    )
    result = fetch_today_formulation_pack(
        root, date_key="20261012", runner=runner, log_path=tmp_path / "s.log"
    )
    assert result.status == "skipped_no_branch"
    assert result.ok_to_continue


def test_fetches_md_and_docx_when_missing(tmp_path: Path):
    root = _repo(tmp_path)
    key = "20261012"
    branch = formulation_branch_name(key)
    ref = f"origin/{branch}"
    md_rel, docx_rel = pack_rel_paths(key)
    md_bytes = b"# ideas\n"
    docx_bytes = b"PK\x03\x04docx-bytes"

    runner = ScriptedRunner(
        {
            ("git", "fetch", "origin", branch): (0, "", ""),
            ("git", "log", "-1", "--format=%ct", ref, "--", md_rel.as_posix()): (
                0,
                "1700000000\n",
                "",
            ),
            ("git", "log", "-1", "--format=%ct", ref, "--", docx_rel.as_posix()): (
                0,
                "1700000000\n",
                "",
            ),
        }
    )

    def blob_reader(_cwd: Path, got_ref: str, rel: str) -> Tuple[int, bytes, str]:
        assert got_ref == ref
        if rel == md_rel.as_posix():
            return 0, md_bytes, ""
        if rel == docx_rel.as_posix():
            return 0, docx_bytes, ""
        return 1, b"", "missing"

    result = fetch_today_formulation_pack(
        root,
        date_key=key,
        runner=runner,
        blob_reader=blob_reader,
        log_path=tmp_path / "s.log",
    )

    assert result.status == "fetched"
    assert set(result.written) == {
        f"business_ideas_{key}.md",
        f"business_ideas_{key}.docx",
    }
    assert (root / md_rel).read_bytes() == md_bytes
    assert (root / docx_rel).read_bytes() == docx_bytes


def test_skips_newer_local_docx(tmp_path: Path):
    root = _repo(tmp_path)
    key = "20261012"
    branch = formulation_branch_name(key)
    ref = f"origin/{branch}"
    md_rel, docx_rel = pack_rel_paths(key)
    out = root / OUTPUTS_REL
    out.mkdir(parents=True)
    local_docx = root / docx_rel
    local_docx.write_bytes(b"local-newer")
    # Local mtime in the future vs remote ts 1000
    future = time.time() + 3600
    import os

    os.utime(local_docx, (future, future))

    runner = ScriptedRunner(
        {
            ("git", "fetch", "origin", branch): (0, "", ""),
            ("git", "log", "-1", "--format=%ct", ref, "--", md_rel.as_posix()): (
                0,
                "1000\n",
                "",
            ),
            ("git", "log", "-1", "--format=%ct", ref, "--", docx_rel.as_posix()): (
                0,
                "1000\n",
                "",
            ),
        }
    )

    def blob_reader(_cwd: Path, _ref: str, rel: str) -> Tuple[int, bytes, str]:
        if rel.endswith(".md"):
            return 1, b"", "missing"
        return 0, b"remote-old", ""

    result = fetch_today_formulation_pack(
        root,
        date_key=key,
        runner=runner,
        blob_reader=blob_reader,
        log_path=tmp_path / "s.log",
    )

    assert result.status == "skipped_local_newer_or_present"
    assert local_docx.read_bytes() == b"local-newer"


def test_skipped_no_files_on_branch(tmp_path: Path):
    root = _repo(tmp_path)
    key = "20261012"
    branch = formulation_branch_name(key)
    runner = ScriptedRunner({("git", "fetch", "origin", branch): (0, "", "")})

    def blob_reader(_cwd: Path, _ref: str, _rel: str) -> Tuple[int, bytes, str]:
        return 1, b"", "not in tree"

    result = fetch_today_formulation_pack(
        root,
        date_key=key,
        runner=runner,
        blob_reader=blob_reader,
        log_path=tmp_path / "s.log",
    )
    assert result.status == "skipped_no_files"


def test_never_documents_force_reset():
    joined = " ".join(fetch_commands_for_tests())
    assert "reset" not in joined
    assert "show" in joined
