# cursor_copy_helper.py

Reusable Python module at the repo root for **Strategy** scripts (Strategy 5, Strategy 1, Strategy 9, etc.). It builds a single copyable block (document path + prompts), copies it to the clipboard, and optionally auto-pastes into Cursor chat after a short delay so you can get analysis without manually pasting.

## What it does

1. **Builds a block** — Document path + Prompt 1a ref + Prompt 1b ref + instruction (e.g. “Read the document… output the business ideas table”).
2. **Prints the block** — Shows “Ready for Cursor” and the block between `--- BEGIN` / `--- END`.
3. **Waits for C** — Press **C** (or Enter on some setups) to copy the block to the clipboard.
4. **Optional auto-paste** — Asks “Auto-paste in 6 sec?”; if yes, after you focus Cursor chat it sends Ctrl+V so you don’t have to paste manually.

## How to use from a Strategy script

1. Ensure the repo root is on `sys.path` when your script runs (see example below).
2. Import and call `offer_cursor_copy_block()` after you’ve saved your output document.

### Example (e.g. in Strategy 5)

```python
import sys
from pathlib import Path

# Add repo root so we can import cursor_copy_helper
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cursor_copy_helper import offer_cursor_copy_block

# After saving your document (e.g. news_problems_*.txt):
offer_cursor_copy_block(
    document_path=Path("news_problems_20260216_172940.txt"),  # or self._last_txt_path
    prompt_1a_ref="Give me problems that can be solved with digital solutions...",
    prompt_1b_ref="Tabulate output (Columns: Linked Website, Problem Identified, ...)",
)
```

### Config file (override block without editing code)

You can override the block by editing a JSON config file so you don’t need to change Python.

- **File:** `cursor_copy_block_config.json` in the repo root (same folder as `cursor_copy_helper.py`).
- **Example:** Copy `cursor_copy_block_config.example.json` to `cursor_copy_block_config.json` and edit.

**Keys (all optional; leave empty or omit to use script defaults):**

| Key | Description |
|-----|-------------|
| `document_path` | Full path to the document. If empty or omitted, the path passed by the script (e.g. last saved run) is used. |
| `prompt_1a_ref` | Short text for “Prompt 1a” in the block. |
| `prompt_1b_ref` | Short text for “Prompt 1b” in the block. |
| `instruction` | Instruction line (e.g. “Read the document… output the business ideas table.”). |

Only non-empty string values override; missing or invalid keys are ignored. If the file is missing or invalid JSON, the script uses the values passed by the caller.

### Custom instruction (in code)

You can override the default instruction with the `instruction` argument:

```python
offer_cursor_copy_block(
    document_path=txt_path,
    prompt_1a_ref="...",
    prompt_1b_ref="...",
    instruction="Read the document and list the top 5 risks.",
)
```

## API

| Function | Description |
|----------|-------------|
| `copy_to_clipboard(text: str) -> bool` | Copy `text` to the system clipboard. Returns `True` if successful. |
| `paste_after_delay(seconds: float = 6.0) -> None` | After a delay, send Ctrl+V to the focused window (requires `pyautogui`). |
| `offer_cursor_copy_block(document_path, prompt_1a_ref, prompt_1b_ref, instruction=None) -> None` | Print the block, wait for C, copy, then optionally run auto-paste. |

## Requirements

- **Clipboard:** Windows (PowerShell), macOS (`pbcopy`), or Linux with `xclip`.
- **Auto-paste:** Optional. Install `pyautogui` for automatic Ctrl+V:  
  `pip install pyautogui`

## File location

- **Module:** `Inc/cursor_copy_helper.py` (repo root).
- **Config (optional):** `Inc/cursor_copy_block_config.json`; example: `Inc/cursor_copy_block_config.example.json`.
- **This README:** `Inc/cursor_copy_helper_README.md`.

Other Strategy folders (e.g. `Business-Idea-Formulation-Strategy-5-...`, `Strategy-1-...`) should add the repo root to `sys.path` and then `from cursor_copy_helper import ...` as in the example above.
