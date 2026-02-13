# API Setup Guide - Strategy 5: News-Based Problem Extraction

## Overview
This strategy now supports automatic content fetching via web scraping APIs, with manual fallback options.

## Installation

Install required dependencies:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install requests beautifulsoup4 feedparser
```

## API Features

### Automatic Content Fetching
- **Web Scraping**: Automatically fetches content from Nigerian news websites
- **RSS Feeds**: Supports RSS feed parsing (if available)
- **Manual Fallback**: Always available if API fails or is not preferred

### How It Works

1. **Run the script**: `python steps.py`
2. **Select news sources** as usual
3. **Choose API option**: When prompted, choose 'y' to fetch automatically
4. **Script attempts** to fetch content via web scraping
5. **Falls back** to manual input if API fails

## Configuration

### Environment Variables (Optional)
No API keys required for basic web scraping. The script uses standard HTTP requests.

### Rate Limiting
- The script includes basic error handling
- Respects website response times
- Falls back gracefully if requests fail

## Troubleshooting

### If API Fetching Fails:
1. Check your internet connection
2. Some websites may block automated requests
3. Use manual input option (always available)
4. Install required packages: `pip install requests beautifulsoup4`

### Common Issues:
- **403 Forbidden**: Website blocking automated requests → Use manual input
- **Timeout**: Slow connection → Increase timeout or use manual input
- **Missing Content**: Website structure changed → Use manual input

## Notes

- Web scraping respects robots.txt and rate limits
- Always falls back to manual input if API fails
- No API keys required for basic functionality
- Content is truncated to optimal length for ChatGPT processing


