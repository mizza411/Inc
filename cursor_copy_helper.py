#!/usr/bin/env python3
"""
Reusable Cursor copy-block helper for Strategy scripts.
Copy a document path + prompts to clipboard; optional auto-paste after delay.
Use from Strategy 5, Strategy 1, Strategy 9, etc.

Config file (Phase 1):
  Sub-phase 1.1: Load config from JSON (path + safe load); no behavior change.
  Sub-phase 1.2: Apply config overrides in offer_cursor_copy_block.
  Sub-phase 1.3: Add example config file and README docs.

Past-ideas file (replace long in-block paragraph):
  Phase 1 (this module): Build/update past_business_ideas.md from business_ideas_*.md. DONE.
  Phase 2: Use path to past_business_ideas.md in block + instruction; stop inlining long list. DONE.
  Phase 3: refresh_past_business_ideas_for_directory() + Strategy 5 run() start. DONE.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Union

CONFIG_FILENAME = "cursor_copy_block_config.json"
CONFIG_EXAMPLE_FILENAME = "cursor_copy_block_config.example.json"

DEFAULT_INSTRUCTION = (
    "Read the document at the path above. Apply Prompt 1a, then Prompt 1b, then Prompt 1c in the same chat (when Prompt 1c is included in this block). "
    "Output one markdown file named business_ideas_YYYYMMDD.md (use today's date) where each idea contains "
    "Business Idea + Digital Solution + Hardware Solution (hardware under each idea, not a separate section)."
)


def _config_path() -> Path:
    """Path to the copy-block config file (same directory as this module)."""
    return Path(__file__).resolve().parent / CONFIG_FILENAME


def _load_copy_block_config() -> Optional[Dict[str, Any]]:
    """
    Load cursor copy-block config from JSON. Tries cursor_copy_block_config.json
    first, then cursor_copy_block_config.example.json if the first is missing.
    Returns None if both missing or invalid.
    """
    base_dir = Path(__file__).resolve().parent
    for name in (CONFIG_FILENAME, CONFIG_EXAMPLE_FILENAME):
        path = base_dir / name
        if not path.exists():
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, dict) else None
        except (OSError, json.JSONDecodeError, TypeError):
            continue
    return None


# Past-ideas file (Phase 1): aggregate file built from business_ideas_*.md
PAST_IDEAS_FILENAME = "past_business_ideas.md"
_MAX_PAST_IDEAS_FILES = 10   # Max files to merge into past_business_ideas.md
_MAX_PAST_IDEAS_TITLES = 100 # Max idea lines in the file


def _write_past_ideas_from_parent(parent: Path) -> Optional[Path]:
    """
    Merge business_ideas_*.md in parent into past_business_ideas.md.
    Returns path to past_business_ideas.md, or None if nothing to write.
    """
    try:
        if not parent.is_dir():
            return None
        pattern = "business_ideas_*.md"
        files = sorted(parent.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
        files = files[:_MAX_PAST_IDEAS_FILES]
        if not files:
            return None
        titles: list[str] = []
        for f in files:
            if len(titles) >= _MAX_PAST_IDEAS_TITLES:
                break
            with open(f, "r", encoding="utf-8") as fp:
                for line in fp:
                    line = line.strip()
                    if line.startswith("## Idea ") or line.startswith("### Idea "):
                        titles.append(line.lstrip("# ").strip())
                    if len(titles) >= _MAX_PAST_IDEAS_TITLES:
                        break
        if not titles:
            return None
        out_path = parent / PAST_IDEAS_FILENAME
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("# Past business ideas (avoid repeating)\n\n")
            f.write("Use this list to avoid proposing the same or near-identical ideas again.\n\n")
            for t in titles:
                f.write("- " + t + "\n")
        return out_path
    except (OSError, ValueError):
        return None


def _ensure_past_ideas_file(document_path: Union[str, Path]) -> Optional[Path]:
    """
    Build or update past_business_ideas.md in the same directory as document_path,
    from existing business_ideas_*.md files (newest first). Returns path to the
    file, or None on any error or if no source files exist.
    """
    try:
        path = Path(document_path).resolve()
        if not path.exists():
            return None
        return _write_past_ideas_from_parent(path.parent)
    except (OSError, ValueError):
        return None


def refresh_past_business_ideas_for_directory(directory: Union[str, Path]) -> Optional[Path]:
    """
    Public API (Phase 3): Rebuild past_business_ideas.md from business_ideas_*.md
    in the given directory. Call after new business_ideas_*.md files appear (e.g.
    at the start of a Strategy 5 run). Returns path to past file or None.
    """
    try:
        d = Path(directory).resolve()
        if not d.is_dir():
            return None
        return _write_past_ideas_from_parent(d)
    except (OSError, ValueError):
        return None


def copy_to_clipboard(text: str) -> bool:
    """Copy text to clipboard. Returns True if successful."""
    try:
        if sys.platform == "win32":
            # Prefer pyperclip if available (handles paths with apostrophes/spaces)
            try:
                import pyperclip
                pyperclip.copy(text)
                return True
            except ImportError:
                pass
            # Fallback: temp file + PowerShell; pass path via env to avoid quoting issues
            import tempfile
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".txt", delete=False, encoding="utf-8"
            ) as f:
                f.write(text)
                tmp = f.name
            try:
                env = os.environ.copy()
                env["_CLIP_TMP"] = tmp
                subprocess.run(
                    [
                        "powershell", "-NoProfile", "-Command",
                        "$p = $env:_CLIP_TMP; if (Test-Path -LiteralPath $p) { Get-Content -LiteralPath $p -Raw | Set-Clipboard }; Remove-Item -LiteralPath $p -ErrorAction SilentlyContinue"
                    ],
                    env=env, check=True, capture_output=True, timeout=10
                )
                return True
            finally:
                try:
                    os.unlink(tmp)
                except OSError:
                    pass
        elif sys.platform == "darwin":
            subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True, timeout=5)
            return True
        else:
            try:
                subprocess.run(
                    ["xclip", "-selection", "clipboard"],
                    input=text.encode("utf-8"), check=True, timeout=5
                )
                return True
            except (FileNotFoundError, subprocess.CalledProcessError):
                return False
    except Exception:
        return False


def paste_after_delay(seconds: float = 6.0) -> None:
    """Send Ctrl+V to focused window after delay (requires pyautogui)."""
    try:
        import time
        import pyautogui
        print(f"  Focus Cursor chat box now. Pasting in {seconds} sec...")
        time.sleep(seconds)
        pyautogui.hotkey("ctrl", "v")
        print("  Done.")
    except ImportError:
        print("  Install pyautogui for auto-paste: pip install pyautogui")


def offer_cursor_copy_block(
    document_path: Union[str, Path],
    prompt_1a_ref: str,
    prompt_1b_ref: str,
    prompt_1c_ref: str = "",
    instruction: str = DEFAULT_INSTRUCTION,
    use_config: bool = True,
    supplementary_block: str = "",
) -> None:
    """
    Print a copyable block (document path + prompts) and offer to copy to clipboard;
    optional auto-paste after user focuses Cursor chat.

    Values can be overridden by cursor_copy_block_config.json (Sub-phase 1.2)
    when use_config is True (default). Pass use_config=False so caller arguments
    are always used (e.g. Strategy 15 vs Strategy 5 prompts in the same repo).
    Any Strategy script can call this after saving its output document.
    Optional prompt_1c_ref: when non-empty, included in the block as Prompt 1c (hardware track, etc.).
    Optional supplementary_block: extra text inserted after the Document line (e.g. local file paths).
    """
    doc_path_val = document_path
    p1a = prompt_1a_ref
    p1b = prompt_1b_ref
    p1c = prompt_1c_ref
    inst = instruction

    config = _load_copy_block_config() if use_config else None
    if config:
        v = config.get("document_path")
        if isinstance(v, str) and v.strip():
            doc_path_val = v.strip()
        v = config.get("prompt_1a_ref")
        if isinstance(v, str) and v.strip():
            p1a = v.strip()
        v = config.get("prompt_1b_ref")
        if isinstance(v, str) and v.strip():
            p1b = v.strip()
        v = config.get("prompt_1c_ref")
        if isinstance(v, str) and v.strip():
            p1c = v.strip()
        v = config.get("instruction")
        if isinstance(v, str) and v.strip():
            inst = v.strip()

    path = Path(doc_path_val)
    if not path.exists():
        return
    doc_path = str(path.resolve())
    past_path = _ensure_past_ideas_file(path)
    block = f"Document: {doc_path}\n\n"
    supp = supplementary_block
    if isinstance(supp, str) and supp.strip():
        block += supp.strip() + "\n\n"
    if past_path is not None:
        block += f"Past ideas (avoid repeating): {past_path.resolve()}\n\n"
    block += f"Prompt 1a: {p1a}\n" f"Prompt 1b: {p1b}\n"
    if isinstance(p1c, str) and p1c.strip():
        block += f"Prompt 1c: {p1c.strip()}\n"
    block += f"\n{inst}"
    config_path = _config_path()
    print("\n" + "="*70)
    print("READY FOR CURSOR — COPY THIS BLOCK INTO CHAT")
    print("="*70)
    print()
    print("  STEP 1: Press the \"C\" key (and only C) to copy the entire block below")
    print("           to your clipboard. To skip, press \"Q\".")
    print()
    print("  STEP 2: Open Cursor and click inside the chat message box (where you")
    print("           type your question).")
    print()
    print("  STEP 3: Either:")
    print("           (A) If you chose auto-paste: keep the chat box focused and wait")
    print("               6 seconds; the block will be pasted for you.")
    print("           (B) If you did not: press Ctrl+V to paste the block yourself.")
    print()
    print("  STEP 4: Press Enter (or click Send) to send the message. Cursor will")
    print("           read the document and output business ideas, including hardware under each idea if Prompt 1c is present.")
    print()
    example_path = config_path.parent / CONFIG_EXAMPLE_FILENAME
    if use_config:
        print("  TO CHANGE THIS BLOCK (i.e. prompts, file paths and instruction) BELOW NEXT TIME,")
        print("  edit the config file in the repo root:")
        print(f"           {example_path}")
        print("           Keys: document_path, prompt_1a_ref, prompt_1b_ref, prompt_1c_ref, instruction.")
        print("           (Optional: copy to cursor_copy_block_config.json to keep overrides separate.)")
        print("           FALLBACK DEFAULTS WHEN NO CONFIG EXISTS: cursor_copy_helper.py (DEFAULT_INSTRUCTION AND CALLER PROMPTS).")
    else:
        print("  This block uses this run's caller arguments only; repo-root cursor_copy_block_config.json")
        print("  is not applied. To change prompts or instruction next time, edit the strategy's")
        print("  prompt files or the script that calls offer_cursor_copy_block(..., use_config=False).")
    print()
    print("--- BEGIN (copy everything below this line into Cursor) ---")
    print()
    print(block)
    print()
    print("--- END (stop copying here) ---")
    print()
    try:
        if sys.platform == "win32":
            import msvcrt
            print("Press C to copy the block above, or Q to skip: ", end="", flush=True)
            while True:
                k = msvcrt.getch()
                if k in (b"c", b"C"):
                    break
                if k in (b"q", b"Q"):
                    print("Skipped.")
                    return
            print("C")
        else:
            choice = input("Press C then Enter to copy the block above, or Enter to skip: ").strip().upper()
            if choice != "C":
                return
    except (ImportError, AttributeError):
        choice = input("Press Enter to copy the block above (or type skip to skip): ").strip().lower()
        if choice == "skip":
            return

    if copy_to_clipboard(block):
        print("  Copied to clipboard.")
        auto = input("  Auto-paste in 6 sec after you focus Cursor chat? (y/n, default=n): ").strip().lower()
        if auto in ("y", "yes"):
            paste_after_delay(6.0)
        else:
            print("  Click in Cursor chat and press Ctrl+V to paste.")
    else:
        print("  Clipboard copy failed. Select the block above and copy manually.")
    print()
