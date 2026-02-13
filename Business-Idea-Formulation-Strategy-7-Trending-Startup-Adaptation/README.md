# Business Idea Formulation Strategy 7: Trending Startup Adaptation

## Overview
This strategy helps you generate business ideas by adapting *trending startup profiles* from Crunchbase for implementation in Nigeria, while **differentiating** the ideas by combining them with other niches or concepts.

## Manual Approach

### Step 1: Access Trending Profiles on Crunchbase
- Go to `https://www.crunchbase.com/`
- Use **Ctrl + F** and search for **"Trending Profiles"**
- Scroll to the **Trending Profiles** section
- Take a clear **screenshot** of the section (showing multiple startups)

### Step 2: Prepare the Screenshot for ChatGPT
- Ensure the screenshot clearly shows:
  - Startup names
  - Short descriptions / tags / industries (as visible)
- If needed, crop the screenshot to focus on the relevant content

### Step 3: Open ChatGPT (Vision Enabled)
- Use a ChatGPT model that supports **images (Vision)**
- Start a new chat

### Step 4: Use Prompt 1a
- Upload the **Trending Profiles screenshot**
- Use this prompt (or your variant):

> **Prompt 1a:**  
> “Give me ideas based on this to implement in Nigeria. Your ideas should be differentiated from the ideas present in the image by combining with a different niche or concept (these different niches do not compulsorily have to be present in the image) in order to generate new startup ideas).”

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

### Using `steps.py`

Run the Python script to guide and partially automate this process:

```bash
python steps.py
```

The script will:
1. **Automated**: Remind you of the exact steps to capture **Trending Profiles** on Crunchbase.  
2. **User Input**: Ask you to confirm when the screenshot has been captured.  
3. **Automated**: Generate a **ready-to-copy Prompt 1a** for ChatGPT Vision.  
4. **User Input**: Let you paste/enter the **viable ideas** returned from Prompt 1a.  
5. **Automated**: Generate **Prompt 1b blocks** for each selected idea (saved in a text file).  
6. **Automated**: Save a JSON log of all ideas and prompts for future reference.

You still manually:
- Capture the screenshot in Crunchbase,
- Upload it to ChatGPT,
- Paste generated ideas back into the script when asked.

## Expected Output

After completing this strategy, you should have:
- A list of **trending global startup concepts** from Crunchbase.
- A set of **localized, differentiated ideas** tailored for Nigeria.
- Detailed **Prompt 1b tables** for your top ideas (problems, solutions, costs, monetization, risks, etc.).
- A shortlist of **2–5 high-potential startups** for deeper research and validation.

## Tips for Success

- **Aim for differentiation**: Don’t just copy trending startups—add a new niche or twist.  
- **Think “Nigeria-first”**: Always ask, “How does this work in the Nigerian context?”  
- **Focus on execution feasibility**: Some ideas may be great globally but too complex locally.  
- **Reuse this monthly**: Trending Profiles change; re-run the process to keep your pipeline fresh.  
- **Track everything**: Keep a central file or sheet of all ideas and their status (researching, validating, parked, etc.).

---

**Remember to use voice typing via AnyDesk for more efficient communication - it's more efficient than Google Docs' voice typing tool and eliminates the need for copying and pasting into IDE text fields.**



