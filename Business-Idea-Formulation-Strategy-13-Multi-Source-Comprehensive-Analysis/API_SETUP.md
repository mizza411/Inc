# API Setup Guide - Strategy 13: Multi-Source Comprehensive Analysis

## Overview
This strategy now supports API integrations for SimilarWeb and AnnualReports.com data fetching.

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

### SimilarWeb API Integration
- **Automatic Traffic Data**: Fetch website traffic and engagement metrics
- **API Key Required**: Set `SIMILARWEB_API_KEY` environment variable
- **Manual Fallback**: Always available if API key not set

### AnnualReports.com Web Scraping
- **Automatic Report Fetching**: Attempts to find and extract annual report content
- **Smart Search**: Searches for company reports automatically
- **Manual Fallback**: Always available if scraping fails

## Configuration

### SimilarWeb API Setup

1. **Get API Key**: Sign up at [SimilarWeb API](https://www.similarweb.com/corp/api/)
2. **Set Environment Variable**:
   ```bash
   # Windows PowerShell
   $env:SIMILARWEB_API_KEY="your_api_key_here"
   
   # Windows CMD
   set SIMILARWEB_API_KEY=your_api_key_here
   
   # Linux/Mac
   export SIMILARWEB_API_KEY=your_api_key_here
   ```
3. **Or create `.env` file** (if using python-dotenv):
   ```
   SIMILARWEB_API_KEY=your_api_key_here
   ```

### Using APIs

When running the script:
- **SimilarWeb**: Choose 'y' when prompted to use API
- **AnnualReports**: Choose 'y' when prompted to fetch automatically
- Script will attempt API calls and fall back to manual input if needed

## API Endpoints Used

### SimilarWeb API
- **Endpoint**: `https://api.similarweb.com/v1/website/{domain}/total-traffic-and-engagement/visits`
- **Method**: GET
- **Authentication**: Bearer token
- **Returns**: Monthly visits, engagement metrics

### AnnualReports.com
- **Method**: Web scraping
- **Searches**: Company name on AnnualReports.com
- **Extracts**: Report content and key sections

## Troubleshooting

### SimilarWeb API Issues:
- **401 Unauthorized**: Check API key is set correctly
- **403 Forbidden**: API key may be invalid or expired
- **Rate Limit**: Too many requests → Wait and retry
- **Solution**: Use manual input option

### AnnualReports Scraping Issues:
- **404 Not Found**: Company report not found → Use manual input
- **403 Forbidden**: Website blocking requests → Use manual input
- **Timeout**: Slow connection → Use manual input

## Notes

- SimilarWeb API requires paid subscription for full access
- Free tier may have limited requests
- Web scraping respects website structure
- Always falls back to manual input if APIs fail
- No API keys required for AnnualReports scraping (uses public data)


