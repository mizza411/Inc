"""
🗄️ YouTube Database Schema - Content Tracking System
Implements the comprehensive database schema for YouTube business automation
Manages content lifecycle, performance tracking, and business intelligence
"""

import sqlite3
import json
import os
from datetime import datetime, date
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YouTubeDatabase:
    """
    YouTube business database management system
    Handles all database operations for content tracking and analytics
    """
    
    def __init__(self, db_path: str = "youtube_business.db"):
        """Initialize the YouTube database system"""
        self.db_path = db_path
        self.connection = None
        self.initialize_database()
    
    def initialize_database(self):
        """Initialize database connection and create tables if they don't exist"""
        try:
            db_dir = os.path.dirname(os.path.abspath(self.db_path))
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)
            
            # Connect to database
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Enable row access by name
            
            # Create tables
            self.create_tables()
            
            # Create indexes
            self.create_indexes()
            
            logger.info(f"✅ Database initialized successfully: {self.db_path}")
            
        except Exception as e:
            logger.error(f"❌ Error initializing database: {str(e)}")
            raise
    
    def create_tables(self):
        """Create all database tables"""
        try:
            cursor = self.connection.cursor()
            
            # 1. CONTENT MANAGEMENT TABLES
            
            # Videos table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS videos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    youtube_id VARCHAR(20) UNIQUE,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    channel_id VARCHAR(50),
                    content_niche VARCHAR(100),
                    language_blending_score DECIMAL(3,2),
                    high_effort_score DECIMAL(3,2),
                    target_duration_minutes INTEGER,
                    actual_duration_minutes INTEGER,
                    status VARCHAR(50) DEFAULT 'draft',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    published_at TIMESTAMP,
                    thumbnail_path VARCHAR(500),
                    video_file_path VARCHAR(500),
                    script_file_path VARCHAR(500),
                    metadata_json TEXT
                )
            """)
            
            # Content scripts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS content_scripts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id INTEGER NOT NULL,
                    script_type VARCHAR(50),
                    content_text TEXT NOT NULL,
                    language_blending_terms TEXT,
                    word_count INTEGER,
                    estimated_duration_minutes DECIMAL(4,2),
                    research_sources TEXT,
                    fact_checking_status VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (video_id) REFERENCES videos(id)
                )
            """)
            
            # Trending topics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trending_topics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic_title VARCHAR(255) NOT NULL,
                    topic_type VARCHAR(50),
                    source_platform VARCHAR(50),
                    viral_score DECIMAL(3,2),
                    cultural_relevance_score DECIMAL(3,2),
                    trending_start_date TIMESTAMP,
                    trending_end_date TIMESTAMP,
                    peak_popularity_score DECIMAL(3,2),
                    metadata_json TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Language blending terms table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS language_blending_terms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    english_term VARCHAR(100) NOT NULL,
                    yoruba_term VARCHAR(100) NOT NULL,
                    blended_result VARCHAR(150) NOT NULL,
                    meaning TEXT,
                    humor_score DECIMAL(3,2),
                    viral_potential DECIMAL(3,2),
                    cultural_relevance DECIMAL(3,2),
                    usage_context TEXT,
                    pronunciation_guide TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    usage_count INTEGER DEFAULT 0,
                    last_used_at TIMESTAMP
                )
            """)
            
            # 2. PERFORMANCE TRACKING TABLES
            
            # Video performance table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS video_performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id INTEGER NOT NULL,
                    youtube_id VARCHAR(20) NOT NULL,
                    date_recorded DATE NOT NULL,
                    views INTEGER DEFAULT 0,
                    likes INTEGER DEFAULT 0,
                    dislikes INTEGER DEFAULT 0,
                    comments INTEGER DEFAULT 0,
                    shares INTEGER DEFAULT 0,
                    watch_time_minutes INTEGER DEFAULT 0,
                    average_view_duration_minutes DECIMAL(4,2),
                    audience_retention_rate DECIMAL(5,2),
                    click_through_rate DECIMAL(5,2),
                    impressions INTEGER DEFAULT 0,
                    revenue_usd DECIMAL(10,2) DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (video_id) REFERENCES videos(id)
                )
            """)
            
            # Content analytics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS content_analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id INTEGER NOT NULL,
                    content_quality_score DECIMAL(3,2),
                    engagement_score DECIMAL(3,2),
                    viral_potential_score DECIMAL(3,2),
                    monetization_readiness_score DECIMAL(3,2),
                    high_effort_compliance TEXT,
                    audience_feedback TEXT,
                    improvement_suggestions TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (video_id) REFERENCES videos(id)
                )
            """)
            
            # Audience insights table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audience_insights (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id INTEGER NOT NULL,
                    audience_demographics TEXT,
                    peak_watching_times TEXT,
                    drop_off_points TEXT,
                    rewatch_behavior TEXT,
                    social_sharing_patterns TEXT,
                    comment_sentiment TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (video_id) REFERENCES videos(id)
                )
            """)
            
            # 3. BUSINESS INTELLIGENCE TABLES
            
            # Monetization tracking table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS monetization_tracking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id INTEGER NOT NULL,
                    monetization_status VARCHAR(50),
                    ad_revenue_usd DECIMAL(10,2) DEFAULT 0,
                    sponsor_revenue_usd DECIMAL(10,2) DEFAULT 0,
                    merchandise_revenue_usd DECIMAL(10,2) DEFAULT 0,
                    total_revenue_usd DECIMAL(10,2) DEFAULT 0,
                    cpm_rate DECIMAL(8,2),
                    monetization_date DATE,
                    requirements_met TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (video_id) REFERENCES videos(id)
                )
            """)
            
            # Content schedule table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS content_schedule (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scheduled_date DATE NOT NULL,
                    content_niche VARCHAR(100),
                    topic_title VARCHAR(255),
                    trending_topic_id INTEGER,
                    target_duration_minutes INTEGER,
                    priority_level VARCHAR(20),
                    status VARCHAR(50) DEFAULT 'planned',
                    assigned_automation_workflow VARCHAR(100),
                    estimated_completion_time TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (trending_topic_id) REFERENCES trending_topics(id)
                )
            """)
            
            # Business metrics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS business_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date_recorded DATE NOT NULL,
                    total_subscribers INTEGER DEFAULT 0,
                    total_views INTEGER DEFAULT 0,
                    total_watch_time_hours DECIMAL(8,2) DEFAULT 0,
                    total_revenue_usd DECIMAL(10,2) DEFAULT 0,
                    videos_published INTEGER DEFAULT 0,
                    average_video_performance DECIMAL(3,2),
                    channel_health_score DECIMAL(3,2),
                    monetization_eligibility_status VARCHAR(50),
                    growth_rate_percentage DECIMAL(5,2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 4. AUTOMATION & WORKFLOW TABLES
            
            # Automation workflows table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS automation_workflows (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    workflow_name VARCHAR(100) NOT NULL,
                    workflow_type VARCHAR(50),
                    status VARCHAR(50) DEFAULT 'active',
                    current_step VARCHAR(100),
                    total_steps INTEGER,
                    progress_percentage DECIMAL(5,2),
                    start_time TIMESTAMP,
                    estimated_completion_time TIMESTAMP,
                    actual_completion_time TIMESTAMP,
                    error_log TEXT,
                    performance_metrics TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Content pipeline table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS content_pipeline (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id INTEGER NOT NULL,
                    pipeline_stage VARCHAR(100),
                    status VARCHAR(50),
                    assigned_workflow_id INTEGER,
                    start_time TIMESTAMP,
                    completion_time TIMESTAMP,
                    duration_minutes INTEGER,
                    quality_score DECIMAL(3,2),
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (video_id) REFERENCES videos(id),
                    FOREIGN KEY (assigned_workflow_id) REFERENCES automation_workflows(id)
                )
            """)
            
            # Commit changes
            self.connection.commit()
            logger.info("✅ All database tables created successfully")
            
        except Exception as e:
            logger.error(f"❌ Error creating tables: {str(e)}")
            raise
    
    def create_indexes(self):
        """Create performance indexes for common queries"""
        try:
            cursor = self.connection.cursor()
            
            # Video performance indexes
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_video_performance_date 
                ON video_performance(date_recorded)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_video_performance_youtube_id 
                ON video_performance(youtube_id)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_video_performance_views 
                ON video_performance(views)
            """)
            
            # Content analytics indexes
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_content_analytics_quality 
                ON content_analytics(content_quality_score)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_content_analytics_engagement 
                ON content_analytics(engagement_score)
            """)
            
            # Trending topics indexes
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_trending_topics_viral 
                ON trending_topics(viral_score)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_trending_topics_cultural 
                ON trending_topics(cultural_relevance_score)
            """)
            
            # Language blending indexes
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_language_blending_viral 
                ON language_blending_terms(viral_potential)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_language_blending_usage 
                ON language_blending_terms(usage_count)
            """)
            
            # Business metrics indexes
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_business_metrics_date 
                ON business_metrics(date_recorded)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_business_metrics_revenue 
                ON business_metrics(total_revenue_usd)
            """)
            
            # Commit changes
            self.connection.commit()
            logger.info("✅ All database indexes created successfully")
            
        except Exception as e:
            logger.error(f"❌ Error creating indexes: {str(e)}")
            raise
    
    def insert_video(self, video_data: Dict[str, Any]) -> int:
        """Insert a new video record"""
        try:
            cursor = self.connection.cursor()
            
            # Prepare data for insertion
            columns = [
                'youtube_id', 'title', 'description', 'channel_id', 'content_niche',
                'language_blending_score', 'high_effort_score', 'target_duration_minutes',
                'actual_duration_minutes', 'status', 'thumbnail_path', 'video_file_path',
                'script_file_path', 'metadata_json'
            ]
            
            values = [video_data.get(col) for col in columns]
            placeholders = ', '.join(['?' for _ in columns])
            column_names = ', '.join(columns)
            
            query = f"INSERT INTO videos ({column_names}) VALUES ({placeholders})"
            cursor.execute(query, values)
            
            video_id = cursor.lastrowid
            self.connection.commit()
            
            logger.info(f"✅ Video inserted successfully with ID: {video_id}")
            return video_id
            
        except Exception as e:
            logger.error(f"❌ Error inserting video: {str(e)}")
            raise
    
    def insert_trending_topic(self, topic_data: Dict[str, Any]) -> int:
        """Insert a new trending topic"""
        try:
            cursor = self.connection.cursor()
            
            columns = [
                'topic_title', 'topic_type', 'source_platform', 'viral_score',
                'cultural_relevance_score', 'trending_start_date', 'trending_end_date',
                'peak_popularity_score', 'metadata_json'
            ]
            
            values = [topic_data.get(col) for col in columns]
            placeholders = ', '.join(['?' for _ in columns])
            column_names = ', '.join(columns)
            
            query = f"INSERT INTO trending_topics ({column_names}) VALUES ({placeholders})"
            cursor.execute(query, values)
            
            topic_id = cursor.lastrowid
            self.connection.commit()
            
            logger.info(f"✅ Trending topic inserted successfully with ID: {topic_id}")
            return topic_id
            
        except Exception as e:
            logger.error(f"❌ Error inserting trending topic: {str(e)}")
            raise
    
    def insert_language_blending_term(self, term_data: Dict[str, Any]) -> int:
        """Insert a new language blending term"""
        try:
            cursor = self.connection.cursor()
            
            columns = [
                'english_term', 'yoruba_term', 'blended_result', 'meaning',
                'humor_score', 'viral_potential', 'cultural_relevance',
                'usage_context', 'pronunciation_guide'
            ]
            
            values = [term_data.get(col) for col in columns]
            placeholders = ', '.join(['?' for _ in columns])
            column_names = ', '.join(columns)
            
            query = f"INSERT INTO language_blending_terms ({column_names}) VALUES ({placeholders})"
            cursor.execute(query, values)
            
            term_id = cursor.lastrowid
            self.connection.commit()
            
            logger.info(f"✅ Language blending term inserted successfully with ID: {term_id}")
            return term_id
            
        except Exception as e:
            logger.error(f"❌ Error inserting language blending term: {str(e)}")
            raise
    
    def update_video_performance(self, video_id: int, performance_data: Dict[str, Any]):
        """Update video performance metrics"""
        try:
            cursor = self.connection.cursor()
            
            # Check if performance record exists for today
            today = date.today()
            cursor.execute("""
                SELECT id FROM video_performance 
                WHERE video_id = ? AND date_recorded = ?
            """, (video_id, today))
            
            existing_record = cursor.fetchone()
            
            if existing_record:
                # Update existing record
                update_query = """
                    UPDATE video_performance SET
                        views = ?, likes = ?, dislikes = ?, comments = ?,
                        shares = ?, watch_time_minutes = ?, average_view_duration_minutes = ?,
                        audience_retention_rate = ?, click_through_rate = ?,
                        impressions = ?, revenue_usd = ?
                    WHERE id = ?
                """
                
                values = [
                    performance_data.get('views', 0),
                    performance_data.get('likes', 0),
                    performance_data.get('dislikes', 0),
                    performance_data.get('comments', 0),
                    performance_data.get('shares', 0),
                    performance_data.get('watch_time_minutes', 0),
                    performance_data.get('average_view_duration_minutes', 0),
                    performance_data.get('audience_retention_rate', 0),
                    performance_data.get('click_through_rate', 0),
                    performance_data.get('impressions', 0),
                    performance_data.get('revenue_usd', 0),
                    existing_record['id']
                ]
                
                cursor.execute(update_query, values)
                
            else:
                # Insert new record
                insert_query = """
                    INSERT INTO video_performance (
                        video_id, youtube_id, date_recorded, views, likes, dislikes,
                        comments, shares, watch_time_minutes, average_view_duration_minutes,
                        audience_retention_rate, click_through_rate, impressions, revenue_usd
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                
                values = [
                    video_id,
                    performance_data.get('youtube_id', ''),
                    today,
                    performance_data.get('views', 0),
                    performance_data.get('likes', 0),
                    performance_data.get('dislikes', 0),
                    performance_data.get('comments', 0),
                    performance_data.get('shares', 0),
                    performance_data.get('watch_time_minutes', 0),
                    performance_data.get('average_view_duration_minutes', 0),
                    performance_data.get('audience_retention_rate', 0),
                    performance_data.get('click_through_rate', 0),
                    performance_data.get('impressions', 0),
                    performance_data.get('revenue_usd', 0)
                ]
                
                cursor.execute(insert_query, values)
            
            self.connection.commit()
            logger.info(f"✅ Video performance updated successfully for video ID: {video_id}")
            
        except Exception as e:
            logger.error(f"❌ Error updating video performance: {str(e)}")
            raise

    def insert_content_analytics(self, video_id: int, analytics_data: Dict[str, Any]) -> int:
        """Insert content quality analytics for a video."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                INSERT INTO content_analytics (
                    video_id, content_quality_score, engagement_score,
                    viral_potential_score, monetization_readiness_score,
                    high_effort_compliance, audience_feedback, improvement_suggestions
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    video_id,
                    analytics_data.get("content_quality_score", 0),
                    analytics_data.get("engagement_score", 0),
                    analytics_data.get("viral_potential_score", 0),
                    analytics_data.get("monetization_readiness_score", 0),
                    json.dumps(analytics_data.get("high_effort_compliance", {})),
                    analytics_data.get("audience_feedback", ""),
                    json.dumps(analytics_data.get("improvement_suggestions", [])),
                ),
            )
            row_id = cursor.lastrowid
            self.connection.commit()
            logger.info("Content analytics inserted for video ID: %s", video_id)
            return row_id
        except Exception as e:
            logger.error("Error inserting content analytics: %s", e)
            raise

    def list_videos(self, limit: int = 50) -> List[Dict]:
        """List recent videos with basic metadata."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                SELECT id, youtube_id, title, content_niche, status,
                       high_effort_score, actual_duration_minutes, created_at
                FROM videos
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (limit,),
            )
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error("Error listing videos: %s", e)
            raise

    def get_content_quality_summary(self) -> Dict[str, Any]:
        """Aggregate pre-publish quality metrics across tracked content."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """
                SELECT
                    COUNT(DISTINCT v.id) AS video_count,
                    AVG(ca.content_quality_score) AS avg_quality,
                    AVG(ca.engagement_score) AS avg_engagement,
                    AVG(ca.monetization_readiness_score) AS avg_monetization_readiness
                FROM videos v
                LEFT JOIN content_analytics ca ON v.id = ca.video_id
                """
            )
            row = cursor.fetchone()
            return dict(row) if row else {}
        except Exception as e:
            logger.error("Error getting content quality summary: %s", e)
            raise
    
    def get_top_performing_videos(self, limit: int = 10) -> List[Dict]:
        """Get top performing videos based on views"""
        try:
            cursor = self.connection.cursor()
            
            query = """
                SELECT 
                    v.title,
                    v.content_niche,
                    vp.views,
                    vp.likes,
                    vp.watch_time_minutes,
                    vp.date_recorded
                FROM videos v
                JOIN video_performance vp ON v.id = vp.video_id
                WHERE vp.date_recorded = (
                    SELECT MAX(date_recorded) FROM video_performance
                )
                ORDER BY vp.views DESC
                LIMIT ?
            """
            
            cursor.execute(query, (limit,))
            results = cursor.fetchall()
            
            # Convert to list of dictionaries
            videos = []
            for row in results:
                videos.append(dict(row))
            
            logger.info(f"✅ Retrieved {len(videos)} top performing videos")
            return videos
            
        except Exception as e:
            logger.error(f"❌ Error retrieving top performing videos: {str(e)}")
            raise
    
    def get_trending_content_opportunities(self, min_score: float = 0.7) -> List[Dict]:
        """Get trending topics suitable for content creation"""
        try:
            cursor = self.connection.cursor()
            
            query = """
                SELECT 
                    topic_title,
                    topic_type,
                    viral_score,
                    cultural_relevance_score,
                    (viral_score + cultural_relevance_score) / 2 as combined_score
                FROM trending_topics
                WHERE trending_start_date >= DATE('now', '-7 days')
                AND (viral_score + cultural_relevance_score) / 2 >= ?
                ORDER BY combined_score DESC
            """
            
            cursor.execute(query, (min_score,))
            results = cursor.fetchall()
            
            # Convert to list of dictionaries
            opportunities = []
            for row in results:
                opportunities.append(dict(row))
            
            logger.info(f"✅ Retrieved {len(opportunities)} trending content opportunities")
            return opportunities
            
        except Exception as e:
            logger.error(f"❌ Error retrieving trending opportunities: {str(e)}")
            raise
    
    def get_monetization_ready_videos(self, min_score: float = 0.8) -> List[Dict]:
        """Get videos ready for monetization"""
        try:
            cursor = self.connection.cursor()
            
            query = """
                SELECT 
                    v.title,
                    v.high_effort_score,
                    v.actual_duration_minutes,
                    v.content_niche
                FROM videos v
                WHERE v.high_effort_score >= ?
                AND v.actual_duration_minutes >= 8
                AND v.status = 'published'
                ORDER BY v.high_effort_score DESC
            """
            
            cursor.execute(query, (min_score,))
            results = cursor.fetchall()
            
            # Convert to list of dictionaries
            videos = []
            for row in results:
                videos.append(dict(row))
            
            logger.info(f"✅ Retrieved {len(videos)} monetization-ready videos")
            return videos
            
        except Exception as e:
            logger.error(f"❌ Error retrieving monetization-ready videos: {str(e)}")
            raise
    
    def get_business_metrics_summary(self) -> Dict:
        """Get overall business performance summary"""
        try:
            cursor = self.connection.cursor()
            
            # Get latest metrics
            query = """
                SELECT 
                    total_subscribers,
                    total_views,
                    total_revenue_usd,
                    videos_published,
                    channel_health_score,
                    monetization_eligibility_status
                FROM business_metrics
                WHERE date_recorded = (
                    SELECT MAX(date_recorded) FROM business_metrics
                )
            """
            
            cursor.execute(query)
            result = cursor.fetchone()
            
            if result:
                summary = dict(result)
                logger.info("✅ Retrieved business metrics summary")
                return summary
            else:
                logger.warning("⚠️ No business metrics found")
                return {}
                
        except Exception as e:
            logger.error(f"❌ Error retrieving business metrics: {str(e)}")
            raise
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("✅ Database connection closed")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


# Example usage and testing
if __name__ == "__main__":
    # Create database instance
    db = YouTubeDatabase()
    
    try:
        # Test inserting a sample video
        sample_video = {
            'youtube_id': 'test123',
            'title': 'Test Video - Language Blending Demo',
            'description': 'A test video for our YouTube business system',
            'content_niche': 'Cultural Commentary',
            'language_blending_score': 0.85,
            'high_effort_score': 0.90,
            'target_duration_minutes': 10,
            'actual_duration_minutes': 10,
            'status': 'published'
        }
        
        video_id = db.insert_video(sample_video)
        print(f"✅ Sample video inserted with ID: {video_id}")
        
        # Test inserting a trending topic
        sample_topic = {
            'topic_title': 'Test Trending Topic',
            'topic_type': 'song',
            'source_platform': 'spotify',
            'viral_score': 0.8,
            'cultural_relevance_score': 0.7
        }
        
        topic_id = db.insert_trending_topic(sample_topic)
        print(f"✅ Sample trending topic inserted with ID: {topic_id}")
        
        # Test retrieving top performing videos
        top_videos = db.get_top_performing_videos(5)
        print(f"✅ Retrieved {len(top_videos)} top performing videos")
        
        # Test retrieving trending opportunities
        opportunities = db.get_trending_content_opportunities(0.6)
        print(f"✅ Retrieved {len(opportunities)} trending opportunities")
        
        print("🎉 Database schema test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
    
    finally:
        db.close()
