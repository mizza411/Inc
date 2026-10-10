"""Tests for section 19 Phase 7.5 catch-up orchestration + 7.6 toggle."""

from __future__ import annotations

import json
from pathlib import Path

from inc_launcher.config import (
    is_formulation_catchup_enabled,
    load_config,
    set_formulation_catchup_enabled,
)
from inc_launcher.formulation_catchup import CatchupResult, run_formulation_catchup
from inc_launcher.formulation_docx_opener import OpenBatchResult
from inc_launcher.formulation_repo_sync import SyncResult
from inc_launcher.tray_app import build_menu


def test_catchup_disabled_skips():
    called = {"sync": 0, "open": 0}

    def sync(_root):
        called["sync"] += 1
        return SyncResult(status="pulled", detail="x")

    def open_packs(_root):
        called["open"] += 1
        return OpenBatchResult()

    result = run_formulation_catchup(
        enabled=False, sync_fn=sync, open_fn=open_packs
    )

    assert result.skipped is True
    assert result.skip_reason == "disabled"
    assert called == {"sync": 0, "open": 0}


def test_catchup_runs_sync_then_open(tmp_path: Path):
    order: list[str] = []

    def sync(_root):
        order.append("sync")
        return SyncResult(status="already_up_to_date", detail="ok")

    def open_packs(_root):
        order.append("open")
        return OpenBatchResult()

    result = run_formulation_catchup(
        tmp_path, enabled=True, sync_fn=sync, open_fn=open_packs
    )

    assert isinstance(result, CatchupResult)
    assert result.skipped is False
    assert order == ["sync", "open"]
    assert result.sync is not None
    assert result.sync.status == "already_up_to_date"


def test_catchup_continues_open_after_sync_exception(tmp_path: Path):
    opened = {"n": 0}

    def sync(_root):
        raise RuntimeError("git down")

    def open_packs(_root):
        opened["n"] += 1
        return OpenBatchResult()

    result = run_formulation_catchup(
        tmp_path, enabled=True, sync_fn=sync, open_fn=open_packs
    )

    assert result.skipped is False
    assert result.sync is not None
    assert result.sync.status == "failed"
    assert opened["n"] == 1


def test_formulation_catchup_default_on():
    assert is_formulation_catchup_enabled() is True


def test_formulation_catchup_toggle_roundtrip(tmp_path: Path):
    source = Path(__file__).resolve().parent.parent / "launcher_config.json"
    config_path = tmp_path / "launcher_config.json"
    data = json.loads(source.read_text(encoding="utf-8"))
    data.setdefault("settings", {})["formulation_catchup_enabled"] = True
    config_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    assert is_formulation_catchup_enabled(config_path) is True
    set_formulation_catchup_enabled(False, config_path)
    assert is_formulation_catchup_enabled(config_path) is False
    saved = json.loads(config_path.read_text(encoding="utf-8"))
    assert saved["settings"]["formulation_catchup_enabled"] is False


def test_tray_menu_shows_formulation_catchup_toggle():
    menu = build_menu(load_config())
    labels = [getattr(entry, "text", "") or "" for entry in menu]
    assert any("Open formulation packs on start" in label for label in labels)
