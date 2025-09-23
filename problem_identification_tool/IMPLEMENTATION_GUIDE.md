# Problem Identification Tool - Implementation Guide

## High-Level Steps to Complete the Project

### Phase 1: Foundation Setup ✅ COMPLETED
**What we built:**
- Created complete project directory structure with data, src, web, and config folders
- Designed comprehensive JSON schema for storing problems, questionnaires, and analytics
- Built a fully functional HTML questionnaire with JavaScript that works on mobile
- Implemented Python backend engine for processing responses and extracting problems
- Created configuration system for easy customization

**How to verify Phase 1:**
1. Open `web/index.html` in your browser
2. Complete the questionnaire to test functionality
3. Check that responses are stored in browser localStorage
4. Run `python src/questionnaire_engine.py` to test Python processing
5. Verify JSON files are created in the data folder

### Phase 2: Enhanced Features (Next Steps)
**What to build next:**
1. **Analytics Dashboard**: Create a web page to view collected data and insights
2. **Data Export**: Add functionality to export responses as CSV/Excel
3. **Advanced Problem Extraction**: Improve AI-powered problem identification
4. **Mobile Optimization**: Ensure perfect mobile experience

**Implementation approach:**
- Create `web/dashboard.html` for analytics visualization
- Add Chart.js for data visualization
- Build export functionality in Python engine
- Enhance problem extraction algorithms

### Phase 3: Automation & Distribution
**What to build:**
1. **QR Code Generator**: Create QR codes for easy sharing
2. **Social Media Integration**: Automated posting scripts
3. **Email Templates**: Automated email campaigns
4. **Analytics Tracking**: UTM parameters and source tracking

**Implementation approach:**
- Use Python libraries for QR code generation
- Create social media automation scripts
- Build email template system
- Add tracking parameters to questionnaire URLs

### Phase 4: Advanced Features
**What to build:**
1. **Multi-language Support**: Support different languages
2. **Custom Questionnaires**: Allow users to create custom surveys
3. **API Endpoints**: REST API for data access
4. **Real-time Analytics**: Live dashboard updates

**Implementation approach:**
- Create questionnaire builder interface
- Build REST API with Flask/FastAPI
- Implement WebSocket for real-time updates
- Add internationalization support

## Current Status: Ready for Testing

**What you can do right now:**
1. **Test the questionnaire**: Open `web/index.html` and complete it
2. **Check data storage**: Look at browser localStorage for responses
3. **Process responses**: Run the Python engine to extract problems
4. **Customize questions**: Edit `data/questionnaires.json` to modify questions
5. **Deploy to web**: Upload the web folder to any static hosting service

**Next immediate steps:**
1. Test the current implementation thoroughly
2. Create analytics dashboard (Phase 2)
3. Add data export functionality
4. Set up automated sharing methods

## Technical Architecture

**Frontend (web/):**
- `index.html`: Main questionnaire interface
- `questionnaire.js`: JavaScript logic for form handling
- Responsive design that works on all devices
- Local storage fallback for data persistence

**Backend (src/):**
- `questionnaire_engine.py`: Core processing engine
- JSON file storage (no database required)
- AI-powered problem extraction
- Analytics and reporting

**Data Storage (data/):**
- `problems.json`: Extracted problems and insights
- `questionnaires.json`: Questionnaire definitions
- `analytics.json`: Usage and performance metrics

**Configuration (config/):**
- `settings.json`: App configuration and preferences
- Easy customization without code changes

## Deployment Options

**Static Hosting (Recommended):**
1. Upload `web/` folder to GitHub Pages, Netlify, or Vercel
2. No server setup required
3. Free hosting available
4. Automatic HTTPS and CDN

**Self-Hosted:**
1. Set up simple web server (Apache, Nginx)
2. Run Python engine for data processing
3. Full control over data and customization

## Success Metrics

**Phase 1 Success Indicators:**
- ✅ Questionnaire loads and functions properly
- ✅ Responses are collected and stored
- ✅ Problem extraction works correctly
- ✅ Mobile experience is smooth
- ✅ No errors in browser console

**Phase 2 Success Indicators:**
- Analytics dashboard shows meaningful insights
- Data export works correctly
- Problem categorization is accurate
- Performance is fast and responsive

## Common Issues and Solutions

**Issue: Questionnaire doesn't load**
- Solution: Check browser console for errors
- Ensure all files are in correct locations
- Test with different browsers

**Issue: Responses not saving**
- Solution: Check localStorage in browser dev tools
- Verify JavaScript is enabled
- Test with different browsers

**Issue: Python engine errors**
- Solution: Check Python version (3.7+ required)
- Verify all dependencies are installed
- Check file permissions

## Next Development Priorities

1. **Analytics Dashboard** (High Priority)
   - Visual data representation
   - Problem trend analysis
   - Export functionality

2. **Mobile Optimization** (High Priority)
   - Touch-friendly interface
   - Offline capability
   - Performance optimization

