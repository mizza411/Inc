#!/usr/bin/env python3
"""
Business Idea Formulation Strategy 7: Trending Startup Adaptation
Hybrid script to guide using Crunchbase “Trending Profiles” + ChatGPT Vision.
"""

import json
import os
import subprocess
import sys
import webbrowser
from datetime import datetime
from pathlib import Path


def open_in_chrome(url: str) -> None:
    """
    Open a URL in Google Chrome if possible, otherwise fall back to default browser.
    Designed for Windows first, but works cross‑platform with sensible fallbacks.
    """
    try:
        browser = None

        if os.name == "nt":
            possible_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    browser = webbrowser.get(f'"{path}" %s')
                    break

        if browser is None:
            browser = webbrowser.get()

        browser.open(url)
        print(f"\n✓ Opened in Chrome/default browser: {url}")
    except Exception as e:
        print(f"\n⚠ Could not open browser automatically ({e}).")
        print(f"Please open this link manually: {url}")


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


class TrendingStartupAdapter:
    def __init__(self):
        self.trending_notes = ""
        self.viable_ideas = []
        self.output_file = (
            f"trending_startup_adaptation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

    def intro(self):
        print("\n" + "=" * 60)
        print("Business Idea Formulation Strategy 7")
        print("Trending Startup Adaptation")
        print("=" * 60)
        print(
            "\nThis script will guide you through:\n"
            "- Capturing Crunchbase 'Trending Profiles'\n"
            "- Using ChatGPT Vision with Prompt 1a\n"
            "- Capturing viable ideas from ChatGPT\n"
            "- Generating Prompt 1b blocks for detailed tables\n"
        )

    def guide_trending_capture(self):
        """Guide user to capture Trending Profiles screenshot."""
        print("\n" + "=" * 60)
        print("STEP 1: Capture Trending Profiles on Crunchbase")
        print("=" * 60)

        print("\nFollow these instructions:")
        print("1. Open: https://www.crunchbase.com/")
        print('2. Press Ctrl + F and search for "Trending Profiles"')
        print("3. Scroll to the Trending Profiles section")
        print("4. Take a clear screenshot of that section (showing multiple startups)")
        print("5. Save the screenshot somewhere easy to access")

        # Automatically open Crunchbase in Chrome/default browser
        open_in_chrome("https://www.crunchbase.com/")

        input("\nPress Enter AFTER you have captured and saved the screenshot...")

        notes = input(
            "\n(Optional) Add any notes about the trending startups you observed: "
        ).strip()
        self.trending_notes = notes

    def generate_prompt_1a(self):
        """Generate Prompt 1a text for ChatGPT Vision."""
        print("\n" + "=" * 60)
        print("STEP 2: Generate Prompt 1a for ChatGPT Vision")
        print("=" * 60)

        base_prompt = (
            'Give me ideas based on this to implement in Nigeria. Your ideas should '
            "be differentiated from the ideas present in the image by combining with "
            "a different niche or concept (these different niches do not compulsorily "
            "have to be present in the image) in order to generate new startup ideas)."
        )

        prompt_1a = base_prompt
        if self.trending_notes:
            prompt_1a += (
                "\n\nAdditional context from my manual observation:\n"
                f"{self.trending_notes}\n"
            )

        with open("chatgpt_strategy7_prompt_1a.txt", "w", encoding="utf-8") as f:
            f.write("PROMPT 1a (Use with the Trending Profiles screenshot):\n\n")
            f.write(prompt_1a)

        print("\n✓ Prompt 1a saved to 'chatgpt_strategy7_prompt_1a.txt'")
        print("\nUse it like this:")
        print("1. Open ChatGPT with Vision enabled")
        print("2. Upload the Trending Profiles screenshot")
        print("3. Paste Prompt 1a from 'chatgpt_strategy7_prompt_1a.txt'")
        print("4. Wait for ChatGPT to generate localized, differentiated ideas")

        return prompt_1a

    def collect_viable_ideas(self):
        """Let user type in viable ideas returned by ChatGPT Vision."""
        print("\n" + "=" * 60)
        print("STEP 3: Enter Viable Ideas from ChatGPT Response")
        print("=" * 60)

        print(
            "\nAfter running Prompt 1a in ChatGPT Vision, paste/type the MOST VIABLE\n"
            "ideas below (one per line). Keep them short but clear.\n"
            "Press Enter twice when you are done.\n"
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
        """Generate Prompt 1b text blocks for each viable idea."""
        print("\n" + "=" * 60)
        print("STEP 4: Generate Prompt 1b Blocks")
        print("=" * 60)

        if not self.viable_ideas:
            print("No viable ideas entered. Skipping Prompt 1b generation.")
            return []

        prompts = []
        header = (
            "Tabulate output for \"{idea}\" "
            "(Columns: Problem Identified/Potential Digital Solution/"
            "Estimated daily sales/ Actualization strategy, Target Audience, "
            "Problem it solves, Competition Analysis, Estimated Costs (in dollars), "
            "Funding Sources (provide links to possible investors and VCs), "
            "No-code Tools to build solution, How to test the viability of the idea, "
            "Potential Challenges, Solution to those potential challenges, "
            "landing page platform, Monetization Strategy, "
            "Market Size and Growth Potential, Technical Expertise and "
            "Skill Requirements, Partnerships and Collaboration, Timeline, "
            "Key Performance Indicators (KPIs), Team Requirements, Time to Market, "
            "Required Skills, Risks and Mitigation, Scalability, Social Impact)."
        )

        for idea in self.viable_ideas:
            text = header.format(idea=idea)
            prompts.append({"idea": idea, "prompt": text})

        with open("chatgpt_strategy7_prompt_1b.txt", "w", encoding="utf-8") as f:
            for idx, item in enumerate(prompts, 1):
                f.write(f"{'=' * 60}\n")
                f.write(f"Prompt 1b for Idea {idx}: {item['idea']}\n")
                f.write(f"{'=' * 60}\n\n")
                f.write(item["prompt"])
                f.write("\n\n")

        print(f"\n✓ Generated {len(prompts)} Prompt 1b blocks.")
        print("Saved to 'chatgpt_strategy7_prompt_1b.txt'.")
        print(
            "\nUsage:\n"
            "- For each viable idea, copy its Prompt 1b block into the SAME ChatGPT\n"
            "  conversation where you ran Prompt 1a.\n"
            "- This will produce the detailed table for that idea.\n"
        )

        return prompts

    def save_summary(self):
        """Save a JSON log of this run."""
        data = {
            "strategy": 7,
            "name": "Trending Startup Adaptation",
            "timestamp": datetime.now().isoformat(),
            "trending_notes": self.trending_notes,
            "viable_ideas": self.viable_ideas,
        }

        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Run summary saved to '{self.output_file}'")
        open_file_automatically(self.output_file)

    def run(self):
        self.intro()
        self.guide_trending_capture()
        self.generate_prompt_1a()
        input(
            "\nNow go to ChatGPT, upload the screenshot, use Prompt 1a, "
            "and wait for ideas.\nPress Enter when you have the ideas..."
        )
        self.collect_viable_ideas()
        self.generate_prompt_1b_blocks()
        self.save_summary()
        print("\n" + "=" * 60)
        print("Process Complete!")
        print("=" * 60)
        print(
            "\nNext steps:\n"
            "1. Open 'chatgpt_strategy7_prompt_1b.txt'.\n"
            "2. For each idea, paste the corresponding Prompt 1b into ChatGPT.\n"
            "3. Save the tables and compare which ideas are strongest.\n"
        )


if __name__ == "__main__":
    adapter = TrendingStartupAdapter()
    adapter.run()


