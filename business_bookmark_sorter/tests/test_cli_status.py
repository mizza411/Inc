"""CLI status command tests."""

from __future__ import annotations

import subprocess
import sys
from types import SimpleNamespace

from business_bookmark_sorter.cli import cmd_status
from business_bookmark_sorter.paths import INC_ROOT, QUEUE_PATH
from business_bookmark_sorter.queue_store import count_by_status, load_queue


def test_cmd_status_on_live_queue(capsys):
    """Status command succeeds when queue.json exists."""
    assert QUEUE_PATH.is_file(), "queue.json required for status smoke"
    assert cmd_status(SimpleNamespace()) == 0
    captured = capsys.readouterr().out
    assert "Total:" in captured
    assert "By status:" in captured
    assert "pending" in captured


def test_queue_pending_count_report():
    """Expose pending count for filing backlog visibility."""
    queue = load_queue()
    counts = count_by_status(queue)
    total = len(queue.get("items", []))
    assert total > 0
    assert "pending" in counts
    assert counts["pending"] >= 0


def test_status_subprocess_entrypoint():
    """Module entrypoint: python -m business_bookmark_sorter status."""
    result = subprocess.run(
        [sys.executable, "-m", "business_bookmark_sorter", "status"],
        cwd=str(INC_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr or result.stdout
    assert "By status:" in result.stdout
