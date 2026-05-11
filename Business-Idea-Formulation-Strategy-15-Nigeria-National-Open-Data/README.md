# Business Idea Formulation Strategy 15: Nigeria National / Open Data

## Overview

Ideas are grounded in **Nigeria official or open statistical data** first (not news headlines). See the playbook for process, provenance columns, and gap handling.

## Data use boundary

Use only **public, aggregated, non-personal** datasets and releases from **official** publishers (NBS, **CBN**, ministries, agencies—when you cite them with indicator, period, and source). Do not attempt individual-level tracking or re-identification; Strategy 15 is for market-level signals and trends.

**Portal menu vs other sources:** `portal_menu.py` lists **shortcut entry points** (NBS eLibrary, NBS Microdata, Open Data for Africa Nigeria + foreign trade). Those are not the only allowed sources—you can still paste or JSON-reference **CBN**, ministry, or other official URLs; they are simply **not** on the default numbered menu.

**Interactive Step 2:** You can use **F** to load a **local download** (path while the script runs; absolute, or relative to the current working directory or the Strategy 15 folder). If the file yields **no readable text** (typical for binary **.xlsx**), the wizard asks you to **paste a short human summary** (sheet, TOTAL row, key figures) so the payload still carries numbers for Prompt 1a. On success, optional prompts record **`file_matches_catalog_search`** (if you used the catalog search-term menu) and **`provenance_note`**. **`catalog_search_term_used`** is saved whenever you pick a preset/custom term. These fields appear in **`nigeria_inputs.json`** and in **`strategy15_prompt_1a_payload.txt`**.

## Files

| File | Purpose |
|------|---------|
| `business-idea-formulation-strategy-15-nigeria-national-open-data.md` | Full playbook |
| `chatgpt_prompt_1a.txt` | Prompt 1a (hooks from excerpt + optional portal file path) |
| `chatgpt_prompt_1b.txt` | Prompt 1b (section-style expansion per idea) |
| `chatgpt_prompt_1c.txt` | Prompt 1c (conditional hardware under each idea) |
| `nigeria_national_open_data.py` | Validates `nigeria_inputs.json`, payloads, optional fetch/open-links |
| `portal_menu.py` | Interactive portal picker (Strategy 5–style) |
| `catalog_search_terms.py` | Per-portal catalog search presets (clipboard in Step 2) |
| `browser_links.py` | Opens `http(s)` URLs from JSON or portal picks |
| `open_all_strategy15_sources.py` | Opens every `DEFAULT_PORTALS` URL in the browser |

## Common commands

Default **interactive** run (Step 1 portal menu uses `DEFAULT_PORTALS` in `portal_menu.py`):

```bash
python nigeria_national_open_data.py
```

File-driven run (no wizard):

```bash
python nigeria_national_open_data.py --non-interactive --inputs nigeria_inputs.json
```

Optional: open `source_url` values from JSON after validation:

```bash
python nigeria_national_open_data.py --non-interactive --inputs nigeria_inputs.json --open-links
```

Open every default portal URL in the browser (helper script):

```bash
python open_all_strategy15_sources.py
```

Optional Python dependencies for automated fetching are listed in `requirements.txt` (commented) when used.
