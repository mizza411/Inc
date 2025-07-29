import requests
from bs4 import BeautifulSoup
import time
import random

class QuoraSource:
    def __init__(self, topics):
        self.topics = topics
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def fetch_problems(self):
        problems = []
        for topic in self.topics:
            try:
                # Search for questions related to the topic
                search_url = f"https://www.quora.com/search?q={topic.replace(' ', '+')}&type=question"
                response = self.session.get(search_url)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    questions = soup.find_all('div', class_='question_link')
                    
                    for question in questions[:10]:  # Limit to 10 questions per topic
                        title_elem = question.find('span', class_='question_text')
                        if title_elem:
                            title = title_elem.get_text().strip()
                            # Look for problem indicators
                            problem_indicators = ['problem', 'issue', 'difficulty', 'challenge', 'help', 'how to', 'why', 'what if']
                            if any(indicator in title.lower() for indicator in problem_indicators):
                                problems.append({
                                    'source': f'quora/{topic}',
                                    'title': title,
                                    'description': f"Quora question about {topic}",
                                    'category': 'problem_identification'
                                })
                
                time.sleep(random.uniform(1, 3))  # Be respectful to Quora
                
            except Exception as e:
                print(f"Error fetching from Quora for topic '{topic}': {e}")
                continue
                
        return problems 