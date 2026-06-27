# API Integration Guide - Business Idea Formulation Strategies

## Strategies That Can Use BeautifulSoup (Web Scraping)

### ✅ Already Implemented:
1. **Strategy 5: News-Based Problem Extraction** ✅
   - Scrapes: Vanguard, Punch, Guardian, ThisDay, Premium Times, etc.
   - Status: BeautifulSoup implemented

2. **Strategy 9: Financial News Problem Extraction** ✅
   - Scrapes: Nairametrics, FinancialNigeria, BusinessDay
   - Status: BeautifulSoup implemented

3. **Strategy 13: Multi-Source Comprehensive Analysis** ✅
   - Scrapes: AnnualReports.com
   - Status: BeautifulSoup implemented

### 🔄 Can Be Added:
4. **Strategy 6: Startup Niche Combination**
   - Can scrape: Crunchbase.com/hub/nigeria-startups
   - Benefit: Auto-extract startup list and niches

5. **Strategy 7: Trending Startup Adaptation**
   - Can scrape: Crunchbase "Trending Profiles" section
   - Benefit: Auto-extract trending startup data

6. **Strategy 14: Global Data Trend Adaptation**
   - Can scrape: OurWorldInData.org pages
   - Benefit: Auto-extract data visualizations and insights

> **Retired:** Strategy **8** (TrendHunter) was removed from the master runner — no licensed automation path. Use **Strategy 14** for global trend adaptation instead.

## Free APIs We Can Use

### NewsAPI (Free Tier Available)
**Best for:**
- Strategy 5: News-Based Problem Extraction
- Strategy 9: Financial News Problem Extraction

**Free Tier Limits:**
- 100 requests/day
- Headlines only (no full articles)
- Can filter by country (ng for Nigeria)

**Setup:**
```python
import requests

NEWSAPI_KEY = os.getenv('NEWSAPI_KEY', '')
NEWSAPI_URL = 'https://newsapi.org/v2/top-headlines'

# For Nigerian news
params = {
    'country': 'ng',
    'apiKey': NEWSAPI_KEY,
    'pageSize': 10
}
```

### RSS Feeds (Free, No API Key)
**Best for:**
- Strategy 5: News-Based Problem Extraction
- Strategy 9: Financial News Problem Extraction

**Available RSS Feeds:**
- Nairametrics RSS: `https://nairametrics.com/feed/`
- BusinessDay RSS: `https://businessday.ng/feed/`
- Premium Times RSS: `https://www.premiumtimesng.com/feed/`
- Vanguard RSS: `https://www.vanguardngr.com/feed/`

### OurWorldInData API (Free, Public Data)
**Best for:**
- Strategy 14: Global Data Trend Adaptation

**Access:**
- Public CSV/JSON exports available
- No API key required
- Direct data downloads

### Google Trends API (Free via pytrends)
**Best for:**
- Strategy 5: News-Based Problem Extraction (trending topics)
- Strategy 12: High-Value Problem Filtering (trending problems)

**Setup:**
```python
from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)
pytrends.build_payload(['keyword'], geo='NG', timeframe='today 3-m')
```

## Strategies That DON'T Need APIs

### Manual Input Only:
- **Strategy 3**: Network-Based (personal contacts)
- **Strategy 4**: Business Owner Problem Collection (questionnaires)
- **Strategy 11**: Personal Problem Conversion (personal list)
- **Strategy 12**: High-Value Problem Filtering (manual problem evaluation)

## Implementation Priority

### High Priority (Easy Wins):
1. ✅ Strategy 5: NewsAPI + RSS feeds
2. ✅ Strategy 9: NewsAPI + RSS feeds  
3. 🔄 Strategy 6: Crunchbase scraping
4. 🔄 Strategy 14: OurWorldInData scraping

### Medium Priority:
5. 🔄 Strategy 7: Crunchbase trending scraping
6. 🔄 Strategy 12: Google Trends integration

### Low Priority (Already Manual):
- Strategies 3, 4, 10, 11 (better as manual processes)

## Recommended Free API Stack

```python
# Free APIs to use:
1. NewsAPI - News headlines (100/day free)
2. RSS Feeds - News articles (unlimited, free)
3. Google Trends (pytrends) - Trending topics (free)
4. OurWorldInData - Public data exports (free)
5. BeautifulSoup - Web scraping (free, no limits)
```

## Cost Comparison

| Method | Cost | Rate Limits | Best For |
|--------|------|-------------|----------|
| BeautifulSoup | Free | None (respect robots.txt) | All scrapable sites |
| NewsAPI | Free tier: 100/day | 100 requests/day | News headlines |
| RSS Feeds | Free | Unlimited | News articles |
| Google Trends | Free | ~5 requests/min | Trending topics |
| OurWorldInData | Free | Unlimited | Global data |

## Next Steps

1. Add NewsAPI to Strategies 5 & 9
2. Add RSS feed parsing to Strategies 5 & 9
3. Add BeautifulSoup to Strategies 6, 7, 8, 14
4. Add Google Trends to Strategy 12 (optional)


