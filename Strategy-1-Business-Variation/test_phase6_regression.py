#!/usr/bin/env python3
"""
Strategy 1 Phase 6 regression (automated only).

Static checks + existing Phase 2–4 smokes + prior-strategy registration.
Does not launch the interactive Hub or run_all_strategies menu.
"""

from __future__ import annotations

import json
import py_compile
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def run(cmd: list[str], *, cwd: Path, timeout: int = 240) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def main() -> int:
    errors: list[str] = []

    # --- 6.1 static ---
    runner_text = (REPO / "run_all_strategies.py").read_text(encoding="utf-8")
    if "Strategies 1 and 2 are verbal" in runner_text:
        errors.append("runner still says Strategies 1 and 2 are verbal")
    if "Strategy 2 is verbal" not in runner_text:
        errors.append("runner missing Strategy 2-only verbal note")

    prompt = (REPO / "prompts" / "agent_formulation_run.txt").read_text(encoding="utf-8")
    if "include strategies 1," not in prompt and "strategies 1, 5" not in prompt:
        errors.append("agent prompt missing Strategy 1 include")
    if "Successful Business + Recurring Complaint" not in prompt:
        errors.append("agent prompt missing Strategy 1 formula")
    if "strategy_1_discovery" not in prompt:
        errors.append("agent prompt missing strategy_1_discovery")
    if "seed_businesses.json" not in prompt:
        errors.append("agent prompt must mention seed_businesses.json forbid rule")
    if "URL" not in prompt and "url" not in prompt:
        errors.append("agent prompt missing S1 URL citation rule")

    r_reg = run(
        [
            sys.executable,
            "-c",
            (
                "import run_all_strategies as m\n"
                "assert 1 in m.STRATEGY_SCRIPTS and m.STRATEGY_SCRIPTS[1].exists()\n"
                "assert 2 not in m.STRATEGY_SCRIPTS\n"
                "for n in (3,5,6,7,9,11,12,13,14,15):\n"
                "    assert n in m.STRATEGY_SCRIPTS\n"
                "assert 8 in m.RETIRED_STRATEGIES and 10 in m.RETIRED_STRATEGIES\n"
                "print('ok', len(m.STRATEGY_SCRIPTS))\n"
            ),
        ],
        cwd=REPO,
    )
    if r_reg.returncode != 0:
        errors.append(f"registration: {r_reg.stderr or r_reg.stdout}")

    # py_compile Strategy 1 modules only (do not touch gadget tree)
    for name in (
        "business_variation_collector.py",
        "seeds.py",
        "complaint_intake.py",
        "variation_prompts.py",
    ):
        path = ROOT / name
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as ex:
            errors.append(f"py_compile {name}: {ex}")

    # Gadget ops path still present (untouched existence check)
    gadget = ROOT / "gadget-business" / "gadget-business-automation"
    if not gadget.is_dir():
        errors.append("gadget-business-automation folder missing (should remain untouched)")

    # --- 6.2 existing smokes ---
    for smoke in (
        "test_phase2_smoke.py",
        "test_phase3_runner_smoke.py",
        "test_phase4_agent_smoke.py",
        "test_phase11_signoff.py",
    ):
        r = run([sys.executable, str(ROOT / smoke)], cwd=ROOT)
        if r.returncode != 0:
            errors.append(f"{smoke} FAIL: {r.stdout or r.stderr}")

    # --- 6.3 agent fetch still writes JSON + prior keys ---
    inputs_dir = REPO / "agent-business-idea-runs" / "inputs"
    before = set(inputs_dir.glob("agent_strategy_inputs_*.json"))
    r_fetch = run(
        [sys.executable, str(REPO / "agent-business-idea-runs" / "agent_strategy_run.py"), "--fetch-only"],
        cwd=REPO,
    )
    if r_fetch.returncode != 0:
        errors.append(f"agent fetch-only: {r_fetch.stderr or r_fetch.stdout}")
    else:
        after = set(inputs_dir.glob("agent_strategy_inputs_*.json"))
        new = after - before
        latest = max(new or after, key=lambda p: p.stat().st_mtime) if (new or after) else None
        if latest is None:
            errors.append("no agent_strategy_inputs_*.json after fetch-only")
        else:
            text = latest.read_text(encoding="utf-8")
            for needle in (
                "strategy_1_discovery",
                "strategy_5_9_rss",
                "strategy_6_startup_directory",
                "strategy_7_trending",
                "strategy_14_owid",
                "strategy_15_run",
            ):
                if needle not in text:
                    errors.append(f"fetch JSON missing {needle}")
            if "strategy_1_seeds" in text and '"strategy_1_seeds"' in text:
                # Allow mention inside forbidden notes, but not as a top-level key dump of seed data
                data = json.loads(text)
                if "strategy_1_seeds" in data:
                    errors.append("fetch JSON still has top-level strategy_1_seeds")

    # Launcher config regression (narrow)
    r_pytest = run(
        [
            sys.executable,
            "-m",
            "pytest",
            str(REPO / "inc_launcher" / "tests" / "test_config.py"),
            "-q",
            "--tb=line",
        ],
        cwd=REPO,
    )
    if r_pytest.returncode != 0:
        errors.append(f"inc_launcher test_config: {r_pytest.stdout or r_pytest.stderr}")

    # Former MANUAL_TEST A–D (fully automated)
    r_signoff = run(
        [sys.executable, str(ROOT / "test_signoff_automated.py")],
        cwd=ROOT,
        timeout=180,
    )
    if r_signoff.returncode != 0:
        errors.append(f"signoff automated: {r_signoff.stdout or r_signoff.stderr}")

    if errors:
        print("FAIL Phase 6 regression")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("PASS Strategy 1 Phase 6 regression")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
