#!/usr/bin/env python3
"""
Nigerian Content Creation - News Fetcher
Automated news fetching for content creation
"""

import requests
import json
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time
import random
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NewsFetcher:
    def __init__(self, db_path: str = "content_creation.db"):
        """Initialize the news fetcher with database connection"""
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.setup_database()
    
    def setup_database(self):
        """Setup database tables for storing news and trends"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS news_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT,
                    source TEXT NOT NULL,
                    category TEXT NOT NULL,
                    url TEXT,
                    published_date DATETIME,
                    fetched_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    processed BOOLEAN DEFAULT FALSE,
                    content_quality_score FLOAT DEFAULT 0.0
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS trending_topics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    category TEXT NOT NULL,
                    popularity_score INTEGER DEFAULT 0,
                    source TEXT,
                    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    processed BOOLEAN DEFAULT FALSE
                )
            ''')
            
            conn.commit()
    
    def fetch_nigerian_news(self) -> List[Dict]:
        """Fetch latest Nigerian news from multiple sources"""
        news_items = []
        
        # Nigerian news sources
        sources = [
            {
                'name': 'Punch Newspapers',
                'url': 'https://punchng.com/',
                'category': 'naija_news'
            },
            {
                'name': 'Vanguard',
                'url': 'https://vanguardngr.com/',
                'category': 'naija_news'
            },
            {
                'name': 'This Day',
                'url': 'https://thisdaylive.com/',
                'category': 'naija_news'
            },
            {
                'name': 'Premium Times',
                'url': 'https://premiumtimesng.com/',
                'category': 'naija_news'
            }
        ]
        
        for source in sources:
            try:
                logger.info(f"Fetching news from {source['name']}")
                news = self._scrape_news_site(source['url'], source['name'], source['category'])
                news_items.extend(news)
                time.sleep(random.uniform(1, 3))  # Be respectful to servers
            except Exception as e:
                logger.error(f"Error fetching from {source['name']}: {str(e)}")
        
        return news_items
    
    def fetch_it_news(self) -> List[Dict]:
        """Fetch latest IT and tech news"""
        it_news = []
        
        # IT news sources
        sources = [
            {
                'name': 'Tech Point Africa',
                'url': 'https://techpoint.africa/',
                'category': 'it_news'
            },
            {
                'name': 'Tech Cabal',
                'url': 'https://techcabal.com/',
                'category': 'it_news'
            },
            {
                'name': 'Disrupt Africa',
                'url': 'https://disrupt-africa.com/',
                'category': 'it_news'
            }
        ]
        
        for source in sources:
            try:
                logger.info(f"Fetching IT news from {source['name']}")
                news = self._scrape_news_site(source['url'], source['name'], source['category'])
                it_news.extend(news)
                time.sleep(random.uniform(1, 3))
            except Exception as e:
                logger.error(f"Error fetching from {source['name']}: {str(e)}")
        
        return it_news
    
    def _scrape_news_site(self, url: str, source_name: str, category: str) -> List[Dict]:
        """Scrape news from a specific website"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            news_items = []
            
            # Common selectors for news headlines
            selectors = [
                'h1', 'h2', 'h3', 'h4',
                '.headline', '.title', '.news-title',
                'article h2', '.post-title', '.entry-title'
            ]
            
            for selector in selectors:
                headlines = soup.select(selector)
                for headline in headlines[:10]:  # Limit to first 10
                    title = headline.get_text().strip()
                    if len(title) > 20 and len(title) < 200:  # Reasonable length
                        news_items.append({
                            'title': title,
                            'content': title,  # For now, use title as content
                            'source': source_name,
                            'category': category,
                            'url': url,
                            'published_date': datetime.now(),
                            'content_quality_score': self._calculate_quality_score(title)
                        })
            
            return news_items
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return []
    
    def _calculate_quality_score(self, text: str) -> float:
        """Calculate content quality score for filtering"""
        score = 0.0
        
        # Length score (optimal length for one-liners)
        if 30 <= len(text) <= 100:
            score += 0.3
        elif 20 <= len(text) <= 150:
            score += 0.2
        
        # Keyword score (interesting topics)
        interesting_keywords = [
            'naira', 'dollar', 'fuel', 'electricity', 'internet', 'phone',
            'tech', 'startup', 'money', 'business', 'government', 'politics',
            'sport', 'entertainment', 'food', 'transport', 'education'
        ]
        
        text_lower = text.lower()
        for keyword in interesting_keywords:
            if keyword in text_lower:
                score += 0.1
        
        # Avoid duplicate content
        if text.count(' ') > 3:  # Has multiple words
            score += 0.2
        
        return min(score, 1.0)
    
    def fetch_social_media_trends(self) -> List[Dict]:
        """Fetch trending topics from social media"""
        trends = []
        
        # Mock trending topics (in real implementation, use Twitter API or similar)
        mock_trends = [
            {'topic': 'Naira devaluation', 'category': 'naija_news', 'popularity': 95},
            {'topic': 'Fuel scarcity', 'category': 'naija_news', 'popularity': 88},
            {'topic': 'Tech startup funding', 'category': 'it_news', 'popularity': 82},
            {'topic': 'Internet shutdown', 'category': 'it_news', 'popularity': 75},
            {'topic': 'Electricity bill increase', 'category': 'naija_news', 'popularity': 90},
            {'topic': 'Mobile money adoption', 'category': 'it_news', 'popularity': 70},
            {'topic': 'E-commerce boom', 'category': 'it_news', 'popularity': 65},
            {'topic': 'Government policies', 'category': 'naija_news', 'popularity': 85}
        ]
        
        for trend in mock_trends:
            trends.append({
                'topic': trend['topic'],
                'category': trend['category'],
                'popularity_score': trend['popularity'],
                'source': 'social_media',
                'processed': False
            })
        
        return trends
    
    def save_news_items(self, news_items: List[Dict]):
        """Save news items to database"""
        with sqlite3.connect(self.db_path) as conn:
            for item in news_items:
                conn.execute('''
                    INSERT INTO news_items (title, content, source, category, url, published_date, content_quality_score)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    item['title'], item['content'], item['source'], 
                    item['category'], item['url'], item['published_date'],
                    item['content_quality_score']
                ))
            conn.commit()
    
    def save_trending_topics(self, trends: List[Dict]):
        """Save trending topics to database"""
        with sqlite3.connect(self.db_path) as conn:
            for trend in trends:
                conn.execute('''
                    INSERT INTO trending_topics (topic, category, popularity_score, source)
                    VALUES (?, ?, ?, ?)
                ''', (
                    trend['topic'], trend['category'], 
                    trend['popularity_score'], trend['source']
                ))
            conn.commit()
    
    def get_unprocessed_news(self, limit: int = 50) -> List[Dict]:
        """Get unprocessed news items for content creation"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT * FROM news_items 
                WHERE processed = FALSE AND content_quality_score > 0.3
                ORDER BY content_quality_score DESC, fetched_date DESC
                LIMIT ?
            ''', (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def get_unprocessed_trends(self, limit: int = 20) -> List[Dict]:
        """Get unprocessed trending topics"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT * FROM trending_topics 
                WHERE processed = FALSE
                ORDER BY popularity_score DESC, created_date DESC
                LIMIT ?
            ''', (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def mark_as_processed(self, item_id: int, table: str = 'news_items'):
        """Mark an item as processed"""
        with sqlite3.connect(self.db_path) as conn:
            if table == 'news_items':
                conn.execute('UPDATE news_items SET processed = TRUE WHERE id = ?', (item_id,))
            elif table == 'trending_topics':
                conn.execute('UPDATE trending_topics SET processed = TRUE WHERE id = ?', (item_id,))
            conn.commit()
    
    def run_daily_fetch(self):
        """Run the complete daily news fetching process"""
        logger.info("Starting daily news fetch...")
        
        # Fetch Nigerian news
        nigerian_news = self.fetch_nigerian_news()
        logger.info(f"Fetched {len(nigerian_news)} Nigerian news items")
        
        # Fetch IT news
        it_news = self.fetch_it_news()
        logger.info(f"Fetched {len(it_news)} IT news items")
        
        # Fetch social media trends
        trends = self.fetch_social_media_trends()
        logger.info(f"Fetched {len(trends)} trending topics")
        
        # Save all items
        self.save_news_items(nigerian_news + it_news)
        self.save_trending_topics(trends)
        
        logger.info("Daily news fetch completed successfully!")

if __name__ == "__main__":
    # Test the news fetcher
    fetcher = NewsFetcher()
    fetcher.run_daily_fetch()
    
    # Get some unprocessed items
    news_items = fetcher.get_unprocessed_news(5)
    trends = fetcher.get_unprocessed_trends(5)
    
    print(f"Found {len(news_items)} news items and {len(trends)} trends for content creation") 