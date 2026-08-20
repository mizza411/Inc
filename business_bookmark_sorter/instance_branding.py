"""Product branding for this sorter instance (BB-LINKS-UX-1 Phase 4).

Business links is instance #1 of a reusable shell. A future Health/Investment
instance would swap ``routes.json`` → ``product`` (and chrome filter / master
path) without forking a second app package.
"""

from __future__ import annotations

from typing import Any, Dict

DEFAULT_APP_TITLE = "Business links bookmark Reviewer"
DEFAULT_MASTER_TITLE = "Business Links"
DEFAULT_TEMPLATE_BANNER = (
    "Template shell — this is the Business links instance. "
    "The same review + queue + master-links + tray pattern can later host "
    "other concept types (e.g. “Health links bookmark reviewer”, "
    "“Investment links bookmark reviewer”) via config, not a second app."
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
