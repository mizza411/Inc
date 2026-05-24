#!/usr/bin/env python3
"""
ARCHIVED (May 2026) — Do not run for production workflows.

Original Strategy 8 TrendHunter script, kept for reference only.
Active replacement: Strategy 14 (OurWorldInData) via global_trend_adapter.py
Master runner: Strategy 8 is retired from run_all_strategies.py
"""

import json
import os
import re
import subprocess
import sys
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_SCRAPING = True
except ImportError:
    HAS_SCRAPING = False
    print("Note: Install 'requests' and 'beautifulsoup4' for automatic content fetching:")
    print("  pip install requests beautifulsoup4")


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


class TrendAdaptationRunner:
    def __init__(self):
        self.categories = [
            "Technology",
            "Business",
            "Social Good",
            "Health",
            "Finance",
            "Lifestyle",
            "Food",
            "Travel",
            "Fashion",
            "Entertainment",
        ]
        self.trend_content = ""
        self.viable_ideas = []
        self.output_file = (
            f"trend_adaptation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

    def intro(self):
        print("\n" + "=" * 60)
        print("Business Idea Formulation Strategy 8")
        print("Trend Adaptation (TrendHunter)")
        print("=" * 60)
        print(
            "\nThis script will guide you to:\n"
            "- Choose TrendHunter categories to explore\n"
            "- Paste TrendHunter content you copied\n"
            "- Generate Prompt 1a for ChatGPT\n"
            "- Capture viable ideas from ChatGPT\n"
            "- Generate Prompt 1b blocks for detailed tables\n"
        )

    def select_categories(self):
        """Step 1: Suggest categories and let user pick focus areas."""
        print("\n" + "=" * 60)
        print("STEP 1: Select TrendHunter Categories")
        print("=" * 60)

        print("\nRecommended categories on TrendHunter:")
        for idx, cat in enumerate(self.categories, 1):
            print(f"{idx}. {cat}")

        print(
            "\nYou don't have to match these exactly on the site, "
            "but use them as a guide."
        )
        input(
            "\nOpen TrendHunter now, pick 1–3 relevant sections, and press Enter once you've decided where to copy from..."
        )

    def fetch_trendhunter_via_scraping(self, url: str) -> Optional[str]:
        """Attempt to scrape TrendHunter page"""
        if not HAS_SCRAPING:
            return None
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(["script", "style", "nav", "footer", "header", "aside", "ad"]):
                element.decompose()
            
            # Try to find main content
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile('content|main|article', re.I))
            
            if main_content:
                text = main_content.get_text()
            else:
                text = soup.get_text()
            
            # Clean up whitespace
            lines = [line.strip() for line in text.splitlines()]
            lines = [line for line in lines if line and len(line) > 10]
            content = '\n'.join(lines[:300])  # Limit to 300 meaningful lines
            
            return content[:8000]  # Truncate to 8000 chars
        except Exception as e:
            print(f"  ⚠ Scraping failed: {str(e)}")
            return None
    
    def collect_trend_content(self):
        """Step 2: Paste TrendHunter content."""
        print("\n" + "=" * 60)
        print("STEP 2: Collect TrendHunter Content")
        print("=" * 60)

        # Try scraping first if available
        content = None
        if HAS_SCRAPING:
            choice = input("\nFetch TrendHunter content automatically via scraping? (y/n, default=n): ").strip().lower()
            if choice in ('y', 'yes'):
                trendhunter_url = input("Enter TrendHunter page URL (or press Enter to skip): ").strip()
                if trendhunter_url:
                    print("  Attempting to scrape TrendHunter...")
                    content = self.fetch_trendhunter_via_scraping(trendhunter_url)
                    if content:
                        print(f"  ✓ Scraped {len(content)} characters")
        
        if not content:
            print(
                "\nManual collection:\n"
                "1. On a TrendHunter page, press Ctrl + A to select all content.\n"
                "2. Press Ctrl + C to copy.\n"
                "3. Come back here and paste (right-click or Ctrl + V).\n"
                "4. Press Enter on an empty line when you're done.\n"
            )

            lines = []
            while True:
                try:
                    line = input()
                except EOFError:
                    break
                if not line and not lines:
                    break
                if not line and lines:
                    break
                lines.append(line)

            if lines:
                content = "\n".join(lines)
        
        if not content:
            print("\nNo content collected. You can re-run this step later.")
            return None
        # Soft limit for ChatGPT readability
        if len(content) > 8000:
            content = (
                content[:8000]
                + "\n\n[Content truncated for optimal ChatGPT processing]"
            )

        self.trend_content = content
        print(f"\n✓ Collected TrendHunter content ({len(content)} characters).")
        return content

    def generate_prompt_1a(self):
        """Step 3: Generate Prompt 1a text file."""
        print("\n" + "=" * 60)
        print("STEP 3: Generate Prompt 1a")
        print("=" * 60)

        if not self.trend_content:
            print("No TrendHunter content available. Skipping Prompt 1a generation.")
            return None

        base_prompt = (
            "Give me ideas based on this to implement in Nigeria. Your ideas should "
            "be differentiated from the ideas present in the content by combining "
            "with a different niche or concept."
        )

        prompt_1a = base_prompt + "\n\n[TrendHunter content starts below]\n\n"
        prompt_1a += self.trend_content

        with open("chatgpt_strategy8_prompt_1a.txt", "w", encoding="utf-8") as f:
            f.write("PROMPT 1a (Use with pasted TrendHunter text):\n\n")
            f.write(prompt_1a)

        print("\n✓ Prompt 1a saved to 'chatgpt_strategy8_prompt_1a.txt'.")
        print(
            "\nUse it like this:\n"
            "1. Open ChatGPT.\n"
            "2. Paste the content from 'chatgpt_strategy8_prompt_1a.txt'.\n"
            "3. Run it as Prompt 1a and wait for the idea list."
        )

        return prompt_1a

    def collect_viable_ideas(self):
        """Step 4: Capture the best ideas from ChatGPT's response."""
        print("\n" + "=" * 60)
        print("STEP 4: Enter Viable Ideas from ChatGPT")
        print("=" * 60)

        print(
            "\nAfter running Prompt 1a in ChatGPT, paste/type ONLY the best ideas\n"
            "below (one per line). Press Enter twice when you're done.\n"
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
        """Step 5: Generate Prompt 1b blocks for each viable idea."""
        print("\n" + "=" * 60)
        print("STEP 5: Generate Prompt 1b Blocks")
        print("=" * 60)

        if not self.viable_ideas:
            print("No viable ideas entered. Skipping Prompt 1b generation.")
            return []

        header = (
            "Tabulate output for \"{idea}\" "
            "(Columns: Problem Identified/Potential Digital Solution/"
            "Estimated daily sales/ Actualization strategy, Target Audience, "
            "Problem it solves, Competition Analysis, Estimated Costs (in dollars), "
            "Funding Sources (provide links to possible investors and VCs), "
            "No-code Tools to build solution, How to test the viability of the idea, "
            "Potential Challenges, Solution to those challenges, landing page platform, "
            "Monetization Strategy, Market Size and Growth Potential, "
            "Technical Expertise and Skill Requirements, Partnerships and Collaboration, "
            "Timeline, Key Performance Indicators (KPIs), Team Requirements, "
            "Time to Market, Required Skills, Risks and Mitigation, Scalability, "
            "Social Impact)."
        )

        prompts = []
        for idea in self.viable_ideas:
            text = header.format(idea=idea)
            prompts.append({"idea": idea, "prompt": text})

        with open("chatgpt_strategy8_prompt_1b.txt", "w", encoding="utf-8") as f:
            for idx, item in enumerate(prompts, 1):
                f.write(f"{'=' * 60}\n")
                f.write(f"Prompt 1b for Idea {idx}: {item['idea']}\n")
                f.write(f"{'=' * 60}\n\n")
                f.write(item["prompt"])
                f.write("\n\n")

        print(f"\n✓ Generated {len(prompts)} Prompt 1b blocks.")
        print("Saved to 'chatgpt_strategy8_prompt_1b.txt'.")
        print(
            "\nUsage:\n"
            "- For each idea, copy its Prompt 1b into the SAME ChatGPT chat\n"
            "  where you used Prompt 1a.\n"
            "- This will give you the full analysis table for that trend-based idea.\n"
        )

        return prompts

    def save_summary(self):
        """Step 6: Save JSON summary of the run."""
        data = {
            "strategy": 8,
            "name": "Trend Adaptation",
            "timestamp": datetime.now().isoformat(),
            "trend_content_length": len(self.trend_content or ""),
            "viable_ideas": self.viable_ideas,
        }

        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Run summary saved to '{self.output_file}'.")
        open_file_automatically(self.output_file)

    def run(self):
        self.intro()
        self.select_categories()
        self.collect_trend_content()
        self.generate_prompt_1a()
        input(
            "\nNow go to ChatGPT, use Prompt 1a, and wait for trend-based ideas.\n"
            "Press Enter here when you're ready to log viable ideas..."
        )
        self.collect_viable_ideas()
        self.generate_prompt_1b_blocks()
        self.save_summary()
        print("\n" + "=" * 60)
        print("Process Complete!")
        print("=" * 60)
        print(
            "\nNext steps:\n"
            "1. Open 'chatgpt_strategy8_prompt_1b.txt'.\n"
            "2. Paste each Prompt 1b into ChatGPT to get detailed tables.\n"
            "3. Compare which trend-based ideas are strongest for Nigeria.\n"
        )


if __name__ == "__main__":
    runner = TrendAdaptationRunner()
    runner.run()
