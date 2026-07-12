#!/usr/bin/env python3
"""
Business Idea Formulation Strategy 1: Business Variation & Complaint Fixing

URL-cited online discovery intake (task §11 Phase B).
seed_businesses.json retired — use --inputs or interactive URL paste.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from complaint_intake import interactive_collect_businesses, parse_inputs_payload
from variation_prompts import build_prompt_1a_payload, build_prompt_1b_scaffold

STRATEGY_DIR = Path(__file__).resolve().parent
DEFAULT_INPUTS_FIXTURE = STRATEGY_DIR / "fixtures" / "sample_inputs.json"

REQUIRED_FILES = {
    "playbook": STRATEGY_DIR / "strategy-1-business-variation.md",
    "prompt_1a": STRATEGY_DIR / "chatgpt_prompt_1a.txt",
    "prompt_1b": STRATEGY_DIR / "chatgpt_prompt_1b.txt",
    "prompt_1c": STRATEGY_DIR / "chatgpt_prompt_1c.txt",
    "readme": STRATEGY_DIR / "README.md",
    "fixture_inputs": DEFAULT_INPUTS_FIXTURE,
}


def print_intro() -> None:
    print("=" * 60)
    print("Strategy 1: Business Variation & Complaint Fixing")
    print("=" * 60)
    print()
    print("Formula:")
    print("  Successful Business + Recurring Complaint = Profitable Variation")
    print()
    print("Not Strategy 6 (niche combination) or Strategy 7 (trending adaptation).")
    print("Intake: online / URL-cited only (seed_businesses.json retired).")
    print()


def check_required_files() -> List[str]:
    missing = []
    print("Files:")
    for label, path in REQUIRED_FILES.items():
        ok = path.exists()
        print(f"  [{'ok' if ok else 'MISSING'}] {label}: {path.name}")
        if not ok:
            missing.append(label)
    print()
    return missing


def resolve_path(path_str: str) -> Path:
    p = Path(path_str)
    if p.is_file():
        return p
    alt = STRATEGY_DIR / path_str
    if alt.is_file():
        return alt
    return p


def run_interactive() -> List[Dict[str, Any]]:
    return interactive_collect_businesses()


def run_non_interactive(*, inputs_path: Path) -> List[Dict[str, Any]]:
    if not inputs_path.exists():
        raise FileNotFoundError(f"Inputs file not found: {inputs_path}")
    data = json.loads(inputs_path.read_text(encoding="utf-8"))
    return parse_inputs_payload(data)


def persist_run(
    businesses: List[Dict[str, Any]],
    *,
    mode: str,
) -> Dict[str, Path]:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = STRATEGY_DIR / f"business_variation_{stamp}.json"
    payload_1a = STRATEGY_DIR / f"strategy1_prompt_1a_payload_{stamp}.txt"
    scaffold_1b = STRATEGY_DIR / f"strategy1_prompt_1b_scaffold_{stamp}.txt"

    record = {
        "strategy": 1,
        "mode": mode,
        "generated_at": datetime.now().isoformat(),
        "formula": "Successful Business + Recurring Complaint = Profitable Variation",
        "intake": "url_cited_online",
        "businesses": businesses,
    }
    json_path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    payload_1a.write_text(build_prompt_1a_payload(businesses), encoding="utf-8")
    scaffold_1b.write_text(build_prompt_1b_scaffold(businesses), encoding="utf-8")
    return {"json": json_path, "prompt_1a": payload_1a, "prompt_1b_scaffold": scaffold_1b}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Strategy 1: Business Variation (URL-cited complaint -> variation)"
    )
    p.add_argument(
        "--non-interactive",
        action="store_true",
        help="No input() prompts; requires --inputs JSON with success_url + source_url",
    )
    p.add_argument(
        "--inputs",
        metavar="PATH",
        help="JSON: businesses[].success_url + complaints[].source_url (http/https)",
    )
    p.add_argument(
        "--seed-ids",
        metavar="IDS",
        help=argparse.SUPPRESS,  # retired; show clear error if used
    )
    p.add_argument(
        "--seeds",
        metavar="PATH",
        help=argparse.SUPPRESS,
    )
    p.add_argument(
        "--check-only",
        action="store_true",
        help="Only verify required files exist; exit 0/1",
    )
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    print_intro()
    print(f"Folder: {STRATEGY_DIR}\n")
    missing = check_required_files()
    if missing:
        print(f"Missing required files: {', '.join(missing)}")
        return 1
    if args.check_only:
        print("Check-only OK.")
        return 0

    if args.seed_ids or args.seeds:
        print(
            "\nError: --seed-ids / --seeds are retired (task §11 Phase B).\n"
            "Use: --non-interactive --inputs Strategy-1-Business-Variation/fixtures/sample_inputs.json\n"
            "Or run interactively and paste http(s) URLs for businesses and complaints."
        )
        return 1

    try:
        if args.non_interactive:
            print("NON-INTERACTIVE MODE (URL-cited inputs)")
            if not args.inputs:
                raise ValueError(
                    "Non-interactive mode requires --inputs <json> "
                    "(each business needs success_url; each complaint needs source_url)"
                )
            inputs_path = resolve_path(args.inputs)
            businesses = run_non_interactive(inputs_path=inputs_path)
            mode = "non-interactive"
        else:
            print("INTERACTIVE MODE (paste online URLs; use --non-interactive for smokes)")
            businesses = run_interactive()
            mode = "interactive"
    except (ValueError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"\nError: {exc}")
        return 1

    paths = persist_run(businesses, mode=mode)
    n_complaints = sum(len(b.get("complaints") or []) for b in businesses)
    print(f"\nCaptured {len(businesses)} business(es), {n_complaints} complaint(s).")
    print(f"  JSON:              {paths['json'].name}")
    print(f"  Prompt 1a payload: {paths['prompt_1a'].name}")
    print(f"  Prompt 1b scaffold:{paths['prompt_1b_scaffold'].name}")
    print("\nTip: also available via run_all_strategies.py (Strategy 1).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
