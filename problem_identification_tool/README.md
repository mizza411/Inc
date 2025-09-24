# Problem Identification Automation Tool

An automated tool for identifying people's problems through questionnaires and passive data collection, designed for introverted creators who want to gather insights without direct social interaction.

## 🎯 Features

- **Anonymous Questionnaire System**: Collect problem data without requiring personal information
- **JSON-Based Storage**: Simple, portable data storage without complex database setup
- **Mobile-Friendly Interface**: Responsive design that works on all devices
- **Automated Problem Extraction**: AI-powered analysis of responses to identify key problems
- **Analytics Dashboard**: Track completion rates, trends, and insights
- **Privacy-First Design**: GDPR compliant with data anonymization

## 🚀 Quick Start

### Prerequisites
- Python 3.7+ (for data processing)
- Modern web browser
- No database setup required!

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd problem_identification_tool
   ```

2. **Open the questionnaire**
   - Navigate to the `web` folder
   - Open `index.html` in your web browser
   - Start collecting responses immediately!

3. **Process responses (optional)**
   ```bash
   cd src
   python questionnaire_engine.py
   ```

## 📁 Project Structure

```
problem_identification_tool/
├── data/                    # JSON data storage
│   ├── problems.json       # Extracted problems
│   ├── questionnaires.json # Questionnaire definitions
│   └── analytics.json      # Analytics data
├── src/                    # Python processing engine
│   └── questionnaire_engine.py
├── web/                    # Web interface
│   ├── index.html         # Main questionnaire page
│   └── questionnaire.js   # Frontend logic
├── config/                 # Configuration files
│   └── settings.json
└── README.md
```

## 🔧 How It Works

### 1. **Questionnaire Collection**
- Users complete the questionnaire anonymously
- Responses are stored in JSON format
- No personal information is collected

### 2. **Problem Extraction**
- AI-powered analysis identifies problems from text responses
- Problems are categorized and scored for severity
- Keywords are extracted for better understanding

### 3. **Analytics & Insights**
- Track completion rates and response patterns
- Identify trending problems and categories
- Generate reports for decision-making

## 📊 Data Flow

```
User Response → JSON Storage → Problem Extraction → Analytics → Insights
```

## 🎨 Customization

### Adding New Questions
Edit `data/questionnaires.json` to add new questions or modify existing ones.

### Changing Categories
Update the categories list in `data/problems.json` to match your needs.

### Styling
Modify the CSS in `web/index.html` to match your brand.

## 🔒 Privacy & Security

- **Anonymous Collection**: No personal information required
- **Local Storage**: Data stored locally by default
- **GDPR Compliant**: Built with privacy regulations in mind
- **Data Control**: Users can request data deletion

## 📈 Analytics Features

- **Response Tracking**: Monitor completion rates
- **Problem Categorization**: Automatic problem classification
- **Trend Analysis**: Identify emerging issues
- **Export Options**: Export data in various formats

## 🚀 Deployment Options

### Static Hosting (Recommended)
- GitHub Pages
- Netlify
- Vercel
- Any static hosting service

### Self-Hosted
- Simple web server
- No database required
- Easy to maintain

### Netlify Deployment (Upload/Drag & Drop)
1. Go to Netlify Drop: https://app.netlify.com/drop
2. Drag the folder `problem_identification_tool/web` into the drop area
3. Wait for the deploy to finish; copy the live URL (ends with `.netlify.app`)
4. Optional: set a custom domain in Site settings → Domains

### Netlify Deployment (Connect Git)
1. Push this repository to GitHub
2. In Netlify: New site → Import from Git → choose your repo
3. Build settings:
   - Framework preset: None (static site)
   - Build command: (leave empty)
   - Publish directory: `problem_identification_tool/web`
4. Deploy

### Netlify Deployment (CLI, optional)
```
npm i -g netlify-cli
netlify deploy --prod --dir "problem_identification_tool/web"
```

### Delete a Netlify Project (if no longer needed)
1. Open the project in Netlify (Site overview)
2. Go to Site settings → General → Danger zone → Delete site
3. Confirm deletion (type the site name if prompted)
4. If a custom domain is attached, remove it first in Site settings → Domains

## 🔧 Technical Details

### Frontend
- **HTML5/CSS3/JavaScript**: Modern web standards
- **Responsive Design**: Works on all devices
- **Progressive Enhancement**: Works without JavaScript

### Backend (Optional)
- **Python 3.7+**: Data processing engine
- **JSON Storage**: Simple file-based storage
- **No Dependencies**: Minimal external requirements

## 📝 Usage Examples

### Basic Questionnaire
```javascript
// The questionnaire loads automatically when you open index.html
// No configuration needed!
```

### Processing Responses
```python
from src.questionnaire_engine import QuestionnaireEngine

