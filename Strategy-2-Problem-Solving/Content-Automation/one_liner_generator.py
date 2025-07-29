#!/usr/bin/env python3
"""
Nigerian Content Creation - One-Liner Generator
Generates funny one-liners based on news and trends
"""

import sqlite3
import random
import re
from datetime import datetime
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class OneLinerGenerator:
    def __init__(self, db_path: str = "content_creation.db"):
        """Initialize the one-liner generator"""
        self.db_path = db_path
        self.setup_database()
        self.load_templates()
    
    def setup_database(self):
        """Setup database table for generated one-liners"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS generated_content (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_text TEXT NOT NULL,
                    one_liner TEXT NOT NULL,
                    category TEXT NOT NULL,
                    humor_type TEXT NOT NULL,
                    quality_score FLOAT DEFAULT 0.0,
                    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    processed BOOLEAN DEFAULT FALSE,
                    image_created BOOLEAN DEFAULT FALSE
                )
            ''')
            conn.commit()
    
    def load_templates(self):
        """Load humor templates for different categories"""
        self.naija_templates = [
            "Only in Nigeria: {topic} but we still dey manage 😂",
            "Naija people and {topic} - name a better duo 🤝",
            "When {topic} happen, we just dey like 'na wa o' 😅",
            "Nigeria: where {topic} is just another Tuesday 🗓️",
            "Abeg, who else notice say {topic}? 👀",
            "Meanwhile in Nigeria: {topic} but the generator still dey work ⚡",
            "Naija life: {topic} but we go survive 💪",
            "Only in 9ja: {topic} and we still dey smile 😊",
            "When {topic} dey happen, we just dey like 'God abeg' 🙏",
            "Nigeria: {topic} but the hustle never stops 💼",
            "Abeg, {topic} no be new thing for this country 🇳🇬",
            "Naija people when {topic}: *nervous laughter* 😅",
            "Meanwhile: {topic} but the internet still dey work 📱",
            "Only in Nigeria: {topic} and we still dey manage somehow 🤷‍♂️",
            "When {topic} happen, we just dey like 'na normal' 😂"
        ]
        
        self.it_templates = [
            "Tech people when {topic}: *nervous laughter* 😅",
            "Meanwhile in tech: {topic} but the WiFi still dey work 📶",
            "IT department be like: {topic}? Have you tried turning it off and on? 🔄",
            "Tech trend: {topic}. Me: still using Windows 7 💻",
            "Silicon Valley: {topic}. Naija developers: 'we go manage' 💪",
            "When {topic} happen in tech: *panic mode activated* 😱",
            "Tech world: {topic}. Me: still trying to understand blockchain 🤔",
            "Meanwhile developers: {topic} but the code still dey work 💻",
            "Tech startup when {topic}: *sweating profusely* 😰",
            "IT support: {topic}? Let me Google that for you 🔍",
            "Tech conference: {topic}. Attendees: *taking notes furiously* 📝",
            "When {topic} trend: everyone becomes an expert overnight 🧠",
            "Tech industry: {topic}. Me: still using Internet Explorer 🌐",
            "Startup founders when {topic}: *checking bank account nervously* 💰",
            "Tech news: {topic}. Me: still trying to understand AI 🤖"
        ]
        
        self.general_templates = [
            "Life be like: {topic} but we move 🚶‍♂️",
            "When {topic} happen: *insert shocked face* 😲",
            "Meanwhile: {topic} and we still dey here 😂",
            "Only in this world: {topic} but life goes on 🌍",
            "When {topic} trend: everyone becomes a commentator 📢",
            "Life: {topic}. Me: *confused noises* 🤷‍♀️",
            "Meanwhile somewhere: {topic} and people dey survive 💪",
            "When {topic} happen: *insert dramatic music* 🎵",
            "Life be like: {topic} but we still dey manage somehow 😅",
            "Meanwhile in the world: {topic} and we still dey smile 😊"
        ]
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract key topics from text for humor generation"""
        # Common Nigerian and tech keywords
        keywords = []
        
        # Nigerian-specific keywords
        naija_keywords = [
            'naira', 'dollar', 'fuel', 'electricity', 'generator', 'internet',
            'phone', 'data', 'transport', 'traffic', 'government', 'politics',
            'sport', 'football', 'entertainment', 'food', 'education', 'health',
            'money', 'business', 'market', 'price', 'scarcity', 'shortage'
        ]
        
        # Tech-specific keywords
        tech_keywords = [
            'tech', 'startup', 'funding', 'investment', 'app', 'software',
            'internet', 'social media', 'digital', 'online', 'mobile',
            'AI', 'artificial intelligence', 'blockchain', 'crypto',
            'e-commerce', 'fintech', 'edtech', 'healthtech', 'agritech'
        ]
        
        text_lower = text.lower()
        
        # Extract Nigerian keywords
        for keyword in naija_keywords:
            if keyword in text_lower:
                keywords.append(keyword)
        
        # Extract tech keywords
        for keyword in tech_keywords:
            if keyword in text_lower:
                keywords.append(keyword)
        
        # Extract other potential topics (words with 4+ characters)
        words = re.findall(r'\b\w{4,}\b', text_lower)
        keywords.extend(words[:3])  # Add first 3 longer words
        
        return list(set(keywords))  # Remove duplicates
    
    def generate_one_liners(self, text: str, category: str, count: int = 5) -> List[Dict]:
        """Generate multiple one-liners based on input text"""
        one_liners = []
        keywords = self.extract_keywords(text)
        
        # Choose appropriate templates based on category
        if category == 'naija_news':
            templates = self.naija_templates
            humor_type = 'naija_humor'
        elif category == 'it_news':
            templates = self.it_templates
            humor_type = 'tech_humor'
        else:
            templates = self.general_templates
            humor_type = 'general_humor'
        
        # Generate one-liners using different approaches
        for i in range(count):
            one_liner = self._create_one_liner(text, keywords, templates, humor_type)
            if one_liner:
                one_liners.append({
                    'original_text': text,
                    'one_liner': one_liner,
                    'category': category,
                    'humor_type': humor_type,
                    'quality_score': self._calculate_humor_score(one_liner),
                    'created_date': datetime.now()
                })
        
        return one_liners
    
    def _create_one_liner(self, text: str, keywords: List[str], templates: List[str], humor_type: str) -> Optional[str]:
        """Create a single one-liner using various techniques"""
        try:
            # Method 1: Use template with extracted topic
            if keywords:
                topic = random.choice(keywords)
                template = random.choice(templates)
                one_liner = template.format(topic=topic)
                return one_liner
            
            # Method 2: Create from scratch based on text
            if len(text) > 20:
                # Extract a shorter version of the text
                words = text.split()
                if len(words) > 5:
                    short_text = ' '.join(words[:5])
                    if humor_type == 'naija_humor':
                        return f"Only in Nigeria: {short_text} but we still dey manage 😂"
                    elif humor_type == 'tech_humor':
                        return f"Tech people when {short_text}: *nervous laughter* 😅"
                    else:
                        return f"Life be like: {short_text} but we move 🚶‍♂️"
            
            # Method 3: Generic response
            if humor_type == 'naija_humor':
                return "Only in Nigeria: we go manage somehow 😂"
            elif humor_type == 'tech_humor':
                return "Tech world: have you tried turning it off and on? 🔄"
            else:
                return "Life: we still dey manage 💪"
                
        except Exception as e:
            logger.error(f"Error creating one-liner: {str(e)}")
            return None
    
    def _calculate_humor_score(self, one_liner: str) -> float:
        """Calculate humor quality score"""
        score = 0.0
        
        # Length score (optimal for social media)
        if 50 <= len(one_liner) <= 150:
            score += 0.3
        elif 30 <= len(one_liner) <= 200:
            score += 0.2
        
        # Emoji score (engaging content)
        emoji_count = len(re.findall(r'[😀-🙏🌀-🗿]', one_liner))
        score += min(emoji_count * 0.1, 0.3)
        
        # Nigerian slang score
        naija_slang = ['dey', 'abeg', 'na', 'o', 'wahala', 'manage', 'hustle']
        text_lower = one_liner.lower()
        for slang in naija_slang:
            if slang in text_lower:
                score += 0.1
        
        # Humor indicators
        humor_words = ['laugh', 'funny', 'haha', 'lol', '😂', '😅', '😊']
        for word in humor_words:
            if word in text_lower:
                score += 0.1
        
        # Avoid excessive punctuation
        if one_liner.count('!') <= 2 and one_liner.count('?') <= 2:
            score += 0.1
        
        return min(score, 1.0)
    
    def save_generated_content(self, one_liners: List[Dict]):
        """Save generated one-liners to database"""
        with sqlite3.connect(self.db_path) as conn:
            for one_liner in one_liners:
                conn.execute('''
                    INSERT INTO generated_content (original_text, one_liner, category, humor_type, quality_score, created_date)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    one_liner['original_text'], one_liner['one_liner'], 
                    one_liner['category'], one_liner['humor_type'],
                    one_liner['quality_score'], one_liner['created_date']
                ))
            conn.commit()
    
    def get_unprocessed_content(self, limit: int = 20) -> List[Dict]:
        """Get unprocessed generated content for image creation"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT * FROM generated_content 
                WHERE processed = FALSE AND quality_score > 0.4
                ORDER BY quality_score DESC, created_date DESC
                LIMIT ?
            ''', (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def mark_as_processed(self, content_id: int):
        """Mark content as processed"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('UPDATE generated_content SET processed = TRUE WHERE id = ?', (content_id,))
            conn.commit()
    
    def mark_as_image_created(self, content_id: int):
        """Mark content as having image created"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('UPDATE generated_content SET image_created = TRUE WHERE id = ?', (content_id,))
            conn.commit()
    
    def process_news_items(self, news_items: List[Dict]):
        """Process news items and generate one-liners"""
        logger.info(f"Processing {len(news_items)} news items for one-liner generation")
        
        all_one_liners = []
        
        for item in news_items:
            try:
                # Generate one-liners for each news item
                one_liners = self.generate_one_liners(
                    text=item['title'],
                    category=item['category'],
                    count=3  # Generate 3 one-liners per news item
                )
                
                all_one_liners.extend(one_liners)
                
            except Exception as e:
                logger.error(f"Error processing news item {item.get('id', 'unknown')}: {str(e)}")
        
        # Save all generated content
        if all_one_liners:
            self.save_generated_content(all_one_liners)
            logger.info(f"Generated and saved {len(all_one_liners)} one-liners")
        
        return all_one_liners
    
    def process_trending_topics(self, trends: List[Dict]):
        """Process trending topics and generate one-liners"""
        logger.info(f"Processing {len(trends)} trending topics for one-liner generation")
        
        all_one_liners = []
        
        for trend in trends:
            try:
                # Generate one-liners for each trend
                one_liners = self.generate_one_liners(
                    text=trend['topic'],
                    category=trend['category'],
                    count=2  # Generate 2 one-liners per trend
                )
                
                all_one_liners.extend(one_liners)
                
            except Exception as e:
                logger.error(f"Error processing trend {trend.get('id', 'unknown')}: {str(e)}")
        
        # Save all generated content
        if all_one_liners:
            self.save_generated_content(all_one_liners)
            logger.info(f"Generated and saved {len(all_one_liners)} one-liners from trends")
        
        return all_one_liners

if __name__ == "__main__":
    # Test the one-liner generator
    generator = OneLinerGenerator()
    
    # Test with sample news items
    test_news = [
        {
            'title': 'Naira falls to new low against dollar in parallel market',
            'category': 'naija_news'
        },
        {
            'title': 'Tech startup raises $5 million in Series A funding',
            'category': 'it_news'
        }
    ]
    
    # Generate one-liners
    one_liners = generator.process_news_items(test_news)
    
    print(f"Generated {len(one_liners)} one-liners:")
    for i, one_liner in enumerate(one_liners, 1):
        print(f"{i}. {one_liner['one_liner']}")
        print(f"   Quality Score: {one_liner['quality_score']:.2f}")
        print() 