#!/usr/bin/env python3
"""Smoke: Strategy 1 discovery key in agent_strategy_run fetch."""

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

    sys.path.insert(0, str(RUNNER.parent))
    import agent_strategy_run as asr  # noqa: E402

    if not hasattr(asr, "build_strategy1_discovery"):
        errors.append("build_strategy1_discovery missing")
    else:
        empty = asr.build_strategy1_discovery(rss=[], startup_directory={}, trending={})
        if empty.get("primary") != "agent_native_web_research":
            errors.append(f"unexpected primary: {empty.get('primary')}")
        if "strategy_1_seeds" in (empty.get("forbidden") or []):
            pass  # expected forbid mention
        sample = asr.build_strategy1_discovery(
            rss=[
                {
                    "source": "techpoint",
                    "articles": [
                        {
                            "title": "OPay AI finance",
                            "link": "https://techpoint.africa/example",
                            "published": "2026-07-10",
                        }
                    ],
                }
            ],
            startup_directory={
                "source": "startuplist_africa",
                "url": "https://www.startuplist.africa/startups",
            },
            trending={
                "source": "product_hunt",
                "products": [
                    {"title": "Basedash SCIM", "link": "https://www.producthunt.com/posts/x"}
                ],
            },
        )
        if sample.get("status") not in ("ok", "agent_web_research_only"):
            errors.append(f"sample discovery status={sample.get('status')}")
        if sample.get("discovery_leads_count", 0) < 2:
            errors.append("expected discovery_leads from sample RSS/PH/directory")

    if hasattr(asr, "fetch_strategy1_seeds"):
        errors.append("fetch_strategy1_seeds should be removed in Phase C")

    prompt = PROMPT.read_text(encoding="utf-8")
    if "include strategies 1," not in prompt and "strategies 1, 5" not in prompt:
        errors.append("agent_formulation_run.txt missing Strategy 1 in include list")
    if "Successful Business + Recurring Complaint" not in prompt:
        errors.append("agent prompt missing Strategy 1 formula")
    if "strategy_1_discovery" not in prompt:
        errors.append("agent prompt missing strategy_1_discovery guidance")
    if "seed_businesses.json" not in prompt or "do not use" not in prompt.lower():
        errors.append("agent prompt must forbid seed_businesses.json as S1 problem evidence")
    if "URL" not in prompt and "url" not in prompt:
        errors.append("agent prompt missing S1 citation/URL requirement")

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
        all_files = list((REPO / "agent-business-idea-runs" / "inputs").glob("agent_strategy_inputs_*.json"))
        latest = max(new or all_files, key=lambda p: p.stat().st_mtime) if (new or all_files) else None
        if latest is None:
            errors.append("no agent_strategy_inputs_*.json written")
        else:
            data = json.loads(latest.read_text(encoding="utf-8"))
            if "strategy_1_seeds" in data:
                errors.append("fetch JSON must not ship strategy_1_seeds after Phase C")
            disc = data.get("strategy_1_discovery") or {}
            if disc.get("primary") != "agent_native_web_research":
                errors.append(f"strategy_1_discovery primary bad: {disc}")
            if data.get("strategy_1_run", {}).get("status") != "skipped":
                errors.append("default strategy_1_run should be skipped")
            if 2 not in (data.get("strategies_skipped") or []):
                errors.append("strategies_skipped should include 2")
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
