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


def test_formulated_has_prospect_businesses_folder():
    """Phase 3.1 — additive Formulated card; path must resolve; no pillar renumber."""
    config = load_config()
    formulated = next(p for p in list_pillars(config) if p["id"] == "formulated")
    by_id = {item.get("id"): item for item in formulated.get("items", []) if item.get("id")}
    assert "prospect_businesses_folder" in by_id
    card = by_id["prospect_businesses_folder"]
    assert card["action"] == "folder"
    assert card["path"] == "Prospect-Businesses"
    assert resolve_path(card["path"]).is_dir()
    # Existing Formulated anchors still present after append
    assert "agent_formulation_run" in by_id
    assert "bookmark_review" in by_id
    established = next(p for p in list_pillars(config) if p["id"] == "established")
    assert any("Started Businesses folder" in i["label"] for i in established["items"])


def test_strategy1_hub_and_established_paths_resolve():
    """Former MANUAL_TEST A/B — config targets exist on disk."""
    config = load_config()
    formulated = next(p for p in list_pillars(config) if p["id"] == "formulated")
    s1 = next(i for i in formulated["items"] if i.get("id") == "strategy1_run")
    assert resolve_path(s1.get("cwd") or ".").is_dir()
    collector = resolve_path("Strategy-1-Business-Variation/business_variation_collector.py")
    assert collector.is_file()

    established = next(p for p in list_pillars(config) if p["id"] == "established")
    folder = next(i for i in established["items"] if "Strategy 1 folder" in i["label"])
    gadget = next(i for i in established["items"] if "Gadget business automation" in i["label"])
    assert resolve_path(folder["path"]).is_dir()
    assert resolve_path(gadget["path"]).is_dir()


def test_tray_menu_builds():
    from inc_launcher.tray_app import build_menu

    menu = build_menu(load_config())
    assert menu is not None
