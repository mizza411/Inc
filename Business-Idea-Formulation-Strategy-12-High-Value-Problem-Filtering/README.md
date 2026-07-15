# Business Idea Formulation Strategy 12: High-Value Problem Filtering

## Overview
This strategy filters a list of problems down to the **highest-value opportunities** by checking whether they are **growing, urgent, expensive to solve, mandatory, and frequent** (**GUEMF**).

**Authoritative backlog:** `.cursor/rules/task.md` Current Priority **§13** + Notes **§13** (GUEMF dual-mode).

---

## Dual-mode contract (Mode A + Mode B)

Strategy 12 has **two** jobs. Both are required in multi-strategy **agent** runs. Standalone CLI / `run_all_strategies.py` focus on scoring & ranking (and, after Phase 1, non-interactive inputs); Mode A **discovery** in agent runs uses Prompt 1a-style synthesis when the script is interactive-only.

| Mode | Name | What it does | Where ideas appear |
|------|------|--------------|--------------------|
| **A** | Standalone GUEMF discovery | Find problems that are Growing, Urgent, Expensive to solve, Mandatory, and Frequent (Prompt **1a**-style), then turn strong ones into Nigeria-focused business ideas | Same `business_ideas_YYYYMMDD.md` ranked table / details; **primary strategy trace includes `S12`** (or starts with S12) |
| **B** | Overlay scoring | Apply GUEMF scores to ideas that originated from **other** strategies (1, 5, 6, 7, 9, 11, 13, 14, 15, …) | Ranked table columns `GUEMF (G/U/E/M/F)` + composite; idea detail may note filter via S12 |

**Not optional in agent runs:** doing only Mode B (scoring sticker) without Mode A (S12-origin ideas) is an incomplete Strategy 12 pass.

**Execution summary (agent):** Strategy 12 status must note **both** legs, e.g. Mode A `synthesized`/`ran` + Mode B applied — not only “Applied in ranked table.”

### Scale mapping (CLI vs agent)

| Surface | Per-criterion | Aggregate | High-value heuristic |
|---------|---------------|-----------|----------------------|
| **Interactive CLI today** (`problem_filter.py`) | Y/N → **0 or 1** | Sum **0–5** | Prefer ≥ **4/5** for Prompt 1b selection |
| **Agent markdown / Docx** (recent runs) | **1–5** each (G/U/E/M/F) | Composite sum **max 25** | Rank / Best ideas by composite + judgment |

**Mapping when bridging CLI → agent (document only until Phase 1 codes it):**

- CLI `0` → treat as weak → agent band **1–2**
- CLI `1` → treat as strong → agent band **4–5**
- Prefer recording explicit 1–5 in agent outputs; do not invent fake “precision” from a yes/no bit

Playbook also allows a 0–2 manual scale; agent runs standardize on **1–5**.

### Explicitly not this strategy

- Strategy 6 niche combination alone, Strategy 7 trending adaptation alone, or Strategy 1 business+complaint variation — those remain their own traces; Mode B may still **score** their ideas.

---

## Manual Approach

### Step 1: Gather a Problem List
- Collect problems from:
    - Other strategies (news, Strategy 14 / OurWorldInData, StartupList / Product Hunt, Crunchbase optional legacy, personal problems, etc.)
    - **Mode A:** GUEMF Prompt 1a discovery (problems that already meet the five criteria)
    - Existing notes, spreadsheets, or idea backlogs
- For each problem, keep at least:
  - Short description
  - Source (e.g. Strategy 5, 6, 11, **12-Prompt1a**, etc.)

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
- Agent outputs: prefer **1–5** per criterion (see scale mapping above).

### Step 3: Calculate a High-Value Score
- For each problem, sum the scores across the 5 criteria.
- Example (0–1 scale):  
  - Growing: 1, Urgent: 1, Expensive: 1, Mandatory: 0, Frequent: 1 → **Score = 4/5**
- Mark problems with scores **≥ 4/5** (or **≥ 7/10** for 0–2 scale) as **high-value**.

### Step 4: Use Prompt 1a to Discover More High-Value Problems
You can also ask ChatGPT (or the Cursor agent) directly:

> **Prompt 1a:**  
> “Find problems that are growing, urgent, expensive to solve, mandatory, and frequent. Give me business ideas based on problems that meet these criteria.”

This is the core of **Mode A**. Use it to **augment** lists that only came from other strategies.

### Step 5: Use Prompt 1b for Top Problems
For the **top-scoring problems**, run Prompt 1b (same as other strategies):

