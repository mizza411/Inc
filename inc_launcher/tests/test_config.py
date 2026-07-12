"""Tests for inc_launcher config (Phase 1)."""

from pathlib import Path

from inc_launcher.config import INC_ROOT, load_config, list_pillars, resolve_path


def test_load_config_has_core_pillars():
    config = load_config()
    pillars = list_pillars(config)
    assert len(pillars) >= 4
    labels = [p["label"] for p in pillars]
    assert "My Established business ideas" in labels
    assert "My leads" in labels
    assert "Formulated ideas" in labels
    assert "Problem identification" in labels
    assert "Automation hub" in labels


def test_resolve_inc_root_paths():
    path = resolve_path("Started-Businesses")
    assert path.is_dir() or path.parent == INC_ROOT


def test_config_items_have_actions():
    config = load_config()
    for pillar in list_pillars(config):
        for item in pillar.get("items", []):
            assert "action" in item
            assert "label" in item


def test_formulated_has_bookmark_review():
    config = load_config()
    formulated = next(p for p in list_pillars(config) if p["id"] == "formulated")
    by_id = {item.get("id"): item for item in formulated.get("items", []) if item.get("id")}
    assert "bookmark_review" in by_id
    review = by_id["bookmark_review"]
    assert review["action"] == "command"
    assert "business_bookmark_sorter review" in review["command"]


def test_formulated_has_agent_formulation_run():
    config = load_config()
    formulated = next(p for p in list_pillars(config) if p["id"] == "formulated")
    by_id = {item.get("id"): item for item in formulated.get("items", []) if item.get("id")}
    assert "agent_formulation_run" in by_id
    agent = by_id["agent_formulation_run"]
    assert agent["action"] == "agent_run"
    assert agent.get("pinned") is True
    labels = [item["label"] for item in formulated.get("items", [])]
    assert "Run all strategies (CLI menu)" in labels
    assert "strategy1_run" in by_id
    s1 = by_id["strategy1_run"]
    assert s1["action"] == "command"
    assert "business_variation_collector.py" in s1["command"]
    assert s1.get("cwd") == "Strategy-1-Business-Variation"


def test_established_keeps_strategy1_folder_and_gadget():
    config = load_config()
    established = next(p for p in list_pillars(config) if p["id"] == "established")
    labels = [item["label"] for item in established.get("items", [])]
    assert any("Strategy 1 folder" in label for label in labels)
    assert any("Gadget business automation" in label for label in labels)


def test_tray_menu_builds():
    from inc_launcher.tray_app import build_menu

    menu = build_menu(load_config())
    assert menu is not None
