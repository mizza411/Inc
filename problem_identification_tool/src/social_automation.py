#!/usr/bin/env python3
"""
Social Media Automation for Problem Identification Tool
Automated posting and sharing scripts for introverted creators
"""

import json
import os
import schedule
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any
import random

class SocialMediaAutomation:
    def __init__(self, config_file="config/social_config.json"):
        self.config_file = config_file
        self.load_config()
        self.post_templates = self.load_post_templates()
    
    def load_config(self):
        """Load social media configuration"""
        default_config = {
            "questionnaire_url": "https://yoursite.com/web/index.html",
            "posting_schedule": {
                "twitter": ["10:00", "15:00", "19:00"],
                "linkedin": ["09:00", "14:00"],
                "reddit": ["12:00", "18:00"]
            },
            "hashtags": {
                "primary": ["#problemsolving", "#communityhelp", "#feedback"],
                "secondary": ["#survey", "#research", "#insights", "#community"],
                "niche": ["#entrepreneur", "#smallbusiness", "#productivity"]
            },
            "communities": {
                "reddit": [
                    "r/entrepreneur",
                    "r/smallbusiness", 
                    "r/productivity",
                    "r/startups",
                    "r/AskReddit"
                ],
                "linkedin_groups": [
                    "Small Business Owners",
                    "Entrepreneurs Network",
                    "Product Management"
                ]
            },
            "posting_enabled": False  # Set to True when ready to post
        }
        
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = {**default_config, **json.load(f)}
        else:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        """Save configuration to file"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def load_post_templates(self):
        """Load post templates for different platforms"""
        return {
            "twitter": [
                "Help us understand community challenges! Take our quick survey: {url} #problemsolving #communityhelp",
                "What problems do you face daily? Share your insights: {url} #feedback #research",
                "We're researching common challenges. 3 minutes to help: {url} #survey #insights",
                "Your problems matter! Help us build better solutions: {url} #community #entrepreneur"
            ],
            "linkedin": [
                "We're conducting research on common business and personal challenges. Your insights would be invaluable in helping us understand what problems people face most frequently.\n\nTake our quick 3-minute survey: {url}\n\n#BusinessResearch #CommunityInsights #ProblemSolving",
                "Understanding real problems is the first step to creating meaningful solutions. We'd love your input on the challenges you face in your work and personal life.\n\nParticipate in our research: {url}\n\n#Research #Community #Innovation #Feedback",
                "Help us identify the most pressing problems in our community. Your responses will guide us in developing better tools and solutions.\n\nSurvey link: {url}\n\n#CommunityResearch #ProblemIdentification #Innovation"
            ],
            "reddit": [
                "We're researching common problems people face in their daily lives. Would love your input on a quick 3-minute survey: {url}\n\nThis will help us understand what challenges are most widespread and how we might address them.",
                "Quick research request: What are the biggest problems you face regularly? We're collecting insights to better understand community needs: {url}\n\nAll responses are anonymous and will help guide future solution development.",
                "Community research: We're studying common challenges people encounter. Your input would be really valuable: {url}\n\nTakes about 3 minutes, completely anonymous, and helps us build better solutions."
            ]
        }
    
    def generate_post(self, platform: str, template_vars: Dict[str, str] = None):
        """Generate a post for a specific platform"""
        if platform not in self.post_templates:
            return None
        
        templates = self.post_templates[platform]
        template = random.choice(templates)
        
        # Default template variables
        defaults = {
            "url": self.config["questionnaire_url"],
            "hashtags": " ".join(self.config["hashtags"]["primary"])
        }
        
        if template_vars:
            defaults.update(template_vars)
        
        return template.format(**defaults)
    
    def create_utm_url(self, source: str, medium: str, campaign: str = "social_automation"):
        """Create UTM-tracked URL"""
        from urllib.parse import urlencode
        
        utm_params = {
            "utm_source": source,
            "utm_medium": medium,
            "utm_campaign": campaign,
            "utm_content": f"post_{datetime.now().strftime('%Y%m%d')}"
        }
        
        base_url = self.config["questionnaire_url"]
        return f"{base_url}?{urlencode(utm_params)}"
    
    def generate_daily_posts(self):
        """Generate posts for all platforms for the day"""
        posts = {}
        
        for platform in ["twitter", "linkedin", "reddit"]:
            if platform in self.config["posting_schedule"]:
                # Create UTM-tracked URL
                utm_url = self.create_utm_url(platform, "social_media")
                
                # Generate post
                post = self.generate_post(platform, {"url": utm_url})
                if post:
                    posts[platform] = {
                        "content": post,
                        "url": utm_url,
                        "scheduled_times": self.config["posting_schedule"][platform]
                    }
        
        return posts
    
    def save_posts_to_file(self, posts: Dict[str, Any], filename: str = None):
        """Save generated posts to file for manual posting"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_posts_{timestamp}.json"
        
        filepath = os.path.join("generated_content", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(posts, f, indent=2)
        
        return filepath
    
    def create_posting_schedule(self):
        """Create a weekly posting schedule"""
        schedule_data = {
            "monday": self.generate_daily_posts(),
            "tuesday": self.generate_daily_posts(),
            "wednesday": self.generate_daily_posts(),
            "thursday": self.generate_daily_posts(),
            "friday": self.generate_daily_posts(),
            "saturday": self.generate_daily_posts(),
            "sunday": self.generate_daily_posts()
        }
        
        filename = f"weekly_schedule_{datetime.now().strftime('%Y%m%d')}.json"
        filepath = os.path.join("generated_content", filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(schedule_data, f, indent=2)
        
        return filepath
    
    def generate_community_posts(self):
        """Generate posts specifically for community forums"""
        community_posts = {}
        
        # Reddit communities
        for subreddit in self.config["communities"]["reddit"]:
            utm_url = self.create_utm_url("reddit", "community", subreddit.replace("r/", ""))
            post = self.generate_post("reddit", {"url": utm_url})
            community_posts[subreddit] = {
                "content": post,
                "url": utm_url,
                "platform": "reddit"
            }
        
        # LinkedIn groups
        for group in self.config["communities"]["linkedin_groups"]:
            utm_url = self.create_utm_url("linkedin", "group", group.replace(" ", "_").lower())
            post = self.generate_post("linkedin", {"url": utm_url})
            community_posts[group] = {
                "content": post,
                "url": utm_url,
                "platform": "linkedin"
            }
        
        return community_posts
    
    def print_posting_guide(self):
        """Print a guide for manual posting"""
        print("📱 Social Media Posting Guide")
        print("=" * 50)
        print(f"Questionnaire URL: {self.config['questionnaire_url']}")
        print("\nGenerated Posts:")
        
        posts = self.generate_daily_posts()
        for platform, data in posts.items():
            print(f"\n{platform.upper()}:")
            print(f"Content: {data['content']}")
            print(f"URL: {data['url']}")
            print(f"Scheduled times: {', '.join(data['scheduled_times'])}")
        
        print("\nCommunity Posts:")
        community_posts = self.generate_community_posts()
        for community, data in community_posts.items():
            print(f"\n{community} ({data['platform']}):")
            print(f"Content: {data['content']}")
            print(f"URL: {data['url']}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Social Media Automation for Problem Identification Tool")
    parser.add_argument("--generate", action="store_true", help="Generate posts for today")
    parser.add_argument("--schedule", action="store_true", help="Create weekly posting schedule")
    parser.add_argument("--communities", action="store_true", help="Generate community-specific posts")
    parser.add_argument("--guide", action="store_true", help="Print posting guide")
    parser.add_argument("--config", help="Update questionnaire URL in config")
    
    args = parser.parse_args()
    
    automation = SocialMediaAutomation()
    
    if args.config:
        automation.config["questionnaire_url"] = args.config
        automation.save_config()
        print(f"Updated questionnaire URL to: {args.config}")
    
    if args.generate:
        posts = automation.generate_daily_posts()
        filepath = automation.save_posts_to_file(posts)
        print(f"Generated posts saved to: {filepath}")
    
    if args.schedule:
        filepath = automation.create_posting_schedule()
        print(f"Weekly schedule saved to: {filepath}")
    
    if args.communities:
        community_posts = automation.generate_community_posts()
        filepath = automation.save_posts_to_file(community_posts, "community_posts.json")
        print(f"Community posts saved to: {filepath}")
    
    if args.guide:
        automation.print_posting_guide()
    
    if not any([args.generate, args.schedule, args.communities, args.guide, args.config]):
        automation.print_posting_guide()

if __name__ == "__main__":
    main()
