"""Orchestrate Inc Hub agent formulation run (Phase 5.2)."""

from __future__ import annotations

import logging
import sys
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

from inc_launcher.config import INC_ROOT

logger = logging.getLogger(__name__)

DEFAULT_PROMPT_PATH = "prompts/agent_formulation_run.txt"
DEFAULT_PASTE_DELAY_SEC = 8.0


@dataclass(frozen=True)
class AgentRunResult:
    prompt_loaded: bool
    clipboard_ok: bool
    cursor_opened: bool
    paste_scheduled: bool
    error: Optional[str] = None


def _clipboard_helpers() -> tuple[Callable[[str], bool], Callable[[float], None]]:
    root = str(INC_ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)
    from cursor_copy_helper import copy_to_clipboard, paste_after_delay

    return copy_to_clipboard, paste_after_delay


def load_agent_prompt(inc_root: Path, prompt_rel: str = DEFAULT_PROMPT_PATH) -> Optional[str]:
    path = (inc_root / prompt_rel).resolve()
    if not path.is_file():
        logger.error("Agent formulation prompt not found: %s", path)
        return None
    try:
        text = path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        logger.error("Failed to read agent prompt %s: %s", path, exc)
        return None
    if not text:
        logger.error("Agent formulation prompt is empty: %s", path)
        return None
    return text


def run_agent_formulation(
    inc_root: Path | None = None,
    *,
    prompt_path: str = DEFAULT_PROMPT_PATH,
    paste_delay_sec: float = DEFAULT_PASTE_DELAY_SEC,
    auto_paste: bool = True,
    copy_fn: Callable[[str], bool] | None = None,
    open_cursor_fn: Callable[[Path], None] | None = None,
    paste_fn: Callable[[float], None] | None = None,
) -> AgentRunResult:
    """Load prompt, copy to clipboard, open Cursor, optionally schedule paste."""
    root = inc_root or INC_ROOT
    text = load_agent_prompt(root, prompt_path)
    if text is None:
        return AgentRunResult(False, False, False, False, "prompt_not_found")

    if copy_fn is None or paste_fn is None:
        clipboard_copy, paste_after_delay = _clipboard_helpers()
        copy_fn = copy_fn or clipboard_copy
        paste_fn = paste_fn or paste_after_delay

    if open_cursor_fn is None:
        from inc_launcher.actions import _open_in_cursor

        open_cursor_fn = _open_in_cursor

    clipboard_ok = bool(copy_fn(text))
    if not clipboard_ok:
        logger.warning("Agent run: clipboard copy failed; Cursor will still open")

    try:
        open_cursor_fn(root)
    except Exception as exc:
        logger.exception("Agent run: failed to open Cursor")
        return AgentRunResult(True, clipboard_ok, False, False, str(exc))

    paste_scheduled = False
    if auto_paste and clipboard_ok:
        threading.Thread(
            target=paste_fn,
            args=(paste_delay_sec,),
            daemon=True,
            name="inc-agent-run-paste",
        ).start()
        paste_scheduled = True

    return AgentRunResult(True, clipboard_ok, True, paste_scheduled)
