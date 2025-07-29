"""
Live Gadget Scraper (Non-Phone Gadgets)
Fetches live gadget data from a popular e-commerce site, excluding phones/smartphones.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from demand_analyzer import calculate_demand_score

# URLs for non-phone gadgets (smartwatches, headphones, speakers, etc.)
GADGET_URLS = [
    "https://www.jumia.com.ng/smartwatches/",
    "https://www.jumia.com.ng/headphones/",
    "https://www.jumia.com.ng/speakers/",
    "https://www.jumia.com.ng/tablets/",
    "https://www.jumia.com.ng/laptops/"
]

def fetch_live_gadgets(urls: List[str] = GADGET_URLS, max_items: int = 10) -> List[Dict[str, str]]:
    """
    Scrape live non-phone gadget data from multiple e-commerce URLs with demand analysis.
    Args:
        urls: List of URLs to try for scraping gadgets.
        max_items: Maximum number of gadgets to fetch.
    Returns:
        List of dictionaries with gadget info (name, price, link) and demand data.
    """
    gadgets = []
    
    for i, url in enumerate(urls):
        try:
            print(f"Trying URL {i+1}/{len(urls)}: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.select('article.prd')
            
            if products:
                for product in products[:max_items]:
                    name = product.select_one('h3.name')
                    price = product.select_one('div.prc')
                    link = product.select_one('a.core')
                    
                    gadget_name = name.text.strip() if name else 'N/A'
                    
                    # Get demand analysis for the gadget
                    demand_data = calculate_demand_score(gadget_name)
                    
                    gadgets.append({
                        'name': gadget_name,
                        'price': price.text.strip() if price else 'N/A',
                        'link': f"https://www.jumia.com.ng{link['href']}" if link and link.has_attr('href') else 'N/A',
                        'source': f'Jumia Nigeria - {url.split("/")[-2]}',
                        'demand_score': demand_data['demand_score'],
                        'demand_level': demand_data['demand_level'],
                        'trending': demand_data['trending'],
                        'recommendation': demand_data['recommendation']
                    })
                print(f"Found {len(gadgets)} gadgets from {url}")
                break
            else:
                print(f"No products found at {url}")
                if i < len(urls) - 1:  # Not the last URL
                    user_input = input(f"No gadgets found. Try next URL ({urls[i+1]})? (y/n): ").strip().lower()
                    if user_input != 'y':
                        break
                        
        except Exception as e:
            print(f"Error fetching from {url}: {e}")
            if i < len(urls) - 1:  # Not the last URL
                user_input = input(f"Error occurred. Try next URL ({urls[i+1]})? (y/n): ").strip().lower()
                if user_input != 'y':
                    break
    
    # Sort gadgets by demand score (highest demand first)
    gadgets.sort(key=lambda x: x.get('demand_score', 0), reverse=True)
    return gadgets

if __name__ == "__main__":
    live_gadgets = fetch_live_gadgets()
    for g in live_gadgets:
        print(f"{g['name']}: {g['demand_level']} demand (Score: {g['demand_score']}) - {g['recommendation']}") 