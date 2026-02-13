#!/usr/bin/env python3
"""
Business Idea Formulation Strategy 12: High-Value Problem Filtering
Hybrid script to score and rank problems by 5 criteria:
Growing, Urgent, Expensive to Solve, Mandatory, Frequent.
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


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


CRITERIA = [
    "Growing",
    "Urgent",
    "Expensive to Solve",
    "Mandatory",
    "Frequent",
]


class HighValueProblemFilter:
    def __init__(self):
        self.problems = []
        self.selected_indices = []
        self.output_file = (
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
            "\nEnter problems you want to evaluate (from news, TrendHunter,\n"
            "personal problems, questionnaires, etc.). For each problem, you\n"
            "can also specify a source/tag. Press Enter on an empty description\n"
            "when you're done.\n"
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
        """Step 2: Score problems against the 5 criteria."""
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

            total = 0
            scores = {}
            for crit in CRITERIA:
                ans = input(f"  {crit}? [Y/N]: ").strip().lower()
                val = 1 if ans in ("y", "yes") else 0
                scores[crit] = val
                total += val

            p["criteria_scores"] = scores
            p["total_score"] = total

        print("\n✓ Scoring complete.")

    def show_ranked_problems(self):
        """Step 3: Display problems ranked by score."""
        print("\n" + "=" * 60)
        print("STEP 3: Ranked Problems")
        print("=" * 60)

        if not self.problems:
            print("No problems available.")
            return []

        ranked = sorted(self.problems, key=lambda x: x["total_score"], reverse=True)

        print("\nProblems ranked by total score (0–5):\n")
        for idx, p in enumerate(ranked, 1):
            src = f"[{p['source']}]" if p["source"] else ""
            print(
                f"{idx}. {src} {p['description']} "
                f"(Score: {p['total_score']}/5, "
                f"Growing:{p['criteria_scores'].get('Growing')}, "
                f"Urgent:{p['criteria_scores'].get('Urgent')}, "
                f"Expensive:{p['criteria_scores'].get('Expensive to Solve')}, "
                f"Mandatory:{p['criteria_scores'].get('Mandatory')}, "
                f"Frequent:{p['criteria_scores'].get('Frequent')})"
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

    def generate_prompts_file(self):
        """Step 5: Generate Prompt 1b-style text for selected problems."""
        print("\n" + "=" * 60)
        print("STEP 5: Generate Prompt Text for ChatGPT")
        print("=" * 60)

        if not self.selected_indices:
            print("No problems selected; skipping prompt generation.")
            return None

        filename = "chatgpt_strategy12_prompts.txt"
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
            "problems": self.problems,
            "selected_indices": self.selected_indices,
        }

        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Summary saved to '{self.output_file}'.")
        open_file_automatically(self.output_file)

    def run(self):
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


if __name__ == "__main__":
    runner = HighValueProblemFilter()
    runner.run()


