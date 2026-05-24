#!/usr/bin/env python3
"""
Phase 4.1 final system testing — E2E create pipeline + full pytest suite.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def run_pytest() -> int:
    print("Running pytest suite (unit + E2E)...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests", "-q", "--tb=short"],
        cwd=ROOT,
    )
    return result.returncode


def run_e2e_smoke() -> None:
    import tempfile

    from core.performance_tracker import ContentPerformanceTracker
    from core.subtitle_generator import SubtitleGenerator
    from main import YouTubeBusinessSystem

    print("\nE2E smoke: full create pipeline (single video)...")
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        system = YouTubeBusinessSystem()
        system.subtitle_generator = SubtitleGenerator(output_dir=tmp_path / "subtitles")
        system.performance_tracker = ContentPerformanceTracker(db_path=tmp_path / "smoke.db")

        result = system.create_complete_video("Launch Smoke Test", "culture", target_minutes=8)
        if not result.get("success"):
            raise RuntimeError(result.get("error", "create_complete_video failed"))

        assert result["subtitles"]["cues"]
        assert Path(result["subtitles"]["srt_path"]).is_file()
        system.performance_tracker.db.close()

    print("  E2E smoke passed.")


def main() -> int:
    print("=" * 60)
    print("PHASE 4.1 — Final system testing")
    print("=" * 60)

    try:
        run_e2e_smoke()
    except Exception as exc:
        print(f"E2E smoke FAILED: {exc}")
        return 1

    code = run_pytest()
    if code == 0:
        print("\nPhase 4.1 test suite: PASSED")
    else:
        print(f"\nPhase 4.1 test suite: FAILED (exit {code})")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
