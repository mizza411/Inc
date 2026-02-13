#!/usr/bin/env python3
"""
Master Orchestrator: Run Business Idea Formulation Strategies 3–14 from one place.

Phase 1 (implemented):
- Simple, linear runner (run all strategies in fixed order).

Phase 2 (implemented):
- Adds a CLI menu.
- Option to run ALL strategies 3–14.
- Option to run a SELECTED subset (e.g. 3,5,9,13).

Phase 3 (now implemented):
- Option to run ONE strategy (e.g. 5).

Usage:
    python run_all_strategies.py
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parent


STRATEGY_SCRIPTS: Dict[int, Path] = {
    3: ROOT / "Business-Idea-Formulation-Strategy-3-Network-Based-Problem-Identification" / "network_problem_collector.py",
    4: ROOT / "Business-Idea-Formulation-Strategy-4-Business-Owner-Problem-Collection" / "business_owner_problem_collector.py",
    5: ROOT / "Business-Idea-Formulation-Strategy-5-News-Based-Problem-Extraction" / "news_problem_extractor.py",
    6: ROOT / "Business-Idea-Formulation-Strategy-6-Startup-Niche-Combination" / "startup_niche_combiner.py",
    7: ROOT / "Business-Idea-Formulation-Strategy-7-Trending-Startup-Adaptation" / "trending_startup_adapter.py",
    8: ROOT / "Business-Idea-Formulation-Strategy-8-Trend-Adaptation" / "trend_adapter.py",
    9: ROOT / "Business-Idea-Formulation-Strategy-9-Financial-News-Problem-Extraction" / "financial_news_extractor.py",
    10: ROOT / "Business-Idea-Formulation-Strategy-10-Visual-Content-Analysis" / "visual_content_analyzer.py",
    11: ROOT / "Business-Idea-Formulation-Strategy-11-Personal-Problem-Conversion" / "personal_problem_converter.py",
    12: ROOT / "Business-Idea-Formulation-Strategy-12-High-Value-Problem-Filtering" / "problem_filter.py",
    13: ROOT / "Business-Idea-Formulation-Strategy-13-Multi-Source-Comprehensive-Analysis" / "multisource_analyzer.py",
    14: ROOT / "Business-Idea-Formulation-Strategy-14-Global-Data-Trend-Adaptation" / "global_trend_adapter.py",
}


STRATEGY_META: Dict[int, Dict[str, str]] = {
    3: {
        "name": "Network-Based Problem Identification",
        "desc": "Collects problems from your personal/professional network and structures them for analysis.",
    },
    4: {
        "name": "Business Owner Problem Collection",
        "desc": "Uses questionnaires to collect self-identified problems directly from business owners.",
    },
    5: {
        "name": "News-Based Problem Extraction",
        "desc": "Extracts problems from Nigerian news sources (web/RSS/NewsAPI).",
    },
    6: {
        "name": "Startup Niche Combination",
        "desc": "Combines Nigerian startup niches from Crunchbase with other niches to generate ideas.",
    },
    7: {
        "name": "Trending Startup Adaptation",
        "desc": "Uses Crunchbase 'Trending Profiles' + ChatGPT Vision to adapt trending startups for Nigeria.",
    },
    8: {
        "name": "Trend Adaptation",
        "desc": "Adapts global trends from TrendHunter to the Nigerian context.",
    },
    9: {
        "name": "Financial News Problem Extraction",
        "desc": "Extracts problems from Nigerian financial/business news (Nairametrics, Financial Nigeria, BusinessDay).",
    },
    10: {
        "name": "Visual Content Analysis",
        "desc": "Uses ChatGPT Vision on real-estate/project images to generate business/IT solutions.",
    },
    11: {
        "name": "Personal Problem Conversion",
        "desc": "Turns your own recurring personal problems into structured business ideas.",
    },
    12: {
        "name": "High-Value Problem Filtering",
        "desc": "Scores problems on growing/urgent/expensive/mandatory/frequent to find high-value ones.",
    },
    13: {
        "name": "Multi-Source Comprehensive Analysis",
        "desc": "Combines SimilarWeb + AnnualReports.com data into data-backed business ideas.",
    },
    14: {
        "name": "Global Data Trend Adaptation",
        "desc": "Adapts global trends from OurWorldInData to Nigerian opportunities.",
    },
}


def run_strategy(number: int) -> bool:
    """Run a single strategy script as a subprocess. Returns True on success, False on failure."""
    script_path = STRATEGY_SCRIPTS[number]

    if not script_path.exists():
        print(f"\n⚠ Strategy {number}: Script not found at {script_path}")
        return False

    meta = STRATEGY_META.get(number, {})
    name = meta.get("name", f"Strategy {number}")
    desc = meta.get("desc", "").strip()

    print("\n" + "=" * 80)
    print(f"Starting Strategy {number}: {name} ({script_path.name})")
    if desc:
        print(f"Description: {desc}")
    print("=" * 80 + "\n")

    try:
        # Use the same Python interpreter that is running this script.
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=script_path.parent,
        )
        if result.returncode != 0:
            print(f"\n⚠ Strategy {number} exited with code {result.returncode}")
            return False

        print(f"\n✓ Strategy {number} completed successfully.")
        return True
    except KeyboardInterrupt:
        print("\n✋ Execution interrupted by user (Ctrl+C).")
        return False
    except Exception as exc:
        print(f"\n⚠ Error while running Strategy {number}: {exc}")
        return False


def run_sequence(strategy_numbers: List[int]) -> None:
    """Run a sequence of strategies and print a summary at the end."""
    if not strategy_numbers:
        print("\nNo strategies selected. Nothing to run.")
        return

    results: Dict[int, bool] = {}

    for number in strategy_numbers:
        success = run_strategy(number)
        results[number] = success

        if not success:
            choice = input(
                "\nStrategy failed or was interrupted. "
                "Continue with the next strategy? (y/n, default=y): "
            ).strip().lower()
            if choice not in ("", "y", "yes"):
                print("\nStopping further execution as requested.")
                break

    # Summary
    print("\n" + "=" * 80)
    print("Execution Summary")
    print("=" * 80)
    for number in sorted(results.keys()):
        status = "OK" if results[number] else "FAILED"
        print(f"Strategy {number}: {status}")

    print("\nAll done.")


def parse_selection(selection: str) -> List[int]:
    """
    Parse a user string like '3,5,7-9, 14' into a list of valid strategy numbers.
    Invalid or out-of-range entries are ignored.
    """
    numbers: List[int] = []
    if not selection.strip():
        return numbers

    parts = [p.strip() for p in selection.split(",") if p.strip()]
    for part in parts:
        if "-" in part:
            start_str, end_str = [x.strip() for x in part.split("-", 1)]
            if start_str.isdigit() and end_str.isdigit():
                start, end = int(start_str), int(end_str)
                if start > end:
                    start, end = end, start
                for n in range(start, end + 1):
                    if n in STRATEGY_SCRIPTS and n not in numbers:
                        numbers.append(n)
        elif part.isdigit():
            n = int(part)
            if n in STRATEGY_SCRIPTS and n not in numbers:
                numbers.append(n)

    return sorted(numbers)


def main() -> None:
    """Phase 3: menu-based runner for strategies 3–14 with single strategy option."""
    while True:
        print("\n" + "=" * 80)
        print("Business Idea Formulation - Master Runner (Phase 3)")
        print("=" * 80)
        print("\nNote: Strategies 1 and 2 are verbal instructions only (no scripts to run).")
        print("Only Strategies 3–14 are executable scripts.\n")
        print("Available strategies:")
        print("  - Strategy 1: [Verbal instructions only - not a script]")
        print("  - Strategy 2: [Verbal instructions only - not a script]")
        for num in sorted(STRATEGY_SCRIPTS.keys()):
            meta = STRATEGY_META.get(num, {})
            name = meta.get("name", f"Strategy {num}")
            print(f"  - Strategy {num}: {name}")

        print("\nMenu:")
        print("  1) Run ALL strategies (3–14) in order")
        print("  2) Run SELECTED strategies (e.g. 3,5,7-9)")
        print("  3) Run ONE strategy (e.g. 5)")
        print("  4) Exit")

        choice = input("\nChoose an option (1/2/3/4, default=1): ").strip()

        if choice in ("", "1"):
            confirm = input(
                "\nRun ALL strategies 3–14 in order? (y/n, default=y): "
            ).strip().lower()
            if confirm in ("", "y", "yes"):
                run_sequence(sorted(STRATEGY_SCRIPTS.keys()))
            else:
                print("Cancelled running all strategies.")

        elif choice == "2":
            print(
                "\nEnter strategy numbers or ranges, separated by commas.\n"
                "Examples:\n"
                "  3,5,9\n"
                "  3-6\n"
                "  3,5-7,10,14\n"
            )
            selection = input("Your selection: ")
            selected = parse_selection(selection)
            if not selected:
                print("\nNo valid strategies selected. Nothing to run.")
                print("Note: Strategies 1 and 2 are not executable scripts (verbal instructions only).")
            else:
                print(f"\nSelected strategies: {', '.join(str(n) for n in selected)}")
                confirm = input(
                    "Proceed with these strategies? (y/n, default=y): "
                ).strip().lower()
                if confirm in ("", "y", "yes"):
                    run_sequence(selected)
                else:
                    print("Cancelled running selected strategies.")

        elif choice == "3":
            print("\nEnter a single strategy number (3–14):")
            selection = input("Strategy number: ").strip()
            if not selection.isdigit():
                print("\nInvalid input. Please enter a number between 3 and 14.")
            else:
                num = int(selection)
                if num not in STRATEGY_SCRIPTS:
                    print(f"\nStrategy {num} is not available.")
                    print("Note: Strategies 1 and 2 are not executable scripts (verbal instructions only).")
                    print(f"Available strategies: {', '.join(str(n) for n in sorted(STRATEGY_SCRIPTS.keys()))}")
                else:
                    meta = STRATEGY_META.get(num, {})
                    name = meta.get("name", f"Strategy {num}")
                    print(f"\nSelected: Strategy {num} - {name}")
                    confirm = input("Run this strategy? (y/n, default=y): ").strip().lower()
                    if confirm in ("", "y", "yes"):
                        success = run_strategy(num)
                        if success:
                            print(f"\n✓ Strategy {num} completed successfully.")
                        else:
                            print(f"\n⚠ Strategy {num} did not complete successfully.")
                    else:
                        print("Cancelled running the strategy.")

        elif choice == "4":
            print("\nExiting master runner.")
            break
        else:
            print("\nInvalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()


