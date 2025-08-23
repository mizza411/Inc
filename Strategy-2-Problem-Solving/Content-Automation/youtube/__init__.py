"""
🎥 YouTube Business Automation System
Automated faceless video creation with English-Yoruba language blending
"""

__version__ = "1.0.0"
__author__ = "AI Assistant"
__description__ = "YouTube Business Automation for Faceless Videos"

# Import core modules
from .core.language_blender import LanguageBlender
from .core.song_analyzer import SongAnalyzer
from .core.script_generator import ScriptGenerator
from .core.video_assembler import VideoAssembler

# Import utility modules
from .utils.thumbnail_creator import ThumbnailCreator
from .utils.trend_analyzer import TrendAnalyzer
from .utils.performance_tracker import PerformanceTracker
from .utils.text_to_speech import TextToSpeech
from .utils.video_effects import VideoEffects

# Import database modules
from .database.youtube_schema import YouTubeSchema
from .database.content_tracker import ContentTracker
from .database.monetization_checker import MonetizationChecker

# Import configuration
from .config.settings import Settings
from .config.youtube_policies import YouTubePolicies

__all__ = [
    # Core modules
    'LanguageBlender',
    'SongAnalyzer', 
    'ScriptGenerator',
    'VideoAssembler',
    
    # Utility modules
    'ThumbnailCreator',
    'TrendAnalyzer',
    'PerformanceTracker',
    'TextToSpeech',
    'VideoEffects',
    
    # Database modules
    'YouTubeSchema',
    'ContentTracker',
    'MonetizationChecker',
    
    # Configuration
    'Settings',
    'YouTubePolicies',
]
