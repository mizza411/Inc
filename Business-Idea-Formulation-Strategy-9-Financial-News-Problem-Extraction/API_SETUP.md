# API Setup Guide - Strategy 9: Financial News Problem Extraction

## Overview
This strategy now supports automatic content fetching from financial news websites via web scraping, with manual fallback options.

## Installation

Install required dependencies:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install requests beautifulsoup4
```

## API Features

### Automatic Content Fetching
- **Web Scraping**: Automatically fetches content from:
  - Nairametrics.com
  - FinancialNigeria.com
  - BusinessDay.ng
- **Smart Content Extraction**: Focuses on main article content
- **Manual Fallback**: Always available if API fails

### How It Works

1. **Run the script**: `python steps.py`
2. **Select source** (or use scheduled source for the day)
3. **Choose API option**: When prompted, choose 'y' to fetch automatically
4. **Script attempts** to fetch and extract main content
5. **Falls back** to manual input if API fails

## Configuration

### Environment Variables
No API keys required. The script uses standard HTTP requests with proper headers.

### Scheduled Sources
The script automatically suggests the right source based on the day:
- **Monday/Tuesday**: Nairametrics
- **Wednesday/Thursday**: Financial Nigeria
- **Friday/Saturday**: BusinessDay

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

- Web scraping respects website structure and extracts main content
- Always falls back to manual input if API fails
- Content is optimized for ChatGPT processing (max 9000 chars)
- No API keys required for basic functionality


