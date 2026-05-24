"""
🎥 YouTube Business Automation - Main Integration System
Main entry point that integrates all components for automated video creation
"""

import json
import re
import sys
import os
from datetime import datetime
from typing import Dict, List, Optional

# Add the parent directory to the path to import from Content-Automation
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our YouTube business modules
from core.language_blender import EnhancedLanguageBlender as LanguageBlender
from core.song_analyzer import SongAnalyzer
from core.topic_analyzer import TrendingTopicAnalyzer
from core.script_generator import ScriptGenerator
from core.video_assembler import VideoAssembler
from core.performance_tracker import ContentPerformanceTracker
from core.content_scheduler import ContentScheduler
from core.analytics_dashboard import AnalyticsDashboard
from core.research_engine import ResearchEngine
from config.settings import Settings


def _parse_uploads_per_week(freq: str) -> int:
    match = re.search(r"(\d+)", freq or "")
    return int(match.group(1)) if match else 3

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
        self.topic_analyzer = TrendingTopicAnalyzer()
        self.script_generator = ScriptGenerator()
        self.video_assembler = VideoAssembler()
        self.performance_tracker = ContentPerformanceTracker()
        self.content_scheduler = ContentScheduler(
            topic_analyzer=self.topic_analyzer,
            uploads_per_week=_parse_uploads_per_week(self.settings.youtube.upload_frequency),
            target_duration_minutes=self.settings.youtube.video_length_target,
        )
        self.analytics_dashboard = AnalyticsDashboard()
        self.research_engine = ResearchEngine()
        
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

            topic_terms: List[str] = []
            topic_report = None
            if self.settings.content_generation.trending_topic_integration:
                print("2b️⃣ Analyzing trending topics (search & culture)...")
                topic_report = self.topic_analyzer.analyze()
                topic_terms = self.topic_analyzer.topic_terms(topic_report)
                export_path = self.topic_analyzer.export_report(topic_report)
                print(f"   📁 Topic report: {export_path}")
                if topic_report.top_picks:
                    print(f"   🔥 Top topic: {topic_report.top_picks[0].query}")

            # Step 3: Generate video script
            print("3️⃣ Generating video script...")
            script = self.script_generator.generate_script(
                topic, context, target_minutes, extra_trending_terms=topic_terms or None
            )

            script_data = {
                "title": script.title,
                "hook": script.hook,
                "introduction": script.introduction,
                "main_content": script.main_content,
                "conclusion": script.conclusion,
                "call_to_action": script.call_to_action,
                "description": f"Automated video about {topic} with English-Yoruba language blending",
                "tags": ["nigerian", "yoruba", "culture", "humor", "trending"],
                "category": "Entertainment",
            }

            print("3b️⃣ Running research and fact-check...")
            extra_sources = []
            if topic_report:
                for pick in topic_report.top_picks[:5]:
                    extra_sources.append(
                        {
                            "title": pick.query,
                            "url": "",
                            "snippet": f"Trending topic in {pick.region} via {pick.source}",
                            "source_type": "trend",
                            "credibility_score": 0.65,
                        }
                    )
            research_report = self.research_engine.analyze_topic(
                topic, script_data, extra_sources=extra_sources or None
            )
            research_path = self.research_engine.export_report(research_report)
            print(
                f"   Research quality={research_report.research_quality_score:.2f} "
                f"status={research_report.fact_checking_status}"
            )
            print(f"   Exported: {research_path}")

            # Step 4: Assemble video
            print("4️⃣ Assembling video...")
            assembled_video = self.video_assembler.assemble_video(script_data)
            
            # Step 5: Prepare results
            results = {
                "success": True,
                "video_title": script.title,
                "script": script,
                "assembled_video": assembled_video,
                "language_blends": [term.blended_result for term in language_blends],
                "trending_songs": [song.title for song in trending_songs],
                "trending_topics": topic_terms,
                "topic_analysis": topic_report.to_dict() if topic_report else None,
                "research": research_report.to_dict(),
                "creation_date": datetime.now().isoformat(),
                "estimated_duration": script.estimated_duration,
                "target_length": script.target_length
            }
            
            print(f"\n✅ Video creation completed successfully!")
            print(f"Title: {script.title}")
            print(f"Duration: {script.estimated_duration} minutes")
            print(f"Language Blends: {len(results['language_blends'])}")

            if self.settings.content_generation.quality_validation_enabled:
                print("5️⃣ Recording content performance metrics...")
                tracking = self.performance_tracker.track_created_video(
                    topic,
                    context,
                    script,
                    extra_metadata={
                        "trending_topics": topic_terms,
                        "trending_songs": results["trending_songs"],
                    },
                )
                results["performance_tracking"] = tracking
                print(
                    f"   Tracked video_id={tracking['video_id']} "
                    f"quality_score={tracking['validation_score']:.2f}"
                )

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
                "topic_analyzer": "ready",
                "script_generator": "ready",
                "video_assembler": "ready",
                "performance_tracker": "ready",
                "content_scheduler": "ready",
                "analytics_dashboard": "ready",
                "research_engine": "ready",
            },
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
        
        # Demo 3: Trending topic analysis
        print("\n3️⃣ Trending Topic Analysis Demo:")
        topic_report = self.topic_analyzer.analyze()
        for i, pick in enumerate(topic_report.top_picks[:3], 1):
            print(f"   {i}. {pick.query} ({pick.category}, {pick.source})")
        print(f"   Live data: {topic_report.used_live_data}")

        # Demo 4: Script Generation
        print("\n4️⃣ Script Generation Demo:")
        extra = self.topic_analyzer.topic_terms(topic_report)
        script = self.script_generator.generate_script(
            "Trending Music", "music", 8, extra_trending_terms=extra
        )
        print(f"   📝 Title: {script.title}")
        print(f"   ⏱️ Duration: {script.estimated_duration} minutes")
        print(f"   📚 Content Sections: {len(script.main_content)}")
        
        # Demo 5: System Status
        print("\n5️⃣ System Status:")
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
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    print("YouTube Business Automation System")
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
        elif command == "trends":
            report = system.topic_analyzer.analyze()
            path = system.topic_analyzer.export_report(report)
            print(f"Trending topic analysis (live={report.used_live_data})")
            print(f"Exported: {path}")
            for i, t in enumerate(report.top_picks[:10], 1):
                print(f"  {i}. {t.query} [{t.category}] ({t.region})")
            if report.video_ideas:
                print("\nSuggested video ideas:")
                for idea in report.video_ideas[:5]:
                    print(f"  - {idea['title']}")
        elif command == "performance":
            sub = sys.argv[2].lower() if len(sys.argv) > 2 else "summary"
            if sub == "import" and len(sys.argv) >= 4:
                count = system.performance_tracker.import_metrics_file(sys.argv[3])
                print(f"Imported performance metrics for {count} video(s)")
            else:
                summary = system.performance_tracker.get_summary()
                export_path = system.performance_tracker.export_summary()
                print("Content performance summary")
                print(f"  Database: {summary['database']}")
                cq = summary.get("content_quality") or {}
                print(f"  Videos tracked: {cq.get('video_count', 0)}")
                print(f"  Avg quality score: {cq.get('avg_quality')}")
                print(f"  Exported: {export_path}")
                for row in summary.get("recent_videos", [])[:5]:
                    print(
                        f"  - [{row.get('id')}] {row.get('title')} "
                        f"({row.get('status')}, score={row.get('high_effort_score')})"
                    )
        elif command == "schedule":
            sub = sys.argv[2].lower() if len(sys.argv) > 2 else "list"
            if sub == "plan":
                days = int(sys.argv[3]) if len(sys.argv) > 3 else 14
                created = system.content_scheduler.generate_plan(days_ahead=days)
                export_path = system.content_scheduler.export_plan()
                print(f"Scheduled {len(created)} slots over {days} days")
                print(f"Exported: {export_path}")
                for row in created[:8]:
                    print(
                        f"  - {row['scheduled_date']}: {row['topic_title']} "
                        f"[{row['content_niche']}]"
                    )
            elif sub == "list":
                rows = system.content_scheduler.list_upcoming(limit=20)
                print(f"Upcoming planned slots: {len(rows)}")
                for row in rows:
                    print(
                        f"  - [{row['id']}] {row['scheduled_date']}: "
                        f"{row['topic_title']} ({row['status']})"
                    )
            elif sub == "run-due":
                dry_run = "--dry-run" in sys.argv
                results = system.content_scheduler.run_due(
                    lambda topic, ctx, mins: system.create_complete_video(
                        topic, ctx, target_minutes=mins
                    ),
                    dry_run=dry_run,
                )
                mode = "dry-run" if dry_run else "live"
                print(f"Processed {len(results)} due slot(s) ({mode})")
                for row in results:
                    if dry_run:
                        print(
                            f"  - [{row['schedule_id']}] would create: "
                            f"{row['topic']} ({row['context']})"
                        )
                    else:
                        print(
                            f"  - [{row['schedule_id']}] {row['topic']} -> "
                            f"{row['status']}"
                        )
            else:
                print("Usage: schedule plan [days] | schedule list | schedule run-due [--dry-run]")
        elif command == "dashboard":
            path = system.analytics_dashboard.generate_html()
            print("Analytics dashboard generated")
            print(f"  Open: {path}")
            print("  Tip: python -m http.server 8000 from youtube/ then visit web/analytics_dashboard.html")
        elif command == "research":
            if len(sys.argv) >= 3:
                topic = " ".join(sys.argv[2:])
                script = system.script_generator.generate_script(topic, "culture", 8)
                script_data = {
                    "title": script.title,
                    "hook": script.hook,
                    "introduction": script.introduction,
                    "main_content": script.main_content,
                    "conclusion": script.conclusion,
                    "call_to_action": script.call_to_action,
                }
                report = system.research_engine.analyze_topic(topic, script_data)
                path = system.research_engine.export_report(report)
                print(f"Research report for: {topic}")
                print(f"  Quality score: {report.research_quality_score:.2f}")
                print(f"  Fact-check status: {report.fact_checking_status}")
                print(f"  Sources gathered: {len(report.sources)}")
                print(f"  Claims checked: {len(report.fact_checks)}")
                print(f"  Exported: {path}")
                for item in report.fact_checks[:5]:
                    print(f"  - [{item.status}] {item.claim[:90]}...")
            else:
                print("Usage: python main.py research <topic>")
        else:
            print(
                "Unknown command. Available: demo, status, create, batch, report, "
                "trends, performance, schedule, dashboard, research"
            )
    else:
        # Interactive mode
        print("\nAvailable commands:")
        print("  demo    - Run system demonstration")
        print("  status  - Show system status")
        print("  create  - Create a single video")
        print("  batch   - Create multiple videos")
        print("  report  - Export system report")
        print("  trends  - Run trending topic analysis (Phase 3.1)")
        print("  performance - Show/export performance summary (Phase 3.2)")
        print("  performance import <file.json> - Import YouTube metrics")
        print("  schedule plan [days] - Generate content calendar from trends")
        print("  schedule list - Show upcoming planned slots")
        print("  schedule run-due [--dry-run] - Run due scheduled creations")
        print("  dashboard - Generate analytics HTML dashboard (Phase 3.4)")
        print("  research <topic> - Run research and fact-check (Phase 3.5)")
        print("\nOr run with command: python main.py <command>")
        
        # Run demo by default
        print("\nRunning demo...")
        system.run_demo()

if __name__ == "__main__":
    main()
