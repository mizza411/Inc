#!/usr/bin/env python3
"""
Business Idea Formulation Strategy 9: Financial News Problem Extraction
Hybrid script to help extract business problems from Nigerian financial news.
"""

import json
import os
import re
import subprocess
import sys
import webbrowser
from datetime import datetime
import calendar
from pathlib import Path
from typing import Optional, List, Dict

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_SCRAPING = True
except ImportError:
    HAS_SCRAPING = False
    print("Note: Install 'requests' and 'beautifulsoup4' for automatic content fetching:")
    print("  pip install requests beautifulsoup4")

try:
    import feedparser
    HAS_RSS = True
except ImportError:
    HAS_RSS = False
    print("Note: Install 'feedparser' for RSS feed support:")
    print("  pip install feedparser")

# NewsAPI (Free tier: 100 requests/day)
NEWSAPI_KEY = os.getenv('NEWSAPI_KEY', '')
NEWSAPI_URL = 'https://newsapi.org/v2/top-headlines'


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

# RSS Feeds for Financial News (Free, unlimited)
FINANCIAL_RSS_FEEDS = {
    'nairametrics': 'https://nairametrics.com/feed/',
    'financial_nigeria': 'https://www.financialnigeria.com/feed/',
    'businessday': 'https://businessday.ng/feed/'
}


SOURCES = {
    "nairametrics": "https://nairametrics.com/",
    "financial_nigeria": "https://www.financialnigeria.com/",
    "businessday": "https://businessday.ng/",
}

SCHEDULE = {
    "Monday": "nairametrics",
    "Tuesday": "nairametrics",
    "Wednesday": "financial_nigeria",
    "Thursday": "financial_nigeria",
    "Friday": "businessday",
    "Saturday": "businessday",
    "Sunday": None,  # Optional / rest day
}


