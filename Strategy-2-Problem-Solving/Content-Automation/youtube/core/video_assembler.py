"""
🎬 Video Assembler - Automated Video Creation System
Assembles complete videos from scripts using text-to-speech, music, and effects
"""

import os
import json
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import random

@dataclass
class VideoSegment:
    """Represents a video segment with audio and visual elements"""
    text: str
    duration: float  # in seconds
    audio_file: str
    background_music: str
    visual_effects: List[str]
    transitions: List[str]

@dataclass
class AssembledVideo:
    """Represents a complete assembled video"""
    title: str
    segments: List[VideoSegment]
    total_duration: float
    output_file: str
    thumbnail_path: str
    metadata: Dict
    assembly_date: datetime

class VideoAssembler:
    """
    Automatically assembles videos from scripts
    Integrates text-to-speech, music, effects, and transitions
    """
    
    def __init__(self, assets_path: str = "assets"):
        """
        Initialize the video assembler
        
        Args:
            assets_path: Path to assets directory
        """
        self.assets_path = assets_path
        self.music_library = os.path.join(assets_path, "music_library")
        self.effect_templates = os.path.join(assets_path, "effect_templates")
        self.brand_assets = os.path.join(assets_path, "brand_assets")
        
        # Video assembly settings
        self.default_settings = {
            "fps": 30,
            "resolution": (1920, 1080),
            "background_color": "#1a1a1a",
            "text_color": "#ffffff",
            "font_size": 48,
            "transition_duration": 0.5,
            "music_volume": 0.3,
            "speech_volume": 0.8
        }
        
        # Available visual effects
        self.visual_effects = [
            "fade_in", "fade_out", "slide_left", "slide_right",
            "zoom_in", "zoom_out", "bounce", "shake", "glow",
            "particle_effects", "text_animations", "color_transitions"
        ]
        
        # Transition types
        self.transition_types = [
            "cross_fade", "slide", "wipe", "dissolve", "zoom",
            "flip", "cube", "page_turn", "iris", "random"
        ]
    
    def assemble_video(self, script_data: Dict, output_path: str = "output") -> AssembledVideo:
        """
        Assemble a complete video from script data
        
        Args:
            script_data: Script data dictionary
            output_path: Output directory for the video
            
        Returns:
            AssembledVideo object
        """
        # Create output directory
        os.makedirs(output_path, exist_ok=True)
        
        # Generate video segments
        segments = self._generate_video_segments(script_data)
        
        # Calculate total duration
        total_duration = sum(segment.duration for segment in segments)
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_path, f"video_{timestamp}.mp4")
        
        # Create thumbnail
        thumbnail_path = self._generate_thumbnail(script_data.get('title', 'Video'), output_path)
        
        # Prepare metadata
        metadata = {
            "title": script_data.get('title', ''),
            "description": script_data.get('description', ''),
            "tags": script_data.get('tags', []),
            "category": script_data.get('category', 'Entertainment'),
            "language": "en",
            "duration": total_duration,
            "resolution": self.default_settings["resolution"],
            "fps": self.default_settings["fps"]
        }
        
        return AssembledVideo(
            title=script_data.get('title', 'Video'),
            segments=segments,
            total_duration=total_duration,
            output_file=output_file,
            thumbnail_path=thumbnail_path,
            metadata=metadata,
            assembly_date=datetime.now()
        )
    
    def _generate_video_segments(self, script_data: Dict) -> List[VideoSegment]:
        """
        Generate video segments from script data
        
        Args:
            script_data: Script data dictionary
            
        Returns:
            List of VideoSegment objects
        """
        segments = []
        
        # Hook segment
        if 'hook' in script_data:
            hook_segment = self._create_segment(
                script_data['hook'],
                segment_type="hook",
                duration_multiplier=1.2  # Hook gets more time
            )
            segments.append(hook_segment)
        
        # Introduction segment
        if 'introduction' in script_data:
            intro_segment = self._create_segment(
                script_data['introduction'],
                segment_type="introduction",
                duration_multiplier=1.0
            )
            segments.append(intro_segment)
        
        # Main content segments
        if 'main_content' in script_data:
            for i, content in enumerate(script_data['main_content']):
                content_segment = self._create_segment(
                    content,
                    segment_type="main_content",
                    duration_multiplier=1.0,
                    segment_index=i
                )
                segments.append(content_segment)
        
        # Conclusion segment
        if 'conclusion' in script_data:
            conclusion_segment = self._create_segment(
                script_data['conclusion'],
                segment_type="conclusion",
                duration_multiplier=0.8  # Conclusion is shorter
            )
            segments.append(conclusion_segment)
        
        # Call to action segment
        if 'call_to_action' in script_data:
            cta_segment = self._create_segment(
                script_data['call_to_action'],
                segment_type="call_to_action",
                duration_multiplier=0.9
            )
            segments.append(cta_segment)
        
        return segments
    
    def _create_segment(self, text: str, segment_type: str, 
                       duration_multiplier: float = 1.0, 
                       segment_index: int = 0) -> VideoSegment:
        """
        Create a video segment from text
        
        Args:
            text: Text content for the segment
            segment_type: Type of segment (hook, introduction, etc.)
            duration_multiplier: Multiplier for duration calculation
            segment_index: Index of the segment
            
        Returns:
            VideoSegment object
        """
        # Calculate duration based on text length (average speaking rate: 150 words per minute)
        words = len(text.split())
        base_duration = (words / 150) * 60  # Convert to seconds
        duration = base_duration * duration_multiplier
        
        # Generate audio file path
        audio_file = f"audio_{segment_type}_{segment_index}.mp3"
        
        # Select background music based on segment type
        background_music = self._select_background_music(segment_type)
        
        # Select visual effects
        visual_effects = self._select_visual_effects(segment_type, segment_index)
        
        # Select transitions
        transitions = self._select_transitions(segment_type, segment_index)
        
        return VideoSegment(
            text=text,
            duration=duration,
            audio_file=audio_file,
            background_music=background_music,
            visual_effects=visual_effects,
            transitions=transitions
        )
    
    def _select_background_music(self, segment_type: str) -> str:
        """
        Select appropriate background music for segment type
        
        Args:
            segment_type: Type of video segment
            
        Returns:
            Background music file path
        """
        music_mapping = {
            "hook": ["upbeat_intro.mp3", "energetic_start.mp3", "attention_grabbing.mp3"],
            "introduction": ["warm_welcome.mp3", "friendly_greeting.mp3", "casual_intro.mp3"],
            "main_content": ["steady_rhythm.mp3", "conversational.mp3", "engaging_background.mp3"],
            "conclusion": ["wrapping_up.mp3", "gentle_finish.mp3", "smooth_end.mp3"],
            "call_to_action": ["motivational.mp3", "action_oriented.mp3", "inspiring_close.mp3"]
        }
        
        available_music = music_mapping.get(segment_type, ["default_background.mp3"])
        return random.choice(available_music)
    
    def _select_visual_effects(self, segment_type: str, segment_index: int) -> List[str]:
        """
        Select visual effects for segment type
        
        Args:
            segment_type: Type of video segment
            segment_index: Index of the segment
            
        Returns:
            List of visual effects
        """
        effects_mapping = {
            "hook": ["fade_in", "zoom_in", "glow", "particle_effects"],
            "introduction": ["slide_left", "fade_in", "text_animations"],
            "main_content": ["fade_in", "text_animations", "color_transitions"],
            "conclusion": ["fade_out", "slide_right", "gentle_effects"],
            "call_to_action": ["bounce", "glow", "attention_effects"]
        }
        
        available_effects = effects_mapping.get(segment_type, ["fade_in"])
        
        # Select 2-3 effects per segment
        num_effects = random.randint(2, 3)
        selected_effects = random.sample(available_effects, min(num_effects, len(available_effects)))
        
        return selected_effects
    
    def _select_transitions(self, segment_type: str, segment_index: int) -> List[str]:
        """
        Select transitions for segment type
        
        Args:
            segment_type: Type of video segment
            segment_index: Index of the segment
            
        Returns:
            List of transition types
        """
        # Hook and introduction get special transitions
        if segment_type in ["hook", "introduction"]:
            return ["fade_in", "zoom_in"]
        
        # Main content gets varied transitions
        if segment_type == "main_content":
            transitions = ["cross_fade", "slide", "dissolve"]
            return random.sample(transitions, 1)
        
        # Conclusion and CTA get smooth transitions
        if segment_type in ["conclusion", "call_to_action"]:
            return ["fade_out", "cross_fade"]
        
        return ["cross_fade"]
    
    def _generate_thumbnail(self, title: str, output_path: str) -> str:
        """
        Generate thumbnail for the video
        
        Args:
            title: Video title
            output_path: Output directory path
            
        Returns:
            Thumbnail file path
        """
        # Generate thumbnail filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        thumbnail_filename = f"thumbnail_{timestamp}.jpg"
        thumbnail_path = os.path.join(output_path, thumbnail_filename)
        
        # In a real implementation, you would:
        # 1. Create a canvas with the specified resolution
        # 2. Add background image or color
        # 3. Add title text with styling
        # 4. Add brand elements
        # 5. Save as JPG
        
        # For now, return the path
        return thumbnail_path
    
    def get_assembly_summary(self, video: AssembledVideo) -> str:
        """
        Get a summary of the assembled video
        
        Args:
            video: AssembledVideo object
            
        Returns:
            Formatted summary string
        """
        summary = f"🎬 VIDEO ASSEMBLY SUMMARY\n"
        summary += f"Title: {video.title}\n"
        summary += f"Total Duration: {video.total_duration:.2f} seconds ({video.total_duration/60:.2f} minutes)\n"
        summary += f"Segments: {len(video.segments)}\n"
        summary += f"Output File: {video.output_file}\n"
        summary += f"Thumbnail: {video.thumbnail_path}\n"
        summary += f"Assembly Date: {video.assembly_date.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        summary += "📋 SEGMENT BREAKDOWN:\n"
        for i, segment in enumerate(video.segments, 1):
            summary += f"{i}. {segment.text[:50]}... ({segment.duration:.2f}s)\n"
            summary += f"   Audio: {segment.audio_file}\n"
            summary += f"   Music: {segment.background_music}\n"
            summary += f"   Effects: {', '.join(segment.visual_effects)}\n"
            summary += f"   Transitions: {', '.join(segment.transitions)}\n\n"
        
        return summary
    
    def export_assembly_data(self, video: AssembledVideo, export_path: str) -> str:
        """
        Export assembly data to JSON file
        
        Args:
            video: AssembledVideo object
            export_path: Export directory path
            
        Returns:
            Export file path
        """
        os.makedirs(export_path, exist_ok=True)
        
        # Convert to serializable format
        export_data = {
            "title": video.title,
            "total_duration": video.total_duration,
            "output_file": video.output_file,
            "thumbnail_path": video.thumbnail_path,
            "metadata": video.metadata,
            "assembly_date": video.assembly_date.isoformat(),
            "segments": []
        }
        
        for segment in video.segments:
            segment_data = {
                "text": segment.text,
                "duration": segment.duration,
                "audio_file": segment.audio_file,
                "background_music": segment.background_music,
                "visual_effects": segment.visual_effects,
                "transitions": segment.transitions
            }
            export_data["segments"].append(segment_data)
        
        # Export to JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_filename = f"assembly_data_{timestamp}.json"
        export_file_path = os.path.join(export_path, export_filename)
        
        with open(export_file_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return export_file_path

# Example usage
if __name__ == "__main__":
    assembler = VideoAssembler()
    
    # Sample script data
    sample_script = {
        "title": "Omo, This Song is Giving Me Serious Wahala!",
        "hook": "Omo, you won't believe what I just discovered about this trending song!",
        "introduction": "Welcome back to the channel! Today we're diving deep into this viral music phenomenon.",
        "main_content": [
            "Let's talk about why this song is trending. This is where things get really interesting because music has a way of bringing people together.",
            "When I think about the cultural impact, I can't help but notice how it connects to our daily lives."
        ],
        "conclusion": "So there you have it! This song is definitely more complex than we thought, right?",
        "call_to_action": "If you enjoyed this video, make sure to like, subscribe, and hit that notification bell!"
    }
    
    # Assemble video
    print("🎬 Assembling video...")
    assembled_video = assembler.assemble_video(sample_script)
    
    # Display summary
    summary = assembler.get_assembly_summary(assembled_video)
    print(summary)
    
    # Export data
    export_path = assembler.export_assembly_data(assembled_video, "exports")
    print(f"📁 Assembly data exported to: {export_path}")
