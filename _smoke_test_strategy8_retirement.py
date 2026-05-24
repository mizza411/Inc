#!/usr/bin/env python3
"""One-off smoke checks for Strategy 8 retirement (safe to delete after review)."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> int:
    errors = []

    from run_all_strategies import RETIRED_STRATEGIES, STRATEGY_SCRIPTS

    if 8 in STRATEGY_SCRIPTS:
        errors.append("Strategy 8 still in STRATEGY_SCRIPTS")
    if 8 not in RETIRED_STRATEGIES:
        errors.append("Strategy 8 missing from RETIRED_STRATEGIES")
    if 14 not in STRATEGY_SCRIPTS:
        errors.append("Strategy 14 missing from STRATEGY_SCRIPTS")

    stub = ROOT / "Business-Idea-Formulation-Strategy-8-Trend-Adaptation" / "trend_adapter.py"
    s14 = (
        ROOT
        / "Business-Idea-Formulation-Strategy-14-Global-Data-Trend-Adaptation"
        / "global_trend_adapter.py"
    )
    if not stub.is_file():
        errors.append(f"Stub missing: {stub}")
    if not s14.is_file():
        errors.append(f"Strategy 14 script missing: {s14}")

    result = subprocess.run(
        [sys.executable, str(stub)],
        cwd=stub.parent,
        capture_output=True,
        text=True,
    )
    out = (result.stdout or "") + (result.stderr or "")
    if result.returncode != 0:
        errors.append(f"trend_adapter.py stub exit code {result.returncode}")
    for needle in ("RETIRED", "Strategy 14", "OurWorldInData"):
        if needle not in out:
            errors.append(f"Stub output missing expected text: {needle!r}")

    if errors:
        print("SMOKE TEST FAILED:")
        for e in errors:
            print(f"  - {e}")
        print("\nStub stdout/stderr preview:")
        print(out[:1200])
        return 1

    print("SMOKE TEST OK")
    print(f"  Active strategies: {sorted(STRATEGY_SCRIPTS.keys())}")
    print(f"  Retired: {sorted(RETIRED_STRATEGIES.keys())}")
    print("  trend_adapter.py stub exits 0 with retirement message")
    return 0


if __name__ == "__main__":
    sys.exit(main())
