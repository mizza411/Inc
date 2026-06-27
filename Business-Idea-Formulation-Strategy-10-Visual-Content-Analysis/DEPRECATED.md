# Strategy 10 — Deprecated

**Status:** Retired from the master runner (June 2026)  
**Reason:** ChatGPT Vision workflow relied on manual image upload and copy-paste; no licensed in-repo automation path. The script only generated prompt files and did not meet this repo's automate-first policy.

## Use instead

| Need | Replacement |
|------|-------------|
| Problems from architects, builders, developers | **Strategy 3** — `../Business-Idea-Formulation-Strategy-3-Network-Based-Problem-Identification/network_problem_collector.py` |
| Structured problems from business owners | **Strategy 4** — `../Business-Idea-Formulation-Strategy-4-Business-Owner-Problem-Collection/business_owner_problem_collector.py` |
| Construction / real estate news problems | **Strategy 5** — `../Business-Idea-Formulation-Strategy-5-News-Based-Problem-Extraction/news_problem_extractor.py` |

From repo root:

```bash
python run_all_strategies.py
# Menu option 3 -> enter 3, 4, or 5
```

## What remains in this folder

| Path | Purpose |
|------|---------|
| `visual_content_analyzer.py` | Stub only — prints this message and exits |
| `_archive/visual_content_analyzer_legacy.py` | Original prompt-helper script (reference; do not use in production) |
| `README.md`, `business-idea-formulation-strategy-10-*.md` | Historical playbook (deprecated banner at top) |

## Master runner

Strategy **10** is listed under `RETIRED_STRATEGIES` in `run_all_strategies.py` and is not executed by "Run ALL" or valid selections.
