#!/usr/bin/env python3
"""
Business Idea Formulation Strategy 14: Global Data Trend Adaptation
Automated script to help adapt OurWorldInData trends for Nigeria.
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

class GlobalTrendAdapter:
    def __init__(self):
        self.topic = ""
        self.page_url = ""
        self.content = ""
        self.viable_ideas = []
        self.localization_notes = []
        self.output_file = f"global_trend_adaptation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Popular OurWorldInData topics
        self.popular_topics = [
            "Economic Development",
            "Healthcare",
            "Education",
            "Technology",
            "Energy",
            "Agriculture",
            "Urbanization",
            "Population",
            "Environment",
            "Food Security"
        ]
        
    def select_topic(self):
        """Step 1: Select OurWorldInData topic"""
        print("\n" + "="*60)
        print("STEP 1: Select OurWorldInData Topic")
        print("="*60)
        
        print("\nPopular topics for Nigeria:")
        for i, topic in enumerate(self.popular_topics, 1):
            print(f"{i}. {topic}")
        
        print("\nSelect a topic (enter number) or enter custom topic:")
        selection = input("Selection: ").strip()
        
        if selection.isdigit() and 1 <= int(selection) <= len(self.popular_topics):
            self.topic = self.popular_topics[int(selection) - 1]
        else:
            self.topic = selection if selection else input("Enter topic: ").strip()
        
        self.page_url = input(f"\nOurWorldInData page URL for '{self.topic}': ").strip()
        
        print(f"\n✓ Selected topic: {self.topic}")
        print(f"  URL: {self.page_url}")

        # Offer to open the selected OurWorldInData page in Chrome/default browser
        if self.page_url:
            choice = input("\nOpen this OurWorldInData page in Chrome now? (y/n, default=y): ").strip().lower()
            if choice in ("", "y", "yes"):
                open_in_chrome(self.page_url)
        
        return self.topic, self.page_url
    
    def fetch_ourworldindata_via_scraping(self, url: str) -> Optional[str]:
        """Attempt to scrape OurWorldInData page"""
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
            for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
                element.decompose()
            
            # Try to find main content (OurWorldInData has structured content)
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile('content|article|post', re.I))
            
            if main_content:
                text = main_content.get_text()
            else:
                text = soup.get_text()
            
            # Clean up whitespace
            lines = [line.strip() for line in text.splitlines()]
            lines = [line for line in lines if line and len(line) > 15]  # Filter short lines
            content = '\n'.join(lines[:400])  # Limit to 400 meaningful lines
            
            return content[:8000]  # Truncate to 8000 chars
        except Exception as e:
            print(f"  ⚠ Scraping failed: {str(e)}")
            return None
    
    def collect_content(self):
        """Step 2: Collect OurWorldInData content"""
        print("\n" + "="*60)
        print("STEP 2: Collect OurWorldInData Content")
        print("="*60)
        
        content = None
        if HAS_SCRAPING and self.page_url:
            choice = input(f"\nFetch content automatically from {self.page_url}? (y/n, default=n): ").strip().lower()
            if choice in ('y', 'yes'):
                print("  Attempting to scrape OurWorldInData...")
                content = self.fetch_ourworldindata_via_scraping(self.page_url)
                if content:
                    print(f"  ✓ Scraped {len(content)} characters")
        
        if not content:
            print("\nManual collection:")
            print("1. Go to the OurWorldInData page")
            print("2. Use Ctrl + A to select all content")
            print("3. Copy and paste here")
            print("\nPress Enter twice when done.\n")
            
            lines = []
            print("Paste OurWorldInData content:")
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
            # Truncate if too long (keep under 8000 chars for best ChatGPT results)
            if len(content) > 8000:
                content = content[:8000] + "\n\n[Content truncated for optimal ChatGPT processing]"
            
            self.content = content
            print(f"\n✓ Collected content ({len(content)} characters)")
            return content
        else:
            print("No content collected.")
            return None
    
    def generate_chatgpt_prompt_1a(self):
        """Step 3: Generate ChatGPT Prompt 1a"""
        print("\n" + "="*60)
        print("STEP 3: Generate ChatGPT Prompt 1a")
        print("="*60)
        
        if not self.content:
            print("No content collected yet.")
            return
        
        prompt = "Give me ideas based on this to implement in Nigeria. Your ideas should be differentiated from the ideas present in the image by combining with a different niche or concept.\n\n"
        prompt += f"Topic: {self.topic}\n"
        prompt += f"Source: {self.page_url}\n\n"
        prompt += f"{self.content}\n\n"
        prompt += "Please generate business ideas that adapt these global trends for the Nigerian market, combining them with relevant niches or concepts."
        
        # Save prompt
        with open('chatgpt_prompt_1a.txt', 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        print("\n✓ Prompt 1a generated and saved to 'chatgpt_prompt_1a.txt'")
        print("\nYou can now use this prompt in ChatGPT.")
        
        return prompt
    
    def collect_viable_ideas(self):
        """Step 4: Collect viable ideas"""
        print("\n" + "="*60)
        print("STEP 4: Collect Viable Ideas")
        print("="*60)
        print("\nEnter viable ideas from ChatGPT response (one per line, Enter twice when done):")
        
        ideas = []
        while True:
            idea = input("Viable idea: ").strip()
            if not idea:
                break
            ideas.append(idea)
        
        self.viable_ideas = ideas
        print(f"\n✓ Collected {len(ideas)} viable ideas")
        return ideas
    
    def generate_chatgpt_prompt_1b(self):
        """Step 5: Generate ChatGPT Prompt 1b"""
        print("\n" + "="*60)
        print("STEP 5: Generate ChatGPT Prompt 1b")
        print("="*60)
        
        if not self.viable_ideas:
            print("No viable ideas collected yet.")
            return
        
        prompts = []
        for idea in self.viable_ideas:
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
    
    def create_localization_checklist(self):
        """Step 6: Create localization checklist"""
        print("\n" + "="*60)
        print("STEP 6: Localization Checklist")
        print("="*60)
        
        checklist_items = [
            "Infrastructure: Does Nigeria have the required infrastructure?",
            "Cost: Can Nigerians afford this solution?",
            "Culture: Does this fit Nigerian cultural values?",
            "Regulations: Are there any regulatory barriers?",
            "Market Size: Is the market large enough?",
            "Competition: Who else is addressing this?",
            "Partnerships: What local partnerships are needed?",
            "Language: Does this need to be in local languages?"
        ]
        
        print("\nNigerian Localization Checklist:")
        print("Review each idea against these criteria:\n")
        
        for i, item in enumerate(checklist_items, 1):
            print(f"{i}. {item}")
        
        # Save checklist
        with open('localization_checklist.txt', 'w', encoding='utf-8') as f:
            f.write("Nigerian Localization Checklist\n")
            f.write("="*60 + "\n\n")
            f.write("Review each viable idea against these criteria:\n\n")
            for i, item in enumerate(checklist_items, 1):
                f.write(f"{i}. [ ] {item}\n")
            f.write("\n" + "="*60 + "\n")
            f.write("\nFor each viable idea, document your findings:\n\n")
            for idea in self.viable_ideas:
                f.write(f"\nIdea: {idea}\n")
                f.write("-" * 60 + "\n")
                for item in checklist_items:
                    f.write(f"[ ] {item}\n")
                f.write("\n")
        
        print("\n✓ Localization checklist saved to 'localization_checklist.txt'")
        
        # Collect localization notes
        print("\nEnter localization notes for each idea (optional):")
        for idea in self.viable_ideas:
            print(f"\nIdea: {idea}")
            notes = input("Localization notes (or Enter to skip): ").strip()
            if notes:
                self.localization_notes.append({
                    'idea': idea,
                    'notes': notes
                })
        
        return checklist_items
    
    def save_data(self):
        """Save all data"""
        data = {
            'topic': self.topic,
            'page_url': self.page_url,
            'content_length': len(self.content) if self.content else 0,
            'viable_ideas': self.viable_ideas,
            'localization_notes': self.localization_notes,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ All data saved to '{self.output_file}'")
        open_file_automatically(self.output_file)
    
    def run(self):
        """Main execution flow"""
        print("\n" + "="*60)
        print("Business Idea Formulation Strategy 14")
        print("Global Data Trend Adaptation")
        print("="*60)
        
        # Step 1: Select topic
        self.select_topic()
        
        # Step 2: Collect content
        self.collect_content()
        
        # Step 3: Generate Prompt 1a
        self.generate_chatgpt_prompt_1a()
        
        # Step 4: Collect viable ideas
        input("\nPress Enter after you've used Prompt 1a in ChatGPT and received ideas...")
        self.collect_viable_ideas()
        
        # Step 5: Generate Prompt 1b
        self.generate_chatgpt_prompt_1b()
        
        # Step 6: Create localization checklist
        self.create_localization_checklist()
        
        # Save data
        self.save_data()
        
        print("\n" + "="*60)
        print("Process Complete!")
        print("="*60)
        print("\nNext steps:")
        print("1. Use Prompt 1a from 'chatgpt_prompt_1a.txt' in ChatGPT")
        print("2. Review generated ideas and select viable ones")
        print("3. Use corresponding Prompt 1b for detailed analysis")
        print("4. Complete localization checklist for Nigerian market")
        print("5. Adapt ideas based on localization findings")

if __name__ == "__main__":
    adapter = GlobalTrendAdapter()
    adapter.run()

