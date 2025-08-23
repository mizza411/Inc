"""
🎵 Trending Song Analyzer - Advanced Music Trend Detection System
Analyzes trending songs from multiple platforms to identify viral content opportunities
Integrates with Spotify, YouTube, Billboard, and TikTok APIs for comprehensive trend analysis
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TrendingSong:
    """Represents a trending song with comprehensive metadata"""
    title: str
    artist: str
    platform: str
    popularity_score: float
    viral_potential: float
    cultural_relevance: float
    trending_score: float
    release_date: datetime
    genre: str
    lyrics: Optional[str]
    audio_features: Dict
    social_metrics: Dict
    created_at: datetime

@dataclass
class TrendAnalysis:
    """Comprehensive trend analysis results"""
    trending_songs: List[TrendingSong]
    top_viral_candidates: List[TrendingSong]
    cultural_opportunities: List[TrendingSong]
    cross_platform_validation: Dict
    analysis_timestamp: datetime
    confidence_score: float

class TrendingSongAnalyzer:
    """
    Advanced trending song analyzer with multi-platform integration
    Identifies viral content opportunities for YouTube business automation
    """
    
    def __init__(self, config: Dict):
        """Initialize the trending song analyzer with configuration"""
        self.config = config
        self.spotify_token = config.get('spotify_token')
        self.youtube_api_key = config.get('youtube_api_key')
        self.billboard_api_key = config.get('billboard_api_key')
        
        # API endpoints
        self.spotify_base_url = "https://api.spotify.com/v1"
        self.youtube_base_url = "https://www.googleapis.com/youtube/v3"
        self.billboard_base_url = "https://api.billboard.com/v1"
        
        # Rate limiting and caching
        self.request_cache = {}
        self.last_request_time = {}
        self.rate_limit_delays = {
            'spotify': 0.1,      # 10 requests per second
            'youtube': 0.1,      # 10 requests per second
            'billboard': 0.6     # 1 request per 0.6 seconds
        }
        
        # Trending playlists and categories
        self.spotify_trending_playlists = [
            '37i9dQZEVXbMDoHDwVN2tF',  # Global Top 50
            '37i9dQZEVXbLiRSasKsNU9',  # Viral 50
            '37i9dQZEVXbMDoHDwVN2tF'   # Trending Now
        ]
        
        self.youtube_music_categories = [
            '10',  # Music
            '24',  # Entertainment
            '25'   # News & Politics
        ]
    
    def analyze_trending_songs(self) -> TrendAnalysis:
        """
        Main method to analyze trending songs across all platforms
        Returns comprehensive trend analysis for content creation
        """
        logger.info("🎵 Starting comprehensive trending song analysis...")
        
        try:
            # Collect trending songs from all platforms
            all_trending_songs = []
            
            # Spotify analysis (primary source)
            if self.spotify_token:
                spotify_songs = self._analyze_spotify_trends()
                all_trending_songs.extend(spotify_songs)
                logger.info(f"✅ Spotify: Found {len(spotify_songs)} trending songs")
            
            # YouTube analysis (secondary validation)
            if self.youtube_api_key:
                youtube_songs = self._analyze_youtube_trends()
                all_trending_songs.extend(youtube_songs)
                logger.info(f"✅ YouTube: Found {len(youtube_songs)} trending songs")
            
            # Billboard analysis (historical context)
            if self.billboard_api_key:
                billboard_songs = self._analyze_billboard_trends()
                all_trending_songs.extend(billboard_songs)
                logger.info(f"✅ Billboard: Found {len(billboard_songs)} trending songs")
            
            # Remove duplicates and calculate comprehensive scores
            unique_songs = self._deduplicate_songs(all_trending_songs)
            scored_songs = self._calculate_comprehensive_scores(unique_songs)
            
            # Cross-platform validation
            cross_platform_data = self._cross_validate_trends(scored_songs)
            
            # Identify top opportunities
            top_viral = self._identify_top_viral_candidates(scored_songs)
            cultural_opportunities = self._identify_cultural_opportunities(scored_songs)
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence_score(scored_songs, cross_platform_data)
            
            analysis = TrendAnalysis(
                trending_songs=scored_songs,
                top_viral_candidates=top_viral,
                cultural_opportunities=cultural_opportunities,
                cross_platform_validation=cross_platform_data,
                analysis_timestamp=datetime.now(),
                confidence_score=confidence_score
            )
            
            logger.info(f"🎯 Analysis complete: {len(scored_songs)} songs analyzed, "
                       f"confidence: {confidence_score:.2f}")
            
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Error in trending song analysis: {str(e)}")
            raise
    
    def _analyze_spotify_trends(self) -> List[TrendingSong]:
        """Analyze trending songs from Spotify playlists"""
        trending_songs = []
        
        for playlist_id in self.spotify_trending_playlists:
            try:
                # Respect rate limiting
                self._respect_rate_limit('spotify')
                
                # Get playlist tracks
                url = f"{self.spotify_base_url}/playlists/{playlist_id}/tracks"
                headers = {"Authorization": f"Bearer {self.spotify_token}"}
                
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                
                playlist_data = response.json()
                
                for item in playlist_data.get('items', []):
                    track = item.get('track', {})
                    if not track:
                        continue
                    
                    # Get detailed track information
                    track_id = track.get('id')
                    if track_id:
                        track_details = self._get_spotify_track_details(track_id)
                        if track_details:
                            trending_song = self._create_trending_song_from_spotify(track_details)
                            trending_songs.append(trending_song)
                
                logger.info(f"📊 Spotify playlist {playlist_id}: {len(trending_songs)} songs found")
                
            except Exception as e:
                logger.warning(f"⚠️ Error analyzing Spotify playlist {playlist_id}: {str(e)}")
                continue
        
        return trending_songs
    
    def _analyze_youtube_trends(self) -> List[TrendingSong]:
        """Analyze trending music videos from YouTube"""
        trending_songs = []
        
        for category_id in self.youtube_music_categories:
            try:
                # Respect rate limiting
                self._respect_rate_limit('youtube')
                
                # Get trending videos in music category
                url = f"{self.youtube_base_url}/videos"
                params = {
                    'part': 'snippet,statistics,contentDetails',
                    'chart': 'mostPopular',
                    'videoCategoryId': category_id,
                    'maxResults': 25,
                    'key': self.youtube_api_key
                }
                
                response = requests.get(url, params=params)
                response.raise_for_status()
                
                videos_data = response.json()
                
                for video in videos_data.get('items', []):
                    trending_song = self._create_trending_song_from_youtube(video)
                    trending_songs.append(trending_song)
                
                logger.info(f"📺 YouTube category {category_id}: {len(trending_songs)} videos found")
                
            except Exception as e:
                logger.warning(f"⚠️ Error analyzing YouTube category {category_id}: {str(e)}")
                continue
        
        return trending_songs
    
    def _analyze_billboard_trends(self) -> List[TrendingSong]:
        """Analyze Billboard Hot 100 trends (historical context)"""
        trending_songs = []
        
        try:
            # Respect rate limiting
            self._respect_rate_limit('billboard')
            
            # Get Billboard Hot 100
            url = f"{self.billboard_base_url}/charts/hot-100"
            headers = {"Authorization": f"Bearer {self.billboard_api_key}"}
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            chart_data = response.json()
            
            for entry in chart_data.get('entries', [])[:25]:  # Top 25 for trending analysis
                trending_song = self._create_trending_song_from_billboard(entry)
                trending_songs.append(trending_song)
            
            logger.info(f"📊 Billboard Hot 100: {len(trending_songs)} songs analyzed")
            
        except Exception as e:
            logger.warning(f"⚠️ Error analyzing Billboard trends: {str(e)}")
        
        return trending_songs
    
    def _get_spotify_track_details(self, track_id: str) -> Optional[Dict]:
        """Get detailed track information from Spotify"""
        try:
            self._respect_rate_limit('spotify')
            
            url = f"{self.spotify_base_url}/tracks/{track_id}"
            headers = {"Authorization": f"Bearer {self.spotify_token}"}
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.warning(f"⚠️ Error getting Spotify track details: {str(e)}")
            return None
    
    def _create_trending_song_from_spotify(self, track_data: Dict) -> TrendingSong:
        """Create TrendingSong object from Spotify track data"""
        return TrendingSong(
            title=track_data.get('name', 'Unknown'),
            artist=track_data.get('artists', [{}])[0].get('name', 'Unknown'),
            platform='spotify',
            popularity_score=track_data.get('popularity', 0) / 100,
            viral_potential=0.0,  # Will be calculated later
            cultural_relevance=0.0,  # Will be calculated later
            trending_score=0.0,  # Will be calculated later
            release_date=datetime.fromisoformat(track_data.get('album', {}).get('release_date', '2025-01-01')),
            genre=track_data.get('album', {}).get('genres', ['Unknown'])[0] if track_data.get('album', {}).get('genres') else 'Unknown',
            lyrics=None,  # Spotify doesn't provide lyrics in basic API
            audio_features={},  # Will be fetched separately if needed
            social_metrics={
                'followers': track_data.get('followers', {}).get('total', 0),
                'playlist_appearances': 1
            },
            created_at=datetime.now()
        )
    
    def _create_trending_song_from_youtube(self, video_data: Dict) -> TrendingSong:
        """Create TrendingSong object from YouTube video data"""
        snippet = video_data.get('snippet', {})
        statistics = video_data.get('statistics', {})
        
        return TrendingSong(
            title=snippet.get('title', 'Unknown'),
            artist=snippet.get('channelTitle', 'Unknown'),
            platform='youtube',
            popularity_score=min(1.0, int(statistics.get('viewCount', 0)) / 1000000),  # Normalize to 1M views
            viral_potential=0.0,  # Will be calculated later
            cultural_relevance=0.0,  # Will be calculated later
            trending_score=0.0,  # Will be calculated later
            release_date=datetime.fromisoformat(snippet.get('publishedAt', '2025-01-01T00:00:00Z').replace('Z', '+00:00')),
            genre='Music Video',
            lyrics=None,  # YouTube doesn't provide lyrics
            audio_features={},
            social_metrics={
                'views': int(statistics.get('viewCount', 0)),
                'likes': int(statistics.get('likeCount', 0)),
                'comments': int(statistics.get('commentCount', 0))
            },
            created_at=datetime.now()
        )
    
    def _create_trending_song_from_billboard(self, entry_data: Dict) -> TrendingSong:
        """Create TrendingSong object from Billboard chart data"""
        return TrendingSong(
            title=entry_data.get('title', 'Unknown'),
            artist=entry_data.get('artist', 'Unknown'),
            platform='billboard',
            popularity_score=1.0 - (entry_data.get('rank', 100) / 100),  # Higher rank = higher score
            viral_potential=0.0,  # Will be calculated later
            cultural_relevance=0.0,  # Will be calculated later
            trending_score=0.0,  # Will be calculated later
            release_date=datetime.now() - timedelta(days=entry_data.get('weeks_on_chart', 0) * 7),
            genre=entry_data.get('genre', 'Unknown'),
            lyrics=None,
            audio_features={},
            social_metrics={
                'rank': entry_data.get('rank', 100),
                'weeks_on_chart': entry_data.get('weeks_on_chart', 0),
                'peak_position': entry_data.get('peak_position', 100)
            },
            created_at=datetime.now()
        )
    
    def _deduplicate_songs(self, songs: List[TrendingSong]) -> List[TrendingSong]:
        """Remove duplicate songs based on title and artist similarity"""
        unique_songs = []
        seen_combinations = set()
        
        for song in songs:
            # Create a normalized key for comparison
            key = f"{song.title.lower().strip()}_{song.artist.lower().strip()}"
            
            if key not in seen_combinations:
                seen_combinations.add(key)
                unique_songs.append(song)
            else:
                # If duplicate found, merge platforms and update social metrics
                existing_song = next(s for s in unique_songs if 
                                   f"{s.title.lower().strip()}_{s.artist.lower().strip()}" == key)
                existing_song.platform += f",{song.platform}"
                
                # Merge social metrics
                for metric, value in song.social_metrics.items():
                    if metric in existing_song.social_metrics:
                        existing_song.social_metrics[metric] += value
                    else:
                        existing_song.social_metrics[metric] = value
        
        return unique_songs
    
    def _calculate_comprehensive_scores(self, songs: List[TrendingSong]) -> List[TrendingSong]:
        """Calculate comprehensive scores for all songs"""
        for song in songs:
            # Calculate viral potential
            song.viral_potential = self._calculate_viral_potential(song)
            
            # Calculate cultural relevance
            song.cultural_relevance = self._calculate_cultural_relevance(song)
            
            # Calculate final trending score
            song.trending_score = self._calculate_trending_score(song)
        
        # Sort by trending score
        songs.sort(key=lambda x: x.trending_score, reverse=True)
        return songs
    
    def _calculate_viral_potential(self, song: TrendingSong) -> float:
        """Calculate viral potential score based on multiple factors"""
        base_score = song.popularity_score
        
        # Time decay factor (newer songs get boost)
        days_since_release = (datetime.now() - song.release_date).days
        time_boost = max(0.5, 1 - (days_since_release * 0.1))
        
        # Engagement multiplier (if available)
        engagement_boost = 1.0
        if song.platform == 'youtube' and 'views' in song.social_metrics:
            views = song.social_metrics['views']
            likes = song.social_metrics.get('likes', 0)
            if views > 0:
                engagement_rate = likes / views
                engagement_boost = min(2.0, 1 + engagement_rate * 10)
        
        # Platform diversity bonus
        platform_bonus = 1.0
        if ',' in song.platform:
            platform_bonus = 1.2  # 20% bonus for appearing on multiple platforms
        
        return min(1.0, base_score * time_boost * engagement_boost * platform_bonus)
    
    def _calculate_cultural_relevance(self, song: TrendingSong) -> float:
        """Calculate cultural relevance for language blending opportunities"""
        # Cultural keyword matching
        cultural_keywords = ['africa', 'nigeria', 'yoruba', 'afrobeats', 'amapiano', 
                           'african', 'nigerian', 'west africa', 'lagos', 'abuja']
        
        title_lower = song.title.lower()
        artist_lower = song.artist.lower()
        
        keyword_matches = 0
        for keyword in cultural_keywords:
            if keyword in title_lower or keyword in artist_lower:
                keyword_matches += 1
        
        keyword_score = min(1.0, keyword_matches / len(cultural_keywords))
        
        # Genre relevance
        genre_score = 0.0
        if any(genre in song.genre.lower() for genre in ['afro', 'african', 'world', 'reggae', 'dancehall']):
            genre_score = 0.8
        elif 'pop' in song.genre.lower() or 'hip hop' in song.genre.lower():
            genre_score = 0.6
        else:
            genre_score = 0.3
        
        # Geographic relevance (if available)
        geo_score = 0.5  # Default neutral score
        
        return (keyword_score + genre_score + geo_score) / 3
    
    def _calculate_trending_score(self, song: TrendingSong) -> float:
        """Calculate final trending score combining all factors"""
        # Weighted combination of all scores
        weights = {
            'popularity': 0.3,
            'viral_potential': 0.4,
            'cultural_relevance': 0.3
        }
        
        final_score = (
            song.popularity_score * weights['popularity'] +
            song.viral_potential * weights['viral_potential'] +
            song.cultural_relevance * weights['cultural_relevance']
        )
        
        return min(1.0, max(0.0, final_score))
    
    def _cross_validate_trends(self, songs: List[TrendingSong]) -> Dict:
        """Cross-validate trends across platforms for confidence"""
        validation_data = {
            'total_songs': len(songs),
            'platform_distribution': {},
            'cross_platform_matches': 0,
            'confidence_factors': []
        }
        
        # Count platform distribution
        for song in songs:
            platforms = song.platform.split(',')
            for platform in platforms:
                validation_data['platform_distribution'][platform] = \
                    validation_data['platform_distribution'].get(platform, 0) + 1
        
        # Count cross-platform matches
        for song in songs:
            if ',' in song.platform:
                validation_data['cross_platform_matches'] += 1
        
        # Calculate confidence factors
        if validation_data['total_songs'] > 0:
            cross_platform_rate = validation_data['cross_platform_matches'] / validation_data['total_songs']
            validation_data['confidence_factors'].append(f"Cross-platform rate: {cross_platform_rate:.2f}")
        
        return validation_data
    
    def _identify_top_viral_candidates(self, songs: List[TrendingSong]) -> List[TrendingSong]:
        """Identify top viral candidates for content creation"""
        # Filter songs with high viral potential and trending scores
        viral_candidates = [
            song for song in songs 
            if song.viral_potential >= 0.7 and song.trending_score >= 0.6
        ]
        
        # Sort by trending score and return top 10
        viral_candidates.sort(key=lambda x: x.trending_score, reverse=True)
        return viral_candidates[:10]
    
    def _identify_cultural_opportunities(self, songs: List[TrendingSong]) -> List[TrendingSong]:
        """Identify songs with high cultural relevance for language blending"""
        # Filter songs with high cultural relevance
        cultural_opportunities = [
            song for song in songs 
            if song.cultural_relevance >= 0.6
        ]
        
        # Sort by cultural relevance and return top 10
        cultural_opportunities.sort(key=lambda x: x.cultural_relevance, reverse=True)
        return cultural_opportunities[:10]
    
    def _calculate_confidence_score(self, songs: List[TrendingSong], cross_platform_data: Dict) -> float:
        """Calculate overall confidence score for the analysis"""
        if not songs:
            return 0.0
        
        # Base confidence from data quality
        data_quality_score = min(1.0, len(songs) / 50)  # Normalize to 50 songs
        
        # Cross-platform validation score
        cross_platform_score = 0.0
        if cross_platform_data['total_songs'] > 0:
            cross_platform_rate = cross_platform_data['cross_platform_matches'] / cross_platform_data['total_songs']
            cross_platform_score = cross_platform_rate
        
        # Platform diversity score
        platform_diversity = len(cross_platform_data['platform_distribution'])
        diversity_score = min(1.0, platform_diversity / 3)  # Normalize to 3 platforms
        
        # Weighted combination
        confidence = (
            data_quality_score * 0.4 +
            cross_platform_score * 0.4 +
            diversity_score * 0.2
        )
        
        return min(1.0, max(0.0, confidence))
    
    def _respect_rate_limit(self, platform: str):
        """Respect API rate limits by adding delays"""
        if platform in self.last_request_time:
            time_since_last = time.time() - self.last_request_time[platform]
            delay_needed = self.rate_limit_delays.get(platform, 0.1)
            
            if time_since_last < delay_needed:
                time.sleep(delay_needed - time_since_last)
        
        self.last_request_time[platform] = time.time()
    
    def get_trending_summary(self) -> str:
        """Get a human-readable summary of current trends"""
        try:
            analysis = self.analyze_trending_songs()
            
            summary = f"""
