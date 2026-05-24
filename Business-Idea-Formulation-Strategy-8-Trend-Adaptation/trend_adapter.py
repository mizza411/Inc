#!/usr/bin/env python3
"""
Strategy 8 entrypoint (retired).

TrendHunter has no licensed automation path. This script exits immediately
and points you to Strategy 14 (OurWorldInData).
"""

import sys
from pathlib import Path

STRATEGY_14_DIR = (
    Path(__file__).resolve().parent.parent
    / "Business-Idea-Formulation-Strategy-14-Global-Data-Trend-Adaptation"
)
STRATEGY_14_SCRIPT = STRATEGY_14_DIR / "global_trend_adapter.py"

DEPRECATION_MESSAGE = """
================================================================================
Strategy 8: Trend Adaptation — RETIRED (May 2026)
================================================================================

TrendHunter is no longer part of the active workflow:
  - No official API for automated collection
  - Manual paste / scraping do not meet this repo's automation policy

Use Strategy 14 instead (global trends -> Nigeria):
  Folder:  Business-Idea-Formulation-Strategy-14-Global-Data-Trend-Adaptation
  Script:  global_trend_adapter.py
  Source:  OurWorldInData (open data, clearer license)

From the repo root:
  python run_all_strategies.py
  -> menu option 3 -> enter 14

Or run Strategy 14 directly:
  python "{script}"

Legacy TrendHunter code (reference only):
  _archive/trend_adapter_legacy.py

See DEPRECATED.md in this folder for details.
================================================================================
""".format(script=STRATEGY_14_SCRIPT)


def main() -> int:
    print(DEPRECATION_MESSAGE.strip())
    if not STRATEGY_14_SCRIPT.exists():
        print(
            f"\nWARNING: Expected Strategy 14 script not found at:\n  {STRATEGY_14_SCRIPT}"
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
