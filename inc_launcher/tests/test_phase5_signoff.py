"""Automated sign-off for Phase 5 agent formulation front door (MANUAL_TEST §G)."""

from __future__ import annotations

import subprocess
import sys
import time
import tkinter as tk
from typing import Any
from unittest.mock import patch

import pytest

from inc_launcher.agent_run import DEFAULT_PROMPT_PATH, load_agent_prompt
from inc_launcher.agent_run_modal import BULLETS, MODAL_TITLE, AgentRunModal
from inc_launcher.config import INC_ROOT, load_config, list_pillars
from inc_launcher.hub_window import HubWindow
from inc_launcher.recent import list_pinned

ROOT = INC_ROOT


def _kill_tray_processes() -> None:
    if sys.platform != "win32":
        return
    script = (
        "Get-CimInstance Win32_Process -Filter \"name='python.exe' OR name='pythonw.exe'\" | "
        "Where-Object { $_.CommandLine -match 'inc_launcher\\.tray_app|inc_launcher/tray_app' } | "
        "ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
    )
    subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        capture_output=True,
        timeout=30,
    )


def _widget_texts(widget: tk.Misc, classes: tuple[type, ...] = (tk.Label, tk.Button)) -> list[str]:
    texts: list[str] = []
    for cls in classes:
        if isinstance(widget, cls):
            texts.append(str(widget.cget("text")))
    for child in widget.winfo_children():
        texts.extend(_widget_texts(child, classes))
    return texts


def _find_button(modal: tk.Misc, label: str) -> tk.Button:
    for text in _widget_texts(modal, (tk.Button,)):
        pass
    for child in modal.winfo_children():
        for sub in child.winfo_children() if hasattr(child, "winfo_children") else []:
            if isinstance(sub, tk.Button) and sub.cget("text") == label:
                return sub
    stack: list[tk.Misc] = [modal]
    while stack:
        w = stack.pop()
        if isinstance(w, tk.Button) and w.cget("text") == label:
            return w
        stack.extend(w.winfo_children())
    raise AssertionError(f"Button not found: {label!r}")


@pytest.fixture
def tk_root():
    root = tk.Tk()
    root.withdraw()
    yield root
    try:
        root.destroy()
    except tk.TclError:
        pass


def test_prompt_file_exists_and_loads():
    path = ROOT / DEFAULT_PROMPT_PATH
    assert path.is_file(), f"Missing {path}"
    text = load_agent_prompt(ROOT)
    assert text
    assert "run_all_strategies.py" in text.lower() or "strategies" in text.lower()


def test_formulated_pillar_agent_and_cli_items():
    config = load_config()
    formulated = next(p for p in list_pillars(config) if p["id"] == "formulated")
    by_id = {i.get("id"): i for i in formulated.get("items", []) if i.get("id")}
    assert "agent_formulation_run" in by_id
    assert by_id["agent_formulation_run"]["action"] == "agent_run"
    assert "agent_formulation_pack" in by_id
    assert by_id["agent_formulation_pack"]["action"] == "agent_run"
    assert by_id["agent_formulation_pack"]["prompt_path"] == "prompts/agent_formulation_pack.txt"
    labels = [i["label"] for i in formulated.get("items", [])]
    assert "Agent formulation run" in labels
    assert "Agent formulation pack (Pass 2)" in labels
    assert "Run all strategies (CLI menu)" in labels
    cli = next(i for i in formulated["items"] if i["label"] == "Run all strategies (CLI menu)")
    assert cli["action"] == "command"
    assert "run_all_strategies.py" in cli["command"]


def test_agent_formulation_run_is_pinned():
    pinned = list_pinned(load_config())
    labels = [p["label"] for p in pinned]
    assert "Agent formulation run" in labels
    assert "Agent formulation pack (Pass 2)" not in labels
    assert "Run all strategies (CLI menu)" not in labels


def test_pack_prompt_file_loads():
    pack = ROOT / "prompts" / "agent_formulation_pack.txt"
    assert pack.is_file()
    text = load_agent_prompt(ROOT, "prompts/agent_formulation_pack.txt")
    assert text
    assert "Pass 2" in text
    assert "Regulatory" in text


