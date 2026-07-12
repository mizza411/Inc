#!/usr/bin/env python3
"""Smoke: Strategy 1 keys in agent_strategy_run fetch (no network required for S1)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RUNNER = REPO / "agent-business-idea-runs" / "agent_strategy_run.py"
PROMPT = REPO / "prompts" / "agent_formulation_run.txt"


def main() -> int:
    errors: list[str] = []

    # Unit-style: fetch_strategy1_seeds without full network fetch
    sys.path.insert(0, str(RUNNER.parent))
    import agent_strategy_run as asr  # noqa: E402

    s1 = asr.fetch_strategy1_seeds()
    if s1.get("status") != "ok":
        errors.append(f"fetch_strategy1_seeds status={s1.get('status')} err={s1.get('error')}")
    elif not s1.get("businesses"):
        errors.append("strategy_1_seeds businesses empty")

    # Prompt includes Strategy 1
    prompt = PROMPT.read_text(encoding="utf-8")
    if "include strategies 1," not in prompt and "strategies 1, 5" not in prompt:
        errors.append("agent_formulation_run.txt missing Strategy 1 in include list")
    if "strategy_1_seeds" not in prompt:
        errors.append("agent prompt missing strategy_1_seeds guidance")
    if "Successful Business + Recurring Complaint" not in prompt:
        errors.append("agent prompt missing Strategy 1 formula")

    # Full fetch-only should still write JSON with strategy_1_seeds (may hit network for RSS)
    before = set((REPO / "agent-business-idea-runs" / "inputs").glob("agent_strategy_inputs_*.json"))
    r = subprocess.run(
        [sys.executable, str(RUNNER), "--fetch-only"],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=180,
    )
    if r.returncode != 0:
        errors.append(f"fetch-only failed: {r.stderr or r.stdout}")
    else:
        after = set((REPO / "agent-business-idea-runs" / "inputs").glob("agent_strategy_inputs_*.json"))
        new = after - before
        if not new:
            # fallback: newest file
            all_files = list((REPO / "agent-business-idea-runs" / "inputs").glob("agent_strategy_inputs_*.json"))
            if not all_files:
                errors.append("no agent_strategy_inputs_*.json written")
            else:
                latest = max(all_files, key=lambda p: p.stat().st_mtime)
                data = json.loads(latest.read_text(encoding="utf-8"))
                if "strategy_1_seeds" not in data:
                    errors.append("latest fetch JSON missing strategy_1_seeds")
                if 2 not in (data.get("strategies_skipped") or []):
                    errors.append("strategies_skipped should include 2")
        else:
            latest = max(new, key=lambda p: p.stat().st_mtime)
            data = json.loads(latest.read_text(encoding="utf-8"))
            if data.get("strategy_1_seeds", {}).get("status") != "ok":
                errors.append(f"payload strategy_1_seeds bad: {data.get('strategy_1_seeds')}")
            if data.get("strategy_1_run", {}).get("status") != "skipped":
                errors.append("default strategy_1_run should be skipped")
            # Prior keys still present
            for key in (
                "strategy_5_9_rss",
                "strategy_6_startup_directory",
                "strategy_7_trending",
                "strategy_14_owid",
                "strategy_15_run",
            ):
                if key not in data:
                    errors.append(f"missing prior key {key}")

    if errors:
        print("FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("PASS Strategy 1 Phase 4 agent wiring")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
