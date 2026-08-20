"""BB-TIMED-1 Phase 6 — PR boot config points at Inc review (no auto_launcher.py edit)."""

from __future__ import annotations

import json
from pathlib import Path

PR_CONFIG = Path(r"C:\dev\project_reminder\launcher_config.json")
INC_ROOT = Path(r"C:\dev\Inc")


def test_pr_boot_config_exists_and_targets_inc_review():
    assert PR_CONFIG.is_file(), f"Missing {PR_CONFIG}"
    data = json.loads(PR_CONFIG.read_text(encoding="utf-8"))
    apps = data.get("applications") or {}
    entry = apps.get("inc_business_bookmark_review")
    assert entry is not None, "applications.inc_business_bookmark_review missing"
    assert entry.get("enabled") is True
    assert entry.get("restart_on_crash") is False
    assert "business_bookmark_sorter review" in str(entry.get("arguments", ""))
    assert Path(entry.get("working_dir", "")).resolve() == INC_ROOT.resolve()
    assert Path(entry["path"]).is_file(), f"Python exe missing: {entry['path']}"


def test_pr_legacy_bookmark_sorter_untouched():
    data = json.loads(PR_CONFIG.read_text(encoding="utf-8"))
    scripts = data.get("scripts") or {}
    assert "bookmark_sorter" in scripts
    # Must remain a separate product key — do not remove or retarget
    assert "path" not in scripts["bookmark_sorter"] or "Inc" not in str(
        scripts["bookmark_sorter"].get("path", "")
    )
