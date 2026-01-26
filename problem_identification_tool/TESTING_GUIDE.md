# Testing Guide for Problem Identification Tool

**Complete testing guide covering local testing and GitHub Pages deployment testing.**

## Testing Overview

Test your tool in two phases:
1. **Local Testing** - Test on your computer before deploying
2. **GitHub Pages Testing** - Test the live deployed site (includes setup, functionality tests, Netlify comparison, and troubleshooting)

**What's Included**:
- ✅ Local testing (8 detailed tests)
- ✅ GitHub Pages setup and deployment testing (11 detailed tests)
- ✅ Netlify vs GitHub Pages comparison
- ✅ Troubleshooting for both local and deployment issues
- ✅ Performance and security testing
- ✅ Complete testing checklists

---

## Phase 1: Local Testing (Before Deployment)

### Quick Local Test

> **Why this still matters after GitHub Pages is live**  
> Your production site runs at: `https://mizza411.github.io/Inc/problem_identification_tool/web/`.  
> Local testing at `http://localhost:8000/problem_identification_tool/web/` is still recommended for **development** so you can try changes safely before pushing to GitHub.  
> If you ever choose not to use localhost, you don’t need to delete or change any project files — you would simply skip these local‑testing steps.

#### Option 1: Python HTTP Server (Recommended)

1. **Open terminal in the project root**:
   ```bash
   cd "C:\Users\'Sanmi\Downloads\coding projects\Inc"
   ```

2. **Start a local server**:
   ```bash
   # Python 3
   python -m http.server 8000
   
   # Or if you have Python 2
   python -m SimpleHTTPServer 8000
   ```

3. **Open in browser**:
   - Go to: `http://localhost:8000/problem_identification_tool/web/`
   - Or: `http://localhost:8000/problem_identification_tool/web/index.html`

4. **Stop the server**: Press `Ctrl+C` in the terminal

#### Option 2: VS Code Live Server Extension

1. Install "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"
4. Browser opens automatically

#### Option 3: Direct File Open (Limited)

1. Navigate to `problem_identification_tool/web/`
2. Double-click `index.html`
3. **Note**: Some features may not work (like fetch requests) due to browser security

---

## What to Test

### ✅ Test 1: Questionnaire Loading

**Steps**:
1. Open the questionnaire page
2. Check that questions appear
3. Verify progress bar shows

**Expected Result**:
- Questions load from `data/questionnaires.json` or fallback questions
- Progress bar is visible
- No console errors (press F12 to check)

**If it fails**:
- Check browser console (F12) for errors
- Verify `web/data/questionnaires.json` exists
- Check that JavaScript files load correctly

---

### ✅ Test 2: Question Navigation

**Steps**:
1. Answer the first question
2. Click "Next"
3. Answer the second question
4. Click "Previous" to go back
5. Continue through all questions

**Expected Result**:
- Can navigate forward and backward
- Previous button appears after first question
- "Next" button changes to "Complete Survey" on last question
- Progress bar updates correctly

**If it fails**:
- Check browser console for JavaScript errors
- Verify `questionnaire.js` is loaded
- Check that question IDs match

---

### ✅ Test 3: Response Submission

**Steps**:
1. Complete all questions
2. Click "Complete Survey"
3. Check browser console (F12 → Console tab)
4. Check browser localStorage (F12 → Application → Local Storage)

**Expected Result**:
- Success message appears: "✅ Thank You!"
- Response saved to localStorage
- Console shows: "Response saved to server successfully" or "Server not available, using localStorage fallback"
- localStorage contains `questionnaire_responses` key

**How to Check localStorage**:
1. Press F12
2. Go to **Application** tab (Chrome) or **Storage** tab (Firefox)
3. Expand **Local Storage**
4. Click on your site URL
5. Look for `questionnaire_responses` key
6. Click it to see the saved response

**If it fails**:
- Check browser console for errors
- Verify localStorage is enabled (not in private/incognito mode)
- Check that all required questions are answered

---

### ✅ Test 4: Dashboard Loading

**Steps**:
1. Open dashboard: `http://localhost:8000/problem_identification_tool/web/dashboard.html`
2. Click "Load from this browser"
3. Check that charts appear

