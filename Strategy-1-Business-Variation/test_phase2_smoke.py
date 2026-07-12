#!/usr/bin/env python3
"""Automated smoke for Strategy 1 Phase 2 (no input())."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COLLECTOR = ROOT / "business_variation_collector.py"
FIXTURE = ROOT / "fixtures" / "sample_inputs.json"


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def main() -> int:
    errors: list[str] = []

    r1 = run([sys.executable, str(COLLECTOR), "--check-only"])
    if r1.returncode != 0:
        errors.append(f"--check-only failed: {r1.stderr or r1.stdout}")

    before = set(ROOT.glob("business_variation_*.json"))
    r2 = run(
        [
            sys.executable,
            str(COLLECTOR),
            "--non-interactive",
            "--inputs",
            str(FIXTURE),
        ]
    )
    if r2.returncode != 0:
        errors.append(f"--inputs run failed ({r2.returncode}): {r2.stderr or r2.stdout}")
    else:
        after = set(ROOT.glob("business_variation_*.json"))
        new = after - before
        if not new:
            errors.append("expected new business_variation_*.json after --inputs run")
        else:
            latest = max(new, key=lambda p: p.stat().st_mtime)
            data = json.loads(latest.read_text(encoding="utf-8"))
            if data.get("strategy") != 1:
                errors.append("JSON strategy != 1")
            if len(data.get("businesses") or []) < 2:
                errors.append("expected >=2 businesses in fixture output")
            stamp = latest.stem.replace("business_variation_", "")
            p1a = ROOT / f"strategy1_prompt_1a_payload_{stamp}.txt"
            if not p1a.exists():
                errors.append(f"missing prompt 1a payload: {p1a.name}")

    r3 = run(
        [
            sys.executable,
            str(COLLECTOR),
            "--non-interactive",
            "--seed-ids",
            "jumia_food,bolt",
        ]
    )
    if r3.returncode != 0:
        errors.append(f"--seed-ids run failed: {r3.stderr or r3.stdout}")

    # Confirm Strategy 1 IS registered in master runner (Phase 3)
    r4 = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import run_all_strategies as r; "
                "assert 1 in r.STRATEGY_SCRIPTS; "
                "assert r.STRATEGY_SCRIPTS[1].exists(); "
                "print('ok')"
            ),
        ],
        cwd=str(ROOT.parent),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if r4.returncode != 0:
        errors.append(f"runner registration check failed: {r4.stderr or r4.stdout}")

    if errors:
        print("FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("PASS Strategy 1 Phase 2 smoke")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
