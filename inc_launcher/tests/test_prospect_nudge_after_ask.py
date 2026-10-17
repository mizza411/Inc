"""Prospect folder nudge after Ask dismiss (Established All launchers)."""

from __future__ import annotations

import tkinter as tk
from unittest.mock import MagicMock, patch

from inc_launcher.agent_run_modal import AgentRunModal
from inc_launcher.config import load_config
from inc_launcher.hub_window import (
    PROSPECT_ESTABLISHED_ITEM_ID,
    PROSPECT_NUDGE_TITLE,
    HubController,
    HubWindow,
    build_prospect_nudge_item,
    resolve_prospect_established_item,
)


def test_resolve_prospect_established_item():
    item = resolve_prospect_established_item(load_config())
    assert item is not None
    assert item["id"] == PROSPECT_ESTABLISHED_ITEM_ID
    assert item["action"] == "folder"
    assert item["path"] == "Prospect-Businesses"


def test_build_prospect_nudge_item_copy():
    nudge = build_prospect_nudge_item(load_config())
    assert nudge is not None
    assert nudge["modal_title"] == PROSPECT_NUDGE_TITLE
    assert nudge["modal_start_label"] == "Open folder"
    assert "All launchers" in nudge["modal_bullets"][0]


def test_open_network_ask_modal_passes_on_closed():
    ctrl = HubController.__new__(HubController)
    ctrl._config = load_config()
    ctrl._root = MagicMock()
    window = MagicMock()
    window.winfo_exists.return_value = True
    ctrl._window = window

    HubController._open_network_ask_modal(ctrl)

    window.show_agent_run_for_item.assert_called_once()
    kwargs = window.show_agent_run_for_item.call_args.kwargs
    assert kwargs.get("on_closed") == window.schedule_prospect_nudge_after_ask


def test_modal_on_closed_fires_on_destroy(tk_root: tk.Tk):
    closed: list[str] = []

    modal = AgentRunModal(
        tk_root,
        {"action": "network_ask", "label": "Ask"},
        on_closed=lambda: closed.append("yes"),
    )
    modal.destroy()
    assert closed == ["yes"]
    # Second destroy path must not double-fire
    assert not modal.winfo_exists()


def test_show_prospect_folder_nudge_selects_established(tk_root: tk.Tk, monkeypatch):
    shown: list[dict] = []

    def _fake_show(master, item, on_started=None, on_closed=None):
        shown.append(item)

    monkeypatch.setattr("inc_launcher.hub_window.show_agent_run_modal", _fake_show)

    hub = HubWindow(tk_root, load_config())
    try:
        hub._select_pillar("formulated")
        hub.show_prospect_folder_nudge()
        assert hub._active_pillar_id == "established"
        assert shown and shown[0]["modal_title"] == PROSPECT_NUDGE_TITLE
        assert shown[0].get("modal_start_label") == "Open folder"
        assert shown[0]["path"] == "Prospect-Businesses"
    finally:
        hub.destroy()


def test_schedule_prospect_nudge_uses_after(tk_root: tk.Tk):
    hub = HubWindow(tk_root, load_config())
    try:
        with patch.object(hub, "after") as mock_after:
            hub.schedule_prospect_nudge_after_ask()
            mock_after.assert_called_once()
            assert mock_after.call_args[0][0] == 0
            assert mock_after.call_args[0][1] == hub.show_prospect_folder_nudge
    finally:
        hub.destroy()
