#!/usr/bin/env python3
"""One-off smoke checks for Strategy 10 retirement (safe to delete after review)."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> int:
    errors = []

    from run_all_strategies import RETIRED_STRATEGIES, STRATEGY_SCRIPTS

    if 10 in STRATEGY_SCRIPTS:
        errors.append("Strategy 10 still in STRATEGY_SCRIPTS")
    if 10 not in RETIRED_STRATEGIES:
        errors.append("Strategy 10 missing from RETIRED_STRATEGIES")
    for replacement in (3, 4, 5):
        if replacement not in STRATEGY_SCRIPTS:
            errors.append(f"Strategy {replacement} missing from STRATEGY_SCRIPTS")

    stub = (
        ROOT
        / "Business-Idea-Formulation-Strategy-10-Visual-Content-Analysis"
        / "visual_content_analyzer.py"
    )
    if not stub.is_file():
        errors.append(f"Stub missing: {stub}")

    result = subprocess.run(
        [sys.executable, str(stub)],
        cwd=stub.parent,
        capture_output=True,
        text=True,
    )
    out = (result.stdout or "") + (result.stderr or "")
    if result.returncode != 0:
        errors.append(f"visual_content_analyzer.py stub exit code {result.returncode}")
    for needle in ("RETIRED", "Strategy 3", "Strategy 5"):
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
    print("  visual_content_analyzer.py stub exits 0 with retirement message")
    return 0


if __name__ == "__main__":
    sys.exit(main())
