"""NET-ASK-ALWAYS-SHOW Phase 0b: network_ask Option B wiring."""

from __future__ import annotations

from unittest.mock import patch

from inc_launcher.option_b_actions import prepare_option_b_item, uses_option_b_modal
from inc_launcher.tray_app import _run_menu_action


def test_uses_option_b_for_network_ask():
    assert uses_option_b_modal("network_ask") is True
    assert uses_option_b_modal("agent_run") is True
    assert uses_option_b_modal("folder") is False


def test_prepare_option_b_enriches_network_ask():
    item = prepare_option_b_item({"action": "network_ask", "label": "Ask"})
    assert item["action"] == "network_ask"
    assert item.get("modal_title")
    assert item.get("modal_bullets")


def test_scheduled_network_ask_opens_hub_modal(monkeypatch):
    opened: list[dict] = []

    def _fake_open(config, item):
        opened.append(item)

    monkeypatch.setattr("inc_launcher.hub_window.open_hub_with_option_b", _fake_open)
    monkeypatch.setattr("inc_launcher.tray_app._config_path", None)
    monkeypatch.setattr(
        "inc_launcher.tray_app.load_config",
        lambda path=None: {"pillars": []},
    )

    _run_menu_action({"action": "network_ask", "id": "network_ask_remind", "label": "Ask"})
    assert opened and opened[0]["action"] == "network_ask"


def test_hub_card_click_shows_modal_for_network_ask():
    """Hub _run_item path uses Option B for network_ask (not bare run_action)."""
    from unittest.mock import MagicMock

    with patch("inc_launcher.hub_window.show_agent_run_modal") as mock_modal:
        with patch("inc_launcher.hub_window.run_action") as mock_run:
            from inc_launcher.hub_window import HubWindow

            # Minimal stub: call the method logic via a fake instance
            fake = MagicMock(spec=HubWindow)
            fake._active_pillar_id = "problem_identification"
            HubWindow._run_item(
                fake,
                {"action": "network_ask", "label": "Ask people / owners"},
            )
            mock_modal.assert_called_once()
            mock_run.assert_not_called()
