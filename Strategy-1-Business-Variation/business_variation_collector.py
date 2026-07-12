#!/usr/bin/env python3
"""
Business Idea Formulation Strategy 1: Business Variation & Complaint Fixing

Phase 2: seed load, complaint intake, Prompt 1a/1b payloads, JSON persist,
         --non-interactive / --inputs / --seeds.
Not wired into run_all_strategies.py until Phase 3.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from complaint_intake import (
    complaints_from_seed_examples,
    interactive_collect_complaints,
    interactive_pick_businesses,
    parse_inputs_payload,
)
from seeds import DEFAULT_SEEDS_PATH, find_seed_by_id, find_seed_by_name, load_seeds
from variation_prompts import build_prompt_1a_payload, build_prompt_1b_scaffold

STRATEGY_DIR = Path(__file__).resolve().parent

REQUIRED_FILES = {
    "playbook": STRATEGY_DIR / "strategy-1-business-variation.md",
    "prompt_1a": STRATEGY_DIR / "chatgpt_prompt_1a.txt",
    "prompt_1b": STRATEGY_DIR / "chatgpt_prompt_1b.txt",
    "prompt_1c": STRATEGY_DIR / "chatgpt_prompt_1c.txt",
    "seeds": STRATEGY_DIR / "seed_businesses.json",
    "readme": STRATEGY_DIR / "README.md",
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


def businesses_from_seed_ids(
    seeds: List[Dict[str, Any]], ids: List[str]
) -> List[Dict[str, Any]]:
    """Non-interactive helper: seed id -> business with example complaints loaded."""
    out: List[Dict[str, Any]] = []
    for raw_id in ids:
        bid = raw_id.strip()
        if not bid:
            continue
        seed = find_seed_by_id(seeds, bid) or find_seed_by_name(seeds, bid)
        if not seed:
            raise ValueError(f"Unknown seed id/name: {bid}")
        entry = {
            "id": seed.get("id"),
            "name": seed["name"],
            "category": seed.get("category") or "",
            "complaints": complaints_from_seed_examples(seed),
        }
        if not entry["complaints"]:
            raise ValueError(f"Seed '{bid}' has no example_complaints")
        out.append(entry)
    if not out:
        raise ValueError("No seed ids resolved")
    return out


def run_interactive(seeds_path: Path) -> List[Dict[str, Any]]:
    seeds = load_seeds(seeds_path)
    picked = interactive_pick_businesses(seeds)
    results: List[Dict[str, Any]] = []
    for biz in picked:
        complaints = interactive_collect_complaints(biz)
        results.append(
            {
                "id": biz.get("id"),
                "name": biz["name"],
                "category": biz.get("category") or "",
                "complaints": complaints,
            }
        )
    return results


def run_non_interactive(
    *,
    inputs_path: Optional[Path],
    seed_ids: Optional[List[str]],
    seeds_path: Path,
) -> List[Dict[str, Any]]:
    if inputs_path:
        if not inputs_path.exists():
            raise FileNotFoundError(f"Inputs file not found: {inputs_path}")
        data = json.loads(inputs_path.read_text(encoding="utf-8"))
        return parse_inputs_payload(data)

    if seed_ids:
        seeds = load_seeds(seeds_path)
        return businesses_from_seed_ids(seeds, seed_ids)

    raise ValueError(
        "Non-interactive mode requires --inputs <json> and/or --seed-ids a,b,c"
    )


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
        "businesses": businesses,
    }
    json_path.write_text(json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")
    payload_1a.write_text(build_prompt_1a_payload(businesses), encoding="utf-8")
    scaffold_1b.write_text(build_prompt_1b_scaffold(businesses), encoding="utf-8")
    return {"json": json_path, "prompt_1a": payload_1a, "prompt_1b_scaffold": scaffold_1b}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Strategy 1: Business Variation (complaint -> variation ideas)"
    )
    p.add_argument(
        "--non-interactive",
        action="store_true",
        help="No input() prompts; use --inputs and/or --seed-ids",
    )
    p.add_argument(
        "--inputs",
        metavar="PATH",
        help="JSON file with businesses[].name + businesses[].complaints[]",
    )
    p.add_argument(
        "--seeds",
        metavar="PATH",
        default=str(DEFAULT_SEEDS_PATH),
        help=f"Path to seed_businesses.json (default: {DEFAULT_SEEDS_PATH.name})",
    )
    p.add_argument(
        "--seed-ids",
        metavar="IDS",
        help="Comma-separated seed ids/names; loads example_complaints (non-interactive)",
    )
    p.add_argument(
        "--check-only",
        action="store_true",
        help="Only verify required files exist; exit 0/1 (Phase 1 smoke)",
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

    seeds_path = resolve_path(args.seeds)
    try:
        if args.non_interactive:
            print("NON-INTERACTIVE MODE")
            seed_ids = (
                [x.strip() for x in args.seed_ids.split(",") if x.strip()]
                if args.seed_ids
                else None
            )
            inputs_path = resolve_path(args.inputs) if args.inputs else None
            # Prefer explicit inputs; if both, merge inputs first then append seed-ids
            businesses: List[Dict[str, Any]] = []
            if inputs_path:
                businesses.extend(
                    run_non_interactive(
                        inputs_path=inputs_path, seed_ids=None, seeds_path=seeds_path
                    )
                )
            if seed_ids:
                businesses.extend(
                    run_non_interactive(
                        inputs_path=None, seed_ids=seed_ids, seeds_path=seeds_path
                    )
                )
            if not businesses:
                raise ValueError(
                    "Provide --inputs and/or --seed-ids with --non-interactive"
                )
            mode = "non-interactive"
        else:
            print("INTERACTIVE MODE (use --non-interactive for agent/smoke runs)")
            businesses = run_interactive(seeds_path)
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
