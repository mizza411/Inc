#!/usr/bin/env python3
"""
Business Idea Formulation Strategy 6: Startup Niche Combination
Automated script to help combine Nigerian startup niches for new business ideas.
"""

import json
import os
import re
import subprocess
import sys
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_SCRAPING = True
except ImportError:
    HAS_SCRAPING = False
    print("Note: Install 'requests' and 'beautifulsoup4' for automatic content fetching:")
    print("  pip install requests beautifulsoup4")


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

class StartupNicheCombiner:
    STARTUPLIST_URL = "https://www.startuplist.africa/startups"
    CRUNCHBASE_NG_URL = "https://www.crunchbase.com/hub/nigeria-startups"

    def __init__(self):
        self.common_niches = [
            "FinTech", "EdTech", "HealthTech", "AgriTech", "PropTech",
            "Logistics", "E-commerce", "FoodTech", "FashionTech", "Entertainment",
            "Real Estate", "Transportation", "Energy", "Insurance", "LegalTech",
            "HRTech", "Marketing", "Social Commerce", "Gaming", "Media"
        ]
        self.nigerian_startups = []
        self.identified_niches = []
        self.combinations = []
        self.output_file = f"niche_combinations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
    def fetch_crunchbase_via_scraping(self) -> Optional[str]:
        """Attempt to scrape Crunchbase Nigerian startups page"""
        if not HAS_SCRAPING:
            return None
        
        try:
            url = "https://www.crunchbase.com/hub/nigeria-startups"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
                element.decompose()
            
            # Try to find startup listings
            startup_list = []
            # Look for common startup listing patterns
            listings = soup.find_all(['div', 'li'], class_=re.compile('startup|company|organization', re.I))
            
            for listing in listings[:50]:  # Limit to 50 startups
                text = listing.get_text(strip=True)
                if text and len(text) > 10:
                    startup_list.append(text)
            
            if startup_list:
                content = '\n'.join(startup_list)
                return content[:8000]  # Truncate to 8000 chars
        except Exception as e:
            print(f"  ⚠ Scraping failed: {str(e)}")
        
        return None

    def fetch_startuplist_via_scraping(self) -> Optional[str]:
        """Attempt to scrape StartupList Africa startups directory."""
        if not HAS_SCRAPING:
            return None

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(self.STARTUPLIST_URL, headers=headers, timeout=20)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
                element.decompose()

            text = " ".join(soup.get_text().split())
            if text:
                return text[:8000]
        except Exception as e:
            print(f"  ⚠ StartupList scrape failed: {str(e)}")

        return None

    def _store_directory_content(self, content: str, source: str) -> str:
        if len(content) > 8000:
            content = content[:8000] + "\n\n[Content truncated for optimal ChatGPT processing]"
        self.crunchbase_content = content
        self.content_source = source
        print(f"\n✓ Collected startup directory content ({len(content)} chars, source={source})")
        return content

    def _collect_crunchbase_fallback(self) -> Optional[str]:
        """Legacy Crunchbase path when StartupList is unavailable."""
        print("\n--- Fallback: Crunchbase (legacy) ---")
        content = None
        if HAS_SCRAPING:
            choice = input("\nFetch Crunchbase content automatically via scraping? (y/n, default=n): ").strip().lower()
            if choice in ("y", "yes"):
                print("  Attempting to scrape Crunchbase...")
                content = self.fetch_crunchbase_via_scraping()
                if content:
                    print(f"  ✓ Scraped {len(content)} characters")
                    return self._store_directory_content(content, "crunchbase_scrape")

        print("\nManual Crunchbase collection:")
        print(f"1. Go to: {self.CRUNCHBASE_NG_URL}")
        print("2. Browse through Nigerian startups")
        print("3. Use Ctrl + A to select all content from the page")
        print("4. Copy and paste here")
        print("\nPress Enter twice when done.\n")
        open_in_chrome(self.CRUNCHBASE_NG_URL)

        lines = []
        print("Paste Crunchbase content (or Enter twice to skip):")
        while True:
            line = input()
            if not line and not lines:
                break
            if not line and lines:
                break
            lines.append(line)

        if lines:
            return self._store_directory_content("\n".join(lines), "crunchbase_manual")
        return None

    def collect_startup_directory_content(self):
        """Step 1: Collect startup directory content (StartupList primary; Crunchbase fallback)."""
        print("\n" + "=" * 60)
        print("STEP 1: Collect Startup Directory Content")
        print("=" * 60)
        print("\nPrimary source: StartupList Africa (Nigeria/Africa startups)")
        print(f"  {self.STARTUPLIST_URL}")
        print("Legacy fallback: Crunchbase Nigeria hub (optional)\n")

        content = None
        if HAS_SCRAPING:
            choice = input(
                "\nFetch StartupList Africa content automatically? (y/n, default=y): "
            ).strip().lower()
            if choice in ("", "y", "yes"):
                print("  Attempting to scrape StartupList Africa...")
                content = self.fetch_startuplist_via_scraping()
                if content:
                    print(f"  ✓ Scraped {len(content)} characters")

        if not content:
            print("\nManual StartupList collection:")
            print(f"1. Go to: {self.STARTUPLIST_URL}")
            print("2. Filter by Nigeria and relevant sectors")
            print("3. Copy startup names, sectors, and notes")
            print("4. Paste below (Enter twice when done)\n")
            open_in_chrome(self.STARTUPLIST_URL)

            lines = []
            print("Paste StartupList content:")
            while True:
                line = input()
                if not line and not lines:
                    break
                if not line and lines:
                    break
                lines.append(line)

            if lines:
                content = "\n".join(lines)

        if content:
            return self._store_directory_content(content, "startuplist_africa")

        print("\nNo StartupList content collected.")
        fallback = input("Try Crunchbase legacy fallback? (y/n, default=n): ").strip().lower()
        if fallback in ("y", "yes"):
            return self._collect_crunchbase_fallback()

        print("No content collected.")
        return None
    
    def collect_crunchbase_content(self):
        """Step 1: Collect Crunchbase content"""
        print("\n" + "="*60)
        print("STEP 1: Collect Crunchbase Content")
        print("="*60)
        
        content = None
        if HAS_SCRAPING:
            choice = input("\nFetch Crunchbase content automatically via scraping? (y/n, default=n): ").strip().lower()
            if choice in ('y', 'yes'):
                print("  Attempting to scrape Crunchbase...")
                content = self.fetch_crunchbase_via_scraping()
                if content:
                    print(f"  ✓ Scraped {len(content)} characters")
        
        if not content:
            print("\nManual collection:")
            print("1. Go to: https://www.crunchbase.com/hub/nigeria-startups")
            print("2. Browse through Nigerian startups")
            print("3. Use Ctrl + A to select all content from the page")
            print("4. Copy and paste here")
            print("\nPress Enter twice when done.\n")

            # Automatically open Crunchbase Nigeria Startups hub in Chrome/default browser
            open_in_chrome("https://www.crunchbase.com/hub/nigeria-startups")
            
            lines = []
            print("Paste Crunchbase content:")
            while True:
                line = input()
                if not line and not lines:
                    break
                if not line and lines:
                    break
                lines.append(line)
            
            if lines:
                content = '\n'.join(lines)
        
        if content:
            # Truncate if too long
            if len(content) > 8000:
                content = content[:8000] + "\n\n[Content truncated for optimal ChatGPT processing]"
            
            self.crunchbase_content = content
            print(f"\n✓ Collected Crunchbase content ({len(content)} characters)")
            return content
        else:
            print("No content collected.")
            return None
    
    def identify_niches(self):
        """Step 2: Identify niches from content"""
        print("\n" + "="*60)
        print("STEP 2: Identify Niches")
        print("="*60)
        
        if not hasattr(self, "crunchbase_content"):
            print("No content collected yet.")
            return
        
        print("\nCommon startup niches:")
        for i, niche in enumerate(self.common_niches, 1):
            print(f"{i}. {niche}")
        
        print(
            "\nEnter additional niches found in the startup directory content "
            "(one per line, Enter twice when done):"
        )
        additional_niches = []
        while True:
            niche = input("Niche: ").strip()
            if not niche:
                break
            additional_niches.append(niche)
        
        self.identified_niches = self.common_niches + additional_niches
        
        print(f"\n✓ Identified {len(self.identified_niches)} niches:")
        for niche in self.identified_niches:
            print(f"  - {niche}")
        
        return self.identified_niches
    
    def generate_combinations(self):
        """Step 3: Generate niche combinations"""
        print("\n" + "="*60)
        print("STEP 3: Generate Combinations")
        print("="*60)
        
        if not self.identified_niches:
            print("No niches identified yet.")
            return
        
        print("\nSelect 2-5 niches to combine (enter numbers separated by commas):")
        for i, niche in enumerate(self.identified_niches, 1):
            print(f"{i}. {niche}")
        
        selection = input("\nSelection: ").strip()
        indices = [int(x.strip()) - 1 for x in selection.split(',')]
        selected_niches = [self.identified_niches[i] for i in indices if 0 <= i < len(self.identified_niches)]
        
        if len(selected_niches) < 2:
            print("Please select at least 2 niches.")
            return
        
        print(f"\nSelected niches: {', '.join(selected_niches)}")
        
        # Generate combination ideas
        print("\nGenerating combination ideas...")
        combinations = []
        
        # Primary combination
        combo_name = " + ".join(selected_niches)
        combinations.append({
            'niches': selected_niches,
            'combination': combo_name,
            'description': f"Combining {combo_name} to create innovative solutions"
        })
        
        # Additional combinations with other niches
        print("\nWould you like to combine these with other niches? (y/n):")
        if input().strip().lower() == 'y':
            print("\nSelect additional niches to combine with the selected ones:")
            for i, niche in enumerate(self.identified_niches, 1):
                if niche not in selected_niches:
                    print(f"{i}. {niche}")
            
            additional_selection = input("\nSelection (numbers separated by commas): ").strip()
            additional_indices = [int(x.strip()) - 1 for x in additional_selection.split(',')]
            additional_niches = [self.identified_niches[i] for i in additional_indices if 0 <= i < len(self.identified_niches)]
            
            for add_niche in additional_niches:
                combo = selected_niches + [add_niche]
                combinations.append({
                    'niches': combo,
                    'combination': " + ".join(combo),
                    'description': f"Combining {', '.join(combo)} for unique solutions"
                })
        
        self.combinations = combinations
        
        print(f"\n✓ Generated {len(combinations)} combination ideas:")
        for i, combo in enumerate(combinations, 1):
            print(f"{i}. {combo['combination']}")
        
        return combinations
    
    def generate_chatgpt_prompt_1a(self):
        """Step 4: Generate ChatGPT Prompt 1a"""
        print("\n" + "="*60)
        print("STEP 4: Generate ChatGPT Prompt 1a")
        print("="*60)
        
        if not hasattr(self, "crunchbase_content"):
            print("No startup directory content collected yet.")
            return
        
        source = getattr(self, "content_source", "startup_directory")
        prompt = (
            "First, assess Nigerian startups in the content below (from "
            f"{source}), then combine the startup niche with other niches "
            "(these other niches do not compulsorily have to be present in the "
            "content) in order to generate new startup ideas.\n\n"
        )
        prompt += f"{self.crunchbase_content}\n\n"
        prompt += "Please generate new startup ideas by combining different niches."
        
        with open('chatgpt_prompt_1a.txt', 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        print("\n✓ Prompt 1a generated and saved to 'chatgpt_prompt_1a.txt'")
        print("\nYou can now use this prompt in ChatGPT.")
        
        return prompt
    
    def generate_chatgpt_prompt_1b(self):
        """Step 5: Generate ChatGPT Prompt 1b for viable ideas"""
        print("\n" + "="*60)
        print("STEP 5: Generate ChatGPT Prompt 1b")
        print("="*60)
        
        print("\nEnter the viable ideas from ChatGPT response (one per line, Enter twice when done):")
        viable_ideas = []
        while True:
            idea = input("Viable idea: ").strip()
            if not idea:
                break
            viable_ideas.append(idea)
        
        if not viable_ideas:
            print("No viable ideas entered.")
            return
        
        prompts = []
        for idea in viable_ideas:
            prompt_1b = f"""Tabulate output for "{idea}" (Columns: Problem Identified/Potential Digital Solution/Estimated daily sales/ Actualization strategy, Target Audience, Problem it solves, Competition Analysis, Estimated Costs (in dollars), Funding Sources (provide links to possible investors and VCs), No-code Tools to build solution, How to test the viability of the idea, Potential Challenges, Solution to those potential challenges, landing page platform, Monetization Strategy, Market Size and Growth Potential, Technical Expertise and Skill Requirements, Partnerships and Collaboration, Timeline, Key Performance Indicators (KPIs), Team Requirements, Time to Market, Required Skills, Risks and Mitigation, Scalability, Social Impact)."""
            
            prompts.append({
                'idea': idea,
                'prompt': prompt_1b
            })
        
        # Save prompts
        with open('chatgpt_prompt_1b.txt', 'w', encoding='utf-8') as f:
            for i, item in enumerate(prompts, 1):
                f.write(f"\n{'='*60}\n")
                f.write(f"Prompt 1b for Idea {i}: {item['idea']}\n")
                f.write(f"{'='*60}\n\n")
                f.write(item['prompt'])
                f.write("\n\n")
        
        print(f"\n✓ Generated {len(prompts)} Prompt 1b variations")
        print("Saved to 'chatgpt_prompt_1b.txt'")
        
        return prompts
    
    def save_data(self):
        """Save all data"""
        data = {
            'identified_niches': self.identified_niches,
            'combinations': self.combinations,
            'timestamp': datetime.now().isoformat()
        }
        
        if hasattr(self, "crunchbase_content"):
            data["content_length"] = len(self.crunchbase_content)
            data["content_source"] = getattr(self, "content_source", "unknown")
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ All data saved to '{self.output_file}'")
        open_file_automatically(self.output_file)
    
    def run(self):
        """Main execution flow"""
        print("\n" + "="*60)
        print("Business Idea Formulation Strategy 6")
        print("Startup Niche Combination")
        print("="*60)
        
        # Step 1: Collect startup directory content (StartupList primary)
        self.collect_startup_directory_content()
        
        # Step 2: Identify niches
        self.identify_niches()
        
        # Step 3: Generate combinations
        self.generate_combinations()
        
        # Step 4: Generate Prompt 1a
        self.generate_chatgpt_prompt_1a()
        
        # Step 5: Generate Prompt 1b (after user gets ideas from ChatGPT)
        input("\nPress Enter after you've used Prompt 1a in ChatGPT and received ideas...")
        self.generate_chatgpt_prompt_1b()
        
        # Save data
        self.save_data()
        
        print("\n" + "="*60)
        print("Process Complete!")
        print("="*60)
        print("\nNext steps:")
        print("1. Use Prompt 1a from 'chatgpt_prompt_1a.txt' in ChatGPT")
        print("2. Review the generated combination ideas")
        print("3. Select viable ideas and use corresponding Prompt 1b")
        print("4. Analyze the detailed business plans")

if __name__ == "__main__":
    combiner = StartupNicheCombiner()
    combiner.run()

