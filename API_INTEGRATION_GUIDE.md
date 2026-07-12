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

4. **Strategy 6: Startup Niche Combination** ✅ (Tier 1 — 2026-07)
   - **Primary:** [StartupList Africa](https://www.startuplist.africa/startups) (snippet via `agent_strategy_run.py` + interactive script)
   - **Secondary:** Techpoint RSS (already in agent fetch)
   - **Optional legacy:** Crunchbase Nigeria hub (manual paste / scrape fallback only)
   - Benefit: Nigeria/Africa niche lists without Crunchbase login wall

5. **Strategy 7: Trending Startup Adaptation** ✅ (Tier 1 — 2026-07)
   - **Primary:** Product Hunt RSS (`https://www.producthunt.com/feed`) via `agent_strategy_run.py` + interactive script
   - **Secondary:** Techpoint Digest / YC company list (agent synthesis)
   - **Optional legacy:** Crunchbase “Trending Profiles” screenshot + Vision
   - Benefit: Automable trending signals without screenshot dependence

6. **Strategy 14: Global Data Trend Adaptation** ✅
   - Scrapes: OurWorldInData.org pages (also via `agent_strategy_run.py`)
   - Benefit: Auto-extract data visualizations and insights

> **Retired:** Strategy **8** (TrendHunter) was removed from the master runner — no licensed automation path. Use **Strategy 14** for global trend adaptation instead.

> **Crunchbase:** Not required for Strategies **6** or **7**. Keep only as optional manual secondary for global investor graphs.

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
- Strategy 7: Trending Startup Adaptation (Product Hunt feed)

**Available RSS Feeds:**
- Nairametrics RSS: `https://nairametrics.com/feed/`
- BusinessDay RSS: `https://businessday.ng/feed/`
- Premium Times RSS: `https://www.premiumtimesng.com/feed/`
- Vanguard RSS: `https://www.vanguardngr.com/feed/`
- Techpoint RSS: `https://techpoint.africa/feed/`
- Product Hunt RSS: `https://www.producthunt.com/feed` (Strategy 7)

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
- **Strategy 1**: Business Variation (seed JSON + complaint paste / `--non-interactive`; no paid complaint APIs in v1)
- **Strategy 3**: Network-Based (personal contacts)
- **Strategy 4**: Business Owner Problem Collection (questionnaires)
- **Strategy 11**: Personal Problem Conversion (personal list)
- **Strategy 12**: High-Value Problem Filtering (manual problem evaluation)

## Implementation Priority

### High Priority (Easy Wins):
1. ✅ Strategy 5: NewsAPI + RSS feeds
2. ✅ Strategy 9: NewsAPI + RSS feeds
3. ✅ Strategy 6: StartupList Africa (agent fetch + script); Crunchbase optional legacy
4. ✅ Strategy 14: OurWorldInData scraping / agent OWID snippets

### Medium Priority:
5. ✅ Strategy 7: Product Hunt RSS (agent fetch + script); Crunchbase screenshot optional legacy
6. 🔄 Strategy 12: Google Trends integration

### Low Priority (Already Manual):
- Strategies 3, 4, 10, 11 (better as manual processes)

## Recommended Free API Stack

```python
# Free APIs to use:
1. NewsAPI - News headlines (100/day free)
2. RSS Feeds - News + Product Hunt (unlimited, free)
3. Google Trends (pytrends) - Trending topics (free)
4. OurWorldInData - Public data exports (free)
5. BeautifulSoup - Web scraping (StartupList, OWID, news) (free; respect robots.txt)
```

## Cost Comparison

| Method | Cost | Rate Limits | Best For |
|--------|------|-------------|----------|
| BeautifulSoup | Free | None (respect robots.txt) | All scrapable sites |
| NewsAPI | Free tier: 100/day | 100 requests/day | News headlines |
| RSS Feeds | Free | Unlimited | News + Product Hunt |
| Google Trends | Free | ~5 requests/min | Trending topics |
| OurWorldInData | Free | Unlimited | Global data |

## Next Steps

1. ✅ NewsAPI + RSS for Strategies 5 & 9
2. ✅ Strategy 6 StartupList + Strategy 7 Product Hunt (agent `agent_strategy_run.py`)
3. ✅ OWID via agent runner / Strategy 14 scrape
4. Optional: Google Trends for Strategy 12
5. Optional Tier 3: remove Crunchbase code paths after ≥2 successful agent runs on new sources
