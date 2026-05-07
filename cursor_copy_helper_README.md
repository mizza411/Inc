# cursor_copy_helper.py

Reusable Python module at the repo root for **Strategy** scripts (Strategy 5, Strategy 1, Strategy 9, etc.). It builds a single copyable block (document path + prompts), copies it to the clipboard, and optionally auto-pastes into Cursor chat after a short delay so you can get analysis without manually pasting.

**Adding copy-block support to another strategy?** Under **How to use from a Strategy script**, use the subsection **New strategy: checklist (read this first)** when wiring `offer_cursor_copy_block`—it walks through the steps, repo-root config, and the `use_config` choice.

## What it does

1. **Builds a block** — Document path + optional **Past ideas** path (`past_business_ideas.md`, built from existing `business_ideas_*.md` in the same folder) + Prompt 1a ref + Prompt 1b ref + instruction (e.g. “Read the document… read the Past ideas file if present… output the business ideas”).
2. **Prints the block** — Shows “Ready for Cursor” and the block between `--- BEGIN` / `--- END`.
3. **Waits for C** — Press **C** (or Enter on some setups) to copy the block to the clipboard.
4. **Optional auto-paste** — Asks “Auto-paste in 6 sec?”; if yes, after you focus Cursor chat it sends Ctrl+V so you don’t have to paste manually.

## How to use from a Strategy script

1. Ensure the repo root is on `sys.path` when your script runs (see example below).
2. Import and call `offer_cursor_copy_block()` after you’ve saved your output document.

### New strategy: checklist (read this first)

Use this checklist when you add prompt copy-and-paste (Cursor block) support for a new strategy. Follow it to choose `use_config` correctly and avoid repo-root `cursor_copy_block_config.json` replacing this strategy’s prompts with another strategy’s.

| Step | Action |
|------|--------|
| 1 | **Save the output document to disk first.** `offer_cursor_copy_block` exits quietly if `document_path` does not exist. |
| 2 | **Put prompts in your strategy folder** (e.g. `chatgpt_prompt_1a.txt`, `chatgpt_prompt_1b.txt`) and treat them as the source of truth for what you want in the block. |
| 3 | **Choose `use_config` once** (see table below). Wrong choice = wrong prompts in the block. |
| 4 | **Optional:** Call `refresh_past_business_ideas_for_directory(strategy_dir)` before the copy block so `past_business_ideas.md` is up to date for “avoid repeating” (same pattern as Strategy 5). |
| 5 | **Verify:** Run the script, scroll to `--- BEGIN ---` / `--- END ---`, and confirm **Prompt 1a** and **Prompt 1b** match *this* strategy—not news wording from Strategy 5 unless this *is* Strategy 5. |

**When to use which `use_config`:**

| `use_config` | Use when |
|----------------|----------|
| `True` (default) | You want **optional** overrides from **`cursor_copy_block_config.json`** at repo root (e.g. one shared “production” block you edit without touching Python). Accept that **the same JSON applies to every caller** that leaves `use_config=True`. |
| `False` | This strategy must **always** use the arguments passed from your script (e.g. full text read from **this** folder’s `chatgpt_prompt_*.txt`). **Required** if you also use a repo-root config that was written for a *different* strategy—otherwise that config will replace your prompts. Strategy 15 uses this. |

**Shared-config hazard (why Strategy 5 and 15 looked “mixed up”):** There is only **one** optional file, `cursor_copy_block_config.json`, at repo root. It can override `document_path`, `prompt_1a_ref`, `prompt_1b_ref`, and `instruction` for **any** script that calls `offer_cursor_copy_block` with **`use_config=True`**. So a config created for news-based Strategy 5 will still override a new strategy unless that strategy passes **`use_config=False`** or you clear those keys in the JSON.

**Recommended pattern for a new formulation strategy:** Read `chatgpt_prompt_1a.txt` and `chatgpt_prompt_1b.txt` from `Path(__file__).parent`, pass them into `offer_cursor_copy_block`, set **`instruction=`** to your save/output wording, and use **`use_config=False`** unless you explicitly want repo-root JSON to govern this script.

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
    prompt_1b_ref="Tabulate output (Columns: Proposed domain (not verified), Problem Identified, ...)",
)
```

### Example: prompts from files + `use_config=False` (isolated strategy)

```python
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
sys.path.insert(0, str(here.parents[1]))  # repo root
from cursor_copy_helper import offer_cursor_copy_block

payload = here / "strategy15_prompt_1a_payload.txt"
p1a = (here / "chatgpt_prompt_1a.txt").read_text(encoding="utf-8", errors="replace")
p1b = (here / "chatgpt_prompt_1b.txt").read_text(encoding="utf-8", errors="replace")

offer_cursor_copy_block(
    document_path=payload,
    prompt_1a_ref=p1a,
    prompt_1b_ref=p1b,
    instruction="Read the document at the path above. Apply Prompt 1a then Prompt 1b; save business_ideas_YYYYMMDD.md next to the document.",
    use_config=False,
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

**Bypass config:** Pass `use_config=False` to `offer_cursor_copy_block(...)` so `cursor_copy_block_config.json` never overrides the caller (useful when another strategy’s config would otherwise win). In that case, the console text tells you to change the strategy’s prompt files or the calling script—not the repo-root JSON.

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
| `offer_cursor_copy_block(document_path, prompt_1a_ref, prompt_1b_ref, instruction=None, use_config=True) -> None` | Print the block, wait for C, copy, then optionally run auto-paste. If `use_config=False`, repo-root JSON overrides are skipped. |
| `refresh_past_business_ideas_for_directory(directory) -> Optional[Path]` | Rebuild `past_business_ideas.md` from `business_ideas_*.md` in that folder (Phase 3; Strategy 5 calls this at run start). |

**Past ideas file:** `past_business_ideas.md` is built from existing `business_ideas_*.md` in the same directory. Strategy 5 refreshes it at the **start** of each run so new idea files saved from Cursor are included before you copy the block.

## Requirements

- **Clipboard:** Windows (PowerShell), macOS (`pbcopy`), or Linux with `xclip`.
- **Auto-paste:** Optional. Install `pyautogui` for automatic Ctrl+V:  
  `pip install pyautogui`

## File location

- **Module:** `Inc/cursor_copy_helper.py` (repo root).
- **Config (optional):** `Inc/cursor_copy_block_config.json`; example: `Inc/cursor_copy_block_config.example.json`.
- **This README:** `Inc/cursor_copy_helper_README.md`.

Other Strategy folders (e.g. `Business-Idea-Formulation-Strategy-5-...`, `Strategy-1-...`) should add the repo root to `sys.path` and then `from cursor_copy_helper import ...` as in the example above.
