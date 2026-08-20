# Template guide — building other Bookmark Reviewer apps

**This package:** `business_bookmark_sorter/` — shipped **Business links Bookmark Reviewer**.  
Treat it as a **guide / pattern** when you later build apps such as a **Health links Bookmark Reviewer** or an **Investment links Bookmark Reviewer** (new app folder, or a second configured instance — whichever fits isolation).

**Not in scope here:** implementing those Health/Investment apps now — only the checklist below.

## What to reuse (the pattern)

| Piece | Role |
|-------|------|
| Queue + timed review UI | `review_ui.py`, session settings/timer, auto-open |
| File → master links → docx | `export_markdown.py`, `docx_export.py`, `file_workflow.py` |
| App tray + single-instance | `review_tray.py`, `review_single_instance.py` |
| Branding strings | `instance_branding.py` + `config/routes.json` → `product` |

## Config to adapt (`config/routes.json`)

| Key | Role |
|-----|------|
| `product.app_title` | Window title + header (e.g. `Health links Bookmark Reviewer`) |
| `product.template_banner` | Top-of-app guide line for that app |
| `product.tray_tooltip` | System-tray hover text |
| `product.master_title` | `#` heading in the master markdown |
| `export.master_links_file` | Path to master `.md` (e.g. `…/Health Links.md`) |
| `export.flat_list` / `export.sort_by` | Flat chronological list vs sectioned |
| `chrome_filter.folder_name_contains` | Chrome folder name tokens (today: `business`) |
| `destinations` + `keyword_rules` | Suggest engine for that concept |
| `export_section_order` | Only if `flat_list` is false |

## Code modules (copy or share)

| Module | Role |
|--------|------|
| `review_ui.py` | Timed review panel |
| `review_tray.py` / `review_single_instance.py` | App tray + single-instance |
| `instance_branding.py` | Reads `product.*` |
| `export_markdown.py` / `docx_export.py` | Master md → docx |
| `session_settings*.py` / `session_timer.py` / `auto_open.py` | Timed sessions |

## Launcher / boot (add for each new app)

| Surface | Today (Business links) | New app (example) |
|---------|------------------------|-------------------|
| Inc menu | `bookmark_review` → `python -m business_bookmark_sorter review` | New menu id + command for the new app |
| Inc schedule | `bookmark_review_weekdays` | New schedule item if needed |
| PR boot | `inc_business_bookmark_review` | New applications key for the new app |

## Explicitly out of scope until approved

- Full Health / Investment product builds  
- Renaming this Python package folder  
- Merging with `project_reminder`’s `bookmark_sorter.py`
