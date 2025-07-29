"""
Demand-Driven Gadget Sourcing
First analyzes demand, then dynamically searches for sourcing options.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from demand_analyzer import calculate_demand_score

def get_trending_gadgets() -> List[str]:
    """
    Get trending gadgets from demand websites (Google Trends, social media, news).
    Returns:
        List of trending gadget names.
    """
    trending_gadgets = []
    
    print("🔍 Checking demand sources:")
    
    # Check Google Trends for trending tech searches
    print("   📊 Google Trends - Analyzing search trends...")
    try:
        # Placeholder for Google Trends API
        google_trends_gadgets = [
            "Smartwatch Pro",
            "Wireless Earbuds",
            "Smart Speaker",
            "Fitness Tracker",
            "Bluetooth Headphones"
        ]
        trending_gadgets.extend(google_trends_gadgets)
        print(f"      ✅ Found {len(google_trends_gadgets)} trending gadgets from Google Trends")
    except Exception as e:
        print(f"      ❌ Error fetching Google Trends: {e}")
    
    # Check social media trending hashtags
    print("   📱 Social Media - Checking trending hashtags...")
    try:
        # Placeholder for social media API
        social_media_gadgets = [
            "Smart Home Hub",
            "Portable Charger",
            "Wireless Charger"
        ]
        trending_gadgets.extend(social_media_gadgets)
        print(f"      ✅ Found {len(social_media_gadgets)} trending gadgets from Social Media")
    except Exception as e:
        print(f"      ❌ Error fetching social media trends: {e}")
    
    # Check e-commerce trending products
    print("   🛒 E-commerce - Analyzing popular products...")
    try:
        # Placeholder for e-commerce API
        ecommerce_gadgets = [
            "Smart Camera",
            "Robot Vacuum",
            "Smart Lock"
        ]
        trending_gadgets.extend(ecommerce_gadgets)
        print(f"      ✅ Found {len(ecommerce_gadgets)} trending gadgets from E-commerce")
    except Exception as e:
        print(f"      ❌ Error fetching e-commerce trends: {e}")
    
    # Check tech news and reviews
    print("   📰 Tech News - Checking latest reviews and mentions...")
    try:
        # Placeholder for news API
        news_gadgets = [
            "VR Headset",
            "Smart Thermostat",
            "Security Camera"
        ]
        trending_gadgets.extend(news_gadgets)
        print(f"      ✅ Found {len(news_gadgets)} trending gadgets from Tech News")
    except Exception as e:
        print(f"      ❌ Error fetching tech news: {e}")
    
    # Remove duplicates and show summary
    unique_gadgets = list(set(trending_gadgets))
    print(f"\n📈 Summary: Found {len(unique_gadgets)} unique trending gadgets from 4 sources")
    print("   Sources: Google Trends, Social Media, E-commerce, Tech News")
    
    return unique_gadgets

def search_supplier_platforms(gadget_name: str) -> List[Dict[str, str]]:
    """
    Search multiple supplier platforms for a specific gadget.
    Args:
        gadget_name: Name of the gadget to search for.
    Returns:
        List of sourcing options with platform, price, availability.
    """
    sourcing_options = []
    
    print(f"🔍 Searching for '{gadget_name}' across supplier platforms:")
    
    # Search Jumia Nigeria
    print("   🇳🇬 Jumia Nigeria - Checking local availability...")
    try:
        jumia_results = search_jumia(gadget_name)
        sourcing_options.extend(jumia_results)
        print(f"      ✅ Found {len(jumia_results)} options on Jumia")
    except Exception as e:
        print(f"      ❌ Error searching Jumia: {e}")
    
    # Search Konga
    print("   🇳🇬 Konga - Checking local marketplace...")
    try:
        konga_results = search_konga(gadget_name)
        sourcing_options.extend(konga_results)
        print(f"      ✅ Found {len(konga_results)} options on Konga")
    except Exception as e:
        print(f"      ❌ Error searching Konga: {e}")
    
    # Search Alibaba
    print("   🌏 Alibaba - Checking international suppliers...")
    try:
        alibaba_results = search_alibaba(gadget_name)
        sourcing_options.extend(alibaba_results)
        print(f"      ✅ Found {len(alibaba_results)} options on Alibaba")
    except Exception as e:
        print(f"      ❌ Error searching Alibaba: {e}")
    
    # Search local suppliers
    print("   🏪 Local Suppliers - Checking direct suppliers...")
    try:
        local_results = search_local_suppliers(gadget_name)
        sourcing_options.extend(local_results)
        print(f"      ✅ Found {len(local_results)} options from Local Suppliers")
    except Exception as e:
        print(f"      ❌ Error searching local suppliers: {e}")
    
    print(f"   📊 Total: Found {len(sourcing_options)} sourcing options across 4 platforms")
    
    return sourcing_options

def search_jumia(gadget_name: str) -> List[Dict[str, str]]:
    """Search Jumia for a specific gadget."""
    # Placeholder for Jumia search
    return [{
        'platform': 'Jumia Nigeria',
        'gadget_name': gadget_name,
        'price': '₦25,000',
        'availability': 'In Stock',
        'link': f'https://www.jumia.com.ng/search/{gadget_name}',
        'rating': '4.2'
    }]

def search_konga(gadget_name: str) -> List[Dict[str, str]]:
    """Search Konga for a specific gadget."""
    # Placeholder for Konga search
    return [{
        'platform': 'Konga',
        'gadget_name': gadget_name,
        'price': '₦23,500',
        'availability': 'In Stock',
        'link': f'https://www.konga.com/search/{gadget_name}',
        'rating': '4.0'
    }]

def search_alibaba(gadget_name: str) -> List[Dict[str, str]]:
    """Search Alibaba for a specific gadget."""
    # Placeholder for Alibaba search
    return [{
        'platform': 'Alibaba',
        'gadget_name': gadget_name,
        'price': '$15.50',
        'availability': 'Bulk Available',
        'link': f'https://www.alibaba.com/trade/search/{gadget_name}',
        'rating': '4.5'
    }]

def search_local_suppliers(gadget_name: str) -> List[Dict[str, str]]:
    """Search local suppliers for a specific gadget."""
    # Placeholder for local supplier search
    return [{
        'platform': 'Local Supplier',
        'gadget_name': gadget_name,
        'price': '₦22,000',
        'availability': 'Limited Stock',
        'link': 'Contact supplier',
        'rating': '4.1'
    }]

def get_demand_analysis(gadget_name: str) -> Dict[str, Any]:
    """
    Get demand analysis for a specific gadget.
    Args:
        gadget_name: Name of the gadget to analyze.
    Returns:
        Dictionary with demand analysis data.
    """
    demand_data = calculate_demand_score(gadget_name)
    
    return {
        "level": demand_data.get("demand_level", "Unknown"),
        "score": demand_data.get("demand_score", 0),
        "trend": demand_data.get("trending", "Unknown"),
        "recommendation": demand_data.get("recommendation", "No recommendation")
    }

def get_demand_driven_gadgets() -> List[Dict[str, Any]]:
    """
    Get gadgets based on demand analysis, then find sourcing options.
    Returns:
        List of gadgets with demand data and sourcing options.
    """
    print("🚀 Starting demand-driven sourcing process...")
    
    # Step 1: Get trending gadgets from demand sources
    trending_gadgets = get_trending_gadgets()
    
    if not trending_gadgets:
        print("❌ No trending gadgets found from demand sources.")
        return []
    
    print(f"\n🔍 Analyzing sourcing options for {len(trending_gadgets)} trending gadgets...")
    
    gadgets_with_sourcing = []
    
    for gadget in trending_gadgets:
        print(f"\n📱 Processing: {gadget}")
        
        # Step 2: Find sourcing options for this gadget
        sourcing_options = search_supplier_platforms(gadget)
        
        if sourcing_options:
            # Step 3: Determine best source (prioritize B2B over B2C)
            best_source = determine_best_source(sourcing_options)
            
            # Step 4: Get demand analysis
            demand_data = get_demand_analysis(gadget)
            
            gadget_data = {
                "name": gadget,
                "sourcing_options": sourcing_options,
                "best_source": best_source,
                "demand_level": demand_data["level"],
                "demand_score": demand_data["score"],
                "trend": demand_data["trend"],
                "recommendation": demand_data["recommendation"]
            }
            
            gadgets_with_sourcing.append(gadget_data)
            print(f"   ✅ {gadget}: {len(sourcing_options)} sourcing options, Best: {best_source}")
        else:
            print(f"   ❌ {gadget}: No sourcing options found")
    
    # Sort by demand score (highest first)
    gadgets_with_sourcing.sort(key=lambda x: x["demand_score"], reverse=True)
    
    print(f"\n🎯 Summary: Found sourcing options for {len(gadgets_with_sourcing)} out of {len(trending_gadgets)} trending gadgets")
    
    return gadgets_with_sourcing

def determine_best_source(sourcing_options: List[Dict[str, str]]) -> str:
    """
    Determine the best sourcing option, prioritizing B2B over B2C.
    Args:
        sourcing_options: List of sourcing options with platform info.
    Returns:
        Name of the best source platform.
    """
    if not sourcing_options:
        return "No options available"
    
    # Define source priorities (B2B first, then B2C)
    source_priority = {
        "Alibaba": 1,           # B2B - International wholesale
        "Local Suppliers": 2,    # B2B - Direct suppliers
        "Konga": 3,             # B2C - Local marketplace
        "Jumia": 4              # B2C - Local marketplace
    }
    
    # Sort by priority (lower number = higher priority)
    sorted_options = sorted(sourcing_options, key=lambda x: source_priority.get(x.get("platform", ""), 999))
    
    best_option = sorted_options[0]
    platform = best_option.get("platform", "Unknown")
    
    # Add reasoning for the choice
    if platform in ["Alibaba", "Local Suppliers"]:
        reason = "B2B platform - Better pricing and business terms"
    else:
        reason = "B2C platform - Fallback option"
    
    print(f"      🎯 Best Source: {platform} ({reason})")
    
    return platform

def display_sourcing_options(gadgets_with_sourcing: List[Dict[str, any]]):
    """Display gadgets with their sourcing options."""
    print("\n" + "="*80)
    print("DEMAND-DRIVEN GADGET SOURCING RESULTS")
    print("="*80)
    
    for i, gadget in enumerate(gadgets_with_sourcing):
        print(f"\n{i+1}. {gadget['name']}")
        print(f"   Demand: {gadget['demand_level']} (Score: {gadget['demand_score']})")
        print(f"   Trending: {gadget['trend']}")
        print(f"   Recommendation: {gadget['recommendation']}")
        print("   Sourcing Options:")
        
        for option in gadget['sourcing_options']:
            print(f"     - {option['platform']}: {option['price']} ({option['availability']}) - Rating: {option['rating']}")

if __name__ == "__main__":
    gadgets = get_demand_driven_gadgets()
    display_sourcing_options(gadgets) 