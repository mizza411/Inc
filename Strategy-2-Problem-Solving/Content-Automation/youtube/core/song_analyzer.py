"""
🎵 Song Analyzer - Trending Song Analysis & Lyric Extraction
Analyzes popular songs to find trending terms and create viral content
"""

import requests
import json
import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import time

@dataclass
class SongData:
    """Represents analyzed song data"""
    title: str
    artist: str
    lyrics: str
    trending_score: float
    viral_terms: List[str]
    language_blend_opportunities: List[str]
    content_ideas: List[str]
    analysis_date: datetime

@dataclass
class TrendingTerm:
    """Represents a trending term found in songs"""
    term: str
    frequency: int
    context: str
    viral_potential: float
    language_blend_suggestions: List[str]

class SongAnalyzer:
    """
    Analyzes trending songs to extract viral terms and content opportunities
    Integrates with language blender for content creation
    """
    
    def __init__(self, api_keys: Dict[str, str] = None):
        """
        Initialize the song analyzer
        
        Args:
            api_keys: Dictionary of API keys for different services
        """
        self.api_keys = api_keys or {}
        self.cache = {}
        self.cache_duration = timedelta(hours=6)
        
        # Popular song sources (can be expanded with APIs)
        self.trending_sources = {
            "billboard": "https://www.billboard.com/charts/hot-100",
            "spotify": "https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF",  # Global Top 50
            "youtube": "https://www.youtube.com/feed/trending?bp=4gINGgtBdGhlcm9pZGVz",
        }
        
        # Common viral terms patterns
        self.viral_patterns = [
            r'\b\w{3,8}\b',  # 3-8 letter words
            r'\b[A-Z][a-z]+\b',  # Capitalized words
            r'\b\w+ing\b',  # Words ending in 'ing'
            r'\b\w+ed\b',  # Words ending in 'ed'
        ]
        
        # Language blending opportunities
        self.blending_opportunities = [
            "fire", "lit", "banging", "sick", "dope", "fresh",
            "crazy", "insane", "wild", "amazing", "perfect",
            "beautiful", "gorgeous", "stunning", "incredible"
        ]
    
    def analyze_trending_songs(self, count: int = 10) -> List[SongData]:
        """
        Analyze trending songs to extract viral content opportunities
        
        Args:
            count: Number of songs to analyze
            
        Returns:
            List of analyzed song data
        """
        songs = []
        
        # Get trending songs from multiple sources
        trending_songs = self._get_trending_songs(count)
        
        for song in trending_songs:
            try:
                # Analyze each song
                song_data = self._analyze_single_song(song)
                if song_data:
                    songs.append(song_data)
                
                # Rate limiting
                time.sleep(1)
                
            except Exception as e:
                print(f"Error analyzing song {song.get('title', 'Unknown')}: {e}")
                continue
        
        # Sort by trending score
        songs.sort(key=lambda x: x.trending_score, reverse=True)
        return songs
    
    def extract_viral_terms(self, lyrics: str) -> List[TrendingTerm]:
        """
        Extract viral terms from song lyrics
        
        Args:
            lyrics: Song lyrics text
            
        Returns:
            List of trending terms with viral potential
        """
        # Clean lyrics
        clean_lyrics = self._clean_lyrics(lyrics)
        
        # Find potential viral terms
        terms = {}
        words = clean_lyrics.split()
        
        for word in words:
            word = word.lower().strip()
            if self._is_viral_candidate(word):
                if word in terms:
                    terms[word]['frequency'] += 1
                else:
                    terms[word] = {
                        'term': word,
                        'frequency': 1,
                        'context': self._get_word_context(word, clean_lyrics),
                        'viral_potential': self._calculate_viral_potential(word),
                        'language_blend_suggestions': []
                    }
        
        # Convert to TrendingTerm objects
        trending_terms = []
        for term_data in terms.values():
            trending_term = TrendingTerm(**term_data)
            trending_terms.append(trending_term)
        
        # Sort by viral potential
        trending_terms.sort(key=lambda x: x.viral_potential, reverse=True)
        return trending_terms
    
    def generate_content_ideas(self, song_data: SongData) -> List[str]:
        """
        Generate content ideas based on song analysis
        
        Args:
            song_data: Analyzed song data
            
        Returns:
            List of content ideas
        """
        ideas = []
        
        # Reaction video ideas
        ideas.append(f"Reacting to '{song_data.title}' by {song_data.artist}")
        ideas.append(f"Breaking down the lyrics of '{song_data.title}'")
        ideas.append(f"Why '{song_data.title}' is trending right now")
        
        # Language blending ideas
        for term in song_data.viral_terms[:5]:
            ideas.append(f"Creating Yoruba-English terms from '{term}'")
            ideas.append(f"Reacting to '{term}' in Nigerian style")
        
        # Cultural commentary
        ideas.append(f"Cultural analysis of '{song_data.title}'")
        ideas.append(f"Nigerian perspective on {song_data.artist}'s music")
        
        # Trending analysis
        ideas.append(f"Trending terms from '{song_data.title}' explained")
        ideas.append(f"Viral words that will make you laugh")
        
        return ideas
    
    def _get_trending_songs(self, count: int) -> List[Dict]:
        """
        Get trending songs from various sources
        
        Args:
            count: Number of songs to retrieve
            
        Returns:
            List of song information dictionaries
        """
        # This is a placeholder - in production, you'd integrate with real APIs
        # For now, return sample trending songs
        sample_songs = [
            {
                "title": "Vampire",
                "artist": "Olivia Rodrigo",
                "lyrics": "I used to think I was smart, but you made me look so naive...",
                "trending_score": 9.5
            },
            {
                "title": "Flowers",
                "artist": "Miley Cyrus", 
                "lyrics": "I can buy myself flowers, write my name in the sand...",
                "trending_score": 9.2
            },
            {
                "title": "Last Night",
                "artist": "Morgan Wallen",
                "lyrics": "Last night we let the liquor talk, I can't remember everything we said...",
                "trending_score": 8.9
            }
        ]
        
        return sample_songs[:count]
    
    def _analyze_single_song(self, song: Dict) -> Optional[SongData]:
        """
        Analyze a single song for content opportunities
        
        Args:
            song: Song information dictionary
            
        Returns:
            Analyzed song data or None if analysis fails
        """
        try:
            # Extract viral terms
            viral_terms = self.extract_viral_terms(song.get('lyrics', ''))
            
            # Find language blending opportunities
            blend_opportunities = self._find_blending_opportunities(song.get('lyrics', ''))
            
            # Generate content ideas
            content_ideas = self.generate_content_ideas(SongData(
                title=song.get('title', ''),
                artist=song.get('artist', ''),
                lyrics=song.get('lyrics', ''),
                trending_score=song.get('trending_score', 0.0),
                viral_terms=[term.term for term in viral_terms],
                language_blend_opportunities=blend_opportunities,
                content_ideas=[],
                analysis_date=datetime.now()
            ))
            
            return SongData(
                title=song.get('title', ''),
                artist=song.get('artist', ''),
                lyrics=song.get('lyrics', ''),
                trending_score=song.get('trending_score', 0.0),
                viral_terms=[term.term for term in viral_terms],
                language_blend_opportunities=blend_opportunities,
                content_ideas=content_ideas,
                analysis_date=datetime.now()
            )
            
        except Exception as e:
            print(f"Error in song analysis: {e}")
            return None
    
    def _clean_lyrics(self, lyrics: str) -> str:
        """
        Clean and normalize lyrics text
        
        Args:
            lyrics: Raw lyrics text
            
        Returns:
            Cleaned lyrics text
        """
        # Remove special characters and normalize
        cleaned = re.sub(r'[^\w\s]', ' ', lyrics)
        cleaned = re.sub(r'\s+', ' ', cleaned)
        return cleaned.strip().lower()
    
    def _is_viral_candidate(self, word: str) -> bool:
        """
        Check if a word is a potential viral candidate
        
        Args:
            word: Word to check
            
        Returns:
            True if word is a viral candidate
        """
        # Basic filters
        if len(word) < 3 or len(word) > 12:
            return False
        
        # Skip common words
        common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        if word in common_words:
            return False
        
        # Check for viral patterns
        for pattern in self.viral_patterns:
            if re.match(pattern, word):
                return True
        
        return False
    
    def _get_word_context(self, word: str, lyrics: str) -> str:
        """
        Get context around a word in lyrics
        
        Args:
            word: Target word
            lyrics: Full lyrics text
            
        Returns:
            Context string
        """
        words = lyrics.split()
        try:
            word_index = words.index(word)
            start = max(0, word_index - 2)
            end = min(len(words), word_index + 3)
            context_words = words[start:end]
            return ' '.join(context_words)
        except ValueError:
            return word
    
    def _calculate_viral_potential(self, word: str) -> float:
        """
        Calculate viral potential score for a word
        
        Args:
            word: Word to score
            
        Returns:
            Viral potential score (0.0 to 1.0)
        """
        score = 0.5
        
        # Length bonus
        if 4 <= len(word) <= 8:
            score += 0.2
        
        # Ending patterns
        if word.endswith(('ing', 'ed', 'er', 'est')):
            score += 0.1
        
        # Capitalization potential
        if word[0].isupper():
            score += 0.1
        
        # Language blending potential
        if word.lower() in self.blending_opportunities:
            score += 0.3
        
        return min(1.0, score)
    
    def _find_blending_opportunities(self, lyrics: str) -> List[str]:
        """
        Find words that are good candidates for language blending
        
        Args:
            lyrics: Song lyrics
            
        Returns:
            List of blending opportunity words
        """
        opportunities = []
        words = self._clean_lyrics(lyrics).split()
        
        for word in words:
            if word.lower() in self.blending_opportunities:
                opportunities.append(word)
        
        return list(set(opportunities))  # Remove duplicates

# Example usage
if __name__ == "__main__":
    analyzer = SongAnalyzer()
    
    # Analyze trending songs
    print("🎵 Analyzing trending songs...")
    songs = analyzer.analyze_trending_songs(3)
    
    for song in songs:
        print(f"\n🎤 {song.title} by {song.artist}")
        print(f"📊 Trending Score: {song.trending_score}")
        print(f"🔥 Viral Terms: {', '.join(song.viral_terms[:5])}")
        print(f"💡 Content Ideas: {len(song.content_ideas)} generated")
        
        # Show top content ideas
        for i, idea in enumerate(song.content_ideas[:3], 1):
            print(f"   {i}. {idea}")
