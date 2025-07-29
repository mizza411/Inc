import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

class TwitterSource:
    def __init__(self, keywords):
        self.keywords = keywords
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        
    def fetch_problems(self):
        problems = []
        
        if not self.bearer_token:
            print("Warning: TWITTER_BEARER_TOKEN not found. Skipping Twitter source.")
            return problems
            
        headers = {
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/json'
        }
        
        for keyword in self.keywords:
            try:
                # Search for tweets with problem indicators
                query = f'"{keyword}" (problem OR issue OR complaint OR difficulty OR challenge OR help OR how OR why OR fail OR not working) -is:retweet'
                
                params = {
                    'query': query,
                    'max_results': 20,
                    'tweet.fields': 'created_at,public_metrics,author_id',
                    'expansions': 'author_id',
                    'user.fields': 'username,name'
                }
                
                response = requests.get(
                    'https://api.twitter.com/2/tweets/search/recent',
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for tweet in data.get('data', []):
                        text = tweet.get('text', '')
                        # Look for problem indicators
                        problem_indicators = ['problem', 'issue', 'complaint', 'difficulty', 'challenge', 'help', 'how to', 'why', 'fail', 'not working']
                        
                        if any(indicator in text.lower() for indicator in problem_indicators):
                            problems.append({
                                'source': f'twitter/{keyword}',
                                'title': text[:100] + '...' if len(text) > 100 else text,
                                'description': f"Twitter post about {keyword} with {tweet.get('public_metrics', {}).get('retweet_count', 0)} retweets",
                                'category': 'social_complaint',
                                'engagement': tweet.get('public_metrics', {}).get('retweet_count', 0) + tweet.get('public_metrics', {}).get('like_count', 0)
                            })
                            
            except Exception as e:
                print(f"Error fetching from Twitter for keyword '{keyword}': {e}")
                continue
                
        return problems 