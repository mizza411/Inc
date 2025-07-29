#!/usr/bin/env python3
"""
Nigerian Content Creation - Main Automation System
Orchestrates the complete content creation workflow
"""

import schedule
import time
import logging
import os
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict
import argparse

# Import our modules
from news_fetcher import NewsFetcher
from one_liner_generator import OneLinerGenerator
from visual_content_creator import VisualContentCreator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('content_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ContentAutomationSystem:
    def __init__(self, db_path: str = "content_creation.db"):
        """Initialize the complete automation system"""
        self.db_path = db_path
        
        # Initialize components
        self.news_fetcher = NewsFetcher(db_path)
        self.one_liner_generator = OneLinerGenerator(db_path)
        self.visual_creator = VisualContentCreator(db_path)
        
        logger.info("Content Automation System initialized successfully")
    
    def run_complete_workflow(self, platform: str = 'instagram', image_count: int = 10):
        """Run the complete content creation workflow"""
        logger.info("Starting complete content creation workflow")
        
        try:
            # Step 1: Fetch latest news and trends
            logger.info("Step 1: Fetching latest news and trends...")
            self.news_fetcher.run_daily_fetch()
            
            # Step 2: Generate one-liners from news
            logger.info("Step 2: Generating one-liners from news...")
            news_items = self.news_fetcher.get_unprocessed_news(20)
            if news_items:
                self.one_liner_generator.process_news_items(news_items)
                # Mark news as processed
                for item in news_items:
                    self.news_fetcher.mark_as_processed(item['id'])
            
            # Step 3: Generate one-liners from trends
            logger.info("Step 3: Generating one-liners from trends...")
            trends = self.news_fetcher.get_unprocessed_trends(10)
            if trends:
                self.one_liner_generator.process_trending_topics(trends)
                # Mark trends as processed
                for trend in trends:
                    self.news_fetcher.mark_as_processed(trend['id'], 'trending_topics')
            
            # Step 4: Create visual content
            logger.info("Step 4: Creating visual content...")
            generated_images = self.visual_creator.create_batch_images(platform, image_count)
            
            logger.info(f"Workflow completed successfully! Created {len(generated_images)} images")
            return generated_images
            
        except Exception as e:
            logger.error(f"Error in complete workflow: {str(e)}")
            return []
    
    def run_news_fetch_only(self):
        """Run only the news fetching process"""
        logger.info("Running news fetch only...")
        try:
            self.news_fetcher.run_daily_fetch()
            logger.info("News fetch completed successfully")
        except Exception as e:
            logger.error(f"Error in news fetch: {str(e)}")
    
    def run_content_generation_only(self):
        """Run only the content generation process"""
        logger.info("Running content generation only...")
        try:
            # Get unprocessed news and trends
            news_items = self.news_fetcher.get_unprocessed_news(30)
            trends = self.news_fetcher.get_unprocessed_trends(15)
            
            # Generate one-liners
            if news_items:
                self.one_liner_generator.process_news_items(news_items)
                for item in news_items:
                    self.news_fetcher.mark_as_processed(item['id'])
            
            if trends:
                self.one_liner_generator.process_trending_topics(trends)
                for trend in trends:
                    self.news_fetcher.mark_as_processed(trend['id'], 'trending_topics')
            
            logger.info("Content generation completed successfully")
            
        except Exception as e:
            logger.error(f"Error in content generation: {str(e)}")
    
    def run_image_creation_only(self, platform: str = 'instagram', count: int = 10):
        """Run only the image creation process"""
        logger.info(f"Running image creation only for {platform}...")
        try:
            images = self.visual_creator.create_batch_images(platform, count)
            logger.info(f"Image creation completed successfully! Created {len(images)} images")
            return images
        except Exception as e:
            logger.error(f"Error in image creation: {str(e)}")
            return []
    
    def get_status_report(self) -> Dict:
        """Get a status report of the system"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Get counts from each table
                news_count = conn.execute("SELECT COUNT(*) FROM news_items WHERE processed = FALSE").fetchone()[0]
                trends_count = conn.execute("SELECT COUNT(*) FROM trending_topics WHERE processed = FALSE").fetchone()[0]
                content_count = conn.execute("SELECT COUNT(*) FROM generated_content WHERE image_created = FALSE").fetchone()[0]
                image_count = conn.execute("SELECT COUNT(*) FROM generated_images WHERE posted = FALSE").fetchone()[0]
                
                return {
                    'unprocessed_news': news_count,
                    'unprocessed_trends': trends_count,
                    'unprocessed_content': content_count,
                    'ready_images': image_count,
                    'last_update': datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"Error getting status report: {str(e)}")
            return {}
    
    def schedule_daily_runs(self):
        """Schedule daily automated runs"""
        # Schedule news fetch at 6 AM daily
        schedule.every().day.at("06:00").do(self.run_news_fetch_only)
        
        # Schedule content generation at 8 AM daily
        schedule.every().day.at("08:00").do(self.run_content_generation_only)
        
        # Schedule image creation at 10 AM daily
        schedule.every().day.at("10:00").do(self.run_image_creation_only)
        
        # Schedule complete workflow at 2 PM daily
        schedule.every().day.at("14:00").do(self.run_complete_workflow)
        
        logger.info("Daily schedules set up successfully")
    
    def run_scheduler(self):
        """Run the scheduler loop"""
        logger.info("Starting scheduler...")
        self.schedule_daily_runs()
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def cleanup_old_data(self, days: int = 30):
        """Clean up old data from database"""
        logger.info(f"Cleaning up data older than {days} days...")
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Clean up old news items
                conn.execute("DELETE FROM news_items WHERE fetched_date < ?", (cutoff_date,))
                
                # Clean up old trends
                conn.execute("DELETE FROM trending_topics WHERE created_date < ?", (cutoff_date,))
                
                # Clean up old generated content
                conn.execute("DELETE FROM generated_content WHERE created_date < ?", (cutoff_date,))
                
                # Clean up old images (keep posted ones for a bit longer)
                image_cutoff = datetime.now() - timedelta(days=days * 2)
                conn.execute("DELETE FROM generated_images WHERE created_date < ? AND posted = TRUE", (image_cutoff,))
                
                conn.commit()
                
            logger.info("Cleanup completed successfully")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")

def main():
    """Main function to run the automation system"""
    parser = argparse.ArgumentParser(description='Nigerian Content Creation Automation System')
    parser.add_argument('--mode', choices=['complete', 'news', 'content', 'images', 'scheduler', 'status', 'cleanup'],
                       default='complete', help='Operation mode')
    parser.add_argument('--platform', choices=['instagram', 'twitter', 'facebook'],
                       default='instagram', help='Target platform for images')
    parser.add_argument('--count', type=int, default=10, help='Number of images to create')
    parser.add_argument('--days', type=int, default=30, help='Days for cleanup')
    
    args = parser.parse_args()
    
    # Initialize the system
    automation_system = ContentAutomationSystem()
    
    try:
        if args.mode == 'complete':
            logger.info("Running complete workflow...")
            automation_system.run_complete_workflow(args.platform, args.count)
            
        elif args.mode == 'news':
            logger.info("Running news fetch only...")
            automation_system.run_news_fetch_only()
            
        elif args.mode == 'content':
            logger.info("Running content generation only...")
            automation_system.run_content_generation_only()
            
        elif args.mode == 'images':
            logger.info("Running image creation only...")
            automation_system.run_image_creation_only(args.platform, args.count)
            
        elif args.mode == 'scheduler':
            logger.info("Starting scheduler...")
            automation_system.run_scheduler()
            
        elif args.mode == 'status':
            logger.info("Getting status report...")
            status = automation_system.get_status_report()
            print("\n=== Content Automation System Status ===")
            for key, value in status.items():
                print(f"{key.replace('_', ' ').title()}: {value}")
            print()
            
        elif args.mode == 'cleanup':
            logger.info("Running cleanup...")
            automation_system.cleanup_old_data(args.days)
            
    except KeyboardInterrupt:
        logger.info("Operation interrupted by user")
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")

if __name__ == "__main__":
    main() 