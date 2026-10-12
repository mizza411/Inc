"""Automate section 19 Phase 7.8 behaviors (no real Word / tray process).

Covers multi-pack catch-up, no re-open after shown, and toggle OFF skip.
"""

from __future__ import annotations

import json
from pathlib import Path

from inc_launcher.config import (
    is_formulation_catchup_enabled,
    load_config,
    set_formulation_catchup_enabled,
)
from inc_launcher.formulation_catchup import run_formulation_catchup
from inc_launcher.formulation_docx_opener import open_pending_packs
from inc_launcher.formulation_pending import list_pending_packs
from inc_launcher.formulation_repo_sync import SyncResult
from inc_launcher.tray_app import build_menu


def _touch_docx(folder: Path, date_key: str) -> Path:
    path = folder / f"business_ideas_{date_key}.docx"
    path.write_bytes(b"PK\x03\x04fake")
    return path


def test_78b_multi_pack_opens_all_oldest_first(tmp_path: Path):
    out = tmp_path / "outputs"
    out.mkdir()
    _touch_docx(out, "20261012")
    _touch_docx(out, "20261010")
    _touch_docx(out, "20261011")
    state = tmp_path / "shown.json"
    opened: list[str] = []

    result = open_pending_packs(
        outputs=out,
        state_path=state,
        open_fn=lambda p: opened.append(p.name),
        log_path=tmp_path / "o.log",
    )

    assert result.opened_count == 3
    assert opened == [
        "business_ideas_20261010.docx",
        "business_ideas_20261011.docx",
        "business_ideas_20261012.docx",
    ]


def test_78c_second_run_does_not_reopen(tmp_path: Path):
    out = tmp_path / "outputs"
    out.mkdir()
    _touch_docx(out, "20261010")
    state = tmp_path / "shown.json"
    opened: list[str] = []

    open_pending_packs(
        outputs=out,
        state_path=state,
        open_fn=lambda p: opened.append(p.name),
        log_path=tmp_path / "o1.log",
    )
    assert opened == ["business_ideas_20261010.docx"]

    opened.clear()
    second = open_pending_packs(
        outputs=out,
        state_path=state,
        open_fn=lambda p: opened.append(p.name),
        log_path=tmp_path / "o2.log",
    )

    assert second.attempts == []
    assert opened == []
    assert list_pending_packs(outputs=out, state_path=state) == []


def test_78d_toggle_off_skips_open_via_catchup(tmp_path: Path):
    source = Path(__file__).resolve().parent.parent / "launcher_config.json"
    config_path = tmp_path / "launcher_config.json"
    data = json.loads(source.read_text(encoding="utf-8"))
    data.setdefault("settings", {})["formulation_catchup_enabled"] = True
    config_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    set_formulation_catchup_enabled(False, config_path)
    assert is_formulation_catchup_enabled(config_path) is False

    opened = {"n": 0}

    def sync(_root):
        return SyncResult(status="already_up_to_date", detail="ok")

    def open_packs(_root):
        opened["n"] += 1
        return open_pending_packs(
            outputs=tmp_path / "outputs",
            state_path=tmp_path / "shown.json",
            open_fn=lambda _p: None,
            log_path=tmp_path / "o.log",
        )

    result = run_formulation_catchup(
        tmp_path,
        enabled=is_formulation_catchup_enabled(config_path),
        sync_fn=sync,
        open_fn=open_packs,
    )

    assert result.skipped is True
    assert opened["n"] == 0


def test_78_menu_default_on_label():
    assert is_formulation_catchup_enabled() is True
    labels = [getattr(entry, "text", "") or "" for entry in build_menu(load_config())]
    assert any("Open formulation packs auto [ON]" in label for label in labels)
