"""AUTO-NAR-03 helpers — Hub Option-B modal copy + Start behavior (no tk here)."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from .build_docx import PLAYBOOK_DOCX
from .config_loader import load_config
from .openers import generate_openers
from .paths import PACKAGE_DIR
from .rotate import day_prompt

logger = logging.getLogger(__name__)

LAST_OPENERS = PACKAGE_DIR / "data" / "last_openers.txt"

ACTION_NAME = "network_ask"


def enrich_hub_item(item: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build / refresh a launcher menu item with today's rotate copy."""
    base = dict(item or {})
    cfg = load_config()
    dp = day_prompt(cfg)
    mode_labels = {
        "s3": "Strategy 3 — network",
        "s4": "Strategy 4 — owners",
        "both": "Strategy 3 + 4",
    }
    mode_label = mode_labels.get(dp.mode, dp.mode)
    cadence = "cadence day" if dp.is_cadence_day else "off-cadence preview"
    prompt_snip = dp.prompt_text.replace("\n", " ")
    if len(prompt_snip) > 140:
        prompt_snip = prompt_snip[:137] + "…"

    base.setdefault("id", "network_ask_remind")
    base.setdefault("label", "Ask people / owners (S3+S4)")
    base["action"] = ACTION_NAME
    if not (isinstance(base.get("modal_title"), str) and str(base["modal_title"]).strip()):
        base["modal_title"] = f"Ask people today? ({mode_label})"
    if not base.get("modal_bullets"):
        base["modal_bullets"] = [
            f"Today: {dp.mode} · {cadence} · {dp.day_key}",
            prompt_snip,
            "Start opens the playbook and copies openers (you still send)",
            "Never auto-messages anyone",
        ]
    return base


def run_network_ask_start(inc_root: Path | None = None) -> dict[str, Any]:
    """Start handler: open playbook + write/copy openers. No send."""
    del inc_root  # reserved for future paths relative to Inc
    cfg = load_config()
    dp = day_prompt(cfg)
    opener_mode = "both" if dp.mode == "both" else dp.mode
    text = generate_openers(cfg, opener_mode)  # type: ignore[arg-type]
    header = (
        f"# Today's mode: {dp.mode} ({dp.day_key})"
        f"{' · cadence' if dp.is_cadence_day else ''}\n"
        f"# Prompt: {dp.prompt_text}\n\n"
    )
    full = header + text
    LAST_OPENERS.parent.mkdir(parents=True, exist_ok=True)
    LAST_OPENERS.write_text(full + "\n", encoding="utf-8")

    clipboard_ok = False
    try:
        from cursor_copy_helper import copy_to_clipboard

        clipboard_ok = bool(copy_to_clipboard(full))
    except Exception as exc:
        logger.info("Clipboard copy skipped: %s", exc)

    playbook_opened = False
    if PLAYBOOK_DOCX.is_file():
        try:
            import os

            os.startfile(PLAYBOOK_DOCX)  # noqa: S606 — Windows default app for the Word playbook
            playbook_opened = True
        except OSError as exc:
            logger.warning("Could not open playbook: %s", exc)

    return {
        "mode": dp.mode,
        "playbook_opened": playbook_opened,
        "clipboard_ok": clipboard_ok,
        "openers_path": str(LAST_OPENERS),
    }
