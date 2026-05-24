# Strategy 8 — Deprecated

**Status:** Retired from the master runner (May 2026)  
**Reason:** TrendHunter has no licensed API; the prior workflow relied on manual paste or unofficial scraping, which does not meet this repo's automation and data-use policy.

## Use instead

| Need | Replacement |
|------|-------------|
| Global trend → Nigeria business ideas | **Strategy 14** — `../Business-Idea-Formulation-Strategy-14-Global-Data-Trend-Adaptation/global_trend_adapter.py` |
| Nigerian news problems | **Strategy 5** — news RSS / NewsAPI |
| Nigeria official statistics | **Strategy 15** — `nigeria_national_open_data.py` |

From repo root:

```bash
python run_all_strategies.py
# Menu option 3 → enter 14
```

## What remains in this folder

| Path | Purpose |
|------|---------|
| `trend_adapter.py` | Stub only — prints this message and exits |
| `_archive/trend_adapter_legacy.py` | Original TrendHunter script (reference; do not use in production) |
| `README.md`, `business-idea-formulation-strategy-8-*.md` | Historical playbook (deprecated banner at top) |
| `requirements.txt` | Only needed if you inspect the archived legacy script |

## Master runner

Strategy **8** is listed under `RETIRED_STRATEGIES` in `run_all_strategies.py` and is not executed by "Run ALL" or valid selections.
