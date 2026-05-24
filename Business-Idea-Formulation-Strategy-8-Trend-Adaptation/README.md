# Business Idea Formulation Strategy 8: Trend Adaptation

> **Deprecated (May 2026):** Strategy 8 is **retired** from `run_all_strategies.py`. TrendHunter has no licensed automation path (manual paste / unofficial scraping only). Use **[Strategy 14: Global Data Trend Adaptation](../Business-Idea-Formulation-Strategy-14-Global-Data-Trend-Adaptation/)** (OurWorldInData) for global trend → Nigeria adaptation instead. See **[DEPRECATED.md](./DEPRECATED.md)**. Legacy script: `_archive/trend_adapter_legacy.py`.

## Overview
This strategy helps you generate business ideas by adapting **global trends from TrendHunter** for implementation in Nigeria, while differentiating your ideas by combining them with other niches or concepts.

## Manual Approach

### Step 1: Access TrendHunter
- Go to `https://www.trendhunter.com/`
- Focus on categories that can translate well to Nigeria:
  - Tech, Business, Social Good, Finance, Lifestyle, etc.

### Step 2: Collect Trend Content
- Open a relevant TrendHunter page (e.g. a category or specific trend collection)
- Press **Ctrl + A** to select all content on the page
- Press **Ctrl + C** to copy the content
- (Optional) Paste into a text editor and trim if it is extremely long

### Step 3: Open ChatGPT
- Open a standard ChatGPT chat (text only is fine here)
- Start a new conversation

### Step 4: Use Prompt 1a
- Paste the TrendHunter content into ChatGPT
- Use this prompt:

> **Prompt 1a:**  
> “Give me ideas based on this to implement in Nigeria. Your ideas should be differentiated from the ideas present in the image/content by combining with a different niche or concept.”

### Step 5: Review Generated Ideas
- Go through the list of ideas returned
- Highlight ideas that:
  - Clearly come from global trends
  - Have a realistic Nigerian application
  - Use interesting niche/industry combinations

### Step 6: Use Prompt 1b (For Viable Ideas)
- For each **viable idea**, use Prompt 1b in the same chat:

> **Prompt 1b:**  
> “Tabulate output for **‘[paste viable idea Prompt 1a]’** (Columns: Problem Identified/Potential Digital Solution/Estimated daily sales/ Actualization strategy, Target Audience, Problem it solves, Competition Analysis, Estimated Costs (in dollars), Funding Sources (provide links to possible investors and VCs), No-code Tools to build solution, How to test the viability of the idea, Potential Challenges, Solution to those challenges, landing page platform, Monetization Strategy, Market Size and Growth Potential, Technical Expertise and Skill Requirements, Partnerships and Collaboration, Timeline, Key Performance Indicators (KPIs), Team Requirements, Time to Market, Required Skills, Risks and Mitigation, Scalability, Social Impact).”

### Step 7: Prioritize and Store
- For each table:
  - Check viability, costs, monetization, and scalability
  - Mark each idea as **High / Medium / Low** priority
- Store all tables and priorities in a central file (spreadsheet or markdown).

## Script-Based Approach

### Using `steps.py`

Run the Python script to guide and partially automate this process:

```bash
python steps.py
```

The script will:
1. **Automated**: List recommended TrendHunter categories to explore.  
2. **User Input**: Ask you to paste TrendHunter content you’ve copied.  
3. **Automated**: Clean and (optionally) truncate the content for optimal ChatGPT performance.  
4. **Automated**: Generate a ready-to-copy **Prompt 1a** text file.  
5. **User Input**: After you run Prompt 1a, you paste the **viable ideas** back into the script.  
6. **Automated**: Generate **Prompt 1b** blocks for each selected idea and save them to a file.  
7. **Automated**: Save a JSON log of the run (content length, ideas, timestamps).

You still manually:
- Navigate TrendHunter and copy content.
- Run Prompt 1a and read ChatGPT’s initial idea list.
- Decide which ideas are “viable” and paste them into the script when prompted.

## Expected Output

After completing this strategy, you should have:
- A set of **trend-inspired ideas** adapted for Nigeria.  
- Fully detailed **Prompt 1b tables** for your strongest ideas.  
- A shortlist of **2–5 trend-based concepts** ready for deeper validation or prototyping.

## Tips for Success

- **Target high-signal trends**: Focus on categories where Nigeria is catching up (e.g., payments, creator economy, logistics, agriculture, health).  
- **Think localization first**: Ask, “What has to change in this trend for a Nigerian user?”  
- **Avoid copy-paste startups**: Always add a twist (local culture, regulation, infrastructure).  
- **Re-run regularly**: TrendHunter content changes over time; revisit this strategy monthly or quarterly.  
- **Cross-link with other strategies**: Feed promising TrendHunter ideas into Strategies 12 & 13 (high-value filtering + multi-source analysis).

---

**Remember to use voice typing via AnyDesk for more efficient communication - it's more efficient than Google Docs' voice typing tool and eliminates the need for copying and pasting into IDE text fields.**



