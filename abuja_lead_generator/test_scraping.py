#!/usr/bin/env python3
"""
Test Script for Abuja Lead Generator Scraping
=============================================

This script tests the web scraping functionality to ensure it works correctly.
"""

import sys
import os
import logging

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config_manager import ConfigManager
from database_manager import DatabaseManager
from lead_scraper import LeadScraper

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_scraping():
    """Test the scraping functionality"""
    print("🧪 Testing Abuja Lead Generator Scraping")
    print("=" * 50)
    
    try:
        # Initialize components
        config = ConfigManager()
        db = DatabaseManager(config)
        scraper = LeadScraper(config, db)
        
        print("✅ Components initialized successfully")
        
        # Test individual scraping methods
        print("\n🔍 Testing Yellow Pages scraping...")
        yellow_pages_results = scraper._scrape_yellow_pages()
        print(f"Found {len(yellow_pages_results)} businesses from Yellow Pages")
        
        print("\n🔍 Testing Nigerian Pages scraping...")
        nigerian_pages_results = scraper._scrape_nigerian_pages()
        print(f"Found {len(nigerian_pages_results)} businesses from Nigerian Pages")
        
        print("\n🔍 Testing Abuja.com.ng scraping...")
        abuja_results = scraper._scrape_abuja_com()
        print(f"Found {len(abuja_results)} businesses from Abuja.com.ng")
        
        print("\n🔍 Testing Jiji.ng scraping...")
        jiji_results = scraper._scrape_jiji_abuja()
        print(f"Found {len(jiji_results)} businesses from Jiji.ng")
        
        # Combine all results
        all_results = yellow_pages_results + nigerian_pages_results + abuja_results + jiji_results
        unique_results = scraper._remove_duplicates(all_results)
        
        print(f"\n📊 Total Results:")
        print(f"• Raw results: {len(all_results)}")
        print(f"• Unique results: {len(unique_results)}")
        
        # Show sample results
        if unique_results:
            print(f"\n📋 Sample Results:")
            for i, business in enumerate(unique_results[:3]):
                print(f"{i+1}. {business['name']} - {business['industry']} - {business['source']}")
        
        # Test fallback
        print(f"\n🔄 Testing fallback mechanism...")
        fallback_results = scraper._get_fallback_businesses()
        print(f"Fallback provides {len(fallback_results)} businesses")
        
        print(f"\n✅ Scraping test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_scraping() 