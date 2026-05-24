# Business Idea Formulation - Master Runner

A master orchestrator script that runs all Business Idea Formulation Strategies (3-14) from a single entry point, eliminating the need to manually run each strategy script one by one.

## Overview

This script provides a unified CLI interface to execute any combination of the 12 business idea formulation strategies. Each strategy remains fully interactive (CLI-based with prompts), but you can now run them sequentially without manually switching between scripts.

## Features

- **Menu-Based Interface**: Choose to run all strategies or select specific ones
- **Flexible Selection**: Use ranges (e.g., `3-6`) or individual numbers (e.g., `3,5,9`)
- **Error Handling**: If a strategy fails, you can choose to continue or stop
- **Execution Summary**: See which strategies completed successfully and which failed
- **Interactive**: All individual strategy scripts remain fully interactive with their own prompts

## Requirements

- Python 3.6 or higher
- All strategy scripts must be present in their respective folders
- Individual strategy dependencies (see each strategy's `README.md` or `requirements.txt`)

## Usage

### Basic Usage

From the project root directory:

```bash
python run_all_strategies.py
```

### Menu Options

When you run the script, you'll see:

```
================================================================================
Business Idea Formulation - Master Runner (Phase 2)
================================================================================
Available strategies:
  - Strategy 3
  - Strategy 4
  - Strategy 5
  ...
  - Strategy 14

Menu:
  1) Run ALL strategies (3–14) in order
  2) Run SELECTED strategies (e.g. 3,5,7-9)
  3) Exit
```

### Option 1: Run All Strategies

Select option `1` (or press Enter for default) to run all strategies from 3 to 14 in sequence. You'll be asked to confirm before execution begins.

### Option 2: Run Selected Strategies

Select option `2` to run only specific strategies. You can enter:

- **Individual numbers**: `3,5,9`
- **Ranges**: `3-6` (runs 3, 4, 5, 6)
- **Combined**: `3,5-7,10,14` (runs 3, 5, 6, 7, 10, 14)

**Examples:**
```
Your selection: 3,5,9
Selected strategies: 3, 5, 9

Your selection: 3-6
Selected strategies: 3, 4, 5, 6

Your selection: 3,5-7,10,14
Selected strategies: 3, 5, 6, 7, 10, 14
```

### Option 3: Exit

Select option `3` to exit the master runner without executing any strategies.

## Available Strategies

| Strategy # | Name | Script File |
|------------|------|-------------|
| 3 | Network-Based Problem Identification | `network_problem_collector.py` |
| 4 | Business Owner Problem Collection | `business_owner_problem_collector.py` |
| 5 | News-Based Problem Extraction | `news_problem_extractor.py` |
| 6 | Startup Niche Combination | `startup_niche_combiner.py` |
| 7 | Trending Startup Adaptation | `trending_startup_adapter.py` |
| ~~8~~ | ~~Trend Adaptation (TrendHunter)~~ | **Retired** — use Strategy 14 |
| 9 | Financial News Problem Extraction | `financial_news_extractor.py` |
| 10 | Visual Content Analysis | `visual_content_analyzer.py` |
| 11 | Personal Problem Conversion | `personal_problem_converter.py` |
| 12 | High-Value Problem Filtering | `problem_filter.py` |
| 13 | Multi-Source Comprehensive Analysis | `multisource_analyzer.py` |
| 14 | Global Data Trend Adaptation | `global_trend_adapter.py` |
| 15 | Nigeria National / Open Data | `nigeria_national_open_data.py` |

**Note:** Strategy **8** (TrendHunter) was removed from the master runner — no licensed automation path. Use **Strategy 14** for global trend adaptation instead.

## How It Works

1. **Script Discovery**: The master runner automatically locates each strategy script in its respective folder
2. **Subprocess Execution**: Each strategy runs as a subprocess using the same Python interpreter
3. **Interactive Flow**: Each strategy script maintains its own interactive CLI prompts
4. **Error Handling**: If a strategy fails or is interrupted (Ctrl+C), you can choose to continue or stop
5. **Summary Report**: At the end, you'll see a summary showing which strategies completed successfully

## Example Workflow

```
$ python run_all_strategies.py

================================================================================
Business Idea Formulation - Master Runner (Phase 2)
================================================================================
Available strategies:
  - Strategy 3
  - Strategy 4
  ...

Menu:
  1) Run ALL strategies (3–14) in order
  2) Run SELECTED strategies (e.g. 3,5,7-9)
  3) Exit

Choose an option (1/2/3, default=1): 2

Enter strategy numbers or ranges, separated by commas.
Examples:
  3,5,9
  3-6
  3,5-7,10,14

Your selection: 3,5,9
Selected strategies: 3, 5, 9
Proceed with these strategies? (y/n, default=y): y

================================================================================
Starting Strategy 3: network_problem_collector.py
================================================================================

[Strategy 3's interactive prompts appear here...]

✓ Strategy 3 completed successfully.

[Continues with Strategy 5, then Strategy 9...]

================================================================================
Execution Summary
================================================================================
Strategy 3: OK
Strategy 5: OK
Strategy 9: OK

All done.
```

## Handling Interruptions

If you press **Ctrl+C** during a strategy execution:

- The current strategy will be marked as interrupted/failed
- You'll be asked: "Continue with the next strategy? (y/n, default=y)"
- If you choose `y`, execution continues with the next strategy
- If you choose `n`, execution stops and shows the summary

## Troubleshooting

### Script Not Found Error

If you see:
```
⚠ Strategy X: Script not found at [path]
```

**Solution**: Ensure all strategy folders exist and contain their respective Python scripts. Check that folder names match exactly (case-sensitive).

### Import Errors

If a strategy script fails with import errors:

**Solution**: Install the required dependencies for that specific strategy. Check the strategy's folder for `requirements.txt` or `README.md` for installation instructions.

### Permission Errors

If you encounter permission errors:

**Solution**: Ensure you have read and execute permissions for the script files and directories.

## Notes

- Each strategy script runs in its own subprocess, so environment variables and imports are isolated
- The master runner uses the same Python interpreter (`sys.executable`) that launched it
- All strategies remain fully interactive—this script only orchestrates their execution
- Output files from each strategy are saved in their respective strategy folders

## Future Enhancements (Optional)

Potential future phases could include:
- **Phase 3**: Save and load preset strategy combinations
- **Phase 4**: Logging and resumability (resume from last incomplete strategy)
- **Phase 5**: Non-interactive/batch mode for automated runs
- **Phase 6**: Dashboard summary of collected ideas across all strategies

## See Also

- Individual strategy `README.md` files in each strategy folder for detailed usage
- `API_SETUP.md` files in Strategies 5, 9, and 13 for API configuration
- `requirements.txt` files in relevant strategy folders for dependencies

---

**Created**: Phase 2 Implementation  
**Last Updated**: Current version supports menu-based selection and flexible strategy execution

