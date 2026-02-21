#!/usr/bin/env python3
"""
Reusable Cursor copy-block helper for Strategy scripts.
Copy a document path + prompts to clipboard; optional auto-paste after delay.
Use from Strategy 5, Strategy 1, Strategy 9, etc.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Union

DEFAULT_INSTRUCTION = (
    "Read the document at the path above. Apply Prompt 1a then Prompt 1b. Output the business ideas table."
)


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
    instruction: str = DEFAULT_INSTRUCTION,
) -> None:
    """
    Print a copyable block (document path + prompts) and offer to copy to clipboard;
    optional auto-paste after user focuses Cursor chat.

    Any Strategy script can call this after saving its output document.
    """
    path = Path(document_path)
    if not path.exists():
        return
    doc_path = str(path.resolve())
    block = (
        f"Document: {doc_path}\n\n"
        f"Prompt 1a: {prompt_1a_ref}\n"
        f"Prompt 1b: {prompt_1b_ref}\n\n"
        f"{instruction}"
    )
    print("\n" + "="*70)
    print("Ready for Cursor (paste in chat for analysis)")
    print("="*70)
    print("\n1. Press C to copy the block (then focus Cursor chat; script can auto-paste).")
    print("2. Send in Cursor. It will read the file and output business ideas.\n")
    print("--- BEGIN (paste this in Cursor) ---")
    print(block)
    print("--- END ---\n")

    try:
        if sys.platform == "win32":
            import msvcrt
            print("Press C to copy (or Q to skip): ", end="", flush=True)
            while True:
                k = msvcrt.getch()
                if k in (b"c", b"C"):
                    break
                if k in (b"q", b"Q"):
                    print("Skipped.")
                    return
            print("C")
        else:
            choice = input("Press C then Enter to copy (or Enter to skip): ").strip().upper()
            if choice != "C":
                return
    except (ImportError, AttributeError):
        choice = input("Press Enter to copy (or type skip to skip): ").strip().lower()
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
