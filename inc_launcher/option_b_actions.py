"""Which Hub actions use the Option B confirm modal (tray-running gate)."""

from __future__ import annotations

from typing import Any, Dict

OPTION_B_ACTIONS = frozenset({"agent_run", "network_ask"})


def uses_option_b_modal(action: str | None) -> bool:
    return action in OPTION_B_ACTIONS


def prepare_option_b_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """Return item ready for Option B modal (enrich network_ask copy)."""
    action = item.get("action")
    if action == "network_ask":
        from network_ask_reminder.hub_nudge import enrich_hub_item

        return enrich_hub_item(item)
    return dict(item)
