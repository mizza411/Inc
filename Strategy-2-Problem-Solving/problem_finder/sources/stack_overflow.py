import requests
import json
from datetime import datetime, timedelta

class StackOverflowSource:
    def __init__(self, tags):
        self.tags = tags
        self.base_url = "https://api.stackexchange.com/2.3"

    def fetch_problems(self):
        problems = []
        for tag in self.tags:
            try:
                # Get questions from the last 7 days with high view counts
                params = {
                    'fromdate': int((datetime.now() - timedelta(days=7)).timestamp()),
                    'todate': int(datetime.now().timestamp()),
                    'order': 'desc',
                    'sort': 'votes',
                    'tagged': tag,
                    'site': 'stackoverflow',
                    'pagesize': 20
                }
                
                response = requests.get(f"{self.base_url}/questions", params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for question in data.get('items', []):
                        # Look for problem indicators in title
                        title = question.get('title', '')
                        problem_indicators = ['error', 'issue', 'problem', 'bug', 'fail', 'not working', 'how to', 'why']
                        
                        if any(indicator in title.lower() for indicator in problem_indicators):
                            problems.append({
                                'source': f'stackoverflow/{tag}',
                                'title': title,
                                'description': f"Stack Overflow question with {question.get('answer_count', 0)} answers, {question.get('view_count', 0)} views",
                                'category': 'technical_problem',
                                'score': question.get('score', 0),
                                'answers': question.get('answer_count', 0),
                                'views': question.get('view_count', 0)
                            })
                
            except Exception as e:
                print(f"Error fetching from Stack Overflow for tag '{tag}': {e}")
                continue
                
        return problems 