3. **Automation Features** (Medium Priority)
   - QR code generation
   - Social media integration
   - Email campaigns

4. **Advanced Analytics** (Medium Priority)
   - Machine learning insights
   - Predictive analysis
   - Custom reporting

## Maintenance and Updates

**Regular Tasks:**
- Monitor response quality and completion rates
- Update questions based on feedback
- Backup data regularly
- Update dependencies and security patches

**Scaling Considerations:**
- Move to database if JSON files become too large
- Add caching for better performance
- Implement user authentication if needed
- Add API rate limiting for public access

---

**Current Status: Phase 1 Complete - Ready for Testing and Phase 2 Development**

## Phase 3: Automation & Distribution (Usage Guide)

### Configure Public URL
- Deploy `web/` to a static host (Netlify, Vercel, GitHub Pages) and copy your public URL to the survey (e.g., https://yourdomain/web/index.html).
- Update configs:
  - `config/social_config.json` → set `questionnaire_url` to your public URL
  - `config/sharing_config.json` → set `questionnaire_url` to your public URL

### Generate QR Codes
- Install dependencies once: `pip install -r requirements.txt`
- Generate contextual QR codes:
  - `python src/qr_generator.py --url https://yourdomain/web/index.html --context all`
- Generate UTM-tracked QR for a campaign:
  - `python src/qr_generator.py --url https://yourdomain/web/index.html --utm-source=instagram --utm-medium=story --utm-campaign=launch_week`
- Output PNG files are saved in `qr_codes/`.

### Social Media Automation
- Generate daily posts with UTM links:
  - `python src/social_automation.py --generate`
- Create a weekly schedule JSON:
  - `python src/social_automation.py --schedule`
- Generate community-specific posts for Reddit/LinkedIn groups:
  - `python src/social_automation.py --communities`
- Outputs are saved in `generated_content/` for manual posting or import into schedulers.

### Email/Sharing Kit
- Generate a complete sharing kit (templates + links):
  - `python src/sharing_utilities.py --generate`
- Print a sharing guide:
  - `python src/sharing_utilities.py --guide`
- Create a specific email campaign draft:
  - `python src/sharing_utilities.py --email intro`

### Website Embedding
- Use `web/embed.html` as the iframe source for third-party sites.
- Example snippet:
  - `<iframe src="https://yourdomain/web/embed.html" width="100%" height="900" style="border:0;" allowfullscreen></iframe>`
- The survey auto-resizes via postMessage to fit content.

### Quick Verification Checklist
1. Open `web/index.html`, submit a response without errors.
2. Open `web/dashboard.html` → click "Load from this browser" → confirm charts render.
3. Run `python src/questionnaire_engine.py --export csv` → confirm CSV file created and fields present.
4. Upload the JSON export in the dashboard → confirm charts reflect exported data.
5. Run `python src/qr_generator.py --url https://yourdomain/web/index.html --context all` → confirm PNGs in `qr_codes/`.
6. Run `python src/social_automation.py --generate` → confirm JSON posts in `generated_content/`.

### Deployment Notes
- Netlify: drag-drop `web/` folder or link repo; ensure paths are relative.
- Vercel: import project and set root to `web/` for the static site.
- GitHub Pages: serve from `/web` directory in your repository settings.
- After deployment, update both config files with the live URL and re-generate QR codes and posts.

## Live Deployment (Netlify)

- Live survey URL: https://moonlit-crostata-3f8b85.netlify.app/
- Embed URL: https://moonlit-crostata-3f8b85.netlify.app/embed.html
- Dashboard link: open the live survey and click “View Analytics Dashboard”

### Generated Assets (for Sharing/Scheduling)
- QR codes: `problem_identification_tool/qr_codes/`
  - `qr_business_card.png`, `qr_poster.png`, `qr_social_media.png`, `qr_email_signature.png`, `qr_event.png`
- Social posts (daily): `problem_identification_tool/generated_content/generated_posts.json`
- Weekly schedule: `problem_identification_tool/generated_content/weekly_schedule_YYYYMMDD.json`
- Community posts: `problem_identification_tool/generated_content/community_posts.json`

### After Deployment - Configs in Use
- `config/social_config.json`: questionnaire_url → https://moonlit-crostata-3f8b85.netlify.app/
- `config/sharing_config.json`: questionnaire_url → https://moonlit-crostata-3f8b85.netlify.app/

### Quick Manual Verification (Live)
1. Open the survey and submit a response without errors.
2. Click “View Analytics Dashboard”, then “Load from this browser” → charts should populate.
3. Test UTM link: append `?utm_source=instagram&utm_medium=story&utm_campaign=launch` to the URL and load.
4. Test embed: place this snippet on any HTML page and confirm auto‑resize:
   - `<iframe src="https://moonlit-crostata-3f8b85.netlify.app/embed.html" width="100%" height="900" style="border:0;" allowfullscreen></iframe>`
