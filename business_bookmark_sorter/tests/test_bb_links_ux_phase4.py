"""BB-LINKS-UX-1 Phase 4 — branding / template shell."""

from __future__ import annotations

from pathlib import Path

from business_bookmark_sorter.instance_branding import (
    DEFAULT_APP_TITLE,
    app_title,
    master_title,
    template_banner,
    tray_tooltip,
)
from business_bookmark_sorter.queue_store import load_routes_config

CONFIG = Path(__file__).resolve().parent.parent / "config" / "routes.json"


def test_product_defaults_from_routes():
    config = load_routes_config(CONFIG)
    assert app_title(config) == "Business links bookmark Reviewer"
    assert "Health links" in template_banner(config)
    assert "Investment" in template_banner(config)
    assert master_title(config) == "Business Links"
    assert tray_tooltip(config) == "Business links bookmark Reviewer"


def test_fallback_title_without_product_block():
    assert app_title({}) == DEFAULT_APP_TITLE
    assert "Health" in template_banner({})


def test_ui_source_uses_branding_not_old_title():
    ui = (Path(__file__).resolve().parent.parent / "review_ui.py").read_text(
        encoding="utf-8"
    )
    assert 'text="Bookmark Reviewer"' not in ui
    assert 'title("Bookmark Reviewer")' not in ui
    assert "app_title(" in ui
    assert "template_banner(" in ui


def test_template_md_exists():
    path = Path(__file__).resolve().parent.parent / "TEMPLATE.md"
    text = path.read_text(encoding="utf-8")
    assert "chrome_filter" in text
    assert "product.app_title" in text
    assert "Health" in text