**Expected Result**:
- Dashboard loads without errors
- "Load from this browser" button works
- Charts display (if you have responses in localStorage)
- Metrics show correct numbers

**If it fails**:
- Make sure you have responses in localStorage (complete questionnaire first)
- Check browser console for errors
- Verify Chart.js library loads (check Network tab)

---

### ✅ Test 5: Dashboard Export Upload

**Steps**:
1. Generate an export locally:
   ```bash
   python problem_identification_tool/src/questionnaire_engine.py --export json
   ```
2. Open dashboard
3. Click "Upload export JSON"
4. Select the generated JSON file
5. Check that charts update

**Expected Result**:
- File upload works
- Charts update with exported data
- Metrics show correct totals

**If it fails**:
- Check that JSON file is valid
- Verify file structure matches expected format
- Check browser console for errors

---

### ✅ Test 6: Embed Page

**Steps**:
1. Open embed page: `http://localhost:8000/problem_identification_tool/web/embed.html`
2. Check that iframe loads
3. Complete questionnaire in the iframe
4. Check that it resizes correctly

**Expected Result**:
- Iframe loads the questionnaire
- Can interact with questionnaire inside iframe
- Page resizes to fit content
- No console errors

**If it fails**:
- Check that `index.html` loads in iframe
- Verify postMessage communication works
- Check browser console for iframe errors

---

### ✅ Test 7: Mobile Responsiveness

**Steps**:
1. Open questionnaire in browser
2. Press F12 → Toggle device toolbar (or Ctrl+Shift+M)
3. Test on different screen sizes:
   - Mobile (375px)
   - Tablet (768px)
   - Desktop (1920px)
4. Test touch interactions

**Expected Result**:
- Layout adapts to screen size
- Buttons are touch-friendly
- Text is readable
- No horizontal scrolling

**If it fails**:
- Check CSS media queries
- Verify viewport meta tag in HTML
- Test on actual mobile device

---

### ✅ Test 8: Offline Functionality

**Steps**:
1. Complete questionnaire while online
2. Disconnect internet
3. Try to complete another questionnaire
4. Check that responses still save

**Expected Result**:
- Questionnaire works offline
- Responses save to localStorage
- No network errors (since it uses localStorage)

**If it fails**:
- Check that no external resources are required
- Verify all assets are local

---

## Phase 2: GitHub Pages Testing (After Deployment)

This section helps you test that GitHub Pages works correctly as a replacement for Netlify.

---

### Step 1: Enable GitHub Pages

#### Quick Setup

1. **Go to your repository on GitHub**:
   ```
   https://github.com/YOUR_USERNAME/Inc
   ```

2. **Navigate to Settings**:
   - Click **Settings** tab (top menu bar)

3. **Go to Pages**:
   - Scroll down left sidebar
   - Click **Pages**

