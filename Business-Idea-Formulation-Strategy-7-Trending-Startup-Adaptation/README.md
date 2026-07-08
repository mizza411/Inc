# Business Idea Formulation Strategy 7: Trending Startup Adaptation

## Overview
This strategy helps you generate business ideas by adapting *trending products/startups* for implementation in Nigeria, while **differentiating** the ideas by combining them with other niches or concepts.

**Primary source (2026-07):** [Product Hunt](https://www.producthunt.com/) RSS (`https://www.producthunt.com/feed`) — no screenshot required.  
**Secondary:** Techpoint Digest / YC company list (text).  
**Optional legacy:** Crunchbase “Trending Profiles” screenshot + ChatGPT Vision.

Agent runs also use `agent_strategy_run.py` → `strategy_7_trending` in fetch JSON.

## Manual Approach

### Step 1: Capture trending products (primary — Product Hunt)
- Open [Product Hunt](https://www.producthunt.com/) or use the feed: `https://www.producthunt.com/feed`
- Note 8–15 recent launches (name + one-line description)
- Optionally open Techpoint Africa for Nigeria-relevant launches

### Step 2 (optional legacy): Crunchbase Trending Profiles
- Go to `https://www.crunchbase.com/`
- Use **Ctrl + F** and search for **"Trending Profiles"**
- Take a clear **screenshot** of the section (only if you choose the legacy path)

### Step 3: Open ChatGPT
- Text path (recommended): paste Prompt 1a with your product list — Vision not required
- Legacy screenshot path: use a Vision-enabled model and upload the image

### Step 4: Use Prompt 1a
> **Prompt 1a:**  
> “Give me ideas based on this to implement in Nigeria. Your ideas should be differentiated from the ideas present in the source by combining with a different niche or concept (these different niches do not compulsorily have to be present in the source) in order to generate new startup ideas).”

### Step 5: Review Generated Ideas
- Read through the ideas ChatGPT returns
- Highlight the ones that:
  - Are feasible in Nigeria
  - Clearly differ from the original startups
  - Use **interesting niche combinations**

### Step 6: Use Prompt 1b (For Viable Ideas)
- For each **viable idea**, use Prompt 1b in the **same chat**:

> **Prompt 1b:**  
> “Tabulate output for **‘[paste viable idea Prompt 1a]’** (Columns: Problem Identified/Potential Digital Solution/Estimated daily sales/ Actualization strategy, Target Audience, Problem it solves, Competition Analysis, Estimated Costs (in dollars), Funding Sources (provide links to possible investors and VCs), No-code Tools to build solution, How to test the viability of the idea, Potential Challenges, Solution to those potential challenges, landing page platform, Monetization Strategy, Market Size and Growth Potential, Technical Expertise and Skill Requirements, Partnerships and Collaboration, Timeline, Key Performance Indicators (KPIs), Team Requirements, Time to Market, Required Skills, Risks and Mitigation, Scalability, Social Impact).”

### Step 7: Prioritize and Document
- For each table:
  - Check **market size**, **monetization**, **risks**, **scalability**
  - Decide if the idea is **High / Medium / Low priority**
- Store all results in a spreadsheet or markdown file for later comparison.

## Script-Based Approach

### Using `trending_startup_adapter.py`

```bash
cd Business-Idea-Formulation-Strategy-7-Trending-Startup-Adaptation
python trending_startup_adapter.py
```

The script will:
1. Ask you to choose: **(1) Product Hunt / text** (default) or **(2) Crunchbase screenshot** (legacy)
2. Fetch Product Hunt RSS when available, or guide Crunchbase capture
3. Generate **Prompt 1a** (text or Vision wording)
4. Let you enter viable ideas and generate **Prompt 1b** blocks + JSON log

## Expected Output

After completing this strategy, you should have:
- A list of **trending global product concepts** (Product Hunt or legacy Crunchbase).
- A set of **localized, differentiated ideas** tailored for Nigeria.
- Detailed **Prompt 1b tables** for your top ideas (problems, solutions, costs, monetization, risks, etc.).
- A shortlist of **2–5 high-potential startups** for deeper research and validation.

## Tips for Success

- **Aim for differentiation**: Don’t just copy trending products—add a new niche or twist.  
- **Think “Nigeria-first”**: Always ask, “How does this work in the Nigerian context?”  
- **Focus on execution feasibility**: Some ideas may be great globally but too complex locally.  
- **Reuse this monthly**: Trending lists change; re-run the process to keep your pipeline fresh.  
- **Track everything**: Keep a central file or sheet of all ideas and their status (researching, validating, parked, etc.).

## Resources

- [Product Hunt](https://www.producthunt.com/) ← **primary**
- [Product Hunt RSS](https://www.producthunt.com/feed)
- [Techpoint Africa](https://techpoint.africa/) ← secondary
- [Crunchbase](https://www.crunchbase.com/) ← optional legacy Trending Profiles

---

**Remember to use voice typing via AnyDesk for more efficient communication - it's more efficient than Google Docs' voice typing tool and eliminates the need for copying and pasting into IDE text fields.**
