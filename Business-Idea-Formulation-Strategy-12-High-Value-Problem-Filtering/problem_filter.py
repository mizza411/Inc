#!/usr/bin/env python3
"""
Business Idea Formulation Strategy 12: High-Value Problem Filtering
Hybrid script to score and rank problems by 5 criteria:
Growing, Urgent, Expensive to Solve, Mandatory, Frequent.

Interactive (default): python problem_filter.py
Non-interactive:       python problem_filter.py --non-interactive --inputs fixtures/sample_inputs.json
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from guemf_scoring import (
    CRITERIA,
    apply_cli_scores,
    high_value_indices,
    problems_list_from_payload,
    rank_problems,
    require_complete_cli_scores,
    yn_to_bit,
)

STRATEGY_DIR = Path(__file__).resolve().parent


def open_file_automatically(file_path: str) -> None:
    """
    Automatically open a file in the default system application (text editor/viewer).
    Works cross-platform: Windows, macOS, and Linux.
    """
    try:
        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            print(f"\n⚠ File not found: {file_path}")
            return

        if sys.platform == "win32":
            os.startfile(str(file_path_obj.resolve()))
        elif sys.platform == "darwin":
            subprocess.run(["open", str(file_path_obj.resolve())])
        else:
            subprocess.run(["xdg-open", str(file_path_obj.resolve())])

        print(f"✓ Opened file automatically: {file_path}")
    except Exception as e:
        print(f"\n⚠ Could not open file automatically ({e}).")
        print(f"Please open manually: {file_path}")


class HighValueProblemFilter:
    def __init__(self, *, auto_open: bool = True, output_file: Optional[str] = None):
        self.problems: List[Dict[str, Any]] = []
        self.selected_indices: List[int] = []
        self.auto_open = auto_open
        self.output_file = output_file or (
            f"high_value_problem_filtering_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

    def intro(self):
        print("\n" + "=" * 60)
        print("Business Idea Formulation Strategy 12")
        print("High-Value Problem Filtering")
        print("=" * 60)
        print(
            "\nThis script will help you:\n"
            "- Enter problems from any source\n"
            "- Score them on Growing/Urgent/Expensive/Mandatory/Frequent\n"
            "- Rank them by total score\n"
            "- Generate prompt text for deeper ChatGPT analysis\n"
        )

    def collect_problems(self):
        """Step 1: Enter problems and optional source info."""
        print("\n" + "=" * 60)
        print("STEP 1: Enter Problems to Filter")
        print("=" * 60)

        print(
            "\nEnter problems you want to evaluate (from news, Strategy 14\n"
            "global data, StartupList/Product Hunt, Crunchbase (optional), personal problems, questionnaires, etc.).\n"
            "For each problem, you can also specify a source/tag. Press Enter on\n"
            "an empty description when you're done.\n"
        )

        problems = []
        while True:
            desc = input("Problem description (or press Enter to finish): ").strip()
            if not desc:
                break
            source = input("  Source/Tag (e.g. S5-News, S11-Personal, etc.): ").strip()
            problems.append(
                {
                    "description": desc,
                    "source": source or None,
                    "criteria_scores": {},
                    "total_score": 0,
                    "timestamp": datetime.now().isoformat(),
                }
            )
            print()

        self.problems = problems
        print(f"\n✓ Captured {len(problems)} problems.")
        return problems

    def score_problems(self):
        """Step 2: Score problems against the 5 criteria (interactive Y/N)."""
        print("\n" + "=" * 60)
        print("STEP 2: Score Problems (Yes=1 / No=0)")
        print("=" * 60)

        if not self.problems:
            print("No problems to score.")
            return

        print(
            "\nFor each problem, answer Y/N for whether each criterion applies:\n"
            "- Growing: Becoming more common or severe?\n"
            "- Urgent: Needs to be solved quickly?\n"
            "- Expensive to Solve: Currently costs a lot to handle?\n"
            "- Mandatory: Must be addressed (not optional)?\n"
            "- Frequent: Happens regularly?\n"
        )

        for idx, p in enumerate(self.problems, 1):
            print("\n" + "-" * 60)
            label = (
                f"{idx}. {p['description']}"
                if not p["source"]
                else f"{idx}. [{p['source']}] {p['description']}"
            )
            print(label)

            scores = {}
            for crit in CRITERIA:
                ans = input(f"  {crit}? [Y/N]: ").strip().lower()
                scores[crit] = yn_to_bit(ans)

            apply_cli_scores(p, scores)

        print("\n✓ Scoring complete.")

    def show_ranked_problems(self):
        """Step 3: Display problems ranked by score."""
        print("\n" + "=" * 60)
        print("STEP 3: Ranked Problems")
        print("=" * 60)

        if not self.problems:
            print("No problems available.")
            return []

        ranked = rank_problems(self.problems)

        print("\nProblems ranked by total score (0–5):\n")
        for idx, p in enumerate(ranked, 1):
            src = f"[{p['source']}]" if p.get("source") else ""
            cs = p.get("criteria_scores") or {}
            print(
                f"{idx}. {src} {p['description']} "
                f"(Score: {p['total_score']}/5, "
                f"Growing:{cs.get('Growing')}, "
                f"Urgent:{cs.get('Urgent')}, "
                f"Expensive:{cs.get('Expensive to Solve')}, "
                f"Mandatory:{cs.get('Mandatory')}, "
                f"Frequent:{cs.get('Frequent')})"
            )

        return ranked

    def choose_top_problems(self):
        """Step 4: Choose which high-scoring problems to send to ChatGPT."""
        print("\n" + "=" * 60)
        print("STEP 4: Select High-Value Problems for ChatGPT")
        print("=" * 60)

        if not self.problems:
            print("No problems to select.")
            return []

        print("\nReference (by original index):")
        for i, p in enumerate(self.problems, 1):
            print(
                f"{i}. {p['description']} (Score: {p['total_score']}/5, "
                f"Source: {p['source'] or '-'} )"
            )

        sel = input(
            "\nEnter numbers of problems to analyze with ChatGPT "
            "(comma-separated, e.g. 1,2,5): "
        ).strip()

        chosen = []
        if sel:
            for part in sel.split(","):
                try:
                    i = int(part.strip()) - 1
                    if 0 <= i < len(self.problems):
                        chosen.append(i)
                except ValueError:
                    continue

        self.selected_indices = chosen
        print(f"\n✓ Selected {len(chosen)} problems for prompt generation.")
        return chosen

    def generate_prompts_file(self, prompts_path: Optional[Path] = None):
        """Step 5: Generate Prompt 1b-style text for selected problems."""
        print("\n" + "=" * 60)
        print("STEP 5: Generate Prompt Text for ChatGPT")
        print("=" * 60)

        if not self.selected_indices:
            print("No problems selected; skipping prompt generation.")
            return None

        filename = str(prompts_path) if prompts_path else "chatgpt_strategy12_prompts.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(
                "PROMPT TEMPLATES for High-Value Problems\n"
                "(Use each block separately in ChatGPT):\n\n"
            )

            for num, idx in enumerate(self.selected_indices, 1):
                p = self.problems[idx]
                base_line = (
                    f"High-value problem (score {p['total_score']}/5): "
                    f"{p['description']}"
                )
                prompt = (
                    "Tabulate output for \""
                    + p["description"]
                    + "\" (Columns: Problem Identified/Potential Digital Solution/"
                    "Estimated daily sales/ Actualization strategy, Target Audience, "
                    "Problem it solves, Competition Analysis, Estimated Costs (in dollars), "
                    "Funding Sources (provide links to possible investors and VCs), "
                    "No-code Tools to build solution, How to test the viability of the idea, "
                    "Potential Challenges, Solution to those potential challenges, "
                    "landing page platform, Monetization Strategy, Market Size and Growth Potential, "
                    "Technical Expertise and Skill Requirements, Partnerships and Collaboration, "
                    "Timeline, Key Performance Indicators (KPIs), Team Requirements, Time to Market, "
                    "Required Skills, Risks and Mitigation, Scalability, Social Impact)."
                )

                f.write(f"{'=' * 60}\n")
                f.write(f"Problem {num}: {base_line}\n")
                f.write(f"{'=' * 60}\n\n")
                f.write(prompt + "\n\n")

        print(f"\n✓ Prompt templates saved to '{filename}'.")
        if self.auto_open:
            print(
                "\nUse them like this:\n"
                "- Open ChatGPT.\n"
                "- Copy one problem block at a time from the file.\n"
                "- Paste and run to get the full analysis table.\n"
            )

        return filename

    def save_summary(self):
        """Step 6: Save JSON summary of the run."""
        data = {
            "strategy": 12,
            "name": "High-Value Problem Filtering",
            "timestamp": datetime.now().isoformat(),
            "mode": getattr(self, "_run_mode", "interactive"),
            "problems": self.problems,
            "selected_indices": self.selected_indices,
            "ranked_preview": [
                {
                    "description": p.get("description"),
                    "source": p.get("source"),
                    "total_score": p.get("total_score"),
                    "criteria_scores": p.get("criteria_scores"),
                }
                for p in rank_problems(self.problems)
            ],
        }

        out_path = Path(self.output_file)
        if not out_path.is_absolute():
            out_path = Path.cwd() / out_path
        out_path.parent.mkdir(parents=True, exist_ok=True)

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        self.output_file = str(out_path)
        print(f"\n✓ Summary saved to '{self.output_file}'.")
        if self.auto_open:
            open_file_automatically(self.output_file)
        return self.output_file

    def run(self):
        """Interactive default path (unchanged UX for menu / humans)."""
        self._run_mode = "interactive"
        self.intro()
        self.collect_problems()
        self.score_problems()
        self.show_ranked_problems()
        self.choose_top_problems()
        self.generate_prompts_file()
        self.save_summary()

        print("\n" + "=" * 60)
        print("Process Complete!")
        print("=" * 60)
        print(
            "\nNext steps:\n"
            "1. Open 'chatgpt_strategy12_prompts.txt'.\n"
            "2. Paste each problem block into ChatGPT to get full tables.\n"
            "3. Compare which high-value problems are best to build around.\n"
        )

    def run_noninteractive(
        self,
        inputs_path: Path,
        *,
        select_min_score: Optional[int] = None,
        selected_indices: Optional[List[int]] = None,
        prompts_path: Optional[Path] = None,
    ) -> str:
        """Load pre-scored problems from JSON; no input()."""
        self._run_mode = "non-interactive"
        print("\n" + "=" * 60)
        print("NON-INTERACTIVE MODE (--non-interactive)")
        print("=" * 60)
        print(f"Reading: {inputs_path}")

        raw_text = inputs_path.read_text(encoding="utf-8")
        payload = json.loads(raw_text)
        rows = problems_list_from_payload(payload)

        problems: List[Dict[str, Any]] = []
        for i, row in enumerate(rows):
            if not isinstance(row, dict):
                raise ValueError(f"Problem at index {i} must be an object.")
            desc = (row.get("description") or "").strip()
            if not desc:
                raise ValueError(f"Problem at index {i} missing non-empty 'description'.")
            scores_raw = row.get("criteria_scores")
            if not isinstance(scores_raw, dict):
                raise ValueError(
                    f"Problem at index {i} missing 'criteria_scores' object "
                    "(non-interactive will not invent Y/N)."
                )
            normalized = require_complete_cli_scores(scores_raw)
            problem: Dict[str, Any] = {
                "description": desc,
                "source": row.get("source"),
                "criteria_scores": {},
                "total_score": 0,
                "timestamp": datetime.now().isoformat(),
            }
            apply_cli_scores(problem, normalized)
            problems.append(problem)

        self.problems = problems
        print(f"✓ Loaded and scored {len(problems)} problems.")

        self.show_ranked_problems()

        min_score = select_min_score
        if min_score is None and isinstance(payload, dict):
            min_score = payload.get("select_min_score")
        if min_score is None:
            min_score = 4

        if selected_indices is not None:
            chosen = [i for i in selected_indices if 0 <= i < len(self.problems)]
        elif isinstance(payload, dict) and isinstance(payload.get("selected_indices"), list):
            chosen = [
                int(i)
                for i in payload["selected_indices"]
                if isinstance(i, (int, float)) and 0 <= int(i) < len(self.problems)
            ]
        else:
            chosen = high_value_indices(self.problems, min_score=int(min_score))

        self.selected_indices = chosen
        print(
            f"✓ Selected {len(chosen)} problem(s) for prompts "
            f"(min_score={min_score} or explicit indices)."
        )

        self.generate_prompts_file(prompts_path=prompts_path)
        out = self.save_summary()

        print("\n" + "=" * 60)
        print("Non-interactive process complete!")
        print("=" * 60)
        return out


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Strategy 12 — High-Value Problem Filtering (GUEMF)",
    )
    p.add_argument(
        "--non-interactive",
        action="store_true",
        help="No input() prompts; requires --inputs JSON with complete criteria_scores",
    )
    p.add_argument(
        "--inputs",
        type=str,
        default=None,
        help="Path to inputs JSON (required with --non-interactive)",
    )
    p.add_argument(
        "--output",
        type=str,
        default=None,
        help="Summary JSON output path (default: timestamped file in cwd)",
    )
    p.add_argument(
        "--open",
        action="store_true",
        help="Auto-open summary JSON after save (default on for interactive, off for non-interactive)",
    )
    p.add_argument(
        "--select-min-score",
        type=int,
        default=None,
        help="Non-interactive: auto-select problems with total_score >= N (default 4 or inputs JSON)",
    )
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    if args.non_interactive:
        if not args.inputs:
            print(
                "Non-interactive mode requires --inputs <json>.\n"
                "Example:\n"
                "  python problem_filter.py --non-interactive "
                "--inputs fixtures/sample_inputs.json\n"
                "Schema: fixtures/INPUTS_SCHEMA.md",
                file=sys.stderr,
            )
            return 2
        inputs_path = Path(args.inputs)
        if not inputs_path.is_file():
            print(f"Inputs file not found: {inputs_path}", file=sys.stderr)
            return 2
        auto_open = bool(args.open)
        runner = HighValueProblemFilter(auto_open=auto_open, output_file=args.output)
        try:
            runner.run_noninteractive(
                inputs_path,
                select_min_score=args.select_min_score,
            )
        except (OSError, ValueError, json.JSONDecodeError) as ex:
            print(f"Non-interactive run failed: {ex}", file=sys.stderr)
            return 1
        return 0

    # Interactive default — same as historic menu / bare script launch
    runner = HighValueProblemFilter(auto_open=True, output_file=args.output)
    runner.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
