import os
from dotenv import load_dotenv
import praw

load_dotenv()

class RedditSource:
    def __init__(self, subreddits):
        self.subreddits = subreddits
        client_id = os.getenv('REDDIT_CLIENT_ID')
        client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        user_agent = os.getenv('REDDIT_USER_AGENT')
        if not all([client_id, client_secret, user_agent]):
            raise ValueError("Missing Reddit API credentials. Please set REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, and REDDIT_USER_AGENT in your .env file.")
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )

    def fetch_problems(self):
        problems = []
        for subreddit in self.subreddits:
            for submission in self.reddit.subreddit(subreddit).hot(limit=20):
                if '?' in submission.title or 'problem' in submission.title.lower():
                    problems.append({
                        'source': f'reddit/{subreddit}',
                        'title': submission.title,
                        'description': submission.selftext
                    })
        return problems 