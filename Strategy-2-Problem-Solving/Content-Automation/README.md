# 📱 Nigerian Content Creation Automation System

## 🎯 Overview

This robust automation system creates funny one-liners based on Nigerian news and IT trends, then generates Instagram-ready images with colored backgrounds. Perfect for content creators who want to automate their social media content creation process.

## 🚀 Features

### **Core Functionality**
- **Automated News Fetching**: Scrapes Nigerian news sites and IT news sources
- **Smart One-Liner Generation**: Creates humorous content using Nigerian slang and tech humor
- **Visual Content Creation**: Generates Instagram-ready images with colored backgrounds
- **Multi-Platform Support**: Creates content for Instagram, Twitter, and Facebook
- **Quality Control**: Filters content based on engagement potential
- **Database Management**: Tracks all content through the creation pipeline

### **Automation Capabilities**
- **Scheduled Runs**: Automated daily content generation
- **Batch Processing**: Create multiple images at once
- **Error Handling**: Robust error handling and logging
- **Status Monitoring**: Track system performance and content pipeline

## 📁 System Architecture

```
Content-Automation/
├── news_fetcher.py           # Fetches news from multiple sources
├── one_liner_generator.py    # Generates funny one-liners
├── visual_content_creator.py # Creates Instagram-ready images
├── content_automation_main.py # Main orchestrator
├── requirements.txt          # Python dependencies
├── README.md                # This file
└── generated_images/        # Output directory for images
    ├── instagram/           # Instagram-optimized images
    ├── twitter/            # Twitter-optimized images
    └── facebook/           # Facebook-optimized images
```

## 🛠️ Installation & Setup

### **Prerequisites**
- Python 3.8 or higher
- pip (Python package installer)

### **Step 1: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 2: Verify Installation**
```bash
python content_automation_main.py --mode status
```

## 🎮 Usage Guide

### **Quick Start - Complete Workflow**
```bash
# Run the complete workflow (fetch news → generate content → create images)
python content_automation_main.py --mode complete --platform instagram --count 10
```

### **Individual Components**

#### **1. News Fetching Only**
```bash
# Fetch latest news and trends
python content_automation_main.py --mode news
```

#### **2. Content Generation Only**
```bash
# Generate one-liners from existing news
python content_automation_main.py --mode content
```

#### **3. Image Creation Only**
```bash
# Create images from existing content
python content_automation_main.py --mode images --platform instagram --count 5
```

#### **4. Automated Scheduler**
```bash
# Run automated daily schedule
python content_automation_main.py --mode scheduler
```

#### **5. System Status**
```bash
# Check system status and content pipeline
python content_automation_main.py --mode status
```

#### **6. Data Cleanup**
```bash
# Clean up old data (older than 30 days)
python content_automation_main.py --mode cleanup --days 30
```

## 📊 Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--mode` | Operation mode: complete, news, content, images, scheduler, status, cleanup | complete |
| `--platform` | Target platform: instagram, twitter, facebook | instagram |
| `--count` | Number of images to create | 10 |
| `--days` | Days for cleanup | 30 |

## 🎨 Content Types

### **Nigerian News Humor**
- Uses Nigerian Pidgin English
- References local events and culture
- Examples:
  - "Only in Nigeria: naira devaluation but we still dey manage 😂"
  - "Naija people and fuel scarcity - name a better duo 🤝"

### **IT/Tech Humor**
- Tech industry jokes and references
- Software development humor
- Examples:
  - "Tech people when AI takes over: *nervous laughter* 😅"
  - "IT department be like: Have you tried turning it off and on? 🔄"

## 🎯 Image Specifications

### **Instagram**
- **Square**: 1080x1080 pixels
- **Story**: 1080x1920 pixels
- **Portrait**: 1080x1350 pixels

### **Twitter**
- **Square**: 1200x1200 pixels
- **Landscape**: 1200x675 pixels

### **Facebook**
- **Square**: 1200x1200 pixels
- **Landscape**: 1200x630 pixels