4. **Configure Build and deployment**:
   - Find the **"Build and deployment"** section
   - Under **"Source"** dropdown, select: **Deploy from a branch**
   - Select **Branch**: `main` (or `master` if that's your default branch)
   - Select **Folder**: `/` (root)
   - Click **Save**

   **Note**: You'll also see a **"Visibility"** section on this 
   page. This is about making your site private (requires GitHub 
   Enterprise). For a public repository, your site will be 
   **public by default** — you can safely ignore this section 
   for basic setup.

   **After clicking "Save", you'll see additional sections:**

   - **"Custom domain"** section: This allows you to use your own domain name (e.g., `example.com`) instead of `YOUR_USERNAME.github.io`. **You can ignore this** — the default GitHub Pages URL works perfectly fine. Only configure this if you want to use a custom domain you own.

   - **"Enforce HTTPS"** section: This will show a checked checkbox. **This is already enabled by default** and is good for security — it ensures your site is only accessible via HTTPS (encrypted connection). **You don't need to do anything here** — it's already set up correctly.

   - **"Verified domains"** section: You can ignore this — it's related to custom domain verification.

   - **"Visibility"** section: This is about making your site private (requires GitHub Enterprise). For a public repository, your site will be **public by default** — you don't need to do anything here. This section can be safely ignored for basic setup.

   **Summary**: All these sections can be safely ignored for basic setup. Your site will deploy with HTTPS enabled automatically.

5. **Wait for Deployment**:
   - Open the **Actions** tab and look for a workflow called **"pages build and deployment"** on the `main` branch.
   - Wait for it to complete with a **green checkmark ✅**.
   - This green checkmark means your site is live, even if GitHub’s wording/UI does not literally say "Your site is ready to be published at..." (GitHub sometimes changes the exact text or shows the URL in a different place on the Pages settings screen).

---

### Step 2: Get Your GitHub Pages URL

After enabling, your site will be live at:

```
https://YOUR_USERNAME.github.io/Inc/problem_identification_tool/web/
```

**Note**: Replace `YOUR_USERNAME` with your actual GitHub username.

**Examples**:
- If your username is `johnsmith`  
  URL will be: `https://johnsmith.github.io/Inc/problem_identification_tool/web/`
- For your current setup (`mizza411`):  
  - **Main questionnaire**: `https://mizza411.github.io/Inc/problem_identification_tool/web/`  
  - **Dashboard**: `https://mizza411.github.io/Inc/problem_identification_tool/web/dashboard.html`  
  - **Embed page**: `https://mizza411.github.io/Inc/problem_identification_tool/web/embed.html`

---

### Step 3: Test Basic Access

#### ✅ Test 9: Site Loads (No 404)

**Action**:
1. Open your GitHub Pages URL in a browser
2. Check if the page loads

**Expected Result**:
- ✅ Page loads (not 404 error)
- ✅ Questionnaire appears
- ✅ No "Page not found" message

**If it fails**:
- Wait 2-3 more minutes (first deployment takes time)
- Check Settings → Pages is enabled
- Verify folder path is `/problem_identification_tool/web`
- Check Actions tab for deployment errors

---

#### ✅ Test 10: HTTPS Works

**Action**:
1. Check the URL bar
2. Look for lock icon 🔒

**Expected Result**:
- ✅ URL starts with `https://`
- ✅ Green lock icon (secure connection)
- ✅ No "Not Secure" warning

**If it fails**:
- GitHub Pages always uses HTTPS
- If you see HTTP, you're on the wrong URL
- Clear browser cache and try again

---

#### ✅ Test 11: All Pages Accessible

**Test these URLs**:

1. **Main Questionnaire**:
   ```
   https://YOUR_USERNAME.github.io/Inc/problem_identification_tool/web/
   ```
   - Should load the questionnaire

2. **Dashboard**:
   ```
   https://YOUR_USERNAME.github.io/Inc/problem_identification_tool/web/dashboard.html
   ```
   - Should load the analytics dashboard

3. **Embed Page**:
   ```
   https://YOUR_USERNAME.github.io/Inc/problem_identification_tool/web/embed.html
   ```
   - Should load the embed version

**Expected Result**:
- ✅ All three pages load without 404 errors
- ✅ Each page displays correctly

**If it fails**:
- Check that all files exist in `web/` folder
- Verify file names are correct (case-sensitive)
- Check browser console (F12) for errors

---

### Step 4: Test Functionality

#### ✅ Test 12: Questionnaire Works

**Action**:
1. Open the main questionnaire URL
2. Complete all questions
3. Submit the survey

**Expected Result**:
- ✅ Questions load correctly
- ✅ Can navigate through questions
- ✅ Can submit responses
- ✅ Success message appears
- ✅ Response saves to localStorage

**Check localStorage**:
1. Press F12 (DevTools)
2. Go to **Application** tab → **Local Storage**
3. Click your site URL
4. Look for `questionnaire_responses` key
5. Should contain your response

**If it fails**:
- Check browser console (F12) for JavaScript errors
- Verify `questionnaire.js` loads (Network tab)
- Check that `questionnaires.json` loads from `./data/`

---

#### ✅ Test 13: Dashboard Works

**Action**:
1. Open dashboard URL
2. Click "Load from this browser"
3. Check that charts appear

**Expected Result**:
- ✅ Dashboard loads
- ✅ "Load from this browser" button works
- ✅ Charts display (if you have responses)
- ✅ Metrics show correct numbers

**If it fails**:
- Complete questionnaire first (to have data)
- Check browser console for errors
- Verify Chart.js library loads (Network tab)

---

### Where You See Results (After a User Submits)

Once a user completes the questionnaire on GitHub Pages:

- **Primary place to view results (recommended)**  
  - Open the **dashboard** page:  
    - Example for your setup:  
      - `https://mizza411.github.io/Inc/problem_identification_tool/web/dashboard.html`  
  - Use one of these options:  
    - Click **"Load from this browser"** → reads all responses stored in that browser’s `localStorage`.  
    - Click **"Upload export JSON"** → upload an exported responses file (from `questionnaire_engine.py`) to see aggregated charts.

- **Where the raw data is actually stored**  
  - Each browser stores answers in **`localStorage`** under the key **`questionnaire_responses`**.  
  - To inspect it manually (advanced):  
    - Press `F12` → **Application** (Chrome) or **Storage** (Firefox).  
    - Expand **Local Storage** → select your GitHub Pages URL.  
    - View the `questionnaire_responses` entry to see the saved JSON.

Use the dashboard for normal analysis; only open `localStorage` directly if you need to debug or export raw data.

---

#### ✅ Test 14: Embed Page Works

**Action**:
1. Open embed page URL
2. Check that iframe loads questionnaire
3. Try completing questionnaire in iframe

**Expected Result**:
- ✅ Iframe loads questionnaire
- ✅ Can interact with questionnaire
- ✅ Page resizes to fit content
- ✅ No console errors

**If it fails**:
- Check browser console for iframe errors
- Verify `index.html` loads in iframe
- Check postMessage communication works

---

### Step 5: Test Updates (Deployment Pipeline)

#### ✅ Test 15: Automatic Updates Work

**Action**:
1. Make a small change to `web/index.html`
   - Example: Change the title text
2. Commit and push:
   ```bash
   git add problem_identification_tool/web/index.html
   git commit -m "Test GitHub Pages update"
   git push origin main
   ```
3. Wait 1-2 minutes
4. Refresh your GitHub Pages URL
5. Check if change appears

**Expected Result**:
- ✅ Change appears on live site
- ✅ Updates automatically (no manual deploy needed)
- ✅ Takes 1-2 minutes to update

**Check Deployment Status**:
1. Go to **Actions** tab in your repository
2. Look for "pages build and deployment" workflow
3. Green checkmark ✅ = successful
4. Red X ❌ = failed (check logs)

**If it fails**:
- Check Actions tab for errors
- Verify you pushed to `main` branch
- Wait a few more minutes
- Hard refresh: `Ctrl+Shift+R`

---

### Step 6: Compare with Netlify

#### What Should Work the Same

| Feature | Netlify | GitHub Pages | Status |
|---------|---------|--------------|--------|
| Static hosting | ✅ | ✅ | Should work |
| HTTPS | ✅ | ✅ | Should work |
| Custom domain | ✅ | ✅ | Should work |
| Auto-deploy on push | ✅ | ✅ | Should work |
| CDN | ✅ | ✅ | Should work |

#### What's Different

| Feature | Netlify | GitHub Pages | Notes |
|---------|---------|--------------|-------|
| Serverless functions | ✅ | ❌ | Not needed - uses localStorage |
| Netlify Blobs | ✅ | ❌ | Not needed - uses localStorage |
| Build process | Optional | Optional | Both work with static files |
| Deployment time | ~30s | ~1-2min | GitHub Pages slightly slower |

**Key Point**: Your tool doesn't need serverless functions - it uses localStorage, so GitHub Pages works perfectly!

---

### Step 7: Test from Different Devices

#### ✅ Test 16: Mobile Device

**Action**:
1. Open GitHub Pages URL on your phone
2. Complete questionnaire
3. Check dashboard

**Expected Result**:
- ✅ Site loads on mobile
- ✅ Touch interactions work
- ✅ Layout is responsive
- ✅ All features work

**If it fails**:
- Check viewport meta tag
- Test responsive CSS
- Check mobile browser console

---

#### ✅ Test 17: Different Browsers

**Test on**:
- Chrome/Edge
- Firefox
- Safari (if available)

**Expected Result**:
- ✅ Works consistently across browsers
- ✅ No browser-specific errors

---

### Step 8: Performance Testing

#### ✅ Test 18: Load Speed

**Action**:
1. Open GitHub Pages URL
2. Press F12 → **Network** tab
3. Reload page
4. Check load times

**Expected Result**:
- ✅ Page loads in < 3 seconds
- ✅ All assets load successfully
- ✅ No failed requests (red in Network tab)

**If it's slow**:
- Check file sizes (should be small)
- Verify CDN is working
- Check Network tab for slow requests

---

### Step 9: Verify No Netlify Dependencies

#### ✅ Test 19: No Netlify Function Calls

**Action**:
1. Open questionnaire
2. Complete and submit
3. Open browser console (F12)
4. Check for Netlify-related errors

**Expected Result**:
- ✅ No errors about `/.netlify/functions/`
- ✅ Response saves to localStorage
- ✅ Console shows: "Server not available, using localStorage fallback" (this is OK!)

**Note**: The code tries Netlify functions first, then falls back to localStorage. This is fine - localStorage is the primary storage method.

---

## Testing Checklist

### Before Deployment
- [ ] Questionnaire loads locally
- [ ] Can navigate through questions
- [ ] Responses save to localStorage
- [ ] Dashboard loads from localStorage
- [ ] Export upload works
- [ ] Embed page works
- [ ] Mobile responsive
- [ ] Works offline

### After Deployment (GitHub Pages)
- [ ] GitHub Pages enabled in Settings
- [ ] Site loads at GitHub Pages URL (no 404)
- [ ] HTTPS works (green lock icon)
- [ ] Main questionnaire page works
- [ ] Dashboard page works
- [ ] Embed page works
- [ ] Can submit responses
- [ ] Responses save to localStorage
- [ ] Dashboard loads from localStorage
- [ ] Updates automatically on git push
- [ ] Works on mobile device
- [ ] Works in different browsers
- [ ] Load speed is acceptable (< 3 seconds)
- [ ] No critical console errors
- [ ] No Netlify dependencies (uses localStorage)
- [ ] QR codes point to correct URL
- [ ] Social posts have correct URL

---

## Quick Test Commands

### Start Local Server
```bash
# From project root
python -m http.server 8000
```

### Open in Browser
```bash
# Windows PowerShell
start http://localhost:8000/problem_identification_tool/web/

# Or manually navigate to:
# http://localhost:8000/problem_identification_tool/web/index.html
```

### Check localStorage
1. Open browser DevTools (F12)
2. Go to Application tab (Chrome) or Storage tab (Firefox)
3. Expand Local Storage
4. Click your site URL
5. View `questionnaire_responses` key

### Generate Test Export
```bash
python problem_identification_tool/src/questionnaire_engine.py --export json
```

---

## Common Issues & Solutions

### Issue: Questions Don't Load

**Check**:
1. Browser console for errors
2. Network tab - is `questionnaires.json` loading?
3. File exists at `web/data/questionnaires.json`

**Solution**:
- Verify file path is correct
- Check JSON syntax is valid
- Fallback questions should still work

### Issue: Responses Don't Save

**Check**:
1. Browser console for errors
2. localStorage is enabled (not private mode)
3. Browser allows localStorage

**Solution**:
- Try different browser
- Check browser settings
- Verify JavaScript is enabled

### Issue: Dashboard Shows No Data

**Check**:
1. Do you have responses in localStorage?
2. Did you click "Load from this browser"?
3. Browser console for errors

**Solution**:
- Complete questionnaire first
- Then load dashboard
- Or upload exported JSON file

### Issue: Charts Don't Display

**Check**:
1. Is Chart.js library loading? (Network tab)
2. Browser console for errors
3. Do you have data to display?

**Solution**:
- Check internet connection (Chart.js loads from CDN)
- Verify data exists
- Check Chart.js version compatibility

---

## Automated Testing (Optional)

### Browser Console Tests

Open browser console (F12) and run:

```javascript
// Test localStorage
localStorage.setItem('test', 'value');
console.log(localStorage.getItem('test')); // Should show "value"

// Test questionnaire engine
const engine = new QuestionnaireEngine();
console.log(engine); // Should show object

// Check if Chart.js loaded
console.log(typeof Chart); // Should show "function"
```

---

## Performance Testing

### Check Load Times
1. Open DevTools (F12)
2. Go to Network tab
3. Reload page
4. Check load times:
   - **Good**: < 2 seconds
   - **Acceptable**: 2-5 seconds
   - **Slow**: > 5 seconds

### Check File Sizes
- HTML: Should be < 50KB
- JavaScript: Should be < 100KB each
- Total page load: Should be < 500KB

---

## Security Testing

### Check HTTPS (on live site)
- URL should start with `https://`
- Green lock icon in browser
- No mixed content warnings

### Check Privacy
- No personal data collected
- localStorage only (client-side)
- No external tracking (unless you added it)

---

## Troubleshooting GitHub Pages

### Issue: 404 Error

**Check**:
1. Settings → Pages is enabled
2. Folder path is `/problem_identification_tool/web`
3. Branch is `main` (or `master`)
4. Wait 2-3 minutes for first deployment

**Solution**:
- Verify all settings
- Check Actions tab for deployment status
- Try accessing URL again after waiting

---

### Issue: Changes Not Showing

**Check**:
1. Did you push to `main` branch?
2. Check Actions tab - is deployment successful?
3. Wait 1-2 minutes after push

**Solution**:
- Verify git push was successful
- Check Actions tab for errors
- Hard refresh: `Ctrl+Shift+R`
- Try incognito mode

---

### Issue: Assets Not Loading

**Check**:
1. Browser console (F12) for 404 errors
2. Network tab - which files fail to load?
3. File paths are relative (not absolute)

**Solution**:
- Verify all file paths start with `./` or `../`
- Check file names are correct (case-sensitive)
- Ensure files exist in `web/` folder

---

### Issue: Deployment Fails

**Check**:
1. Actions tab - what's the error?
2. Repository settings - any restrictions?
3. File structure - is it correct?

**Solution**:
- Read error message in Actions tab
- Verify folder structure matches
- Check GitHub Pages documentation
- Try redeploying

---

## Quick Test Commands for GitHub Pages

### Open GitHub Pages URL
```bash
# Windows PowerShell
start https://YOUR_USERNAME.github.io/Inc/problem_identification_tool/web/

# Replace YOUR_USERNAME with your actual username
```

### Check Deployment Status
1. Go to: `https://github.com/YOUR_USERNAME/Inc/actions`
2. Look for "pages build and deployment"
3. Check if it's successful (green ✅) or failed (red ❌)

### Test All Pages
```bash
# Main page
start https://YOUR_USERNAME.github.io/Inc/problem_identification_tool/web/

# Dashboard
start https://YOUR_USERNAME.github.io/Inc/problem_identification_tool/web/dashboard.html

# Embed
start https://YOUR_USERNAME.github.io/Inc/problem_identification_tool/web/embed.html
```

---

## Success Criteria

GitHub Pages is working correctly if:

✅ **Site is accessible** - No 404 errors  
✅ **HTTPS works** - Secure connection  
✅ **All features work** - Questionnaire, dashboard, embed  
✅ **Updates automatically** - Changes appear after git push  
✅ **Performance is good** - Loads quickly  
✅ **Works everywhere** - Mobile, desktop, all browsers  

---

## Comparison: Netlify vs GitHub Pages

| Aspect | Netlify | GitHub Pages | Winner |
|--------|---------|--------------|--------|
| **Ease of Setup** | Easy | Easy | Tie |
| **Cost** | Free | Free | Tie |
| **Deployment Speed** | ~30s | ~1-2min | Netlify |
| **Serverless Functions** | ✅ | ❌ | Netlify (but you don't need it!) |
| **Custom Domain** | ✅ | ✅ | Tie |
| **HTTPS** | ✅ | ✅ | Tie |
| **CDN** | ✅ | ✅ | Tie |
| **Git Integration** | ✅ | ✅ | Tie |
| **Documentation** | Good | Excellent | GitHub Pages |
| **Reliability** | Good | Excellent | GitHub Pages |

**For your use case**: GitHub Pages is perfect because you don't need serverless functions - localStorage handles everything!

---

## How to Share Your Questionnaire (Distribution Guide)

Now that your site is live on GitHub Pages, here's how to share it with people so they can access it from anywhere.

### Your Live URLs

**Main Questionnaire (share this one!):**
```
https://mizza411.github.io/Inc/problem_identification_tool/web/
```

**Dashboard (for viewing results):**
```
https://mizza411.github.io/Inc/problem_identification_tool/web/dashboard.html
```

**Embed Page (for iframes):**
```
https://mizza411.github.io/Inc/problem_identification_tool/web/embed.html
```

---

## 🚀 Quick Start: Share Right Now (No Commands Needed!)

**Just want to share online? Here's all you need:**

1. **Copy this URL:**
   ```
   https://mizza411.github.io/Inc/problem_identification_tool/web/
   ```

2. **Paste it anywhere:**
   - **Social media** (Twitter, Facebook, LinkedIn, Instagram): Just paste the URL in your post
   - **Email**: Paste the URL in your email
   - **WhatsApp/Telegram**: Send the link directly
   - **Text message**: Send via SMS
   - **Website**: Add it as a link on your website

**That's it!** People can click the link and access your questionnaire from anywhere.

**Example post:**
> "Help us understand community challenges! Take our quick survey: https://mizza411.github.io/Inc/problem_identification_tool/web/"

---

## 📱 Advanced Sharing Options (Optional - Only If You Want Extra Features)

The methods below are **optional** and only needed if you want:
- QR codes for physical/digital sharing
- Pre-written social media post templates
- Email campaign templates
- Tracking which sharing method works best

**If you just want to share the URL online, you're done!** Skip to the bottom of this section.

---

### Method 1: Direct Link Sharing (Already Covered Above)

This is the simplest method - just copy and paste the URL. No commands needed!

---

### Method 2: Generate QR Codes (Optional - For Physical/Digital Sharing)

**When to use:** If you want QR codes for posters, flyers, business cards, or digital displays.

QR codes let people scan and access your questionnaire instantly (great for physical locations, posters, flyers).

**Generate QR codes:**

```bash
# From project root directory
python problem_identification_tool/src/qr_generator.py --url https://mizza411.github.io/Inc/problem_identification_tool/web/ --context all
```

**Generate QR with tracking (UTM parameters):**
```bash
# For Instagram campaign
python problem_identification_tool/src/qr_generator.py --url https://mizza411.github.io/Inc/problem_identification_tool/web/ --utm-source=instagram --utm-medium=story --utm-campaign=launch_week

# For physical posters
python problem_identification_tool/src/qr_generator.py --url https://mizza411.github.io/Inc/problem_identification_tool/web/ --utm-source=poster --utm-medium=print --utm-campaign=community_outreach
```

**QR codes are saved in:** `problem_identification_tool/qr_codes/` (PNG files)

**Use QR codes:**
- Print on posters, flyers, business cards
- Share digitally in social media posts
- Display on screens at events
- Include in presentations

---

### Method 3: Social Media Sharing (Optional - For Pre-Written Posts)

**When to use:** If you want pre-written social media post templates with tracking.

**Generate social media posts:**

```bash
# Generate daily posts with UTM tracking
python problem_identification_tool/src/social_automation.py --generate

# Create weekly schedule
python problem_identification_tool/src/social_automation.py --schedule

# Generate community-specific posts
python problem_identification_tool/src/social_automation.py --communities
```

**Outputs saved in:** `problem_identification_tool/generated_content/`

**Pre-made sharing links:**

- **Facebook**: `https://www.facebook.com/sharer/sharer.php?u=https://mizza411.github.io/Inc/problem_identification_tool/web/`
- **Twitter**: `https://twitter.com/intent/tweet?url=https://mizza411.github.io/Inc/problem_identification_tool/web/&text=Help us understand community challenges - take our quick survey!`
- **LinkedIn**: `https://www.linkedin.com/sharing/share-offsite/?url=https://mizza411.github.io/Inc/problem_identification_tool/web/`
- **WhatsApp**: `https://wa.me/?text=Help us understand community challenges - take our quick survey! https://mizza411.github.io/Inc/problem_identification_tool/web/`
- **Telegram**: `https://t.me/share/url?url=https://mizza411.github.io/Inc/problem_identification_tool/web/&text=Help us understand community challenges - take our quick survey!`

---

### Method 4: Email Campaigns (Optional - For Email Templates)

**When to use:** If you want pre-written email templates with subject lines and body text.

**Generate email templates:**

```bash
# Generate complete sharing kit (includes email templates)
python problem_identification_tool/src/sharing_utilities.py --generate

# Generate specific email campaign
python problem_identification_tool/src/sharing_utilities.py --email intro
python problem_identification_tool/src/sharing_utilities.py --email reminder
python problem_identification_tool/src/sharing_utilities.py --email thank_you
```

**Email templates include:**
- Subject lines
- Body text with your questionnaire URL
- Call-to-action buttons
- Ready to copy-paste into your email client

**Outputs saved in:** `problem_identification_tool/generated_content/`

---

### Method 5: Embed on Websites (Optional - For Website Integration)

**When to use:** If you want to embed the questionnaire directly into your website or blog.

Embed the questionnaire directly into your website or blog.

**Embed code:**
```html
<iframe
  src="https://mizza411.github.io/Inc/problem_identification_tool/web/embed.html"
  width="100%"
  height="900"
  style="border:0;"
  allowfullscreen>
</iframe>
```

**How to use:**
1. Copy the iframe code above
2. Paste it into your website's HTML (WordPress, Wix, Squarespace, custom HTML)
3. The questionnaire will appear embedded on your page
4. It automatically resizes to fit content

---

### Method 6: Generate Complete Sharing Kit (Optional - For Everything at Once)

**When to use:** If you want all sharing assets (QR codes, social posts, email templates) generated at once.

Get everything in one go:

```bash
# Generate complete sharing kit (QR codes, social posts, email templates, links)
python problem_identification_tool/src/sharing_utilities.py --generate
```

This creates a JSON file with:
- All sharing links (Facebook, Twitter, LinkedIn, WhatsApp, etc.)
- Email campaign templates
- Social media post templates
- QR code generation instructions

**Output saved in:** `problem_identification_tool/generated_content/sharing_kit_[timestamp].json`

---

### Quick Sharing Checklist

**For Simple Online Sharing:**
- [x] ✅ Config files updated with GitHub Pages URL (already done)
- [ ] Copy the URL: `https://mizza411.github.io/Inc/problem_identification_tool/web/`
- [ ] Share it on social media, email, WhatsApp, etc.
- [ ] **Done!** People can now access your questionnaire.

**Optional Advanced Features (Only If Needed):**
- [ ] Generate QR codes for physical/digital sharing (if you want QR codes)
- [ ] Generate social media posts (if you want pre-written templates)
- [ ] Generate email campaign templates (if you want email templates)
- [ ] Add embed code to your website (if you want to embed it)
- [ ] Print QR codes for physical locations (if you have physical materials)

---

### Tips for Maximum Reach

1. **Use UTM parameters** to track which sharing method works best
2. **Post at optimal times** (check your social media analytics)
3. **Share multiple times** - people miss posts, so repost weekly
4. **Engage with comments** - respond to questions about the survey
5. **Cross-promote** - mention the survey in other content
6. **Make it easy** - QR codes are faster than typing URLs

---

## Ready to Deploy?

Once all local tests pass:
1. ✅ Enable GitHub Pages (see Step 1 above)
2. ✅ Test live site (follow Phase 2 tests)
3. ✅ Update config files with GitHub Pages URL (already done)
4. ✅ Regenerate QR codes with new URL
5. ✅ Regenerate social posts with new URL
6. ✅ Share your URL!

---

**Need help? Check the troubleshooting sections above or see GITHUB_PAGES_GUIDE.md for more details.**

