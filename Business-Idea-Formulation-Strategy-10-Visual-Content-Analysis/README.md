# Business Idea Formulation Strategy 10: Visual Content Analysis

> **Deprecated (June 2026):** Strategy 10 is **retired** from `run_all_strategies.py`. ChatGPT Vision has no in-repo automation path (manual image upload / paste only). Use **[Strategy 3](../Business-Idea-Formulation-Strategy-3-Network-Based-Problem-Identification/)** (network), **[Strategy 4](../Business-Idea-Formulation-Strategy-4-Business-Owner-Problem-Collection/)** (questionnaires), or **[Strategy 5](../Business-Idea-Formulation-Strategy-5-News-Based-Problem-Extraction/)** (news) for problem discovery instead. See **[DEPRECATED.md](./DEPRECATED.md)**. Legacy script: `_archive/visual_content_analyzer_legacy.py`.

## Overview
This strategy helps you generate **business and IT solutions** by analyzing **visual content** (e.g. real estate projects, uncompleted buildings, infrastructure) using **ChatGPT Vision**, and then expanding viable ideas into full business tables.

## Manual Approach

### Step 1: Choose a Visual Target
- Select a visual asset you want to analyze, for example:
  - Photo of an **uncompleted building**
  - Photo of a **completed real estate project**
  - Visuals of **commercial complexes, malls, estates, office parks**
  - [Example: Instagram real estate project photo](https://www.instagram.com/p/C3AAn0XIYqx/?igsh=ZTZjb2kyOGt4NGQw)

### Step 2: Capture or Download the Image
- Ensure the image is **clear** and **shows context** (surroundings, signage, state of completion).
- Save it locally (e.g. `real_estate_project_01.jpg`).

### Step 3: Open ChatGPT (Vision Enabled)
- Use a ChatGPT model that supports **image input (Vision)**.
- Start a new conversation and upload the image.

### Step 4: Choose a Prompt Variant (1a)
Use one (or all) of these variants for **Prompt 1a**:

1. **Standard Prompt**  
   > “Give me business ideas/solutions that can be proposed to the architects or the builders of this uncompleted building [or project].”

2. **IT Solutions Variant**  
   > “Give me business ideas/IT solutions that can be proposed to the architects or the builders of this project.”

3. **Sales Expediting Variant**  
   > “Give me business ideas/IT solutions that can be proposed to the architects or the builders of this project to expedite the sales of the project.”

### Step 5: Review the Generated Ideas
- Read through all suggested ideas.
- Highlight the ideas that:
  - Are technically feasible for you.
  - Offer **clear value** to architects/builders/developers.
  - Address **sales, marketing, operations, or maintenance** pain points.

### Step 6: Use Prompt 1b (For Viable Ideas)
For each **viable idea** from Prompt 1a, run **Prompt 1b** in the same chat:

> **Prompt 1b:**  
> “Tabulate output for ‘[paste viable idea Prompt 1a]’ (Columns: Problem Identified/Potential Digital Solution/Estimated daily sales/ Actualization strategy, Target Audience, Problem it solves, Competition Analysis, Estimated Costs (in dollars), Funding Sources (provide links to possible investors and VCs), No-code Tools to build solution, How to test the viability of the idea, Potential Challenges, Solution to those potential challenges, landing page platform, Monetization Strategy, Market Size and Growth Potential, Technical Expertise and Skill Requirements, Partnerships and Collaboration, Timeline, Key Performance Indicators (KPIs), Team Requirements, Time to Market, Required Skills, Risks and Mitigation, Scalability, Social Impact).”

### Step 7: Store and Prioritize
- Copy each table into your **idea database** (spreadsheet or markdown).
- Tag each row with:
  - **Image name / location**
  - **Idea category** (sales, operations, IT, etc.)
  - **Priority** (High/Medium/Low)
- Select **2–5 strongest ideas** for follow-up research.

## Script-Based Approach

### Using `steps.py`

Run the Python script to guide the process and generate prompts:

```bash
python steps.py
```

The script will:
1. **User Input**: Ask you to describe or name the **image/project** you’re using.  
2. **Automated**: Generate a **Prompt 1a variant file** (`chatgpt_strategy10_prompt_1a.txt`) with all three variants ready to copy.  
3. **User Input**: After you run one or more Prompt 1a variants in ChatGPT, you paste back the **best ideas** into the script.  
4. **Automated**: Generate **Prompt 1b blocks** (saved in `chatgpt_strategy10_prompt_1b.txt`) for each selected idea.  
5. **Automated**: Save a JSON summary of the session (image/project description + ideas) for your records.

You still manually:
- Upload the image to ChatGPT Vision and run Prompt 1a variants.
- Decide which ideas are worth deepening with Prompt 1b.

## Expected Output

After completing this strategy, you should have:
- A set of **image-driven business ideas** tied to specific projects/locations.  
- Detailed Prompt 1b tables for your strongest ideas.  
- A short list of **most attractive real-estate/construction opportunities** to explore further or pitch.

## Tips for Success

- **Use multiple images**: Try different angles, projects, or stages (uncompleted vs completed).  
- **Think in ecosystems**: Consider **buyers, tenants, agents, facility managers, financiers** as potential users.  
- **Re-run after changes**: If the project evolves (e.g. from uncompleted to near-completion), rerun the strategy with updated images.  
- **Cross-link with other strategies**: Feed top ideas into Strategies 12 & 13 for high-value filtering and multi-source validation.

---

**Remember to use voice typing via AnyDesk for more efficient communication - it's more efficient than Google Docs' voice typing tool and eliminates the need for copying and pasting into IDE text fields.**



