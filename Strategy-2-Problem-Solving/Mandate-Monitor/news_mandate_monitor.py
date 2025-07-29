import requests
import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get NewsAPI key from environment variable
API_KEY = os.getenv('NEWSAPI_KEY')

# Keywords to search for
KEYWORDS = [
    'government has mandated',
    'government requires',
    'government mandate',
    'government regulation',
    'government compulsory',
    'government order',
]

# NewsAPI endpoint
NEWSAPI_URL = 'https://newsapi.org/v2/everything'

# Output file
OUTPUT_FILE = 'government_mandates_news.txt'

def fetch_news(keyword):
    params = {
        'q': keyword,
        'language': 'en',
        'sortBy': 'publishedAt',
        'apiKey': API_KEY,
        'pageSize': 10,
    }
    response = requests.get(NEWSAPI_URL, params=params)
    if response.status_code == 200:
        return response.json().get('articles', [])
    else:
        print(f"Error fetching news for '{keyword}': {response.status_code}")
        return []

def main():
    if not API_KEY:
        print("Error: NEWSAPI_KEY not found in environment variables. Please add it to your .env file.")
        return
    all_results = []
    for keyword in KEYWORDS:
        articles = fetch_news(keyword)
        for article in articles:
            all_results.append({
                'keyword': keyword,
                'title': article.get('title'),
                'url': article.get('url'),
                'publishedAt': article.get('publishedAt'),
                'source': article.get('source', {}).get('name'),
                'description': article.get('description'),
            })
    # Write results to file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"Government Mandate News Update - {datetime.datetime.now()}\n\n")
        for item in all_results:
            f.write(f"Keyword: {item['keyword']}\n")
            f.write(f"Title: {item['title']}\n")
            f.write(f"Source: {item['source']}\n")
            f.write(f"Published At: {item['publishedAt']}\n")
            f.write(f"URL: {item['url']}\n")
            f.write(f"Description: {item['description']}\n\n")
        if not all_results:
            f.write("No new government mandate news found today.\n")
    print(f"Results saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    print("If you haven't already, install python-dotenv with: pip install python-dotenv")
    main() 