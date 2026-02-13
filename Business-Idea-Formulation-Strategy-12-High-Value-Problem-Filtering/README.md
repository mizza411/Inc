# Business Idea Formulation Strategy 12: High-Value Problem Filtering

## Overview
This strategy filters a list of problems down to the **highest-value opportunities** by checking whether they are **growing, urgent, expensive to solve, mandatory, and frequent**.

## Manual Approach

### Step 1: Gather a Problem List
- Collect problems from:
  - Other strategies (news, TrendHunter, Crunchbase, personal problems, etc.)
  - Existing notes, spreadsheets, or idea backlogs
- For each problem, keep at least:
  - Short description
  - Source (e.g. Strategy 5, 6, 11, etc.)

### Step 2: Score Each Problem Against the 5 Criteria
For each problem, ask:

1. **Growing** – Is the problem becoming more common or severe?
2. **Urgent** – Do people need to solve it immediately or soon?
3. **Expensive to Solve** – Does solving it currently cost significant money?
4. **Mandatory** – Is it something people/businesses MUST solve (not optional)?
5. **Frequent** – Does it happen repeatedly (daily/weekly/monthly)?

You can use a simple scoring:
- Yes = 1, No = 0  
- Or 0–2 scale per criterion (0 = No, 1 = Maybe, 2 = Strong Yes).

### Step 3: Calculate a High-Value Score
- For each problem, sum the scores across the 5 criteria.
- Example (0–1 scale):  
  - Growing: 1, Urgent: 1, Expensive: 1, Mandatory: 0, Frequent: 1 → **Score = 4/5**
- Mark problems with scores **≥ 4/5** (or **≥ 7/10** for 0–2 scale) as **high-value**.

### Step 4: Use Prompt 1a to Discover More High-Value Problems
You can also ask ChatGPT directly:

> **Prompt 1a:**  
> “Find problems that are growing, urgent, expensive to solve, mandatory, and frequent. Give me business ideas based on problems that meet these criteria.”

Use this to **augment** your manually collected list with additional examples.

### Step 5: Use Prompt 1b for Top Problems
For the **top-scoring problems**, run Prompt 1b (same as other strategies):

> “Tabulate output for ‘[paste high-value problem or idea]’ (Columns: Problem Identified/Potential Digital Solution/Estimated daily sales/ Actualization strategy, Target Audience, Problem it solves, Competition Analysis, Estimated Costs (in dollars), Funding Sources (provide links to possible investors and VCs), No-code Tools to build solution, How to test the viability of the idea, Potential Challenges, Solution to those potential challenges, landing page platform, Monetization Strategy, Market Size and Growth Potential, Technical Expertise and Skill Requirements, Partnerships and Collaboration, Timeline, Key Performance Indicators (KPIs), Team Requirements, Time to Market, Required Skills, Risks and Mitigation, Scalability, Social Impact).”

### Step 6: Final Selection
- From the high-value, fully-tabulated problems, select:
  - 1–3 **primary focus problems** to build around.
  - A few **secondary problems** you may tackle later.

## Script-Based Approach

### Using `steps.py`

Run the Python script to filter problems programmatically:

```bash
python steps.py
```

The script will:
1. **User Input**: Let you enter problems manually (or paste from other sources), including optional source tags.  
2. **User Input**: For each problem, answer Yes/No for: Growing, Urgent, Expensive, Mandatory, Frequent.  
3. **Automated**: Calculate a **High-Value Score** (0–5) for each problem.  
4. **Automated**: Sort and display the problems by score, highlighting the strongest ones.  
5. **User Input**: Let you choose which top problems to send to ChatGPT.  
6. **Automated**: Generate Prompt 1b-style text blocks for each chosen problem and save them to a `.txt` file.  
7. **Automated**: Save everything (problems + scores + selections) in a JSON file for future use.

You still manually:
- Paste the generated prompts into ChatGPT.
- Interpret the tables and decide what to pursue.

## Expected Output

After completing this strategy, you should have:
- A **ranked list of problems** with clear high-value scores.  
- A small number of **top problems** ready for deeper analysis (Prompt 1b tables).  
- A JSON record of your filtered problem set that other strategies can reuse.

## Tips for Success

- **Be strict**: Don’t force problems into “high-value” if they don’t truly match the criteria.  
- **Reuse across strategies**: Re-run this whenever you generate a new batch of problems (from Strategies 3–11).  
- **Track decisions**: Note why you picked or rejected each high-value problem (skills, timing, capital, etc.).  
- **Update over time**: A problem that’s “medium” today might become “high” later (e.g. due to regulation or economic changes).

---

**Remember to use voice typing via AnyDesk for more efficient communication - it's more efficient than Google Docs' voice typing tool and eliminates the need for copying and pasting into IDE text fields.**



