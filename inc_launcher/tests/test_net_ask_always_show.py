"""NET-ASK-ALWAYS-SHOW-1 Phase 1a: Hub open always pairs Ask modal."""

from __future__ import annotations

from unittest.mock import MagicMock

from inc_launcher.config import load_config
from inc_launcher.hub_window import (
    NETWORK_ASK_ITEM_ID,
    HubController,
    resolve_network_ask_item,
)


def test_resolve_network_ask_item_from_repo_config():
    item = resolve_network_ask_item(load_config())
    assert item is not None
    assert item["id"] == NETWORK_ASK_ITEM_ID
    assert item["action"] == "network_ask"


def test_resolve_network_ask_item_missing():
    assert resolve_network_ask_item({"pillars": [], "global_actions": []}) is None


def test_hub_show_enqueues_always_show_network_ask():
    ctrl = HubController.__new__(HubController)
    ctrl._config = {}
    ctrl._thread = MagicMock()
    ctrl._thread.is_alive.return_value = True
    ctrl._ready = MagicMock()
    cmds: list[str] = []
    ctrl._queue = MagicMock()
    ctrl._queue.put.side_effect = lambda c: cmds.append(c)

    HubController.show(ctrl, {"pillars": []})

    assert cmds == ["show", "always_show_network_ask"]


def test_open_network_ask_modal_calls_show_for_item():
    ctrl = HubController.__new__(HubController)
    ctrl._config = load_config()
    ctrl._root = MagicMock()
    window = MagicMock()
    window.winfo_exists.return_value = True
    ctrl._window = window

    HubController._open_network_ask_modal(ctrl)

    window.show_agent_run_for_item.assert_called_once()
    shown = window.show_agent_run_for_item.call_args[0][0]
    assert shown["action"] == "network_ask"


def test_prompt_agent_run_does_not_enqueue_always_show():
    """agent_run Option B path must not stack a second Ask grab."""
    ctrl = HubController.__new__(HubController)
    ctrl._config = {}
    ctrl._thread = MagicMock()
    ctrl._thread.is_alive.return_value = True
    ctrl._ready = MagicMock()
    cmds: list[str] = []
    ctrl._queue = MagicMock()
    ctrl._queue.put.side_effect = lambda c: cmds.append(c)

    HubController.prompt_agent_run(
        ctrl,
        {"pillars": []},
        {"action": "agent_run", "label": "Agent"},
    )

    assert cmds == ["show_agent_run"]


def test_restore_network_ask_opens_option_b(monkeypatch):
    from inc_launcher.hub_window import restore_network_ask

    opened: list[dict] = []

    def _fake_open(config, item):
        opened.append(item)

    monkeypatch.setattr("inc_launcher.hub_window.open_hub_with_option_b", _fake_open)
    assert restore_network_ask(load_config()) is True
    assert opened and opened[0]["action"] == "network_ask"


def test_restore_network_ask_missing_card():
    from inc_launcher.hub_window import restore_network_ask

    assert restore_network_ask({"pillars": [], "global_actions": []}) is False


def test_tray_menu_has_restore_ask_item():
    from inc_launcher.tray_app import build_menu

    menu = build_menu(load_config())
    labels = [getattr(entry, "text", "") or "" for entry in menu]
    assert any("Show Ask people / owners" in label for label in labels)


def test_hub_restore_calls_show_agent_run_for_item():
    from inc_launcher.hub_window import HubWindow

    fake = MagicMock(spec=HubWindow)
    fake.config_data = load_config()
    HubWindow._restore_network_ask(fake)
    fake.show_agent_run_for_item.assert_called_once()
    assert fake.show_agent_run_for_item.call_args[0][0]["action"] == "network_ask"
