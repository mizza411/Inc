"""Run all automated tests for Post-Wedding Comms Pack (no browser required).

Usage: python run_automated_tests.py

Streamlit AppTest can take ~30–60s; this script enforces a timeout so it cannot hang forever.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STREAMLIT_TIMEOUT_SEC = 90


def _run(cmd: list[str], *, timeout: int | None = None) -> int:
    print(f"\n>> {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        cwd=ROOT,
        timeout=timeout,
        text=True,
    )
    return result.returncode


def main() -> int:
    steps: list[tuple[str, list[str], int | None]] = [
        ("P0 logic", [sys.executable, "test_p0_flow.py"], None),
        (
            "LLM providers",
            [sys.executable, "-m", "unittest", "test_generation_providers.py", "-q"],
            None,
        ),
        ("Paystack", [sys.executable, "-m", "unittest", "test_paystack.py", "-q"], None),
        ("Landing smoke", [sys.executable, "-m", "unittest", "test_landing_smoke.py", "-q"], None),
        ("Streamlit UI smoke", [sys.executable, "test_streamlit_p0.py"], STREAMLIT_TIMEOUT_SEC),
    ]
    for name, cmd, timeout in steps:
        code = _run(cmd, timeout=timeout)
        if code != 0:
            print(f"\nFAILED: {name}")
            return code
        print(f"OK: {name}")
    print("\nAll automated tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
