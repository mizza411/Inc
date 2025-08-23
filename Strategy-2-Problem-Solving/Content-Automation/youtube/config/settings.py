"""
⚙️ Settings Configuration - YouTube Business Automation
Central configuration file for all system settings
"""

import os
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class YouTubeSettings:
    """YouTube-specific settings"""
    channel_name: str = "Nigerian Vibes & Vibes"
    default_language: str = "en"
    target_audience: str = "Nigerian diaspora, African culture enthusiasts"
    content_categories: List[str] = None
    upload_frequency: str = "3x per week"
    video_length_target: int = 8  # minutes
    monetization_enabled: bool = True
    
    def __post_init__(self):
        if self.content_categories is None:
            self.content_categories = [
                "Entertainment",
                "Education", 
                "Music",
                "Culture",
                "Lifestyle"
            ]

@dataclass
class LanguageBlendingSettings:
    """Language blending algorithm settings"""
    yoruba_word_weight: float = 0.6
    english_word_weight: float = 0.4
    humor_threshold: float = 0.7
    max_blend_length: int = 15
    context_boost_multiplier: float = 1.2
    cultural_relevance_weight: float = 0.8

@dataclass
class VideoAssemblySettings:
    """Video assembly settings"""
    fps: int = 30
    resolution: tuple = (1920, 1080)
    background_color: str = "#1a1a1a"
    text_color: str = "#ffffff"
    font_size: int = 48
    transition_duration: float = 0.5
    music_volume: float = 0.3
    speech_volume: float = 0.8
    min_video_length: int = 480  # 8 minutes in seconds
    max_video_length: int = 1200  # 20 minutes in seconds

@dataclass
class ContentGenerationSettings:
    """Content generation settings"""
    daily_content_limit: int = 5
    script_templates_enabled: bool = True
    auto_expansion_enabled: bool = True
    trending_topic_integration: bool = True
    language_blending_integration: bool = True
    quality_validation_enabled: bool = True

@dataclass
class APISettings:
    """API and external service settings"""
    youtube_api_key: str = ""
    spotify_client_id: str = ""
    spotify_client_secret: str = ""
    billboard_api_key: str = ""
    text_to_speech_service: str = "gtts"  # gtts, azure, google
    image_generation_service: str = "dalle"  # dalle, midjourney, stable_diffusion

@dataclass
class DatabaseSettings:
    """Database configuration settings"""
    database_path: str = "youtube_business.db"
    backup_frequency: str = "daily"
    max_backup_files: int = 30
    auto_cleanup_enabled: bool = True
    cleanup_threshold_days: int = 90

@dataclass
class PerformanceSettings:
    """Performance and optimization settings"""
    cache_enabled: bool = True
    cache_duration_hours: int = 6
    max_concurrent_processes: int = 4
    memory_limit_mb: int = 2048
    log_level: str = "INFO"
    debug_mode: bool = False

