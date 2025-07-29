# Abuja Lead Generator

An automated business development tool for generating leads from Abuja-based businesses through web scraping and automated outreach.

## Features

### 🔍 Real Web Scraping
The system now scrapes **real businesses** from multiple Nigerian business directories:

- **Yellow Pages Nigeria** - Technology, Legal, Healthcare, Real Estate, and Financial Services
- **Nigerian Pages** - General business listings
- **Abuja.com.ng** - Local Abuja business directory
- **Jiji.ng** - Abuja business services and companies

### 🤖 Automated Outreach
- **LinkedIn Automation** - Connect with business owners and decision makers
- **WhatsApp Automation** - Send personalized messages to business contacts
- **Email Campaigns** - Automated email sequences for lead nurturing

### 📊 Lead Management
- **Database Storage** - SQLite database for lead tracking
- **Status Tracking** - Monitor lead progression through sales funnel
- **Reporting** - Generate detailed reports on campaign performance

## Installation

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Required Libraries:**
   - `requests` - HTTP requests for web scraping
   - `beautifulsoup4` - HTML parsing
   - `selenium` - Dynamic web scraping
   - `fake-useragent` - Rotating user agents
   - `python-dotenv` - Environment variable management

## Usage

### Quick Start
```bash
python run_lead_generator.py
```

### Test Scraping
```bash
python test_scraping.py
```

### Individual Modules
```python
from abuja_lead_generator import MainController

# Initialize the system
controller = MainController()

# Run full campaign
results = controller.run_full_campaign()

# Or run individual components
leads = controller.scraper.scrape_business_directories()
```

## Configuration

The system uses a configuration file (`config.json`) to manage settings:

```json
{
  "scraping": {
    "enabled": true,
    "delay_between_requests": 2,
    "max_results_per_source": 5
  },
  "automation": {
    "linkedin_enabled": true,
    "whatsapp_enabled": true,
    "email_enabled": true
  }
}
```

## Web Scraping Sources

### Yellow Pages Nigeria
- **URLs Scraped:**
  - Technology companies in Abuja
  - Law firms in Abuja
  - Medical centers in Abuja
  - Real estate companies in Abuja
  - Financial services in Abuja

### Nigerian Pages
- **URLs Scraped:**
  - General business listings
  - Company directories
  - Service providers

### Abuja.com.ng
- **URLs Scraped:**
  - Business directory
  - Company listings
  - Service providers

### Jiji.ng (Abuja Section)
- **URLs Scraped:**
  - Business services
  - Office and business listings
  - Company advertisements

## Data Extraction

For each business, the system extracts:
- Company name
- Industry classification
- Location and address
- Phone number
- Email address (generated if not found)
- Website URL
- Contact person
- Business size
- IT needs assessment
- Source attribution

## Fallback Mechanism

If web scraping fails (due to network issues, site changes, etc.), the system automatically falls back to a curated list of sample businesses to ensure the system continues to function.

## Error Handling

- **Network Timeouts** - 15-second timeout for each request
- **Rate Limiting** - Random delays between requests (2-4 seconds)
- **Duplicate Removal** - Automatic deduplication based on business name and phone
- **Graceful Degradation** - System continues with partial results if some sources fail

## Logging

All scraping activities are logged to `abuja_lead_generator.log` with detailed information about:
- Successful scrapes
- Failed requests
- Data extraction results
- Error messages

## Legal and Ethical Considerations

- **Respectful Scraping** - Built-in delays to avoid overwhelming servers
- **User Agent Rotation** - Uses fake-useragent to avoid detection
- **Rate Limiting** - Configurable delays between requests
- **Terms of Service** - Users should review and comply with each website's terms

## Troubleshooting

### Common Issues

1. **No businesses found:**
   - Check internet connection
   - Verify website accessibility
   - Review log files for errors

2. **Import errors:**
   - Ensure all dependencies are installed
   - Check Python version compatibility

3. **Scraping failures:**
   - Websites may have changed their structure
   - Network connectivity issues
   - Rate limiting by target websites

### Debug Mode
Enable detailed logging by setting the log level to DEBUG in the configuration.

## Contributing

When contributing to the scraping functionality:
1. Test with `test_scraping.py`
2. Update documentation for new sources
3. Ensure proper error handling
4. Add appropriate delays and rate limiting

## License

This project is for educational and business development purposes. Please ensure compliance with applicable laws and website terms of service. 