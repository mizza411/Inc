# Business Idea Formulation - Master Runner

A master orchestrator script that runs Business Idea Formulation Strategies **1, 3–7, 9, 11–15** from a single entry point.

## Overview

Unified CLI to execute any combination of the active formulation strategies. Each strategy remains interactive (CLI prompts), but you can run them sequentially without switching scripts manually.

**Active set:** `1, 3–7, 9, 11–15` (12 strategies).  
**Verbal only:** Strategy **2**.  
**Retired:** Strategies **8** and **10**.

## Features

- **Menu-Based Interface**: Run all, selected, or one strategy
- **Flexible Selection**: Ranges (e.g., `3-6`) or individuals (e.g., `1,5,9`)
- **Error Handling**: Continue or stop after a failure
- **Execution Summary**: OK / FAILED per strategy
- **Interactive**: Individual strategy scripts keep their own prompts (Strategy 1 also supports `--non-interactive` when run directly)

## Requirements

- Python 3.6 or higher
- Strategy scripts present in their folders
- Per-strategy dependencies (see each strategy `README.md` / `requirements.txt`)

## Usage

```bash
python run_all_strategies.py
```

### Menu Options

```
1) Run ALL active strategies (1, 3–7, 9, 11–15) in order
2) Run SELECTED strategies (e.g. 1,3,5,7-9)
3) Run ONE strategy (e.g. 1 or 5)
4) Exit
```

### Option 2 examples

```
Your selection: 1,5,9
Your selection: 3-6
Your selection: 1,3,5-7,11,15
```

## Available Strategies

| Strategy # | Name | Script File |
|------------|------|-------------|
| 1 | Business Variation & Complaint Fixing | `Strategy-1-Business-Variation/business_variation_collector.py` |
| 2 | *(verbal only)* | — |
| 3 | Network-Based Problem Identification | `network_problem_collector.py` |
| 4 | Business Owner Problem Collection | `business_owner_problem_collector.py` |
| 5 | News-Based Problem Extraction | `news_problem_extractor.py` |
| 6 | Startup Niche Combination | `startup_niche_combiner.py` |
| 7 | Trending Startup Adaptation | `trending_startup_adapter.py` |
| ~~8~~ | ~~Trend Adaptation (TrendHunter)~~ | **Retired** — use Strategy 14 |
| 9 | Financial News Problem Extraction | `financial_news_extractor.py` |
| ~~10~~ | ~~Visual Content Analysis~~ | **Retired** — use Strategies 3, 4, or 5 |
| 11 | Personal Problem Conversion | `personal_problem_converter.py` |
| 12 | High-Value Problem Filtering | `problem_filter.py` |
| 13 | Multi-Source Comprehensive Analysis | `multisource_analyzer.py` |
| 14 | Global Data Trend Adaptation | `global_trend_adapter.py` |
| 15 | Nigeria National / Open Data | `nigeria_national_open_data.py` |

**Note:** Strategy **8** (TrendHunter) and Strategy **10** (ChatGPT Vision) were removed from the master runner — no licensed in-repo automation path. Use **Strategy 14** for global trends; use **Strategies 3–5** for construction/real-estate problem discovery.

Strategy **1** non-interactive (outside the menu):  
`python Strategy-1-Business-Variation/business_variation_collector.py --non-interactive --seed-ids jumia_food`

## How It Works

1. Locates each strategy script from `STRATEGY_SCRIPTS`
2. Runs it as a subprocess with the same Python interpreter
3. Each strategy keeps its own interactive (or flagged non-interactive) flow
4. On failure/Ctrl+C, you can continue or stop
5. Prints an execution summary

## Troubleshooting

### Script Not Found

Ensure strategy folders and script names match `STRATEGY_SCRIPTS` in `run_all_strategies.py`.

### Import Errors

Install that strategy’s dependencies (`requirements.txt` / README).

## Notes

- Subprocess isolation per strategy
- Strategy 1 outputs land under `Strategy-1-Business-Variation/`
- Strategy 2 remains playbook-only until a separate task automates it

## See Also

- `Strategy-1-Business-Variation/README.md`
- Individual strategy `README.md` files
- `API_SETUP.md` in Strategies 5, 9, and 13

---

**Last Updated:** 2026-07-11 — Strategy 1 registered as executable
