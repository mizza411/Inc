"""Tests for Phase 5.2 agent formulation orchestration."""

from __future__ import annotations

import time
from pathlib import Path
from unittest.mock import MagicMock, patch

from inc_launcher.actions import run_action
from inc_launcher.agent_run import (
    DEFAULT_PROMPT_PATH,
    load_agent_prompt,
    run_agent_formulation,
)


def test_load_agent_prompt_reads_file(tmp_path: Path):
    prompt_file = tmp_path / "prompts" / "agent_formulation_run.txt"
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("  Run strategies 5 and 15.  ", encoding="utf-8")

    text = load_agent_prompt(tmp_path)

    assert text == "Run strategies 5 and 15."


def test_load_agent_prompt_missing_returns_none(tmp_path: Path):
    assert load_agent_prompt(tmp_path) is None


def test_load_agent_prompt_empty_returns_none(tmp_path: Path):
    prompt_file = tmp_path / DEFAULT_PROMPT_PATH
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("   \n", encoding="utf-8")

    assert load_agent_prompt(tmp_path) is None


def test_run_agent_formulation_happy_path(tmp_path: Path):
    prompt_file = tmp_path / DEFAULT_PROMPT_PATH
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Agent prompt body", encoding="utf-8")

    copied: list[str] = []
    pasted: list[float] = []
    opened: list[Path] = []

    result = run_agent_formulation(
        tmp_path,
        copy_fn=lambda t: copied.append(t) or True,
        open_cursor_fn=lambda root: opened.append(root),
        paste_fn=lambda delay: pasted.append(delay),
        paste_delay_sec=8.0,
    )
    time.sleep(0.15)

    assert result.prompt_loaded is True
    assert result.clipboard_ok is True
    assert result.cursor_opened is True
    assert result.paste_scheduled is True
    assert copied == ["Agent prompt body"]
    assert opened == [tmp_path]
    assert pasted == [8.0]


def test_run_agent_formulation_skips_paste_when_clipboard_fails(tmp_path: Path):
    prompt_file = tmp_path / DEFAULT_PROMPT_PATH
    prompt_file.parent.mkdir(parents=True)
    prompt_file.write_text("Agent prompt body", encoding="utf-8")

    paste_fn = MagicMock()

    result = run_agent_formulation(
        tmp_path,
        copy_fn=lambda _t: False,
        open_cursor_fn=lambda _root: None,
        paste_fn=paste_fn,
    )

    assert result.prompt_loaded is True
    assert result.clipboard_ok is False
    assert result.cursor_opened is True
    assert result.paste_scheduled is False
    paste_fn.assert_not_called()


def test_run_agent_formulation_missing_prompt(tmp_path: Path):
    open_cursor_fn = MagicMock()

    result = run_agent_formulation(
        tmp_path,
        open_cursor_fn=open_cursor_fn,
    )

    assert result.prompt_loaded is False
    assert result.error == "prompt_not_found"
    open_cursor_fn.assert_not_called()


def test_run_action_dispatches_agent_run(tmp_path: Path):
    with patch("inc_launcher.agent_run.run_agent_formulation") as mock_run:
        run_action(
            {
                "action": "agent_run",
                "prompt_path": "prompts/agent_formulation_run.txt",
                "paste_delay_sec": 6,
                "auto_paste": False,
            },
            inc_root=tmp_path,
        )

    mock_run.assert_called_once_with(
        tmp_path,
        prompt_path="prompts/agent_formulation_run.txt",
        paste_delay_sec=6.0,
        auto_paste=False,
    )


def test_run_action_dispatches_pack_prompt_path(tmp_path: Path):
    with patch("inc_launcher.agent_run.run_agent_formulation") as mock_run:
        run_action(
            {
                "action": "agent_run",
                "prompt_path": "prompts/agent_formulation_pack.txt",
                "paste_delay_sec": 8,
                "auto_paste": True,
            },
            inc_root=tmp_path,
        )

    mock_run.assert_called_once_with(
        tmp_path,
        prompt_path="prompts/agent_formulation_pack.txt",
        paste_delay_sec=8.0,
        auto_paste=True,
    )


def test_tray_agent_run_opens_hub(monkeypatch):
    opened: list[dict] = []

    def _fake_open(config, item):
        opened.append(item)

    monkeypatch.setattr("inc_launcher.hub_window.open_hub_with_agent_run", _fake_open)

    from inc_launcher.tray_app import _item_handler

    handler = _item_handler({"action": "agent_run", "label": "Agent formulation run"})
    handler()

    assert opened and opened[0]["action"] == "agent_run"


def test_run_action_existing_folder_unchanged(tmp_path: Path):
    folder = tmp_path / "demo"
    folder.mkdir()

    with patch("inc_launcher.actions.os.startfile") as mock_start:
        run_action({"action": "folder", "path": "demo"}, inc_root=tmp_path)

    mock_start.assert_called_once()
