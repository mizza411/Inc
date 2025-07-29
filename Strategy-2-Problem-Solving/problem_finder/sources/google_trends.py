from pytrends.request import TrendReq

class GoogleTrendsSource:
    def __init__(self, keywords):
        self.keywords = keywords
        self.pytrends = TrendReq()

    def fetch_problems(self):
        problems = []
        for kw in self.keywords:
            self.pytrends.build_payload([kw], timeframe='now 7-d')
            try:
                related = self.pytrends.related_queries().get(kw)
                if related and 'top' in related and related['top'] is not None:
                    for _, row in related['top'].iterrows():
                        problems.append({
                            'source': 'google_trends',
                            'title': row['query'],
                            'description': f"Trending query related to '{kw}'"
                        })
                else:
                    # Optionally log or print that no related queries were found for this keyword
                    pass
            except IndexError:
                # Google returned no data at all for this keyword
                # Optionally log or print that no data was found
                continue
        return problems 