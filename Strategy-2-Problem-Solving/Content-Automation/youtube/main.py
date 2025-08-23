"""
🎥 YouTube Business Automation - Main Integration System
Main entry point that integrates all components for automated video creation
"""

import sys
import os
from datetime import datetime
from typing import Dict, List, Optional

# Add the parent directory to the path to import from Content-Automation
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our YouTube business modules
from core.language_blender import LanguageBlender
from core.song_analyzer import SongAnalyzer
from core.script_generator import ScriptGenerator
from core.video_assembler import VideoAssembler
from config.settings import Settings

class YouTubeBusinessSystem:
    """
    Main integration system for YouTube business automation
    Coordinates all components for end-to-end video creation
    """
    
    def __init__(self):
        """Initialize the YouTube business system"""
        self.settings = Settings()
        self.language_blender = LanguageBlender()
        self.song_analyzer = SongAnalyzer()
        self.script_generator = ScriptGenerator()
        self.video_assembler = VideoAssembler()
        
        print("🎥 YouTube Business Automation System Initialized!")
        print(f"Channel: {self.settings.youtube.channel_name}")
        print(f"Target Video Length: {self.settings.video_assembly.min_video_length // 60} minutes")
    
    def create_complete_video(self, topic: str, context: str = "music", 
                            target_minutes: int = 8) -> Dict:
        """
        Create a complete video from start to finish
        
        Args:
            topic: Main topic for the video
            context: Content context (music, food, culture, etc.)
            target_minutes: Target video length in minutes
            
        Returns:
            Dictionary with video creation results
        """
        print(f"\n🎬 Creating video: {topic}")
        print(f"Context: {context}")
        print(f"Target Length: {target_minutes} minutes")
        
        try:
            # Step 1: Generate language blends for the topic
            print("\n1️⃣ Generating language blends...")
            language_blends = self.language_blender.generate_content_batch(5, context)
            
            # Step 2: Analyze trending songs for viral terms
            print("2️⃣ Analyzing trending songs...")
            trending_songs = self.song_analyzer.analyze_trending_songs(3)
            
            # Step 3: Generate video script
            print("3️⃣ Generating video script...")
            script = self.script_generator.generate_script(topic, context, target_minutes)
            
            # Step 4: Assemble video
            print("4️⃣ Assembling video...")
            script_data = {
                "title": script.title,
                "hook": script.hook,
                "introduction": script.introduction,
                "main_content": script.main_content,
                "conclusion": script.conclusion,
                "call_to_action": script.call_to_action,
                "description": f"Automated video about {topic} with English-Yoruba language blending",
                "tags": ["nigerian", "yoruba", "culture", "humor", "trending"],
                "category": "Entertainment"
            }
            
            assembled_video = self.video_assembler.assemble_video(script_data)
            
            # Step 5: Prepare results
            results = {
                "success": True,
                "video_title": script.title,
                "script": script,
                "assembled_video": assembled_video,
                "language_blends": [term.blended_result for term in language_blends],
                "trending_songs": [song.title for song in trending_songs],
                "creation_date": datetime.now().isoformat(),
                "estimated_duration": script.estimated_duration,
                "target_length": script.target_length
            }
            
            print(f"\n✅ Video creation completed successfully!")
            print(f"Title: {script.title}")
            print(f"Duration: {script.estimated_duration} minutes")
            print(f"Language Blends: {len(results['language_blends'])}")
            
            return results
            
        except Exception as e:
            print(f"\n❌ Error creating video: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "creation_date": datetime.now().isoformat()
            }
    
    def generate_content_batch(self, topics: List[str], context: str = "music") -> List[Dict]:
        """
        Generate multiple videos in batch
        
        Args:
            topics: List of topics for videos
            context: Content context
            
        Returns:
            List of video creation results
        """
        print(f"\n🚀 Starting batch content generation for {len(topics)} topics...")
        
        results = []
        for i, topic in enumerate(topics, 1):
            print(f"\n--- Processing {i}/{len(topics)}: {topic} ---")
            result = self.create_complete_video(topic, context)
            results.append(result)
            
            # Add delay between videos to avoid overwhelming the system
            if i < len(topics):
                print("⏳ Waiting 5 seconds before next video...")
                import time
                time.sleep(5)
        
        return results
    
    def get_system_status(self) -> Dict:
        """
        Get current system status and health
        
        Returns:
            Dictionary with system status information
        """
        status = {
            "system_name": "YouTube Business Automation",
            "status": "operational",
            "timestamp": datetime.now().isoformat(),
            "settings": self.settings.get_all_settings(),
            "validation_errors": self.settings.validate_settings(),
            "monetization_checklist": self.settings.get_monetization_checklist(),
            "components": {
                "language_blender": "ready",
                "song_analyzer": "ready", 
                "script_generator": "ready",
                "video_assembler": "ready"
            }
        }
        
        # Check for any validation errors
        if status["validation_errors"]:
            status["status"] = "warning"
            status["warnings"] = status["validation_errors"]
        
        return status
    
    def run_demo(self) -> None:
        """
        Run a demonstration of the system capabilities
        """
        print("\n🎭 YouTube Business System Demo")
        print("=" * 50)
        
        # Demo 1: Language Blending
        print("\n1️⃣ Language Blending Demo:")
        blends = self.language_blender.generate_content_batch(3, "music")
        for i, blend in enumerate(blends, 1):
            print(f"   {i}. {blend.blended_result} (Score: {blend.humor_score:.2f})")
        
        # Demo 2: Song Analysis
        print("\n2️⃣ Song Analysis Demo:")
        songs = self.song_analyzer.analyze_trending_songs(2)
        for song in songs:
            print(f"   🎵 {song.title} by {song.artist}")
            print(f"      Viral Terms: {', '.join(song.viral_terms[:3])}")
        
        # Demo 3: Script Generation
        print("\n3️⃣ Script Generation Demo:")
        script = self.script_generator.generate_script("Trending Music", "music", 8)
        print(f"   📝 Title: {script.title}")
        print(f"   ⏱️ Duration: {script.estimated_duration} minutes")
        print(f"   📚 Content Sections: {len(script.main_content)}")
        
        # Demo 4: System Status
        print("\n4️⃣ System Status:")
        status = self.get_system_status()
        print(f"   Status: {status['status']}")
        print(f"   Channel: {status['settings']['youtube']['channel_name']}")
        
        print("\n✅ Demo completed successfully!")
    
    def export_system_report(self, export_path: str = "reports") -> str:
        """
        Export a comprehensive system report
        
        Args:
            export_path: Directory to export the report
            
        Returns:
            Path to the exported report file
        """
        import json
        
        os.makedirs(export_path, exist_ok=True)
        
        # Gather all system information
        report = {
            "export_date": datetime.now().isoformat(),
            "system_status": self.get_system_status(),
            "capabilities": {
                "language_blending": "English-Yoruba fusion for viral content",
                "song_analysis": "Trending song analysis and viral term extraction",
                "script_generation": "Automated video script creation",
                "video_assembly": "Automated video assembly with effects",
                "monetization_ready": "Meets YouTube monetization requirements"
            },
            "sample_content": {
                "language_blends": [term.blended_result for term in 
                                  self.language_blender.generate_content_batch(5, "music")],
                "script_example": self.script_generator.generate_script("Sample Topic", "music", 8).__dict__
            }
        }
        
        # Export to JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"youtube_business_report_{timestamp}.json"
        filepath = os.path.join(export_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return filepath

def main():
    """Main entry point for the YouTube Business System"""
    print("🎥 YouTube Business Automation System")
    print("=" * 50)
    
    # Initialize the system
    system = YouTubeBusinessSystem()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "demo":
            system.run_demo()
        elif command == "status":
            status = system.get_system_status()
            print(json.dumps(status, indent=2))
        elif command == "create":
            if len(sys.argv) >= 3:
                topic = sys.argv[2]
                context = sys.argv[3] if len(sys.argv) > 3 else "music"
                result = system.create_complete_video(topic, context)
                print(f"Video creation result: {result}")
            else:
                print("Usage: python main.py create <topic> [context]")
        elif command == "batch":
            if len(sys.argv) >= 3:
                topics = sys.argv[2].split(",")
                context = sys.argv[3] if len(sys.argv) > 3 else "music"
                results = system.generate_content_batch(topics, context)
                print(f"Batch creation completed: {len(results)} videos")
            else:
                print("Usage: python main.py batch <topic1,topic2,topic3> [context]")
        elif command == "report":
            export_path = sys.argv[2] if len(sys.argv) > 2 else "reports"
            report_path = system.export_system_report(export_path)
            print(f"System report exported to: {report_path}")
        else:
            print("Unknown command. Available commands: demo, status, create, batch, report")
    else:
        # Interactive mode
        print("\nAvailable commands:")
        print("  demo    - Run system demonstration")
        print("  status  - Show system status")
        print("  create  - Create a single video")
        print("  batch   - Create multiple videos")
        print("  report  - Export system report")
        print("\nOr run with command: python main.py <command>")
        
        # Run demo by default
        print("\nRunning demo...")
        system.run_demo()

if __name__ == "__main__":
    main()
