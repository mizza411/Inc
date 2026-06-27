#!/usr/bin/env python3
"""
Original Strategy 10 Visual Content Analysis script, kept for reference only.

Master runner: Strategy 10 is retired from run_all_strategies.py
(manual ChatGPT Vision upload only; no licensed in-repo automation).
See ../DEPRECATED.md and ../visual_content_analyzer.py (stub).
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


class VisualContentStrategyRunner:
    def __init__(self):
        self.project_description = ""
        self.viable_ideas = []
        self.output_file = (
            f"visual_content_strategy10_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

    def intro(self):
        print("\n" + "=" * 60)
        print("Business Idea Formulation Strategy 10")
        print("Visual Content Analysis (ChatGPT Vision)")
        print("=" * 60)
        print(
            "\nThis script will help you:\n"
            "- Describe the image/project you're analyzing\n"
            "- Generate Prompt 1a variants for ChatGPT Vision\n"
            "- Capture the best ideas from ChatGPT\n"
            "- Generate Prompt 1b blocks for detailed business tables\n"
        )

    def describe_project(self):
        """Step 1: Let the user describe the visual content."""
        print("\n" + "=" * 60)
        print("STEP 1: Describe the Image / Project")
        print("=" * 60)

        print(
            "\nExamples:\n"
            "- \"Uncompleted 10-storey commercial building in Lagos\"\n"
            "- \"Newly built residential estate with 50 duplexes\"\n"
            "- \"Shopping mall under construction near a major highway\"\n"
        )
        desc = input("Short description of the project/image: ").strip()
        self.project_description = desc
        if not desc:
            print("No description provided (you can still continue).")
        else:
            print(f"\n✓ Project description recorded: {desc}")
        return desc

    def generate_prompt_1a_variants(self):
        """Step 2: Generate Prompt 1a variants file."""
        print("\n" + "=" * 60)
        print("STEP 2: Generate Prompt 1a Variants")
        print("=" * 60)

        base_intro = ""
        if self.project_description:
            base_intro = (
                f"For context, the project in this image can be described as: "
                f"\"{self.project_description}\".\n\n"
            )

        variant_1 = (
            base_intro
            + "Give me business ideas/solutions that can be proposed to the architects "
            "or the builders of this uncompleted building [or project]."
        )
        variant_2 = (
            base_intro
            + "Give me business ideas/IT solutions that can be proposed to the architects "
            "or the builders of this project."
        )
        variant_3 = (
            base_intro
            + "Give me business ideas/IT solutions that can be proposed to the architects "
            "or the builders of this project to expedite the sales of the project."
        )

        filename = "chatgpt_strategy10_prompt_1a_variants.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(
                "PROMPT 1a VARIANTS (Use with the uploaded image in ChatGPT Vision)\n\n"
            )
            f.write("Variant 1 (Standard):\n")
            f.write(variant_1 + "\n\n")
            f.write("Variant 2 (IT Solutions):\n")
            f.write(variant_2 + "\n\n")
            f.write("Variant 3 (Sales Expediting):\n")
            f.write(variant_3 + "\n")

        print(f"\n✓ Prompt 1a variants saved to '{filename}'.")
        print(
            "\nUse it like this:\n"
            "1. Open ChatGPT (Vision-enabled).\n"
            "2. Upload your project image.\n"
            "3. Copy one of the variants from the file and paste it as your prompt.\n"
        )

        return [variant_1, variant_2, variant_3]

    def collect_viable_ideas(self):
        """Step 3: Capture best ideas from ChatGPT Vision output."""
        print("\n" + "=" * 60)
        print("STEP 3: Enter Viable Ideas from ChatGPT Vision")
        print("=" * 60)

        print(
            "\nAfter running one or more Prompt 1a variants in ChatGPT Vision, "
            "paste/type the best ideas below (one per line). Press Enter twice when done.\n"
        )

        ideas = []
        while True:
            idea = input("Viable idea: ").strip()
            if not idea:
                break
            ideas.append(idea)

        self.viable_ideas = ideas
        print(f"\n✓ Collected {len(ideas)} viable ideas.")
        return ideas

    def generate_prompt_1b_blocks(self):
        """Step 4: Generate Prompt 1b blocks for each idea."""
        print("\n" + "=" * 60)
        print("STEP 4: Generate Prompt 1b Blocks")
        print("=" * 60)

        if not self.viable_ideas:
            print("No viable ideas entered; skipping Prompt 1b generation.")
            return []

        header = (
            "Tabulate output for \"{idea}\" "
            "(Columns: Problem Identified/Potential Digital Solution/"
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

        blocks = []
        for idea in self.viable_ideas:
            text = header.format(idea=idea)
            blocks.append({"idea": idea, "prompt": text})

        filename = "chatgpt_strategy10_prompt_1b.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for idx, item in enumerate(blocks, 1):
                f.write(f"{'=' * 60}\n")
                f.write(f"Prompt 1b for Idea {idx}: {item['idea']}\n")
                f.write(f"{'=' * 60}\n\n")
                f.write(item["prompt"])
                f.write("\n\n")

        print(f"\n✓ Generated {len(blocks)} Prompt 1b blocks.")
        print(f"Saved to '{filename}'.")
        print(
            "\nUsage:\n"
            "- For each idea, paste the relevant Prompt 1b into the SAME ChatGPT chat\n"
            "  where you ran Prompt 1a (with the image uploaded).\n"
            "  This will give you a full table for each image-driven idea.\n"
        )

        return blocks

    def save_summary(self):
        """Step 5: Save JSON summary of this run."""
        data = {
            "strategy": 10,
            "name": "Visual Content Analysis",
            "timestamp": datetime.now().isoformat(),
            "project_description": self.project_description,
            "viable_ideas": self.viable_ideas,
        }

        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Run summary saved to '{self.output_file}'.")
        open_file_automatically(self.output_file)

    def run(self):
        self.intro()
        self.describe_project()
        self.generate_prompt_1a_variants()
        input(
            "\nNow go to ChatGPT (Vision), upload your image, and use one or more "
            "Prompt 1a variants from the text file. Press Enter here when you're "
            "ready to record the best ideas..."
        )
        self.collect_viable_ideas()
        self.generate_prompt_1b_blocks()
        self.save_summary()

        print("\n" + "=" * 60)
        print("Process Complete!")
        print("=" * 60)
        print(
            "\nNext steps:\n"
            "1. Open 'chatgpt_strategy10_prompt_1b.txt'.\n"
            "2. Paste each Prompt 1b into ChatGPT to get detailed tables.\n"
            "3. Compare which image-driven ideas are strongest and worth pursuing.\n"
        )


if __name__ == "__main__":
    runner = VisualContentStrategyRunner()
    runner.run()
