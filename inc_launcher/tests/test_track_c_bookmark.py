"""Track C: bookmark review tray menu integration."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from inc_launcher.config import load_config, list_pillars

ROOT = Path(__file__).resolve().parent.parent.parent


def test_tray_bookmark_review_menu_item():
    formulated = next(p for p in list_pillars(load_config()) if p["id"] == "formulated")
    review = next(i for i in formulated["items"] if i.get("id") == "bookmark_review")
    assert review["action"] == "command"
    assert review["command"] == "python -m business_bookmark_sorter review"
    assert review.get("cwd", ".") == "."


def test_bookmark_review_cli_registered():
    result = subprocess.run(
        [sys.executable, "-m", "business_bookmark_sorter", "--help"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "review" in result.stdout
