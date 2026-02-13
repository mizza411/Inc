#!/usr/bin/env python3
"""
Business Idea Formulation Strategy 13: Multi-Source Comprehensive Analysis
Automated script to help combine SimilarWeb and AnnualReports.com data for business idea generation.
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
    print("Note: Install 'requests' and 'beautifulsoup4' for automatic data fetching:")
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

# SimilarWeb API (if you have API key)
SIMILARWEB_API_KEY = os.getenv('SIMILARWEB_API_KEY', '')
SIMILARWEB_API_URL = 'https://api.similarweb.com/v1/website/{domain}/total-traffic-and-engagement/visits'

class MultiSourceAnalyzer:
    def __init__(self):
        self.similarweb_data = {}
        self.annualreports_data = {}
        self.market_leaders = []
        self.insights = {}
        self.viable_ideas = []
        self.output_file = f"multisource_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
    def fetch_similarweb_api(self, domain: str) -> Optional[Dict]:
        """Fetch SimilarWeb data via API if API key is available"""
        if not SIMILARWEB_API_KEY:
            return None
        
        try:
            # Extract domain from URL if needed
            domain = re.sub(r'^https?://(www\.)?', '', domain)
            domain = domain.split('/')[0]
            
            url = SIMILARWEB_API_URL.format(domain=domain)
            headers = {
                'Authorization': f'Bearer {SIMILARWEB_API_KEY}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                'monthly_visits': data.get('visits', 'N/A'),
                'avg_visit_duration': data.get('avg_visit_duration', 'N/A'),
                'pages_per_visit': data.get('pages_per_visit', 'N/A'),
                'bounce_rate': data.get('bounce_rate', 'N/A')
            }
        except Exception as e:
            print(f"  ⚠ SimilarWeb API error: {str(e)}")
            return None
    
    def collect_similarweb_data(self):
        """Step 1: Collect SimilarWeb data"""
        print("\n" + "="*60)
        print("STEP 1: SimilarWeb Analysis")
        print("="*60)
        
        target_industry = input("What industry/problem area are you analyzing? ").strip()
        
        use_api = False
        if SIMILARWEB_API_KEY:
            choice = input("\nUse SimilarWeb API for automatic data fetching? (y/n, default=n): ").strip().lower()
            use_api = choice in ('y', 'yes')
        
        if not use_api:
            print("\nGo to: https://www.similarweb.com/")
            print("Search for websites in your target industry/problem area\n")

            # Automatically open SimilarWeb in Chrome/default browser
            open_in_chrome("https://www.similarweb.com/")
        
        print("\nEnter SimilarWeb findings:")
        print("(Press Enter twice when done with each section)\n")
        
        # Demand Analysis
        print("1. DEMAND ANALYSIS (Traffic Data):")
        print("   Enter high-traffic websites and their traffic volumes:")
        demand_data = []
        while True:
            website = input("   Website (or Enter to finish): ").strip()
            if not website:
                break
            
            # Try API if enabled
            api_data = None
            if use_api:
                print(f"     Fetching data for {website}...")
                api_data = self.fetch_similarweb_api(website)
            
            if api_data:
                traffic = f"{api_data.get('monthly_visits', 'N/A')} monthly visits"
                trend = "Growing" if api_data.get('monthly_visits') else "Unknown"
                print(f"     ✓ API data: {traffic}")
            else:
                traffic = input("   Traffic volume/estimate: ").strip()
                trend = input("   Trend (Growing/Stable/Declining): ").strip()
            
            demand_data.append({
                'website': website,
                'traffic': traffic,
                'trend': trend,
                'api_data': api_data
            })
        
        # Audience Size
        print("\n2. AUDIENCE SIZE:")
        print("   Enter audience insights:")
        audience_data = []
        while True:
            website = input("   Website (or Enter to finish): ").strip()
            if not website:
                break
            
            # Try API if enabled
            api_data = None
            if use_api:
                print(f"     Fetching data for {website}...")
                api_data = self.fetch_similarweb_api(website)
            
            if api_data:
                visitors = f"{api_data.get('monthly_visits', 'N/A')} monthly visitors"
                demographics = f"Avg visit: {api_data.get('avg_visit_duration', 'N/A')}, Pages: {api_data.get('pages_per_visit', 'N/A')}"
                print(f"     ✓ API data: {visitors}")
            else:
                visitors = input("   Monthly visitors/estimate: ").strip()
                demographics = input("   Key demographics: ").strip()
            
            audience_data.append({
                'website': website,
                'visitors': visitors,
                'demographics': demographics,
                'api_data': api_data
            })
        
        self.similarweb_data = {
            'target_industry': target_industry,
            'demand_analysis': demand_data,
            'audience_size': audience_data,
            'api_used': use_api
        }
        
        print(f"\n✓ Collected SimilarWeb data for {target_industry}")
        return self.similarweb_data
    
    def identify_market_leaders(self):
        """Step 2: Identify market leaders"""
        print("\n" + "="*60)
        print("STEP 2: Identify Market Leaders")
        print("="*60)
        
        print("\nBased on SimilarWeb data, identify top market leaders:")
        print("(Enter company names, one per line, Enter twice when done)\n")
        
        leaders = []
        while True:
            company = input("Company name (or Enter to finish): ").strip()
            if not company:
                break
            website = input(f"  Website for {company}: ").strip()
            market_position = input(f"  Market position (Leader/#2/#3/etc): ").strip()
            leaders.append({
                'company': company,
                'website': website,
                'position': market_position
            })
        
        self.market_leaders = leaders
        print(f"\n✓ Identified {len(leaders)} market leaders")
        return leaders
    
    def fetch_annualreport_content(self, company_name: str) -> Optional[str]:
        """Attempt to fetch annual report content via web scraping"""
        if not HAS_SCRAPING:
            return None
        
        try:
            # Search AnnualReports.com
            search_url = f"https://www.annualreports.com/Companies?search={company_name.replace(' ', '+')}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            # Try to find report link
            report_link = soup.find('a', href=re.compile('/Company/', re.I))
            
            if report_link:
                report_url = 'https://www.annualreports.com' + report_link.get('href', '')
                report_response = requests.get(report_url, headers=headers, timeout=15)
                report_soup = BeautifulSoup(report_response.content, 'html.parser')
                
                # Extract text content
                for element in report_soup(["script", "style", "nav", "footer", "header"]):
                    element.decompose()
                
                text = report_soup.get_text()
                lines = [line.strip() for line in text.splitlines() if line.strip() and len(line.strip()) > 20]
                return '\n'.join(lines[:100])  # First 100 meaningful lines
        except Exception as e:
            print(f"  ⚠ Could not fetch report automatically: {str(e)}")
        
        return None
    
    def collect_annualreports_data(self):
        """Step 3: Collect AnnualReports.com data"""
        print("\n" + "="*60)
        print("STEP 3: AnnualReports.com Analysis")
        print("="*60)
        
        if not self.market_leaders:
            print("No market leaders identified yet. Please complete Step 2 first.")
            return
        
        use_scraping = False
        if HAS_SCRAPING:
            choice = input("\nFetch annual reports automatically via BeautifulSoup scraping? (y/n, default=n): ").strip().lower()
            use_scraping = choice in ('y', 'yes')
        
        if not use_scraping:
            print("\nGo to: https://www.annualreports.com/")
            print("Search for annual reports of the market leaders\n")

        # Automatically open AnnualReports.com in Chrome/default browser
        open_in_chrome("https://www.annualreports.com/")
        
        print("For each market leader, collect annual report insights:\n")
        
        reports_data = []
        for leader in self.market_leaders:
            print(f"\n--- {leader['company']} ---")
            
            # Try to fetch report content automatically via BeautifulSoup (primary)
            report_content = None
            if use_scraping:
                print(f"  Attempting to fetch annual report via BeautifulSoup...")
                report_content = self.fetch_annualreport_content(leader['company'])
                if report_content:
                    print(f"  ✓ Fetched report content via BeautifulSoup ({len(report_content)} chars)")
                    print("  Review the content and extract key insights:")
            
            revenue = input(f"  Revenue/Growth trend: ").strip()
            profit_margin = input(f"  Profit margin: ").strip()
            business_model = input(f"  Key business model insights: ").strip()
            challenges = input(f"  Challenges mentioned in report: ").strip()
            gaps = input(f"  Market gaps/unaddressed needs: ").strip()
            consumer_needs = input(f"  Evolving consumer needs mentioned: ").strip()
            
            reports_data.append({
                'company': leader['company'],
                'revenue': revenue,
                'profit_margin': profit_margin,
                'business_model': business_model,
                'challenges': challenges,
                'gaps': gaps,
                'consumer_needs': consumer_needs,
                'report_content': report_content[:2000] if report_content else None  # Store snippet
            })
        
        self.annualreports_data = {
            'reports': reports_data,
            'api_used': use_api
        }
        
        print(f"\n✓ Collected annual report data for {len(reports_data)} companies")
        return self.annualreports_data
    
    def synthesize_insights(self):
        """Step 4: Synthesize insights"""
        print("\n" + "="*60)
        print("STEP 4: Synthesize Insights")
        print("="*60)
        
        insights = {
            'high_demand_areas': [],
            'large_audiences': [],
            'market_gaps': [],
            'business_model_insights': [],
            'unsolved_problems': []
        }
        
        # High demand + Unmet needs
        print("\nHigh Demand Areas + Unmet Needs:")
        for demand in self.similarweb_data.get('demand_analysis', []):
            if demand.get('trend', '').lower() in ['growing', 'stable']:
                insights['high_demand_areas'].append({
                    'website': demand['website'],
                    'traffic': demand['traffic'],
                    'trend': demand['trend']
                })
        
        # Large audiences
        for audience in self.similarweb_data.get('audience_size', []):
            insights['large_audiences'].append({
                'website': audience['website'],
                'visitors': audience['visitors'],
                'demographics': audience['demographics']
            })
        
        # Market gaps from annual reports
        for report in self.annualreports_data.get('reports', []):
            if report.get('gaps'):
                insights['market_gaps'].append({
                    'company': report['company'],
                    'gap': report['gaps']
                })
            
            if report.get('business_model'):
                insights['business_model_insights'].append({
                    'company': report['company'],
                    'insight': report['business_model']
                })
            
            if report.get('challenges') and report.get('consumer_needs'):
                insights['unsolved_problems'].append({
                    'company': report['company'],
                    'challenge': report['challenges'],
                    'need': report['consumer_needs']
                })
        
        self.insights = insights
        
        print("\n✓ Synthesized insights:")
        print(f"  - High demand areas: {len(insights['high_demand_areas'])}")
        print(f"  - Large audiences: {len(insights['large_audiences'])}")
        print(f"  - Market gaps: {len(insights['market_gaps'])}")
        print(f"  - Business model insights: {len(insights['business_model_insights'])}")
        print(f"  - Unsolved problems: {len(insights['unsolved_problems'])}")
        
        return insights
    
    def generate_chatgpt_prompt_1a(self):
        """Step 5: Generate ChatGPT Prompt 1a"""
        print("\n" + "="*60)
        print("STEP 5: Generate ChatGPT Prompt 1a")
        print("="*60)
        
        prompt = "Give me a business idea based on these:\n\n"
        
        # 1. Demand Analysis
        prompt += "#### 1. Demand Analysis (Using SimilarWeb.io)\n"
        prompt += "SimilarWeb traffic data shows:\n"
        for item in self.insights.get('high_demand_areas', []):
            prompt += f"- {item['website']}: {item['traffic']} traffic ({item['trend']} trend)\n"
        prompt += "\n"
        
        # 2. Audience Size
        prompt += "#### 2. Audience Size (Using SimilarWeb.io)\n"
        prompt += "Audience insights:\n"
        for item in self.insights.get('large_audiences', []):
            prompt += f"- {item['website']}: {item['visitors']} monthly visitors ({item['demographics']})\n"
        prompt += "\n"
        
        # 3. Market Leaders
        prompt += "#### 3. Market Leaders (Using AnnualReports.com)\n"
        prompt += "Leading companies in this space:\n"
        for report in self.annualreports_data.get('reports', []):
            prompt += f"- {report['company']}: Revenue {report['revenue']}, Margin {report['profit_margin']}\n"
        prompt += "\n"
        
        # 4. Shortcomings of Leaders
        prompt += "#### 4. Shortcomings of Leaders\n"
        prompt += "Issues current market leaders are not addressing:\n"
        for item in self.insights.get('market_gaps', []):
            prompt += f"- {item['company']}: {item['gap']}\n"
        prompt += "\n"
        
        # 5. Effective Business Models
        prompt += "#### 5. Effective Business Models (Using AnnualReports.com)\n"
        prompt += "Successful business model insights:\n"
        for item in self.insights.get('business_model_insights', []):
            prompt += f"- {item['company']}: {item['insight']}\n"
        prompt += "\n"
        
        # 6. Unsolved Problems
        prompt += "#### 6. Unsolved Problems (Using Both SimilarWeb.io and AnnualReports.com)\n"
        prompt += "Combined insights on unmet needs:\n"
        for item in self.insights.get('unsolved_problems', []):
            prompt += f"- {item['company']}: Challenge - {item['challenge']}, Need - {item['need']}\n"
        prompt += "\n"
        
        prompt += "Based on this comprehensive analysis, generate business ideas that address these opportunities."
        
        # Save prompt
        with open('chatgpt_prompt_1a.txt', 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        print("\n✓ Prompt 1a generated and saved to 'chatgpt_prompt_1a.txt'")
        print("\nYou can now use this prompt in ChatGPT.")
        
        return prompt
    
    def generate_chatgpt_prompt_1b(self):
        """Step 6: Generate ChatGPT Prompt 1b"""
        print("\n" + "="*60)
        print("STEP 6: Generate ChatGPT Prompt 1b")
        print("="*60)
        
        print("\nEnter viable ideas from ChatGPT response (one per line, Enter twice when done):")
        viable_ideas = []
        while True:
            idea = input("Viable idea: ").strip()
            if not idea:
                break
            viable_ideas.append(idea)
        
        if not viable_ideas:
            print("No viable ideas entered.")
            return
        
        self.viable_ideas = viable_ideas
        
        # Generate Prompt 1b for each idea
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
            'similarweb_data': self.similarweb_data,
            'market_leaders': self.market_leaders,
            'annualreports_data': self.annualreports_data,
            'insights': self.insights,
            'viable_ideas': self.viable_ideas,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ All data saved to '{self.output_file}'")
        open_file_automatically(self.output_file)
    
    def run(self):
        """Main execution flow"""
        print("\n" + "="*60)
        print("Business Idea Formulation Strategy 13")
        print("Multi-Source Comprehensive Analysis")
        print("="*60)
        
        # Step 1: Collect SimilarWeb data
        self.collect_similarweb_data()
        
        # Step 2: Identify market leaders
        self.identify_market_leaders()
        
        # Step 3: Collect AnnualReports data
        self.collect_annualreports_data()
        
        # Step 4: Synthesize insights
        self.synthesize_insights()
        
        # Step 5: Generate Prompt 1a
        self.generate_chatgpt_prompt_1a()
        
        # Step 6: Generate Prompt 1b (after user gets ideas from ChatGPT)
        input("\nPress Enter after you've used Prompt 1a in ChatGPT and received ideas...")
        self.generate_chatgpt_prompt_1b()
        
        # Save data
        self.save_data()
        
        print("\n" + "="*60)
        print("Process Complete!")
        print("="*60)
        print("\nNext steps:")
        print("1. Use Prompt 1a from 'chatgpt_prompt_1a.txt' in ChatGPT")
        print("2. Review the generated business ideas")
        print("3. Select viable ideas and use corresponding Prompt 1b")
        print("4. Cross-reference ideas with your original data insights")

if __name__ == "__main__":
    analyzer = MultiSourceAnalyzer()
    analyzer.run()

