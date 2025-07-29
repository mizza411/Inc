"""
Demand Analyzer for Gadgets
Fetches and analyzes demand data from multiple sources to guide gadget business decisions.
"""

import requests
from typing import Dict, List
import json

def get_google_trends_data(gadget_name: str) -> Dict[str, any]:
    """
    Get Google Trends data for a gadget to analyze search demand.
    Args:
        gadget_name: Name of the gadget to analyze.
    Returns:
        Dictionary with trend data (interest over time, related queries, etc.).
    """
    # Placeholder for Google Trends API integration
    # In real implementation, would use pytrends or Google Trends API
    return {
        "interest_over_time": [50, 65, 80, 75, 90],  # Mock trend data
        "trending": "increasing",
        "search_volume": "high",
        "related_queries": ["best", "review", "price", "buy"]
    }

def get_social_media_demand(gadget_name: str) -> Dict[str, any]:
    """
    Get social media demand data (mentions, hashtags, engagement).
    Args:
        gadget_name: Name of the gadget to analyze.
    Returns:
        Dictionary with social media metrics.
    """
    # Placeholder for social media API integration
    return {
        "twitter_mentions": 1250,
        "instagram_hashtags": 890,
        "facebook_engagement": 3400,
        "trending_score": 8.5
    }

def get_ecommerce_demand(gadget_name: str) -> Dict[str, any]:
    """
    Get e-commerce demand data (sales rank, views, wishlist additions).
    Args:
        gadget_name: Name of the gadget to analyze.
    Returns:
        Dictionary with e-commerce metrics.
    """
    # Placeholder for e-commerce API integration
    return {
        "sales_rank": 15,
        "page_views": 12500,
        "wishlist_additions": 450,
        "review_count": 89,
        "avg_rating": 4.2
    }

def calculate_demand_score(gadget_name: str) -> Dict[str, any]:
    """
    Calculate overall demand score by combining multiple data sources.
    Args:
        gadget_name: Name of the gadget to analyze.
    Returns:
        Dictionary with comprehensive demand analysis.
    """
    trends_data = get_google_trends_data(gadget_name)
    social_data = get_social_media_demand(gadget_name)
    ecommerce_data = get_ecommerce_demand(gadget_name)
    
    # Calculate demand score (0-100)
    trend_score = 25 if trends_data["trending"] == "increasing" else 10
    social_score = min(social_data["trending_score"] * 10, 30)
    ecommerce_score = min((100 - ecommerce_data["sales_rank"]) * 0.5, 25)
    
    total_score = trend_score + social_score + ecommerce_score
    
    return {
        "gadget_name": gadget_name,
        "demand_score": total_score,
        "demand_level": "high" if total_score > 60 else "medium" if total_score > 30 else "low",
        "trending": trends_data["trending"],
        "social_engagement": social_data["trending_score"],
        "ecommerce_popularity": ecommerce_data["sales_rank"],
        "recommendation": "Focus on this gadget" if total_score > 60 else "Consider this gadget" if total_score > 30 else "Low priority"
    }

def get_demand_ranking(gadget_list: List[str]) -> List[Dict[str, any]]:
    """
    Get demand ranking for a list of gadgets.
    Args:
        gadget_list: List of gadget names to analyze.
    Returns:
        List of gadgets ranked by demand score.
    """
    demand_data = []
    for gadget in gadget_list:
        demand_data.append(calculate_demand_score(gadget))
    
    # Sort by demand score (highest first)
    demand_data.sort(key=lambda x: x["demand_score"], reverse=True)
    return demand_data

if __name__ == "__main__":
    # Example usage
    test_gadgets = ["Smartwatch Pro", "Wireless Earbuds", "Smart Speaker"]
    rankings = get_demand_ranking(test_gadgets)
    for gadget in rankings:
        print(f"{gadget['gadget_name']}: Score {gadget['demand_score']} - {gadget['demand_level']} demand") 