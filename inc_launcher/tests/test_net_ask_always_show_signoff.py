"""NET-ASK-ALWAYS-SHOW-1 Phase 1c automated sign-off (mocked / no live tray click)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from inc_launcher.config import load_config
from inc_launcher.hub_window import HubController, resolve_network_ask_item, restore_network_ask
from inc_launcher.nudge_scheduler import execute_nudge
from inc_launcher.option_b_actions import prepare_option_b_item, uses_option_b_modal
from inc_launcher.scheduled_nudges import load_schedule_settings
from inc_launcher.tray_app import build_menu


def test_1c_hub_open_always_queues_ask():
    ctrl = HubController.__new__(HubController)
    ctrl._thread = MagicMock()
    ctrl._thread.is_alive.return_value = True
    ctrl._ready = MagicMock()
    cmds: list[str] = []
    ctrl._queue = MagicMock()
    ctrl._queue.put.side_effect = lambda c: cmds.append(c)
    HubController.show(ctrl, load_config())
    assert cmds == ["show", "always_show_network_ask"]


def test_1c_daily_inc_hub_uses_show_hub_path():
    """daily_inc_hub target is hub → execute_nudge calls open_hub (show_hub), which pairs Ask."""
    config = load_config()
    settings = load_schedule_settings(config)
    entry = next(e for e in settings.entries if e.id == "daily_inc_hub")
    hubs: list[object] = []

    assert execute_nudge(
        entry,
        config,
        open_hub=lambda cfg: hubs.append(cfg),
        run_menu_action=lambda _item: None,
    )
    assert len(hubs) == 1


def test_1c_network_ask_mwf_opens_option_b(monkeypatch):
    from inc_launcher import tray_app

    opened: list[dict] = []
    monkeypatch.setattr(
        "inc_launcher.hub_window.open_hub_with_option_b",
        lambda config, item: opened.append(item),
    )
    monkeypatch.setattr(tray_app, "_config_path", None)
    monkeypatch.setattr(tray_app, "load_config", lambda path=None: load_config())

    item = resolve_network_ask_item(load_config())
    assert item is not None
    tray_app._run_menu_action(item)
    assert opened and opened[0]["action"] == "network_ask"


def test_1c_restore_and_enrich_and_tray_labels():
    cfg = load_config()
    item = resolve_network_ask_item(cfg)
    assert item is not None
    assert uses_option_b_modal("network_ask")
    enriched = prepare_option_b_item(item)
    assert enriched.get("modal_title")
    assert enriched.get("modal_bullets")

    opened: list[dict] = []
    with patch("inc_launcher.hub_window.open_hub_with_option_b", side_effect=lambda c, i: opened.append(i)):
        assert restore_network_ask(cfg) is True
    assert opened

    labels = [getattr(e, "text", "") or "" for e in build_menu(cfg)]
    assert any("Open Inc Hub" in L for L in labels)
    assert any("Show Ask people / owners" in L for L in labels)


def test_1c_cadence_does_not_block_enrich_off_day():
    """Off-cadence still gets preview copy (always-show must not hide the modal)."""
    item = prepare_option_b_item({"action": "network_ask", "label": "Ask"})
    joined = " ".join(item.get("modal_bullets") or []).lower()
    assert "never auto-messages" in joined
    # day_key present whether cadence or preview
    assert any("cadence" in b.lower() or "preview" in b.lower() for b in item["modal_bullets"])