class FinancialNewsProblemExtractor:
    def __init__(self):
        self.today = datetime.now()
        self.day_name = calendar.day_name[self.today.weekday()]
        self.scheduled_key = SCHEDULE.get(self.day_name)
        self.source_key = None
        self.raw_content = ""
        self.selected_problems = []
        self.output_file = (
            f"financial_news_problems_{self.today.strftime('%Y%m%d_%H%M%S')}.json"
        )

    def intro(self):
        print("\n" + "=" * 60)
        print("Business Idea Formulation Strategy 9")
        print("Financial News Problem Extraction")
        print("=" * 60)
        print(f"\nToday is: {self.day_name}")
        if self.scheduled_key:
            print(
                f"Scheduled source for today: {self.scheduled_key.replace('_', ' ').title()} "
                f"({SOURCES[self.scheduled_key]})"
            )
        else:
            print("No fixed source scheduled for today (Sunday). You can pick any source.")

    def choose_source(self):
        """Step 1: Confirm or override the news source for today."""
        print("\n" + "=" * 60)
        print("STEP 1: Choose Financial News Source")
        print("=" * 60)

        if self.scheduled_key:
            default_url = SOURCES[self.scheduled_key]
            print(
                f"\nRecommended for {self.day_name}: "
                f"{self.scheduled_key.replace('_', ' ').title()} → {default_url}"
            )
            choice = input(
                "Use this source? (Y to accept / N to select another): "
            ).strip().lower()
            if choice in ("", "y", "yes"):
                self.source_key = self.scheduled_key
            else:
                self._manual_source_selection()
        else:
            self._manual_source_selection()

        if not self.source_key:
            print("No source selected. Exiting.")
            return None

        print(
            f"\nUsing source: {self.source_key.replace('_', ' ').title()} "
            f"({SOURCES[self.source_key]})"
        )

        # Offer to open the chosen financial news site in Chrome/default browser
        url = SOURCES.get(self.source_key)
        if url:
            choice = input("\nOpen this news site in Chrome now? (y/n, default=y): ").strip().lower()
            if choice in ("", "y", "yes"):
                open_in_chrome(url)

        return self.source_key

    def _manual_source_selection(self):
        print("\nAvailable sources:")
        for idx, (key, url) in enumerate(SOURCES.items(), 1):
            print(f"{idx}. {key.replace('_', ' ').title()} → {url}")
        sel = input("Select source (1/2/3): ").strip()
        mapping = {str(i + 1): k for i, k in enumerate(SOURCES.keys())}
        self.source_key = mapping.get(sel)

    def fetch_via_newsapi(self) -> Optional[List[Dict]]:
        """Fetch financial news headlines via NewsAPI"""
        if not NEWSAPI_KEY:
            return None
        
        try:
            params = {
                'country': 'ng',
                'category': 'business',
                'apiKey': NEWSAPI_KEY,
                'pageSize': 10
            }
            
            response = requests.get(NEWSAPI_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for article in data.get('articles', [])[:5]:
                articles.append({
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'url': article.get('url', ''),
                    'source': article.get('source', {}).get('name', '')
                })
            
            return articles
        except Exception as e:
            print(f"  ⚠ NewsAPI fetch failed: {str(e)}")
            return None
    
    def fetch_via_rss(self, source_key: str) -> Optional[str]:
        """Fetch financial news content via RSS feed"""
        if not HAS_RSS:
            return None
        
        try:
            rss_url = FINANCIAL_RSS_FEEDS.get(source_key)
            if not rss_url:
                return None
            
            feed = feedparser.parse(rss_url)
            if not feed.entries:
                return None
            
            # Combine recent articles
            content_parts = []
            for entry in feed.entries[:5]:  # Latest 5 articles
                content_parts.append(f"Title: {entry.get('title', '')}")
                content_parts.append(f"Summary: {entry.get('summary', entry.get('description', ''))}")
                content_parts.append("---")
            
            content = '\n'.join(content_parts)
            return content[:9000]  # Truncate to 9000 chars
        except Exception as e:
            error_msg = str(e).lower()
            if 'name resolution' in error_msg or 'getaddrinfo failed' in error_msg or 'failed to resolve' in error_msg:
                print(f"  ⚠ RSS DNS Error: Cannot resolve RSS feed domain")
                print(f"  → Falling back to manual collection or NewsAPI...")
            else:
                print(f"  ⚠ RSS fetch failed: {str(e)}")
                print(f"  → Falling back to manual collection or NewsAPI...")
            return None
    
    def fetch_content_via_api(self, url: str) -> Optional[str]:
        """Attempt to fetch content via web scraping"""
        if not HAS_SCRAPING:
            return None
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script, style, nav, footer, header elements
            for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
                element.decompose()
            
            # Try to get main content area
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile('content|main|article'))
            
            if main_content:
                text = main_content.get_text()
            else:
                text = soup.get_text()
            
            # Clean up whitespace
            lines = [line.strip() for line in text.splitlines()]
            lines = [line for line in lines if line and len(line) > 10]  # Filter short lines
            content = '\n'.join(lines[:300])  # Limit to first 300 meaningful lines
            
            return content[:9000]  # Truncate to 9000 chars
        except requests.exceptions.ConnectionError as e:
            error_msg = str(e).lower()
            if 'name resolution' in error_msg or 'getaddrinfo failed' in error_msg or 'failed to resolve' in error_msg:
                print(f"  ⚠ DNS Error: Cannot resolve domain name. Possible causes:")
                print(f"     - No internet connection")
                print(f"     - DNS server issues")
                print(f"     - Website may be down or domain changed")
                print(f"     - Firewall/proxy blocking the connection")
                print(f"  → Falling back to manual collection or RSS feed...")
            else:
                print(f"  ⚠ Connection Error: Cannot connect to {url}")
                print(f"  → Falling back to manual collection or RSS feed...")
            return None
        except requests.exceptions.Timeout:
            print(f"  ⚠ Timeout: Request to {url} timed out (took longer than 15 seconds)")
            print(f"  → Falling back to manual collection or RSS feed...")
            return None
        except requests.exceptions.RequestException as e:
            print(f"  ⚠ Network Error: {str(e)}")
            print(f"  → Falling back to manual collection or RSS feed...")
            return None
        except Exception as e:
            print(f"  ⚠ Scraping Error: {str(e)}")
            print(f"  → Falling back to manual collection or RSS feed...")
            return None

    def collect_content(self):
        """Step 2: Paste copied website content."""
        print("\n" + "=" * 60)
        print("STEP 2: Collect Website Content")
        print("=" * 60)

        if not self.source_key:
            print("No source selected; cannot collect content.")
            return None

        url = SOURCES[self.source_key]
        
        # Try multiple methods if available
        content = None
        if HAS_SCRAPING or HAS_RSS or NEWSAPI_KEY:
            choice = input(f"\nFetch content automatically from {url}? (y/n, default=n): ").strip().lower()
            if choice in ('y', 'yes'):
                print("  Attempting to fetch content automatically...")
                
                # Try BeautifulSoup web scraping FIRST (primary method)
                if HAS_SCRAPING:
                    print("    Trying web scraping (BeautifulSoup)...")
                    content = self.fetch_content_via_api(url)
                    if content:
                        print("    ✓ Fetched via BeautifulSoup scraping")
                
                # Try RSS feed as fallback
                if not content and HAS_RSS:
                    print("    Trying RSS feed (fallback)...")
                    content = self.fetch_via_rss(self.source_key)
                    if content:
                        print("    ✓ Fetched via RSS")
                
                # Try NewsAPI as final fallback
                if not content and NEWSAPI_KEY:
                    print("    Trying NewsAPI (fallback)...")
                    articles = self.fetch_via_newsapi()
                    if articles:
                        content_parts = []
                        for article in articles:
                            content_parts.append(f"{article['title']}\n{article['description']}\n---")
                        content = '\n'.join(content_parts)[:9000]
                        if content:
                            print("    ✓ Fetched via NewsAPI")
        
        # Fallback to manual if API failed or not requested
        if not content:
            print(
                f"\nManual collection:\n"
                f"1. Open: {url}\n"
                "2. Press CTRL + A to select the entire page content.\n"
                "3. Press CTRL + C to copy.\n"
                "4. Come back here and paste (Ctrl + V / right-click paste).\n"
                "5. Press Enter on an empty line when you're done.\n"
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
            print("\nNo content collected. You can re-run this later.")
            return None

        if len(content) > 9000:
            content = (
                content[:9000]
                + "\n\n[Content truncated for optimal ChatGPT processing]"
            )

        self.raw_content = content
        print(f"\n✓ Collected website content ({len(content)} characters).")
        return content

    def generate_prompt_1a(self):
        """Step 3: Generate Prompt 1a file."""
        print("\n" + "=" * 60)
        print("STEP 3: Generate Prompt 1a")
        print("=" * 60)

        if not self.raw_content or not self.source_key:
            print("Missing content or source; skipping Prompt 1a generation.")
            return None

        source_name = self.source_key.replace("_", " ").title()
        base_prompt = (
            f"Give me problems that can be solved with digital solutions (web apps and others), "
            f"based on content on {source_name} today. Output should have \"With the mention of\".\n\n"
            "[Website content starts below]\n\n"
        )

        prompt_1a = base_prompt + self.raw_content

        filename = "chatgpt_strategy9_prompt_1a.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(
                f"PROMPT 1a for {source_name} (use with pasted website content):\n\n"
            )
            f.write(prompt_1a)

        print(f"\n✓ Prompt 1a saved to '{filename}'.")
        print(
            "\nUse it like this:\n"
            "1. Open ChatGPT.\n"
            "2. Paste the content from this file.\n"
            "3. Run as Prompt 1a and wait for a list of problems.\n"
        )
        return prompt_1a

    def collect_key_problems(self):
        """Step 4: Let user type the most important problems/ideas from ChatGPT."""
        print("\n" + "=" * 60)
        print("STEP 4: Capture Key Problems / Idea Summaries")
        print("=" * 60)

        print(
            "\nAfter running Prompt 1a in ChatGPT, paste/type the key problems or\n"
            "idea summaries you want to deepen (one per line). They should be\n"
            "short descriptions like:\n"
            "- \"Unreliable power tariff information for SMEs\"\n"
            "- \"Hidden bank charges for small businesses\"\n"
            "Press Enter twice when you're done.\n"
        )

        problems = []
        while True:
            p = input("Key problem/idea: ").strip()
            if not p:
                break
            problems.append(p)

        self.selected_problems = problems
        print(f"\n✓ Captured {len(problems)} key problems/ideas.")
        return problems

    def generate_prompt_1b_blocks(self):
        """Step 5: Generate Prompt 1b blocks for each selected problem/idea."""
        print("\n" + "=" * 60)
        print("STEP 5: Generate Prompt 1b Blocks")
        print("=" * 60)

        if not self.selected_problems:
            print("No problems/ideas captured; skipping Prompt 1b generation.")
            return []

        template = (
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
        for idea in self.selected_problems:
            text = template.format(idea=idea)
            blocks.append({"idea": idea, "prompt": text})

        filename = "chatgpt_strategy9_prompt_1b.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for idx, block in enumerate(blocks, 1):
                f.write(f"{'=' * 60}\n")
                f.write(f"Prompt 1b for Idea {idx}: {block['idea']}\n")
                f.write(f"{'=' * 60}\n\n")
                f.write(block["prompt"])
                f.write("\n\n")

        print(f"\n✓ Generated {len(blocks)} Prompt 1b blocks.")
        print(f"Saved to '{filename}'.")
        print(
            "\nUsage:\n"
            "- For each idea, paste the corresponding Prompt 1b into the SAME ChatGPT\n"
            "  conversation where you ran Prompt 1a.\n"
            "- This will produce the detailed analysis table for that financial-news-derived idea.\n"
        )
        return blocks

    def save_summary(self):
        """Step 6: Save summary JSON."""
        data = {
            "strategy": 9,
            "name": "Financial News Problem Extraction",
            "timestamp": datetime.now().isoformat(),
            "day_name": self.day_name,
            "source_key": self.source_key,
            "source_url": SOURCES.get(self.source_key) if self.source_key else None,
            "content_length": len(self.raw_content or ""),
            "selected_problems": self.selected_problems,
        }

        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Run summary saved to '{self.output_file}'.")
        open_file_automatically(self.output_file)

    def run(self):
        self.intro()
        self.choose_source()
        if not self.source_key:
            return

        self.collect_content()
        self.generate_prompt_1a()
        input(
            "\nNow go to ChatGPT, use Prompt 1a (from the text file), and wait for\n"
            "the list of problems. Press Enter here when you're ready to log key problems..."
        )
        self.collect_key_problems()
        self.generate_prompt_1b_blocks()
        self.save_summary()

        print("\n" + "=" * 60)
        print("Process Complete!")
        print("=" * 60)
        print(
            "\nNext steps:\n"
            "1. Open 'chatgpt_strategy9_prompt_1b.txt'.\n"
            "2. Paste each Prompt 1b into ChatGPT to get full tables.\n"
            "3. Compare which financial-news-derived ideas are strongest.\n"
        )


if __name__ == "__main__":
    extractor = FinancialNewsProblemExtractor()
    extractor.run()


