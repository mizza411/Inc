#!/usr/bin/env python3
"""Automated checks for Strategy 1 Phase 3 master-runner wiring (no menu input)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def main() -> int:
    errors: list[str] = []

    # Registration
    r = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import run_all_strategies as m; "
                "assert 1 in m.STRATEGY_SCRIPTS; "
                "assert 1 in m.STRATEGY_META; "
                "assert 2 not in m.STRATEGY_SCRIPTS; "
                "p = m.STRATEGY_SCRIPTS[1]; "
                "assert p.exists(), p; "
                "assert 'Business Variation' in m.STRATEGY_META[1]['name']; "
                "assert m.ACTIVE_RANGE_LABEL.startswith('1'); "
                "keys = sorted(m.STRATEGY_SCRIPTS); "
                "assert keys[0] == 1; "
                "assert 15 in keys; "
                "print('registration_ok', len(keys))"
            ),
        ],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if r.returncode != 0:
        errors.append(f"registration: {r.stderr or r.stdout}")

    # Menu copy should not call Strategy 1 verbal-only
    text = (REPO / "run_all_strategies.py").read_text(encoding="utf-8")
    if "Strategies 1 and 2 are verbal" in text:
        errors.append("stale verbal note still mentions Strategy 1")
    if "Strategy 2 is verbal" not in text and "Strategy 2 is verbal instructions" not in text:
        errors.append("expected Strategy 2-only verbal note")

    # Launch Strategy 1 non-interactive via same path the runner would use (cwd=script parent)
    script = REPO / "Strategy-1-Business-Variation" / "business_variation_collector.py"
    r2 = subprocess.run(
        [
            sys.executable,
            str(script),
            "--non-interactive",
            "--inputs",
            str(REPO / "Strategy-1-Business-Variation" / "fixtures" / "sample_inputs.json"),
        ],
        cwd=str(script.parent),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if r2.returncode != 0:
        errors.append(f"S1 non-interactive launch: {r2.stderr or r2.stdout}")

    # Prior strategies still registered
    for n in (3, 5, 7, 9, 11, 14, 15):
        r3 = subprocess.run(
            [
                sys.executable,
                "-c",
                f"import run_all_strategies as m; assert {n} in m.STRATEGY_SCRIPTS; print('ok')",
            ],
            cwd=str(REPO),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if r3.returncode != 0:
            errors.append(f"strategy {n} missing from runner")

    if errors:
        print("FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("PASS Strategy 1 Phase 3 runner wiring")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
