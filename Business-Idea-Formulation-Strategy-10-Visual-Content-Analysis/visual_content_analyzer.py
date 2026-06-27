#!/usr/bin/env python3
"""
Strategy 10 entrypoint (retired).

ChatGPT Vision image analysis has no licensed in-repo automation path. This script
exits immediately and points you to active strategies for problem discovery.
"""

import sys
from pathlib import Path

STRATEGY_3_SCRIPT = (
    Path(__file__).resolve().parent.parent
    / "Business-Idea-Formulation-Strategy-3-Network-Based-Problem-Identification"
    / "network_problem_collector.py"
)
STRATEGY_4_SCRIPT = (
    Path(__file__).resolve().parent.parent
    / "Business-Idea-Formulation-Strategy-4-Business-Owner-Problem-Collection"
    / "business_owner_problem_collector.py"
)
STRATEGY_5_SCRIPT = (
    Path(__file__).resolve().parent.parent
    / "Business-Idea-Formulation-Strategy-5-News-Based-Problem-Extraction"
    / "news_problem_extractor.py"
)

DEPRECATION_MESSAGE = """
================================================================================
Strategy 10: Visual Content Analysis — RETIRED (June 2026)
================================================================================

ChatGPT Vision is no longer part of the active workflow:
  - Manual image upload and paste only (no in-repo Vision API)
  - Does not meet this repo's automate-first policy

Use these active strategies instead:
  Strategy 3 — Network-Based Problem Identification (architects, builders, developers)
    Script:  network_problem_collector.py
  Strategy 4 — Business Owner Problem Collection (questionnaires)
    Script:  business_owner_problem_collector.py
  Strategy 5 — News-Based Problem Extraction (construction / real estate news)
    Script:  news_problem_extractor.py

From the repo root:
  python run_all_strategies.py
  -> menu option 3 -> enter 3, 4, or 5

Legacy prompt-helper code (reference only):
  _archive/visual_content_analyzer_legacy.py

See DEPRECATED.md in this folder for details.
================================================================================
""".strip()


def main() -> int:
    print(DEPRECATION_MESSAGE)
    missing = [
        path
        for path in (STRATEGY_3_SCRIPT, STRATEGY_4_SCRIPT, STRATEGY_5_SCRIPT)
        if not path.exists()
    ]
    if missing:
        print("\nWARNING: Expected replacement script(s) not found:")
        for path in missing:
            print(f"  {path}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
