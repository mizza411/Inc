"""discover CLI is discontinued — review is the launch command."""

from __future__ import annotations

import subprocess
import sys

from business_bookmark_sorter.paths import INC_ROOT


def test_help_does_not_list_discover():
    result = subprocess.run(
        [sys.executable, "-m", "business_bookmark_sorter", "--help"],
        cwd=str(INC_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "review" in result.stdout
    assert "discover" not in result.stdout


def test_discover_subcommand_rejected():
    result = subprocess.run(
        [sys.executable, "-m", "business_bookmark_sorter", "discover", "--dry-run"],
        cwd=str(INC_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    combined = (result.stderr or "") + (result.stdout or "")
    assert "invalid choice" in combined.lower() or "unrecognized" in combined.lower()
    assert "review" in combined
