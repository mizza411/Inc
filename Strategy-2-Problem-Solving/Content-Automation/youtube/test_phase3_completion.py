#!/usr/bin/env python3
"""
Phase 3 completion smoke test — runs offline-safe checks for all Phase 3 deliverables.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run_pytest() -> int:
    print("Running pytest suite...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests", "-q", "--tb=short"],
        cwd=ROOT,
    )
    return result.returncode


def run_cli_smokes() -> bool:
    from main import YouTubeBusinessSystem

    print("\nCLI smoke checks (offline-safe)...")
    system = YouTubeBusinessSystem()

    status = system.get_system_status()
    assert status["components"]["subtitle_generator"] == "ready"

    report = system.topic_analyzer.analyze()
    assert len(report.top_picks) >= 1

    script = system.script_generator.generate_script("Smoke Test Topic", "culture", 8)
    script_data = {
        "title": script.title,
        "hook": script.hook,
        "introduction": script.introduction,
        "main_content": script.main_content,
        "conclusion": script.conclusion,
        "call_to_action": script.call_to_action,
    }
    track = system.subtitle_generator.generate_from_script(script_data)
    assert len(track.cues) >= 1

    research = system.research_engine.analyze_topic("Smoke Test Topic", script_data)
    assert research.research_quality_score >= 0

    print("  All CLI smoke checks passed.")
    return True


def main() -> int:
    print("=" * 60)
    print("PHASE 3.7 — Comprehensive testing")
    print("=" * 60)

    try:
        run_cli_smokes()
    except Exception as exc:
        print(f"CLI smoke checks FAILED: {exc}")
        return 1

    code = run_pytest()
    if code == 0:
        print("\nPhase 3.7 test suite: PASSED")
    else:
        print(f"\nPhase 3.7 test suite: FAILED (exit {code})")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