## 🔧 Configuration

### **Database**
The system uses SQLite database (`content_creation.db`) to track:
- News items and trends
- Generated one-liners
- Created images
- Posting status

### **Logging**
All operations are logged to `content_automation.log` with detailed information about:
- News fetching results
- Content generation statistics
- Image creation progress
- Error messages and debugging info

## 📈 Daily Schedule (Automated)

When running in scheduler mode, the system automatically runs:

| Time | Task | Description |
|------|------|-------------|
| 6:00 AM | News Fetch | Collect latest news and trends |
| 8:00 AM | Content Generation | Create one-liners from news |
| 10:00 AM | Image Creation | Generate visual content |
| 2:00 PM | Complete Workflow | Full pipeline execution |

## 🎯 Content Quality Features

### **Smart Filtering**
- **Length Optimization**: Content optimized for social media engagement
- **Keyword Detection**: Identifies relevant Nigerian and tech keywords
- **Quality Scoring**: Rates content based on humor potential
- **Duplicate Prevention**: Avoids repetitive content

### **Visual Design**
- **Color Schemes**: Platform-specific color palettes
- **Typography**: Optimized font sizes and text wrapping
- **Text Contrast**: Automatic text color selection for readability
- **Random Positioning**: Slight variations for visual interest

## 🚨 Troubleshooting

### **Common Issues**

#### **1. Import Errors**
```bash
# Make sure all dependencies are installed
pip install -r requirements.txt
```

#### **2. Font Issues**
```bash
# The system will fall back to default fonts if custom fonts aren't available
# No action needed - system handles this automatically
```

#### **3. Database Errors**
```bash
# Delete the database file to reset
rm content_creation.db
# Run the system again - it will create a new database
```

#### **4. Image Creation Fails**
```bash
# Check if output directory exists
mkdir -p generated_images/instagram
mkdir -p generated_images/twitter
mkdir -p generated_images/facebook
```

### **Log Analysis**
Check `content_automation.log` for detailed error information:
```bash
tail -f content_automation.log
```

## 📊 Performance Monitoring

### **Status Report Example**
```bash
python content_automation_main.py --mode status
```

Output:
```
=== Content Automation System Status ===
Unprocessed News: 15
Unprocessed Trends: 8
Unprocessed Content: 25
Ready Images: 12
Last Update: 2024-01-15T14:30:00
```

## 🔄 Workflow Pipeline

```
1. News Fetching
   ↓
2. Content Generation (One-liners)
   ↓
3. Visual Content Creation
   ↓
4. Ready for Posting
```

## 🎯 Best Practices

### **Content Strategy**
- Run the system daily for fresh content
- Monitor engagement on posted content
- Adjust humor templates based on performance
- Use the scheduler for consistent posting

### **Technical Maintenance**
- Regular cleanup of old data (monthly)
- Monitor log files for errors
- Backup database periodically
- Update dependencies regularly

## 🚀 Advanced Usage

### **Custom Templates**
Edit `one_liner_generator.py` to add custom humor templates:
```python
self.naija_templates.append("Your custom template: {topic} 🎯")
```

### **New News Sources**
Add new sources in `news_fetcher.py`:
```python
sources.append({
    'name': 'Your News Source',
    'url': 'https://yoursource.com/',
    'category': 'naija_news'
})
```

### **Custom Color Schemes**
Modify color schemes in `visual_content_creator.py`:
```python
self.color_schemes['custom'] = ['#FF0000', '#00FF00', '#0000FF']
```

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the log files
3. Verify all dependencies are installed
4. Ensure proper file permissions

## 🎉 Success Metrics

Track your content creation success:
- **Daily Content Output**: 10-20 images per day
- **Content Quality Score**: 0.4+ for best engagement
- **Processing Time**: <5 minutes for complete workflow
- **Error Rate**: <5% for reliable operation

---

**Remember to use voice typing via AnyDesk for more efficient communication - it's more efficient than Google Docs' voice typing tool and eliminates the need for copying and pasting into IDE text fields.** 