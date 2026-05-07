#!/usr/bin/env python3
"""
Business Idea Formulation Strategy 5: News-Based Problem Extraction
Automated script to help extract problems from Nigerian news websites.
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

# Reusable Cursor copy-block helper (repo root)
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from cursor_copy_helper import offer_cursor_copy_block, refresh_past_business_ideas_for_directory
except ImportError:
    offer_cursor_copy_block = None
    refresh_past_business_ideas_for_directory = None

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

# Prompt 1b for ChatGPT tabulate step — single source of truth (also written to chatgpt_prompt_1b.txt).
PROMPT_1B_TABULATE = (
    "Tabulate output (Columns: Proposed domain (not verified)/Problem Identified/"
    "Potential Digital Solution/Estimated daily sales/ Actualization strategy, Target Audience, Problem it solves, "
    "Competition Analysis, Estimated Costs (in dollars), Funding Sources (provide links to possible investors "
    "and VCs), No-code Tools to build solution, How to test the viability of the idea, Potential Challenges, "
    "Solution to those potential challenges, landing page platform, Monetization Strategy, "
    "Market Size and Growth Potential, Technical Expertise and Skill Requirements, Partnerships and Collaboration, "
    "Timeline, Key Performance Indicators (KPIs), Team Requirements, Time to Market, Required Skills, "
    "Risks and Mitigation, Scalability, Social Impact.\n\n"
    "In the \"Proposed domain (not verified)\" column: use TBD or illustrative placeholder domains only "
    "(e.g. productname.ng); do not present them as existing live websites unless you have verified them."
)

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

# RSS Feeds for Nigerian News (Free, unlimited)
RSS_FEEDS = {
    'vanguard': 'https://www.vanguardngr.com/feed/',
    'punch': 'https://punchng.com/feed/',
    'guardian': 'https://guardian.ng/feed/',
    'premium_times': 'https://www.premiumtimesng.com/feed/',
    'thisday': 'https://www.thisdaylive.com/feed/',
    'nairametrics': 'https://nairametrics.com/feed/',
    'businessday': 'https://businessday.ng/feed/'
}

class NewsProblemExtractor:
    def __init__(self):
        # Business sources first (positions 1–2); keep them there. General news follows.
        self.news_sources = [
            "https://nairametrics.com/",           # 1 – Business / financial (prefer for business ideas)
            "https://businessday.ng/",             # 2 – Business / financial (prefer for business ideas)
            "https://www.vanguardngr.com/",
            "https://punchng.com/",
            "https://guardian.ng/",
            "https://www.thisdaylive.com/",
            "https://www.premiumtimesng.com/",
            "https://www.thenationonlineng.net/",
        ]
        self.selected_sources = []
        self.news_content = []
        self.problems = []
        self.output_file = f"news_problems_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
    def select_news_sources(self):
        """Step 1: Select news sources"""
        print("\n" + "="*60)
        print("STEP 1: Select News Sources")
        print("="*60)
        
        print("\nAvailable Nigerian News Sources (1–2 = business; prefer these for business ideas):")
        for i, source in enumerate(self.news_sources, 1):
            print(f"{i}. {source}")
        print("\nTip: Prioritise business-focused news sources (1–2) over general news as they yield stronger, more commercially focused ideas.")
        print("\nSelect 2-3 sources (enter numbers separated by commas):")
        selection = input("Selection: ").strip()
        
        indices = [int(x.strip()) - 1 for x in selection.split(',')]
        self.selected_sources = [self.news_sources[i] for i in indices if 0 <= i < len(self.news_sources)]
        
        print(f"\n✓ Selected {len(self.selected_sources)} sources:")
        for source in self.selected_sources:
            print(f"  - {source}")

        # Offer to open selected sources in Chrome/default browser
        if self.selected_sources:
            choice = input("\nOpen selected news sources in Chrome now? (y/n, default=y): ").strip().lower()
            if choice in ("", "y", "yes"):
                for source in self.selected_sources:
                    open_in_chrome(source)
        
        return self.selected_sources
    
    def fetch_via_newsapi(self, source_name: str) -> Optional[List[Dict]]:
        """Fetch news headlines via NewsAPI"""
        if not NEWSAPI_KEY:
            return None
        
        try:
            # Map source names to NewsAPI sources
            source_map = {
                'vanguardngr.com': 'vanguard-ng',
                'punchng.com': 'punch',
                'guardian.ng': 'guardian-ng',
                'premiumtimesng.com': 'premium-times',
                'thisdaylive.com': 'thisday'
            }
            
            params = {
                'country': 'ng',
                'apiKey': NEWSAPI_KEY,
                'pageSize': 10
            }
            
            response = requests.get(NEWSAPI_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for article in data.get('articles', [])[:5]:  # Limit to 5 articles
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
    
    def fetch_via_rss(self, source_url: str) -> Optional[str]:
        """Fetch news content via RSS feed"""
        if not HAS_RSS:
            return None
        
        try:
            # Find matching RSS feed
            rss_url = None
            for key, feed_url in RSS_FEEDS.items():
                if key.replace('_', '') in source_url.lower():
                    rss_url = feed_url
                    break
            
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
            return content[:15000]  # Truncate to 15000 chars
        except Exception as e:
            error_msg = str(e).lower()
            if 'name resolution' in error_msg or 'getaddrinfo failed' in error_msg or 'failed to resolve' in error_msg:
                print(f"  ⚠ Oops! We couldn't fetch the RSS feed automatically")
                print(f"     Don't worry - we'll try other methods or guide you through manual collection.\n")
                print(f"  ⚠ RSS DNS Error: Cannot resolve RSS feed domain")
                print(f"  → Falling back to manual collection or NewsAPI...")
            else:
                print(f"  ⚠ Oops! We couldn't fetch the RSS feed automatically")
                print(f"     Don't worry - we'll try other methods or guide you through manual collection.\n")
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
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            # Clean up whitespace
            lines = [line.strip() for line in text.splitlines()]
            lines = [line for line in lines if line]
            content = '\n'.join(lines[:400])  # Limit to first 400 lines
            
            return content[:15000]  # Truncate to 15000 chars
        except requests.exceptions.ConnectionError as e:
            error_msg = str(e).lower()
            if 'name resolution' in error_msg or 'getaddrinfo failed' in error_msg or 'failed to resolve' in error_msg:
                print(f"  ⚠ Oops! We couldn't automatically fetch content from {url}")
                print(f"     Don't worry - we'll try other methods or guide you through manual collection.\n")
                print(f"  ⚠ DNS Error: Cannot resolve domain name. Possible causes:")
                print(f"     - No internet connection")
                print(f"     - DNS server issues")
                print(f"     - Website may be down or domain changed")
                print(f"     - Firewall/proxy blocking the connection")
                print(f"  → Falling back to manual collection or RSS feed...")
            else:
                print(f"  ⚠ Oops! We couldn't automatically fetch content from {url}")
                print(f"     Don't worry - we'll try other methods or guide you through manual collection.\n")
                print(f"  ⚠ Connection Error: Cannot connect to {url}")
                print(f"  → Falling back to manual collection or RSS feed...")
            return None
        except requests.exceptions.Timeout:
            print(f"  ⚠ Oops! The request to {url} took too long")
            print(f"     Don't worry - we'll try other methods or guide you through manual collection.\n")
            print(f"  ⚠ Timeout: Request to {url} timed out (took longer than 10 seconds)")
            print(f"  → Falling back to manual collection or RSS feed...")
            return None
        except requests.exceptions.RequestException as e:
            print(f"  ⚠ Oops! We encountered a network issue while fetching from {url}")
            print(f"     Don't worry - we'll try other methods or guide you through manual collection.\n")
            print(f"  ⚠ Network Error: {str(e)}")
            print(f"  → Falling back to manual collection or RSS feed...")
            return None
        except Exception as e:
            print(f"  ⚠ Oops! Something went wrong while scraping {url}")
            print(f"     Don't worry - we'll try other methods or guide you through manual collection.\n")
            print(f"  ⚠ Scraping Error: {str(e)}")
            print(f"  → Falling back to manual collection or RSS feed...")
            return None
    
    def collect_news_content(self):
        """Step 2: Collect news content"""
        print("\n" + "="*60)
        print("STEP 2: Collect News Content")
        print("="*60)
        
        use_api = False
        if HAS_SCRAPING:
            choice = input("\nFetch content automatically via API? (y/n, default=n): ").strip().lower()
            use_api = choice in ('y', 'yes')
        
        content_items = []
        for source in self.selected_sources:
            print(f"\n--- Processing: {source} ---")
            
            content = None
            if use_api:
                print("  Attempting to fetch content automatically...")
                
                # Try BeautifulSoup web scraping FIRST (primary method)
                if HAS_SCRAPING:
                    print("    Trying web scraping (BeautifulSoup)...")
                    content = self.fetch_content_via_api(source)
                    if content:
                        print("    ✓ Fetched via BeautifulSoup scraping")
                
                # Try RSS feed as fallback
                if not content and HAS_RSS:
                    print("    Trying RSS feed (fallback)...")
                    content = self.fetch_via_rss(source)
                    if content:
                        print("    ✓ Fetched via RSS")
                
                # Try NewsAPI as final fallback
                if not content and NEWSAPI_KEY:
                    print("    Trying NewsAPI (fallback)...")
                    articles = self.fetch_via_newsapi(source)
                    if articles:
                        content_parts = []
                        for article in articles:
                            content_parts.append(f"{article['title']}\n{article['description']}\n---")
                        content = '\n'.join(content_parts)[:15000]
                        if content:
                            print("    ✓ Fetched via NewsAPI")
            
            if not content:
                # If auto-fetch was attempted and failed, offer retry option
                if use_api:
                    # Offer retry option before manual collection
                    while True:
                        print("\n⚠ Connection failed. Retry automatic fetch?")
                        print("Press (R) to retry | (M) for manual collection | (S) to skip this source | (N) to select a different source: ", end="")
                        retry_choice = input().strip().upper()
                        
                        if retry_choice == 'R':
                            print("  Retrying automatic fetch...")
                            
                            # Retry all auto methods
                            if HAS_SCRAPING:
                                print("    Trying web scraping (BeautifulSoup)...")
                                content = self.fetch_content_via_api(source)
                                if content:
                                    print("    ✓ Fetched via BeautifulSoup scraping")
                                    break
                            
                            if not content and HAS_RSS:
                                print("    Trying RSS feed (fallback)...")
                                content = self.fetch_via_rss(source)
                                if content:
                                    print("    ✓ Fetched via RSS")
                                    break
                            
                            if not content and NEWSAPI_KEY:
                                print("    Trying NewsAPI (fallback)...")
                                articles = self.fetch_via_newsapi(source)
                                if articles:
                                    content_parts = []
                                    for article in articles:
                                        content_parts.append(f"{article['title']}\n{article['description']}\n---")
                                    content = '\n'.join(content_parts)[:15000]
                                    if content:
                                        print("    ✓ Fetched via NewsAPI")
                                        break
                            
                            # Retry failed again
                            if not content:
                                print("  ⚠ Retry failed. Please choose another option.")
                                continue
                        
                        elif retry_choice == 'M':
                            # Manual collection
                            break
                        
                        elif retry_choice == 'S':
                            # Skip this source
                            print(f"  ⊘ Skipping {source}")
                            content = None
                            break
                        
                        elif retry_choice == 'N':
                            # Select a different source
                            print("\nAvailable Nigerian News Sources:")
                            for i, src in enumerate(self.news_sources, 1):
                                print(f"{i}. {src}")
                            
                            print("\nSelect a different source (enter number):")
                            selection = input("Selection: ").strip()
                            
                            try:
                                index = int(selection.strip()) - 1
                                if 0 <= index < len(self.news_sources):
                                    new_source = self.news_sources[index]
                                    print(f"\n  ✓ Selected new source: {new_source}")
                                    source = new_source  # Replace current source
                                    print(f"  Attempting to fetch from {source}...")
                                    
                                    # Try fetching from new source
                                    if HAS_SCRAPING:
                                        print("    Trying web scraping (BeautifulSoup)...")
                                        content = self.fetch_content_via_api(source)
                                        if content:
                                            print("    ✓ Fetched via BeautifulSoup scraping")
                                            break
                                    
                                    if not content and HAS_RSS:
                                        print("    Trying RSS feed (fallback)...")
                                        content = self.fetch_via_rss(source)
                                        if content:
                                            print("    ✓ Fetched via RSS")
                                            break
                                    
                                    if not content and NEWSAPI_KEY:
                                        print("    Trying NewsAPI (fallback)...")
                                        articles = self.fetch_via_newsapi(source)
                                        if articles:
                                            content_parts = []
                                            for article in articles:
                                                content_parts.append(f"{article['title']}\n{article['description']}\n---")
                                            content = '\n'.join(content_parts)[:15000]
                                            if content:
                                                print("    ✓ Fetched via NewsAPI")
                                                break
                                    
                                    # New source also failed
                                    if not content:
                                        print("  ⚠ New source also failed. Please choose another option.")
                                        continue
                                else:
                                    print("  ⚠ Invalid source number. Please try again.")
                                    continue
                            except (ValueError, IndexError):
                                print("  ⚠ Invalid selection. Please enter a valid number.")
                                continue
                        
                        else:
                            print("  ⚠ Invalid choice. Please enter R, M, S, or N.")
                            continue
                
                # Manual collection (if retry not chosen, or user chose M, or use_api was False)
                if not content:
                    print("\nManual collection:")
                    print("1. Visit the website")
                    print("2. Use Ctrl + A to select all content")
                    print("3. Copy and paste here")
                    print("(Press Enter twice when done)\n")
                    
                    lines = []
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
                # Truncate if too long (keep under 15000 chars for best ChatGPT results)
                if len(content) > 15000:
                    content = content[:15000] + "\n\n[Content truncated for optimal ChatGPT processing]"
                
                content_items.append({
                    'source': source,
                    'content': content,
                    'length': len(content),
                    'method': 'api' if use_api and content else 'manual',
                    'timestamp': datetime.now().isoformat()
                })
                print(f"  ✓ Collected {len(content)} characters")
        
        self.news_content = content_items
        print(f"\n✓ Collected content from {len(content_items)} sources")
        return content_items
    
    def generate_chatgpt_prompts(self):
        """Step 3: Generate ChatGPT prompts"""
        print("\n" + "="*60)
        print("STEP 3: Generate ChatGPT Prompts")
        print("="*60)
        
        if not self.news_content:
            print("No news content collected yet.")
            return
        
        # Prompt 1a
        prompt_1a = "Give me problems that can be solved with digital solutions (web apps and others), based on content on nigerian news websites today. Output should have \"With the mention of\"\n\n"
        
        for item in self.news_content:
            content = self._ensure_space_after_date(item['content'])
            prompt_1a += f"Content from {item['source']}:\n"
            prompt_1a += f"{content}\n\n"
            prompt_1a += "---\n\n"
        
        # Prompt 1b
        prompt_1b = PROMPT_1B_TABULATE
        
        # Save prompts
        with open('chatgpt_prompt_1a.txt', 'w', encoding='utf-8') as f:
            f.write(prompt_1a)
        
        with open('chatgpt_prompt_1b.txt', 'w', encoding='utf-8') as f:
            f.write(prompt_1b)
        
        print("\n✓ Generated ChatGPT prompts")
        print("\nIMPORTANT INSTRUCTIONS:")
        print("1. Open ChatGPT with ACCESS LINK and LINK READER plugins enabled")
        print("2. First, paste the content from 'chatgpt_prompt_1a.txt'")
        print("3. Wait for response")
        print("4. Then, in the same chat, use Prompt 1b from 'chatgpt_prompt_1b.txt'")
        print("\nNote: Keep prompts separate for best ChatGPT output quality")
        
        return prompt_1a, prompt_1b
    
    def _ensure_space_after_date(self, text: str) -> str:
        """Insert newline after date/time when directly followed by next article title (no space)."""
        # Full month: January 13, 2026
        full_month = (
            r'(January|February|March|April|May|June|July|August|'
            r'September|October|November|December)\s+\d{1,2},\s*\d{4}'
        )
        # Abbreviated month: Feb 14, 2026
        abbr_month = (
            r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s*\d{4}'
        )
        # Relative times: 14 hrs ago, 53 minutes ago, an hour ago
        relative_time = (
            r'(\d+\s*(?:minutes?|mins?|hours?|hrs?)\s+ago|'
            r'an?\s+(?:hour|minute)\s+ago)'
        )
        pattern = r'(' + full_month + r'|' + abbr_month + r'|' + relative_time + r')(?=[A-Za-z])'
        return re.sub(pattern, r'\1\n', text)

    def format_content_for_display(self, content: str) -> str:
        """Format content with proper line breaks so each article/item appears on separate lines"""
        if not content:
            return ""
        content = self._ensure_space_after_date(content)
        # If content is one big block with no line breaks (common on some sites like Nairametrics),
        # try to split it into sentences so the output looks more regular.
        if "\n" not in content and len(content) > 1000:
            content = re.sub(r"([\.!?])\s+(?=[A-Z])", r"\1\n", content)
        # Split by common separators that indicate article boundaries
        lines = content.split('\n')
        formatted_lines = []
        
        # Track if we're in an article section
        in_article = False
        
        for line in lines:
            line = line.strip()
            if not line:
                if in_article:
                    formatted_lines.append("")  # Add blank line between articles
                continue
            
            # Detect article boundaries (common patterns)
            if line.startswith("Title:") or line.startswith("---"):
                if in_article and formatted_lines:
                    formatted_lines.append("")  # Add separator before new article
                formatted_lines.append(line)
                in_article = True
            elif line.startswith("Summary:") or line.startswith("Description:"):
                formatted_lines.append(line)
            elif len(line) > 50 and not line.startswith("http"):
                # Likely article content - ensure it's on its own line
                # Wrap long lines if needed (but keep them readable)
                if len(line) > 120:
                    # Break long lines at word boundaries
                    words = line.split()
                    current_line = ""
                    for word in words:
                        if len(current_line + " " + word) > 120:
                            if current_line:
                                formatted_lines.append(current_line)
                            current_line = word
                        else:
                            current_line += (" " + word) if current_line else word
                    if current_line:
                        formatted_lines.append(current_line)
                else:
                    formatted_lines.append(line)
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def save_data(self):
        """Save all data"""
        data = {
            'selected_sources': self.selected_sources,
            'news_content': self.news_content,
            'timestamp': datetime.now().isoformat()
        }
        
        # Save structured data to JSON
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Also create a human-readable .txt equivalent and open that instead
        txt_path = Path(self.output_file).with_suffix(".txt")
        with open(txt_path, 'w', encoding='utf-8') as f_txt:
            f_txt.write("News-Based Problem Extraction - Saved Run\n")
            f_txt.write(f"Timestamp: {data['timestamp']}\n")
            f_txt.write("\nSelected sources:\n")
            for src in data['selected_sources']:
                f_txt.write(f"  - {src}\n")
            f_txt.write("\n" + "="*70 + "\n")
            f_txt.write("COLLECTED CONTENT (Formatted for Readability)\n")
            f_txt.write("="*70 + "\n")
            
            for idx, item in enumerate(data['news_content'], 1):
                source = item.get('source', '')
                content = item.get('content', '')
                method = item.get('method', '')
                length = item.get('length', 0)
                
                f_txt.write(f"\n{'─'*70}\n")
                f_txt.write(f"SOURCE {idx}: {source}\n")
                f_txt.write(f"Method: {method} | Length: {length} characters\n")
                f_txt.write(f"{'─'*70}\n\n")
                
                # Format content with proper line breaks
                formatted_content = self.format_content_for_display(content)
                f_txt.write(formatted_content)
                f_txt.write("\n\n")
            
            f_txt.write("\n" + "="*70 + "\n")
            f_txt.write("FULL JSON DATA (for reference)\n")
            f_txt.write("="*70 + "\n\n")
            f_txt.write(json.dumps(data, indent=2, ensure_ascii=False))
        
        print(f"\n✓ All data saved to '{self.output_file}'")
        print(f"✓ Text summary saved to '{txt_path.name}'")
        open_file_automatically(str(txt_path))
        self._last_txt_path = txt_path

    def run(self):
        """Main execution flow"""
        print("\n" + "="*60)
        print("Business Idea Formulation Strategy 5")
        print("News-Based Problem Extraction")
        print("="*60)

        # Phase 3: refresh past_business_ideas.md from any business_ideas_*.md in this folder
        # (picks up files saved since the last run, e.g. from Cursor)
        if refresh_past_business_ideas_for_directory is not None:
            strat_dir = Path(__file__).resolve().parent
            past = refresh_past_business_ideas_for_directory(strat_dir)
            if past is not None:
                print(f"  ✓ Past ideas aggregate updated: {past.name}")
        
        # Step 1: Select sources
        self.select_news_sources()
        
        # Step 2: Collect content
        self.collect_news_content()
        
        # Step 3: Generate prompts
        self.generate_chatgpt_prompts()
        
        # Save data
        self.save_data()
        
        # Offer copy-block for Cursor (reusable helper)
        if offer_cursor_copy_block is not None:
            txt_path = getattr(self, "_last_txt_path", None)
            if txt_path is not None:
                offer_cursor_copy_block(
                    document_path=txt_path,
                    prompt_1a_ref='Give me problems that can be solved with digital solutions (web apps and others), based on content on nigerian news websites today. Output should have "With the mention of".',
                    prompt_1b_ref=(
                        "Tabulate output (Columns: Proposed domain (not verified), "
                        "Problem Identified, Potential Digital Solution, Estimated daily sales, ...). "
                        "Proposed domain: TBD/illustrative unless verified."
                    ),
                )
        
        print("\n" + "="*60)
        print("Process Complete!")
        print("="*60)
        print("\nNext steps:")
        print("1. (If you copied) Paste in Cursor chat and send for business ideas table.")
        print("2. Or open ChatGPT: use Prompt 1a from 'chatgpt_prompt_1a.txt', then Prompt 1b from 'chatgpt_prompt_1b.txt'.")
        print("3. Review and analyze the generated business ideas.")

if __name__ == "__main__":
    extractor = NewsProblemExtractor()
    extractor.run()

