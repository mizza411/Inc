"""BB-LINKS-UX-1 Phase 4 + BB-BRAND-1 — branding / template-as-guide."""

from __future__ import annotations

from pathlib import Path

from business_bookmark_sorter.instance_branding import (
    DEFAULT_APP_TITLE,
    DEFAULT_TEMPLATE_BANNER,
    app_title,
    master_title,
    template_banner,
    tray_tooltip,
)
from business_bookmark_sorter.queue_store import load_routes_config

CONFIG = Path(__file__).resolve().parent.parent / "config" / "routes.json"
TITLE = "Business links Bookmark Reviewer"


def test_product_defaults_from_routes():
    config = load_routes_config(CONFIG)
    assert app_title(config) == TITLE
    banner = template_banner(config)
    assert "Health" in banner
    assert "Investment" in banner
    assert "guide" in banner.lower() or "Guide" in banner
    assert "not a second app" not in banner.lower()
    assert "via config, not a second app" not in banner.lower()
    assert master_title(config) == "Business Links"
    assert tray_tooltip(config) == TITLE


def test_fallback_title_without_product_block():
    assert app_title({}) == DEFAULT_APP_TITLE == TITLE
    assert "Health" in template_banner({})
    assert "guide" in DEFAULT_TEMPLATE_BANNER.lower()
    assert "not a second app" not in DEFAULT_TEMPLATE_BANNER.lower()


def test_ui_source_uses_branding_not_old_title():
    ui = (Path(__file__).resolve().parent.parent / "review_ui.py").read_text(
        encoding="utf-8"
    )
    assert 'text="Bookmark Reviewer"' not in ui
    assert 'title("Bookmark Reviewer")' not in ui
    assert "Business links bookmark Reviewer" not in ui
    assert "app_title(" in ui
    assert "template_banner(" in ui


def test_template_md_is_guide_for_other_apps():
    path = Path(__file__).resolve().parent.parent / "TEMPLATE.md"
    text = path.read_text(encoding="utf-8")
    assert "chrome_filter" in text
    assert "product.app_title" in text
    assert "Health" in text
    assert "guide" in text.lower() or "Guide" in text
    assert "build" in text.lower()
    assert "not a second app" not in text.lower()
    assert "do **not** fork a second app" not in text.lower()
