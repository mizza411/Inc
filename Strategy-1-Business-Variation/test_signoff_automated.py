#!/usr/bin/env python3
"""
Automate former MANUAL_TEST.md steps A–D for Strategy 1 (no human Hub clicks).

A Hub Formulated card  -> launcher config + resolve paths + Hub command target runs
B Established cards     -> launcher config + folders exist
C Master runner menu    -> stdin-driven menu (select 1/2/5, cancel launches)
D Playbook intact       -> required sections present in markdown
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def run(
    cmd: list[str],
    *,
    cwd: Path,
    stdin: str | None = None,
    timeout: int = 120,
) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        input=stdin,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def check_hub_formulated(errors: list[str]) -> None:
    """Former MANUAL A — without tray GUI."""
    sys.path.insert(0, str(REPO))
    from inc_launcher.config import list_pillars, load_config, resolve_path

    config = load_config()
    formulated = next(p for p in list_pillars(config) if p["id"] == "formulated")
    by_id = {i.get("id"): i for i in formulated.get("items", []) if i.get("id")}
    if "strategy1_run" not in by_id:
        errors.append("A: formulated missing strategy1_run")
        return
    item = by_id["strategy1_run"]
    if "Business Variation" not in item.get("label", ""):
        errors.append(f"A: unexpected label {item.get('label')!r}")
    if "business_variation_collector.py" not in item.get("command", ""):
        errors.append("A: strategy1_run command missing collector script")
    cwd = item.get("cwd") or "."
    cwd_path = resolve_path(cwd)
    if not cwd_path.is_dir():
        errors.append(f"A: strategy1_run cwd missing: {cwd_path}")

    # Same entrypoint Hub would invoke — non-interactive so it cannot hang
    r = run(
        [
            sys.executable,
            str(ROOT / "business_variation_collector.py"),
            "--non-interactive",
            "--inputs",
            str(ROOT / "fixtures" / "sample_inputs.json"),
        ],
        cwd=ROOT,
        timeout=90,
    )
    if r.returncode != 0:
        errors.append(f"A: Hub command target failed: {r.stderr or r.stdout}")


def check_established(errors: list[str]) -> None:
    """Former MANUAL B."""
    sys.path.insert(0, str(REPO))
    from inc_launcher.config import list_pillars, load_config, resolve_path

    config = load_config()
    established = next(p for p in list_pillars(config) if p["id"] == "established")
    folder_item = next(
        (i for i in established["items"] if "Strategy 1 folder" in i.get("label", "")),
        None,
    )
    gadget_item = next(
        (i for i in established["items"] if "Gadget business automation" in i.get("label", "")),
        None,
    )
    if not folder_item:
        errors.append("B: Established missing Strategy 1 folder card")
    else:
        p = resolve_path(folder_item["path"])
        if not p.is_dir():
            errors.append(f"B: Strategy 1 folder path missing: {p}")
    if not gadget_item:
        errors.append("B: Established missing Gadget business automation card")
    else:
        p = resolve_path(gadget_item["path"])
        if not p.is_dir():
            errors.append(f"B: gadget path missing: {p}")


def check_master_runner_menu(errors: list[str]) -> None:
    """Former MANUAL C — drive menu with stdin; cancel runs that would be interactive."""
    # 3=one strategy, 1, n=cancel; 3, 2=verbal; 3, 5, n=cancel; 4=exit
    stdin = "\n".join(["3", "1", "n", "3", "2", "3", "5", "n", "4", ""])
    r = run(
        [sys.executable, str(REPO / "run_all_strategies.py")],
        cwd=REPO,
        stdin=stdin,
        timeout=60,
    )
    out = (r.stdout or "") + (r.stderr or "")
    if "Selected: Strategy 1" not in out and "Strategy 1 -" not in out:
        # Menu prints: Selected: Strategy 1 - Business Variation...
        if "Business Variation" not in out or "Strategy 1" not in out:
            errors.append(f"C: menu did not select Strategy 1 cleanly\n---\n{out[-2000:]}")
    if "verbal" not in out.lower() or "Strategy 2" not in out:
        errors.append(f"C: Strategy 2 verbal path missing\n---\n{out[-1500:]}")
    if "Strategy 5" not in out:
        errors.append(f"C: Strategy 5 not offered/selected\n---\n{out[-1500:]}")
    if "Exiting master runner" not in out and r.returncode not in (0,):
        # Exit via 4 should print Exiting
        if "Exiting" not in out:
            errors.append(f"C: menu did not exit cleanly (code={r.returncode})")

    # parse_selection unit check (no menu)
    sys.path.insert(0, str(REPO))
    import run_all_strategies as m

    if m.parse_selection("1") != [1]:
        errors.append("C: parse_selection('1') failed")
    if m.parse_selection("1,5") != [1, 5]:
        errors.append("C: parse_selection('1,5') failed")
    if 1 not in m.STRATEGY_SCRIPTS or 5 not in m.STRATEGY_SCRIPTS:
        errors.append("C: STRATEGY_SCRIPTS missing 1 or 5")


def check_playbook(errors: list[str]) -> None:
    """Former MANUAL D — structural playbook checks (not subjective tone)."""
    path = ROOT / "strategy-1-business-variation.md"
    if not path.is_file():
        errors.append("D: playbook missing")
        return
    text = path.read_text(encoding="utf-8")
    required = [
        "Technical status",
        "Successful Business + Recurring Complaint = Profitable Variation",
        "Core Strategy",
        "Choose a Successful Business",
        "Collect Complaints",
        "business_variation_collector.py",
    ]
    for needle in required:
        if needle not in text:
            errors.append(f"D: playbook missing section/marker: {needle!r}")


def main() -> int:
    errors: list[str] = []
    check_hub_formulated(errors)
    check_established(errors)
    check_master_runner_menu(errors)
    check_playbook(errors)

    if errors:
        print("FAIL Strategy 1 automated sign-off (former MANUAL A-D)")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("PASS Strategy 1 automated sign-off (former MANUAL A-D)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