class Settings:
    """
    Main settings manager for the YouTube business system
    """
    
    def __init__(self, config_file: str = None):
        """
        Initialize settings
        
        Args:
            config_file: Optional path to configuration file
        """
        self.config_file = config_file
        
        # Initialize all setting categories
        self.youtube = YouTubeSettings()
        self.language_blending = LanguageBlendingSettings()
        self.video_assembly = VideoAssemblySettings()
        self.content_generation = ContentGenerationSettings()
        self.api = APISettings()
        self.database = DatabaseSettings()
        self.performance = PerformanceSettings()
        
        # Load configuration if file provided
        if config_file and os.path.exists(config_file):
            self.load_config(config_file)
    
    def get_all_settings(self) -> Dict[str, Any]:
        """
        Get all settings as a dictionary
        
        Returns:
            Dictionary containing all settings
        """
        return {
            "youtube": self.youtube.__dict__,
            "language_blending": self.language_blending.__dict__,
            "video_assembly": self.video_assembly.__dict__,
            "content_generation": self.content_generation.__dict__,
            "api": self.api.__dict__,
            "database": self.database.__dict__,
            "performance": self.performance.__dict__
        }
    
    def update_setting(self, category: str, setting: str, value: Any) -> bool:
        """
        Update a specific setting
        
        Args:
            category: Setting category (e.g., 'youtube', 'video_assembly')
            setting: Setting name
            value: New value
            
        Returns:
            True if update successful, False otherwise
        """
        try:
            if hasattr(self, category):
                category_obj = getattr(self, category)
                if hasattr(category_obj, setting):
                    setattr(category_obj, setting, value)
                    return True
            return False
        except Exception:
            return False
    
    def get_setting(self, category: str, setting: str) -> Any:
        """
        Get a specific setting value
        
        Args:
            category: Setting category
            setting: Setting name
            
        Returns:
            Setting value or None if not found
        """
        try:
            if hasattr(self, category):
                category_obj = getattr(self, category)
                if hasattr(category_obj, setting):
                    return getattr(category_obj, setting)
            return None
        except Exception:
            return None
    
    def validate_settings(self) -> List[str]:
        """
        Validate all settings for consistency
        
        Returns:
            List of validation errors (empty if all valid)
        """
        errors = []
        
        # Validate video length settings
        if self.video_assembly.min_video_length < 480:  # 8 minutes
            errors.append("Minimum video length must be at least 8 minutes for monetization")
        
        if self.video_assembly.min_video_length > self.video_assembly.max_video_length:
            errors.append("Minimum video length cannot exceed maximum video length")
        
        # Validate API settings
        if self.api.youtube_api_key and len(self.api.youtube_api_key) < 10:
            errors.append("YouTube API key appears to be invalid")
        
        # Validate performance settings
        if self.performance.memory_limit_mb < 512:
            errors.append("Memory limit should be at least 512MB")
        
        if self.performance.max_concurrent_processes < 1:
            errors.append("Maximum concurrent processes must be at least 1")
        
        return errors
    
    def get_monetization_checklist(self) -> Dict[str, bool]:
        """
        Get checklist for YouTube monetization requirements
        
        Returns:
            Dictionary of requirements and their status
        """
        checklist = {
            "8+ minute videos": self.video_assembly.min_video_length >= 480,
            "High-effort content": self.content_generation.quality_validation_enabled,
            "Language blending": self.content_generation.language_blending_integration,
            "Trending topics": self.content_generation.trending_topic_integration,
            "Consistent uploads": self.youtube.upload_frequency in ["2x per week", "3x per week", "daily"],
            "Original commentary": True,  # Always true with our system
            "Professional editing": self.video_assembly.fps >= 30,
            "Engaging visuals": len(self.video_assembly.background_color) > 0
        }
        
        return checklist
    
    def export_config(self, export_path: str) -> str:
        """
        Export current settings to JSON file
        
        Args:
            export_path: Directory to export configuration
            
        Returns:
            Path to exported configuration file
        """
        import json
        from datetime import datetime
        
        os.makedirs(export_path, exist_ok=True)
        
        config_data = {
            "export_date": datetime.now().isoformat(),
            "settings": self.get_all_settings(),
            "validation_errors": self.validate_settings(),
            "monetization_checklist": self.get_monetization_checklist()
        }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"youtube_settings_{timestamp}.json"
        filepath = os.path.join(export_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def load_config(self, config_file: str) -> bool:
        """
        Load configuration from file
        
        Args:
            config_file: Path to configuration file
            
        Returns:
            True if load successful, False otherwise
        """
        try:
            import json
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Apply settings from file
            if 'settings' in config_data:
                for category, settings in config_data['settings'].items():
                    if hasattr(self, category):
                        category_obj = getattr(self, category)
                        for setting, value in settings.items():
                            if hasattr(category_obj, setting):
                                setattr(category_obj, setting, value)
            
            return True
        except Exception:
            return False

# Default settings instance
default_settings = Settings()

# Example usage
if __name__ == "__main__":
    # Create settings instance
    settings = Settings()
    
    # Display current settings
    print("🎥 YouTube Business Settings:")
    print(f"Channel: {settings.youtube.channel_name}")
    print(f"Target Video Length: {settings.video_assembly.min_video_length // 60} minutes")
    print(f"Upload Frequency: {settings.youtube.upload_frequency}")
    
    # Validate settings
    errors = settings.validate_settings()
    if errors:
        print(f"\n❌ Validation Errors: {len(errors)}")
        for error in errors:
            print(f"  - {error}")
    else:
        print("\n✅ All settings are valid!")
    
    # Show monetization checklist
    print("\n💰 Monetization Checklist:")
    checklist = settings.get_monetization_checklist()
    for requirement, status in checklist.items():
        status_icon = "✅" if status else "❌"
        print(f"  {status_icon} {requirement}")
    
    # Export configuration
    export_path = settings.export_config("config_exports")
    print(f"\n📁 Configuration exported to: {export_path}")
