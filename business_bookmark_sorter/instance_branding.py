"""Product branding for this sorter instance (BB-LINKS-UX-1 / BB-BRAND-1).

Business links is the shipped first app built on this review shell. Use it as a
guide when building later apps (e.g. Health or Investment Bookmark Reviewers).
"""

from __future__ import annotations

from typing import Any, Dict

DEFAULT_APP_TITLE = "Business links Bookmark Reviewer"
DEFAULT_MASTER_TITLE = "Business Links"
DEFAULT_TEMPLATE_BANNER = (
    "Guide for other apps — this Business links Bookmark Reviewer shows the "
    "pattern (queue + timed review + file + master links + tray). Use it when "
    "you build apps like a Health links Bookmark Reviewer or an Investment "
    "links Bookmark Reviewer later."
)


def product_section(config: Dict[str, Any] | None) -> Dict[str, Any]:
    if not config:
        return {}
    raw = config.get("product")
    return raw if isinstance(raw, dict) else {}


def app_title(config: Dict[str, Any] | None = None) -> str:
    return str(product_section(config).get("app_title") or DEFAULT_APP_TITLE)


def master_title(config: Dict[str, Any] | None = None) -> str:
    export = (config or {}).get("export") or {}
    if export.get("master_title"):
        return str(export["master_title"])
    return str(product_section(config).get("master_title") or DEFAULT_MASTER_TITLE)


def template_banner(config: Dict[str, Any] | None = None) -> str:
    return str(
        product_section(config).get("template_banner") or DEFAULT_TEMPLATE_BANNER
    )


def tray_tooltip(config: Dict[str, Any] | None = None) -> str:
    return str(product_section(config).get("tray_tooltip") or app_title(config))