> “Tabulate output for ‘[paste high-value problem or idea]’ (Columns: Problem Identified/Potential Digital Solution/Estimated daily sales/ Actualization strategy, Target Audience, Problem it solves, Competition Analysis, Estimated Costs (in dollars), Funding Sources (provide links to possible investors and VCs), No-code Tools to build solution, How to test the viability of the idea, Potential Challenges, Solution to those potential challenges, landing page platform, Monetization Strategy, Market Size and Growth Potential, Technical Expertise and Skill Requirements, Partnerships and Collaboration, Timeline, Key Performance Indicators (KPIs), Team Requirements, Time to Market, Required Skills, Risks and Mitigation, Scalability, Social Impact).”

### Step 6: Final Selection
- From the high-value, fully-tabulated problems, select:
  - 1–3 **primary focus problems** to build around.
  - A few **secondary problems** you may tackle later.

## Script-Based Approach

### Using `problem_filter.py`

**Interactive (default)** — humans / `run_all_strategies.py` menu (unchanged):

```bash
cd Business-Idea-Formulation-Strategy-12-High-Value-Problem-Filtering
python problem_filter.py
```

**Non-interactive (Phase 1)** — CI / agent wrappers; **no** `input()`; requires complete `criteria_scores` in JSON:

```bash
python problem_filter.py --non-interactive --inputs fixtures/sample_inputs.json
```

Optional: `--output path.json`, `--select-min-score 4`, `--open` (auto-open summary; off by default in non-interactive).

Schema: [`fixtures/INPUTS_SCHEMA.md`](./fixtures/INPUTS_SCHEMA.md).  
Scoring helpers (pure): `guemf_scoring.py`.  
Smoke: `python -m pytest test_strategy12_noninteractive.py -q`

Also launched as Strategy **12** from repo-root `run_all_strategies.py` (same script; menu still starts **interactive** default).

The **interactive** script will:
1. **User Input**: Let you enter problems manually (or paste from other sources), including optional source tags.  
2. **User Input**: For each problem, answer Yes/No for: Growing, Urgent, Expensive, Mandatory, Frequent.  
3. **Automated**: Calculate a **High-Value Score** (0–5) for each problem.  
4. **Automated**: Sort and display the problems by score, highlighting the strongest ones.  
5. **User Input**: Let you choose which top problems to send to ChatGPT.  
6. **Automated**: Generate Prompt 1b-style text blocks for each chosen problem and save them to a `.txt` file.  
7. **Automated**: Save everything (problems + scores + selections) in a JSON file for future use.

You still manually (interactive path):
- Paste the generated prompts into ChatGPT (or synthesize in Cursor).
- Interpret the tables and decide what to pursue.

**Phase 2 (planned):** agent prompt dual-mode (Mode A discovery + Mode B overlay) — see `task.md` §13.

## Expected Output

After completing this strategy, you should have:
- A **ranked list of problems** with clear high-value scores.  
- A small number of **top problems** ready for deeper analysis (Prompt 1b tables).  
- A JSON record of your filtered problem set that other strategies can reuse.
- In **agent** multi-strategy packs: Mode A ideas (S12-traced) **and** Mode B GUEMF columns on the full ranked set.

## Tips for Success

- **Be strict**: Don’t force problems into “high-value” if they don’t truly match the criteria.  
- **Reuse across strategies**: Re-run Mode B whenever you generate a new batch of problems (from Strategies 1, 5–7, 9, 11, 13–15).  
- **Track decisions**: Note why you picked or rejected each high-value problem (skills, timing, capital, etc.).  
- **Update over time**: A problem that’s “medium” today might become “high” later (e.g. due to regulation or economic changes).
- **Agent dual-mode**: Never treat “GUEMF columns filled” as complete Strategy 12 without Mode A ideas.

---

## Phase 0 artifacts

- **Contract:** this README section (**Dual-mode contract**).
- **Inventory + acceptance checklist for Phases 1–4:** [`PHASE0_INVENTORY_AND_ACCEPTANCE.md`](./PHASE0_INVENTORY_AND_ACCEPTANCE.md).
- **Manual / sign-off:** [`MANUAL_TEST.md`](./MANUAL_TEST.md) — **no user steps** for dual-mode Phases 0–3; run `python test_strategy12_regression.py`.

---

**Remember to use voice typing via AnyDesk for more efficient communication - it's more efficient than Google Docs' voice typing tool and eliminates the need for copying and pasting into IDE text fields.**
