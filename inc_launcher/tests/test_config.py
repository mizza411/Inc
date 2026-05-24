"""Tests for inc_launcher config (Phase 1)."""

from pathlib import Path

from inc_launcher.config import INC_ROOT, load_config, list_pillars, resolve_path


def test_load_config_has_four_pillars():
    config = load_config()
    pillars = list_pillars(config)
    assert len(pillars) == 4
    labels = [p["label"] for p in pillars]
    assert "My Established business ideas" in labels
    assert "My leads" in labels
    assert "Formulated ideas" in labels
    assert "Problem identification" in labels


def test_resolve_inc_root_paths():
    path = resolve_path("Started-Businesses")
    assert path.is_dir() or path.parent == INC_ROOT


def test_config_items_have_actions():
    config = load_config()
    for pillar in list_pillars(config):
        for item in pillar.get("items", []):
            assert "action" in item
            assert "label" in item


def test_tray_menu_builds():
    from inc_launcher.tray_app import build_menu

    menu = build_menu(load_config())
    assert menu is not None
