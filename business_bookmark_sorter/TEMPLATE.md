# Template hooks — second category instance (no full build yet)

**Package stays:** `business_bookmark_sorter/` (Python import path unchanged).  
**Business links** = instance #1 of this shell (queue + timed review + file + master links + tray).

To host e.g. **Health links bookmark reviewer** later, copy/adapt config — do **not** fork a second app unless isolation forces it.

## Config hooks (`config/routes.json`)

| Key | Role |
|-----|------|
| `product.app_title` | Window title + header (e.g. `Health links bookmark Reviewer`) |
| `product.template_banner` | Top-of-app message about the shell |
| `product.tray_tooltip` | System-tray hover text |
| `product.master_title` | `#` heading in the master markdown |
| `export.master_links_file` | Path to master `.md` (e.g. `…/Health Links.md`) |
| `export.flat_list` / `export.sort_by` | Flat chronological list vs sectioned |
| `chrome_filter.folder_name_contains` | Chrome folder name tokens (today: `business`) |
| `destinations` + `keyword_rules` | Suggest engine categories for that concept |
| `export_section_order` | Only if `flat_list` is false |

## Code modules (reuse as-is)

| Module | Role |
|--------|------|
| `review_ui.py` | Timed review panel |
| `review_tray.py` / `review_single_instance.py` | App tray + single-instance |
| `instance_branding.py` | Reads `product.*` |
| `export_markdown.py` / `docx_export.py` | Master md → docx |
| `session_settings*.py` / `session_timer.py` / `auto_open.py` | Timed sessions |

## Launcher / boot (additive)

| Surface | Today (business) | Second instance |
|---------|------------------|-----------------|
| Inc menu | `bookmark_review` → `python -m business_bookmark_sorter review` | New menu id + command **or** same module with `ROUTES_CONFIG` env later |
| Inc schedule | `bookmark_review_weekdays` | New schedule item |
| PR boot | `inc_business_bookmark_review` | New applications key |

## Explicitly out of scope until approved

- Full Health / Investment routes + Chrome trees  
- Renaming the Python package folder  
- Merging with `project_reminder`’s `bookmark_sorter.py`