engine = QuestionnaireEngine()
summary = engine.get_analytics_summary()
print(f"Total responses: {summary['total_responses']}")
```

### Exporting Data
```python
# Export all data as JSON
export_file = engine.export_data("json")
print(f"Data exported to: {export_file}")
```

## 🎯 Use Cases

- **Market Research**: Understand customer pain points
- **Product Development**: Identify features to build
- **Community Building**: Understand community needs
- **Problem Validation**: Test if problems are real and widespread
- **Content Creation**: Generate content ideas based on real problems

## 🔄 Workflow Integration

This tool integrates with the automated sharing workflow:
1. **Create Questionnaire**: Design your problem identification survey
2. **Deploy**: Host on static hosting service
3. **Share**: Use automated distribution methods
4. **Collect**: Gather responses passively
5. **Analyze**: Extract insights and problems
6. **Act**: Use insights for business decisions

## 📞 Support

For questions or issues:
1. Check the task file: `problem_identification_automation_tasks.md`
2. Review the workflow: `questionnaire_sharing_workflow.md`
3. Check the code comments for implementation details

## 🎉 Success Metrics

- **Completion Rate**: Target 80%+ questionnaire completion
- **Response Volume**: Collect 100+ responses per month
- **Problem Quality**: Identify actionable, specific problems
- **User Experience**: Smooth, engaging questionnaire flow

## 🔮 Future Enhancements

- **Advanced Analytics**: Machine learning insights
- **API Integration**: Connect with external services
- **Multi-language Support**: International questionnaires
- **Advanced Automation**: More sophisticated sharing methods

---

**Built for introverted creators who want to understand problems at scale without direct social interaction.**

## 🔎 Live Testing & Commands

### Open Live Site
- Windows (PowerShell):
  - `start https://vermillion-figolla-b9efb8.netlify.app/`
- macOS: `open https://vermillion-figolla-b9efb8.netlify.app/`
- Linux: `xdg-open https://vermillion-figolla-b9efb8.netlify.app/`

### Check Site is Up (HTTP 200)
```
curl -I https://vermillion-figolla-b9efb8.netlify.app/
```

### Test UTM Links
```
start "https://vermillion-figolla-b9efb8.netlify.app/?utm_source=instagram&utm_medium=story&utm_campaign=launch"
```

### Dashboard
- Open the live site → click "View Analytics Dashboard" → click "Load from this browser".

### Embed Test
Add this snippet to any HTML page and open it:
```
<iframe src="https://vermillion-figolla-b9efb8.netlify.app/embed.html" width="100%" height="900" style="border:0;" allowfullscreen></iframe>
```

### Local Data Processing (Optional)
```
python problem_identification_tool/src/questionnaire_engine.py --export json
python problem_identification_tool/src/questionnaire_engine.py --export csv
python problem_identification_tool/src/report_emailer.py --print
```

### Generate Sharing Assets (Safe One‑Liners)
```
# QR codes
python -c "import sys; sys.path.append('problem_identification_tool'); from src.qr_generator import QRCodeGenerator; QRCodeGenerator('https://vermillion-figolla-b9efb8.netlify.app').generate_contextual_qrs('/')"

# Social posts (daily JSON)
python -c "import sys, json, os; sys.path.append('problem_identification_tool'); from src.social_automation import SocialMediaAutomation; a=SocialMediaAutomation(); p=a.generate_daily_posts(); os.makedirs('problem_identification_tool/generated_content', exist_ok=True); open('problem_identification_tool/generated_content/generated_posts.json','w').write(json.dumps(p, indent=2)); print('generated_content/generated_posts.json')"

# Weekly schedule
python -c "import sys; sys.path.append('problem_identification_tool'); from src.social_automation import SocialMediaAutomation; a=SocialMediaAutomation(); print(a.create_posting_schedule())"

# Community posts
python -c "import sys, json, os; sys.path.append('problem_identification_tool'); from src.social_automation import SocialMediaAutomation; a=SocialMediaAutomation(); c=a.generate_community_posts(); os.makedirs('problem_identification_tool/generated_content', exist_ok=True); open('problem_identification_tool/generated_content/community_posts.json','w').write(json.dumps(c, indent=2)); print('generated_content/community_posts.json')"
```

## 👤 Admin: Viewing Results

### Quick View (same device that submitted)
- Open the dashboard directly: `https://vermillion-figolla-b9efb8.netlify.app/dashboard.html`
- Click "Load from this browser" to see responses saved in this browser's localStorage.

### Load Consolidated Exports
- Generate an export locally on your machine:
  - JSON: `python problem_identification_tool/src/questionnaire_engine.py --export json`
  - CSV: `python problem_identification_tool/src/questionnaire_engine.py --export csv`
- On the dashboard, click "Upload export JSON" and select the generated JSON file to view aggregated charts.

### Important (Current Architecture)
- This is a JSON‑first, privacy‑friendly setup. By default, survey responses are saved to each respondent's browser (localStorage) and are not sent to a central server.
- Use exports to consolidate and analyze data, or switch to a centralized collection (e.g., serverless functions/Sheets) if you need real‑time, multi‑device aggregation.