def test_hub_header_subtitle_separate_rows(tk_root: tk.Tk):
    hub = HubWindow(tk_root, load_config())
    try:
        assert hub._header.grid_info()["row"] == 0
        assert hub._subtitle.grid_info()["row"] == 1
    finally:
        hub.destroy()


def test_option_b_modal_copy(tk_root: tk.Tk):
    modal = AgentRunModal(tk_root, {"action": "agent_run", "label": "Agent formulation run"})
    try:
        modal.update()
        texts = _widget_texts(modal)
        assert MODAL_TITLE in texts
        for line in BULLETS:
            assert f"• {line}" in texts
        button_texts = _widget_texts(modal, (tk.Button,))
        assert "Start" in button_texts
        assert "Not now" in button_texts
    finally:
        modal.destroy()


def test_option_b_modal_pack_custom_copy(tk_root: tk.Tk):
    item = {
        "action": "agent_run",
        "label": "Agent formulation pack (Pass 2)",
        "prompt_path": "prompts/agent_formulation_pack.txt",
        "modal_title": "Ready for Pass 2 pack?",
        "modal_bullets": [
            "Opens Cursor at the Inc repo",
            "Pastes pack prompt into chat (~8s)",
            "Same dated .md → uniform cards → Docx once",
        ],
    }
    modal = AgentRunModal(tk_root, item)
    try:
        modal.update()
        texts = _widget_texts(modal)
        assert "Ready for Pass 2 pack?" in texts
        assert "• Pastes pack prompt into chat (~8s)" in texts
        assert MODAL_TITLE not in texts
    finally:
        modal.destroy()


def test_modal_not_now_skips_run_action(tk_root: tk.Tk):
    item = {"action": "agent_run", "label": "Agent formulation run"}
    with patch("inc_launcher.agent_run_modal.run_action") as mock_run:
        modal = AgentRunModal(tk_root, item)
        try:
            _find_button(modal, "Not now").invoke()
            modal.update()
        finally:
            if modal.winfo_exists():
                modal.destroy()
        mock_run.assert_not_called()


def test_modal_start_runs_agent_action(tk_root: tk.Tk):
    item = {"action": "agent_run", "label": "Agent formulation run"}
    started: list[str] = []

    def _on_started() -> None:
        started.append("ok")

    with patch("inc_launcher.agent_run_modal.run_action") as mock_run:
        modal = AgentRunModal(tk_root, item, on_started=_on_started)
        modal._on_start()
        mock_run.assert_called_once()
        assert started == ["ok"]


def test_hub_card_routes_to_modal_not_direct_action(tk_root: tk.Tk, monkeypatch):
    shown: list[dict[str, Any]] = []

    def _fake_show(master, item, on_started=None):
        shown.append(item)

    monkeypatch.setattr("inc_launcher.hub_window.show_agent_run_modal", _fake_show)

    def _fail_run(*_a, **_k):
        raise AssertionError("run_action should not be called directly for agent_run")

    monkeypatch.setattr("inc_launcher.hub_window.run_action", _fail_run)

    hub = HubWindow(tk_root, load_config())
    try:
        hub._select_pillar("formulated")
        item = {"action": "agent_run", "label": "Agent formulation run"}
        hub._run_item(item)
        assert shown == [item]
    finally:
        hub.destroy()


@pytest.mark.skipif(sys.platform != "win32", reason="tray lifecycle test is Windows-only")
def test_tray_restart_single_instance():
    _kill_tray_processes()
    time.sleep(0.5)

    proc = subprocess.Popen(
        [sys.executable, "-m", "inc_launcher.tray_app"],
        cwd=str(ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        time.sleep(2.5)
        assert proc.poll() is None, "Tray process should stay running"

        dup = subprocess.run(
            [sys.executable, "-m", "inc_launcher.tray_app"],
            cwd=str(ROOT),
            capture_output=True,
            timeout=15,
        )
        assert dup.returncode == 0, "Second instance should exit 0 (single instance)"
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
        _kill_tray_processes()
