# Strategy 15: Nigeria National / Open Data (Data-First)

## Core strategy

Generate business ideas from **Nigeria-sourced or Nigeria-filtered official and open statistical inputs** as the **primary** artifact. Each derived problem or idea should be traceable to **indicator (or metric)**, **period**, and **source** where possible. This strategy does **not** use news headlines as the main input.

## Data-use ethics boundary

Use only **public, aggregated, non-personal** data releases from official publishers (including **CBN** statistical publications when you use them). Do not use Strategy 15 to infer or track identifiable individuals; keep analysis at sector, category, channel, or macro/market trend level.

**Note:** The runnable script’s **numbered portal menu** is a curated shortcut list (NBS eLibrary, Microdata, Open Data for Africa). **CBN, ministries, and other agencies** remain valid sources whenever you supply their **URL, excerpt, or file**—they are omitted from that menu by design, not by rule.

## How this differs from nearby strategies

| Strategy | Primary input |
|----------|----------------|
| **5** — News-Based Problem Extraction | Nigerian **news** content |
| **14** — Global Data Trend Adaptation | **OurWorldInData** (global) → adapt to Nigeria |
| **15** — This strategy | **Nigeria** national / official / open **statistics** (or Nigeria-filtered series) first |

## Process

### Step 1: Choose inputs (data-first)

Use **national or official** sources and **open data** where available. Examples of categories (verify current URLs and catalogs yourself):

- **Default portal shortcuts** (in `portal_menu.py`): NBS **eLibrary** (reports), NBS **Microdata** catalog, **Open Data for Africa** (Nigeria + Nigeria foreign trade subdomain)—used by the interactive runner’s Step 1 menu
- **National Bureau of Statistics (NBS)** — surveys, bulletins, GDP, labour, prices, demographics (beyond those entry points when needed)
- **Central Bank of Nigeria (CBN)** — monetary and financial statistics; use via **direct report URL**, download, or paste—not required to appear on the portal menu
- **Federal Ministry sources** and sector agencies (education, health, agriculture, trade, etc.) as published
- **Other Nigeria open data portals** when accessible
- **Multilateral tables with Nigeria rows** only as supporting context — the **lead** story should still be Nigeria-specific tables or extracts, not a global dashboard as the main paste

Prefer **machine-readable** (CSV, Excel, API) when available; **PDFs and tables in reports** are valid — see “Handling messy data” below.

### Step 2: Record provenance before prompting

For each dataset or table you use, write down (you will reuse these in Prompt 1b):

- **Statistical indicator (or metric)** — what exactly is measured and the unit if applicable
- **Period** — as published (e.g. Q1 2024, FY 2023, 2018–2022 average)
- **Source** — publishing organization + **direct link** or **file name** (e.g. “NBS, Labour Force Statistics, March 2024, PDF p.12”)

### Step 3: Prompt 1a

Use the text in **`chatgpt_prompt_1a.txt`** in this folder in the same chat session. Paste **statistical content** (short excerpts, key figures, or your summary table — keep length reasonable for model context).

### Step 4: Prompt 1b (after ideas look viable)

Use **`chatgpt_prompt_1b.txt`** in this folder. Request the **standard table** with **lead provenance columns** first, then the same wide analysis columns used in Strategies 5 and 14 (including **Proposed domain (not verified)**).

## Handling messy data (required honesty)

- **Gaps:** If a series is missing years or discontinuous, say so in **Gaps / limitations**; do not interpolate without labeling it as an estimate.
- **PDFs:** Cite **document title, publisher, date, page or table id**; note if figures were hand-copied.
- **Revisions:** If a figure was revised in a later release, prefer the **latest** official number and mention the revision briefly in gaps.
- **Irregular releases:** Use the **latest available period** and state the **reference date** of the publication.
- **Lags:** Official data often lags reality; state that limitation when inferring “current” opportunities.

## Output format (Prompt 1b)

**Lead columns (provenance — repeat or key each row to these):**

| Statistical indicator (or metric) | Period (as published) | Source (organization + URL or file name) | Gaps / limitations (optional) |

**Then** the same wide columns as Strategy 5 / 14 (Prompt 1b style), including:

| Proposed domain (not verified) | Problem Identified | Potential Digital Solution | Estimated daily sales | Actualization strategy | Target Audience | Problem it solves | Competition Analysis | Estimated Costs (in dollars) | Funding Sources (provide links to possible investors and VCs) | No-code Tools to build solution | How to test the viability of the idea | Potential Challenges | Solution to those potential challenges | Landing page platform | Monetization Strategy | Market Size and Growth Potential | Technical Expertise and Skill Requirements | Partnerships and Collaboration | Timeline | Key Performance Indicators (KPIs) | Team Requirements | Time to Market | Required Skills | Risks and Mitigation | Scalability | Social Impact |
|---------------|-------------------|---------------------------|---------------------|----------------------|----------------|-------------------|---------------------|----------------------------|------------------------------------------------------------|--------------------------------|-----------------------------------|-------------------|-----------------------------------|---------------------|---------------------|--------------------------------|----------------------------------------|----------------------------|---------|--------------------------------|------------------|---------------|---------------|-------------------|------------|--------------|

**Column note:** In **Proposed domain (not verified)**, use TBD or illustrative placeholders (e.g. `productname.ng`) unless verified live.

## Key advantage

Ideas are anchored to **documented national or official statistics**, improving auditability and reducing headline noise — while still allowing human judgment on what the numbers imply for opportunities.

---

**Remember to use voice typing via AnyDesk for more efficient communication — it is more efficient than Google Docs' voice typing tool and eliminates the need for copying and pasting into IDE text fields.**