🎵 TRENDING SONGS ANALYSIS SUMMARY
{'='*50}
📊 Total Songs Analyzed: {len(analysis.trending_songs)}
🎯 Top Viral Candidates: {len(analysis.top_viral_candidates)}
🌍 Cultural Opportunities: {len(analysis.cultural_opportunities)}
✅ Confidence Score: {analysis.confidence_score:.2f}

🔥 TOP 5 TRENDING SONGS:
"""
            
            for i, song in enumerate(analysis.trending_songs[:5], 1):
                summary += f"""
{i}. {song.title} - {song.artist}
   Platform: {song.platform}
   Trending Score: {song.trending_score:.2f}
   Viral Potential: {song.viral_potential:.2f}
   Cultural Relevance: {song.cultural_relevance:.2f}
"""
            
            summary += f"""
🌍 TOP CULTURAL OPPORTUNITIES:
"""
            
            for i, song in enumerate(analysis.cultural_opportunities[:3], 1):
                summary += f"""
{i}. {song.title} - {song.artist}
   Cultural Score: {song.cultural_relevance:.2f}
   Perfect for language blending content!
"""
            
            summary += f"""
📈 Analysis completed at: {analysis.analysis_timestamp.strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            return summary
            
        except Exception as e:
            return f"❌ Error generating trending summary: {str(e)}"


# Example usage and testing
if __name__ == "__main__":
    # Sample configuration (replace with actual API keys)
    config = {
        'spotify_token': 'your_spotify_token_here',
        'youtube_api_key': 'your_youtube_api_key_here',
        'billboard_api_key': 'your_billboard_api_key_here'
    }
    
    # Create analyzer instance
    analyzer = TrendingSongAnalyzer(config)
    
    # Get trending summary
    summary = analyzer.get_trending_summary()
    print(summary)
