#!/usr/bin/env python3
"""
Test script for Nigerian Content Creation Automation System
Verifies all components work correctly
"""

import os
import sys
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    """Test if all required modules can be imported"""
    logger.info("Testing module imports...")
    
    try:
        from news_fetcher import NewsFetcher
        logger.info("✓ NewsFetcher imported successfully")
    except ImportError as e:
        logger.error(f"✗ Failed to import NewsFetcher: {e}")
        return False
    
    try:
        from one_liner_generator import OneLinerGenerator
        logger.info("✓ OneLinerGenerator imported successfully")
    except ImportError as e:
        logger.error(f"✗ Failed to import OneLinerGenerator: {e}")
        return False
    
    try:
        from visual_content_creator import VisualContentCreator
        logger.info("✓ VisualContentCreator imported successfully")
    except ImportError as e:
        logger.error(f"✗ Failed to import VisualContentCreator: {e}")
        return False
    
    try:
        from content_automation_main import ContentAutomationSystem
        logger.info("✓ ContentAutomationSystem imported successfully")
    except ImportError as e:
        logger.error(f"✗ Failed to import ContentAutomationSystem: {e}")
        return False
    
    return True

def test_news_fetcher():
    """Test news fetcher functionality"""
    logger.info("Testing news fetcher...")
    
    try:
        from news_fetcher import NewsFetcher
        fetcher = NewsFetcher("test_content_creation.db")
        
        # Test database setup
        logger.info("✓ Database setup successful")
        
        # Test trending topics (mock data)
        trends = fetcher.fetch_social_media_trends()
        logger.info(f"✓ Generated {len(trends)} mock trends")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ News fetcher test failed: {e}")
        return False

def test_one_liner_generator():
    """Test one-liner generator functionality"""
    logger.info("Testing one-liner generator...")
    
    try:
        from one_liner_generator import OneLinerGenerator
        generator = OneLinerGenerator("test_content_creation.db")
        
        # Test with sample content
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
        
        one_liners = generator.process_news_items(test_news)
        logger.info(f"✓ Generated {len(one_liners)} one-liners")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ One-liner generator test failed: {e}")
        return False

def test_visual_creator():
    """Test visual content creator functionality"""
    logger.info("Testing visual content creator...")
    
    try:
        from visual_content_creator import VisualContentCreator
        creator = VisualContentCreator("test_content_creation.db", "test_generated_images")
        
        # Test with sample content
        test_content = [
            {
                'id': 1,
                'one_liner': 'Only in Nigeria: naira devaluation but we still dey manage 😂',
                'humor_type': 'naija_humor'
            },
            {
                'id': 2,
                'one_liner': 'Tech people when AI takes over: *nervous laughter* 😅',
                'humor_type': 'tech_humor'
            }
        ]
        
        images = creator.create_visual_content(test_content, 'instagram', 'square')
        logger.info(f"✓ Created {len(images)} test images")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Visual creator test failed: {e}")
        return False

def test_main_system():
    """Test main automation system"""
    logger.info("Testing main automation system...")
    
    try:
        from content_automation_main import ContentAutomationSystem
        system = ContentAutomationSystem("test_content_creation.db")
        
        # Test status report
        status = system.get_status_report()
        logger.info("✓ Status report generated successfully")
        logger.info(f"  Status: {status}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Main system test failed: {e}")
        return False

def cleanup_test_files():
    """Clean up test files"""
    logger.info("Cleaning up test files...")
    
    test_files = [
        "test_content_creation.db",
        "test_generated_images"
    ]
    
    for file_path in test_files:
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                logger.info(f"✓ Removed {file_path}")
            elif os.path.isdir(file_path):
                import shutil
                shutil.rmtree(file_path)
                logger.info(f"✓ Removed {file_path}")
        except Exception as e:
            logger.warning(f"Could not remove {file_path}: {e}")

def main():
    """Run all tests"""
    logger.info("=" * 50)
    logger.info("NIGERIAN CONTENT CREATION SYSTEM - TEST SUITE")
    logger.info("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("News Fetcher", test_news_fetcher),
        ("One-Liner Generator", test_one_liner_generator),
        ("Visual Content Creator", test_visual_creator),
        ("Main System", test_main_system)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n--- Testing {test_name} ---")
        if test_func():
            passed += 1
            logger.info(f"✓ {test_name} PASSED")
        else:
            logger.error(f"✗ {test_name} FAILED")
    
    logger.info("\n" + "=" * 50)
    logger.info(f"TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 ALL TESTS PASSED! System is ready to use.")
        logger.info("\nNext steps:")
        logger.info("1. Install dependencies: pip install -r requirements.txt")
        logger.info("2. Run complete workflow: python content_automation_main.py --mode complete")
        logger.info("3. Check status: python content_automation_main.py --mode status")
    else:
        logger.error("❌ Some tests failed. Please check the errors above.")
    
    # Cleanup
    cleanup_test_files()
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 