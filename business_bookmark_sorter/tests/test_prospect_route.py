"""Phase 3.2 — Prospect-Businesses destination is additive and does not break prior routes."""

from pathlib import Path

from business_bookmark_sorter.paths import INC_ROOT
from business_bookmark_sorter.queue_store import load_routes_config
from business_bookmark_sorter.suggest import suggest_destination

CONFIG = Path(__file__).resolve().parent.parent / "config" / "routes.json"


def test_prospects_destination_exists_and_folder_resolves():
    config = load_routes_config(CONFIG)
    dests = config["destinations"]
    assert "prospects" in dests
    assert dests["prospects"]["folder"] == "Prospect-Businesses"
    assert dests["prospects"]["label"] == "Prospect businesses"
    folder = INC_ROOT / dests["prospects"]["folder"]
    assert folder.is_dir()
    assert "prospects" in config.get("export_section_order", [])


def test_prior_destinations_still_present():
    config = load_routes_config(CONFIG)
    dests = config["destinations"]
    for key in (
        "started",
        "formulated",
        "formulation_strategy",
        "problem_identification",
        "leads",
        "automation",
        "other",
        "inbox",
        "stay_in_chrome",
    ):
        assert key in dests
    assert dests["started"]["folder"] == "Started-Businesses"
    assert dests["formulated"]["folder"] == "business_research"


def test_suggest_prospect_keyword_and_started_unchanged():
    config = load_routes_config(CONFIG)
    prospect_entry = {
        "type": "url",
        "title": "ExamFee notes",
        "url": "https://example.com/examfee-planner",
        "folder_path": "",
    }
    dest, _ = suggest_destination(prospect_entry, config)
    assert dest == "prospects"

    started_entry = {
        "type": "url",
        "title": "Software development ops",
        "url": "https://example.com/started-business",
        "folder_path": "software-development",
    }
    dest2, _ = suggest_destination(started_entry, config)
    assert dest2 == "started"
