#!/usr/bin/env python3
"""
Business Idea Formulation Strategy 11: Personal Problem Conversion
Hybrid script to help turn your own problems into structured business ideas.
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
            # Windows: use os.startfile() or subprocess with 'start'
            os.startfile(str(file_path_obj.resolve()))
        elif sys.platform == "darwin":
            # macOS: use 'open' command
            subprocess.run(["open", str(file_path_obj.resolve())])
        else:
            # Linux and other Unix-like systems: use 'xdg-open'
            subprocess.run(["xdg-open", str(file_path_obj.resolve())])
        
        print(f"✓ Opened file automatically: {file_path}")
    except Exception as e:
        print(f"\n⚠ Could not open file automatically ({e}).")
        print(f"Please open manually: {file_path}")


class PersonalProblemConverter:
    def __init__(self):
        self.problems = []
        self.chosen_indices = []
        self.output_file = (
            f"personal_problem_conversion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

    def intro(self):
        print("\n" + "=" * 60)
        print("Business Idea Formulation Strategy 11")
        print("Personal Problem Conversion")
        print("=" * 60)
        print(
            "\nThis script will help you:\n"
            "- List and score your personal problems\n"
            "- Highlight high-frequency, high-pain problems\n"
            "- Generate Prompt 1a text for ChatGPT\n"
            "- Save everything for later review\n"
        )

    def collect_problems(self):
        """Step 1: Collect personal problems with frequency and pain level."""
        print("\n" + "=" * 60)
        print("STEP 1: List Personal Problems")
        print("=" * 60)

        print(
            "\nEnter your personal problems/frustrations (one per block).\n"
            "For each problem, you will be asked:\n"
            "- Frequency (Daily/Weekly/Monthly/Occasional)\n"
            "- Pain level (High/Medium/Low)\n"
            "Press Enter on an empty line when you're done.\n"
        )

        problems = []
        while True:
            desc = input("Problem description (or press Enter to finish): ").strip()
            if not desc:
                break

            freq = input(
                "  Frequency [Daily/Weekly/Monthly/Occasional]: "
            ).strip() or "Occasional"
            pain = input("  Pain level [High/Medium/Low]: ").strip() or "Medium"
            area = input(
                "  Area of life [Home/Work/Finance/Health/Transport/Other]: "
            ).strip() or "Other"

            problems.append(
                {
                    "description": desc,
                    "frequency": freq,
                    "pain": pain,
                    "area": area,
                    "timestamp": datetime.now().isoformat(),
                }
            )
            print()

        self.problems = problems
        print(f"\n✓ Captured {len(problems)} problems.")
        return problems

    def highlight_high_value(self):
        """Step 2: Highlight high-frequency, high-pain problems."""
        print("\n" + "=" * 60)
        print("STEP 2: Highlight High-Value Problems")
        print("=" * 60)

        if not self.problems:
            print("No problems captured yet.")
            return []

        def score(p):
            freq_map = {"Daily": 3, "Weekly": 2, "Monthly": 1, "Occasional": 0}
            pain_map = {"High": 3, "Medium": 2, "Low": 1}
            return freq_map.get(p["frequency"], 0) + pain_map.get(p["pain"], 0)

        scored = [(idx, p, score(p)) for idx, p in enumerate(self.problems)]
        scored.sort(key=lambda x: x[2], reverse=True)

        print("\nProblems ranked by score (Frequency + Pain):\n")
        for idx, prob, sc in scored:
            print(
                f"{idx + 1}. [{prob['area']}] "
                f"{prob['description']} "
                f"(Freq: {prob['frequency']}, Pain: {prob['pain']}, Score: {sc})"
            )

        high_value = [item for item in scored if item[2] >= 4]
        print(f"\n✓ Found {len(high_value)} high-value problems (score ≥ 4).")

        return high_value

    def choose_problems_for_chatgpt(self):
        """Step 3: Let user choose which problems to send to ChatGPT."""
        print("\n" + "=" * 60)
        print("STEP 3: Choose Problems for ChatGPT")
        print("=" * 60)

        if not self.problems:
            print("No problems captured.")
            return []

        print("\nAll problems:")
        for idx, p in enumerate(self.problems, 1):
            print(
                f"{idx}. [{p['area']}] {p['description']} "
                f"(Freq: {p['frequency']}, Pain: {p['pain']})"
            )

        sel = input(
            "\nEnter numbers of problems to analyze with ChatGPT "
            "(comma-separated, e.g. 1,3,4): "
        ).strip()

        chosen_indices = []
        if sel:
            for part in sel.split(","):
                try:
                    i = int(part.strip()) - 1
                    if 0 <= i < len(self.problems):
                        chosen_indices.append(i)
                except ValueError:
                    continue

        self.chosen_indices = chosen_indices
        print(f"\n✓ Selected {len(chosen_indices)} problems for ChatGPT prompts.")
        return chosen_indices

    def generate_prompts_file(self):
        """Step 4: Generate Prompt 1a text for selected problems."""
        print("\n" + "=" * 60)
        print("STEP 4: Generate Prompt 1a Text")
        print("=" * 60)

        if not self.chosen_indices:
            print("No problems selected; skipping prompt generation.")
            return None

        filename = "chatgpt_strategy11_prompt_1a.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(
                "PROMPT 1a TEMPLATES for Personal Problem Conversion\n"
                "(Use each block separately in ChatGPT):\n\n"
            )
            for num, idx in enumerate(self.chosen_indices, 1):
                p = self.problems[idx]
                prompt = (
                    "Based on this personal problem:\n"
                    f"\"{p['description']}\"\n\n"
                    "Generate digital business ideas (web apps, mobile apps, platforms, "
                    "or IT solutions) that could solve it. Then, for the best idea, "
                    "tabulate output with these columns: Problem Identified/Potential "
                    "Digital Solution/Estimated daily sales/ Actualization strategy, "
                    "Target Audience, Problem it solves, Competition Analysis, "
                    "Estimated Costs (in dollars), Funding Sources (provide links to "
                    "possible investors and VCs), No-code Tools to build solution, "
                    "How to test the viability of the idea, Potential Challenges, "
                    "Solution to those potential challenges, landing page platform, "
                    "Monetization Strategy, Market Size and Growth Potential, "
                    "Technical Expertise and Skill Requirements, Partnerships and "
                    "Collaboration, Timeline, Key Performance Indicators (KPIs), "
                    "Team Requirements, Time to Market, Required Skills, Risks and "
                    "Mitigation, Scalability, Social Impact."
                )

                f.write(f"{'=' * 60}\n")
                f.write(f"Problem {num}: {p['description']}\n")
                f.write(f"{'=' * 60}\n\n")
                f.write(prompt + "\n\n")

        print(f"\n✓ Prompt 1a templates saved to '{filename}'.")
        print(
            "\nUse them like this:\n"
            "- Open ChatGPT.\n"
            "- Copy one problem block at a time from the file.\n"
            "- Paste it into ChatGPT and run.\n"
        )
        return filename

    def save_summary(self):
        """Step 5: Save JSON summary."""
        data = {
            "strategy": 11,
            "name": "Personal Problem Conversion",
            "timestamp": datetime.now().isoformat(),
            "problems": self.problems,
            "chosen_indices": self.chosen_indices,
        }

        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Summary saved to '{self.output_file}'.")
        open_file_automatically(self.output_file)

    def run(self):
        self.intro()
        self.collect_problems()
        self.highlight_high_value()
        self.choose_problems_for_chatgpt()
        self.generate_prompts_file()
        self.save_summary()

        print("\n" + "=" * 60)
        print("Process Complete!")
        print("=" * 60)
        print(
            "\nNext steps:\n"
            "1. Open 'chatgpt_strategy11_prompt_1a.txt'.\n"
            "2. Paste each block into ChatGPT to get full tables.\n"
            "3. Compare which personal-problem-based ideas are strongest.\n"
        )


if __name__ == "__main__":
    runner = PersonalProblemConverter()
    runner.run()


