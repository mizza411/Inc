# Nigeria telecom statistics — business ideas (Strategy 15)

**Provenance (auditable):**

| Field | Value |
|--------|--------|
| **Statistical indicator (or metric)** | Active voice subscriptions (national and per state); active internet subscriptions (national and per state); mobile number porting (port-in / port-out by operator), as in workbook |
| **Period (as published)** | Q3 2025; voice/internet tables titled “AS AT SEPTEMBER, 2025” on sheets **Q3 2025 VOICE** and **Q3 2025 INTERNET** |
| **Source (organization + URL or file name)** | National Bureau of Statistics / Nigerian statistical microdata portal — `microdata.nigerianstat.gov.ng`; local file **`Telecoms_Q3_2025.xlsx`** |
| **Gaps / limitations** | Payload text file embedded raw XLSX bytes in one run; working figures taken from **`_telecoms_q3_dump.txt`** / opened workbook. Units are subscription counts as published; sector labels (MTN, GLO, AIRTEL, EMTS, etc.) are as in the file. |

**Figures used from the open file (TOTAL rows, Q3 2025 sheets):**

- **Voice (national sub-total):** about **173,541,983** active voice subscriptions; comparison columns on the same row show about **+12.03%** year-on-year vs the **Q3 2024** column and about **+1.06%** quarter-on-quarter vs **Q2 2025** (sheet **Q3 2025 VOICE**).
- **Internet (national sub-total):** about **140,949,570** active internet subscriptions; about **+6.05%** YoY vs **Q3 2024** and about **−0.16%** QoQ vs **Q2 2025** (sheet **Q3 2025 INTERNET**).
- **Porting (Q3 2025):** port-in total **1,255** and port-out total **1,255** for the quarter; operator columns include MTN, GLO, AIRTEL, EMTS, VTEL (sheet **Q3 2025 Porting**).
- **Lagos (illustrative subnational):** Lagos row on **Q3 2025 VOICE** shows large operator-level counts and a sub-total column about **21.4 million** with positive YoY and QoQ on that row; **Q3 2025 INTERNET** Lagos row sub-total about **17.7 million** with near-flat YoY and slightly positive QoQ on the published comparison columns.

---

## Prompt 1a — Problem–opportunity hooks (digital)

1. **Signal:** National active **voice** subscriptions rebound sharply YoY in Q3 2025 (~**+12%** vs Q3 2024 on the TOTAL row). **Affected:** Businesses that depend on voice traffic (SMEs, logistics, field teams, contact centres). **Product angle:** A **voice-centric usage and spend analytics** dashboard (web/mobile) tied to retail GSM plans and workforce calling patterns.

2. **Signal:** **Internet** subscriptions grow YoY (~**+6%**) but are roughly flat QoQ (~**−0.16%**), suggesting a maturing mobile-data base with short-run plateau. **Affected:** ISPs, digital marketers, edtech, health-tech going beyond SMS. **Product angle:** A **data-plan ROI planner** that models uptake vs revenue for SMEs switching users from voice-led to data-led engagement.

3. **Signal:** **Voice QoQ ~+1%** nationally vs **internet QoQ ~flat**, so voice and data are on different short-run dynamics. **Affected:** Operators’ distribution partners and enterprise procurement. **Product angle:** **Dual-track forecasting** SaaS (voice vs data) for retailers stocking SIMs, routers, and bundled devices.

4. **Signal:** **Lagos** dominates state rows (multi-million subscriptions on both voice and internet sheets); concentration implies uneven infrastructure and demand. **Affected:** Retail chains, logistics hubs, metro advertisers. **Product angle:** **Subnational demand heatmaps** (state × operator) for outlet expansion and localised campaigns—sold as analytics subscription.

5. **Signal:** Market structure columns across sheets (**MTN, GLO, AIRTEL, EMTS**, plus fixed/other categories where published) support competitive benchmarking. **Affected:** Comparison sites, fintech airtime APIs, enterprise mobility teams. **Product angle:** **Operator mix benchmarking tool** for SMEs (“share of subscriptions by operator in my state vs national”).

6. **Signal:** **Porting** totals (**~1,255** port-in and **~1,255** port-out in Q3 2025) are tiny relative to national subscription bases—low churn mobility in portability terms for the quarter as recorded. **Affected:** CX teams, regulators’ transparency portals, telco partnerships. **Product angle:** **MNP transparency digest**—quarterly dashboards interpreting porting flows for analysts and consumer advocates (not for gaming rankings).

7. **Signal:** Official series are published as large spreadsheets with **YoY / QoQ** columns—high value but heavy for casual users. **Affected:** Researchers, startups, investors needing trusted series. **Product angle:** **CSV/API normalization layer** that tags NBS telecom tables with indicator, period, and column definitions for internal modelling.

8. **Signal:** Some states show **negative YoY** on voice rows while the **national** TOTAL shows strong positive YoY—divergence across states. **Affected:** Policy-facing NGOs, state ICT agencies, donors. **Product angle:** **State inclusion index** product combining voice/internet subscription growth ranks with open maps for targeting connectivity interventions.

---

## Idea 1 – Voice rebound analytics (national YoY ~+12%)

### Business Idea

- **Proposed domain (not verified):** voicepulse.ng (TBD)
- **Sector:** Telecom / Data & analytics
- **Business model type:** B2B SaaS (SMB tier + enterprise)
- **Stage:** Idea
- **Priority:** High
- **Signal from the data** (excerpt + **named file**): National TOTAL on sheet **Q3 2025 VOICE** shows active voice sub-total **~173.5m** with **~+12% YoY** vs the Q3 2024 comparison column—**both** dump excerpt and **`Telecoms_Q3_2025.xlsx`**.
- **Problem Identified:** Teams still optimise around data buzz while official stats show a strong **voice** recovery at national level—misalignment between planning and reported subscription dynamics.
- **Target Audience:** SME owners, logistics coordinators, sales managers using GSM voice heavily.
- **Problem it solves (max 1 sentence):** Aligns operational planning (staffing, calling budgets, SIM procurement) with **published** national voice growth.
- **Market Size and Growth Potential:** Large GSM retail and B2B voice user base in Nigeria; growth tied to credibility of ongoing NBS releases rather than speculative TAM.
- **Estimated daily sales** (range band): ₦15k–₦150k equivalent monthly recurring from SMB tiers (illustrative until validated).
- **Estimated Costs (USD)** (rough band): MVP **$3k–$12k** (single developer + cloud + design).
- **Funding Sources:** Lagos Angel Network; CcHub; personal runway; possible PTDF-adjacent innovation grants (verify eligibility).
- **Monetization Strategy:** Tiered SaaS; paid API for aggregated indices; optional consulting on interpreting official tables.
- **Timeline to MVP:** 3–5 months.
- **Regulatory / institutional obstacles (Nigeria-focused):** No claim of NBS endorsement; data redistribution must respect publisher terms; avoid misrepresenting microdata as real-time network KPIs.
- **Key Risks and Mitigation:** **Risk:** Users expect live CDR-level truth—**Mitigation:** Position as **statistics-aligned planning**, not carrier-grade analytics.

### Digital Solution

- **Potential Digital Solution:** Web app importing user-uploaded **NBS table snapshots** (same structure as workbook) and producing executive charts: national YoY/QoQ, user-selected state vs national.
- **No-code / low-code stack** (concrete example tools): Bubble or FlutterFlow frontend; Airtable or Supabase for config; Metabase for chart prototyping.
- **Landing page platform:** Framer or Carrd.
- **Actualization strategy** (max 2–3 sentences): Publish one **interpretation article** per NBS drop referencing exact sheet names and TOTAL rows. Offer a **free Lagos-only** view to drive signups.
- **Competition Analysis:** Generic BI tools lack Nigeria telecom column semantics; telco apps are customer-facing, not planning-from-open-stats.
- **How to test viability** (one concrete experiment): Recruit **10 logistics SMEs** to compare one quarter of internal airtime spend against **state row** trends from the official file.
- **Potential Challenges:** Users confused by YoY vs QoQ columns.
- **Solutions to those challenges:** Inline glossary matching **workbook headers** (Active Voice Q3 2024, YoY, QoQ).

### Hardware Solution

Not applicable — product is analytics SaaS grounded in published spreadsheets, not a handset or CPE requirement.

---

## Idea 2 – Data maturity planner (internet YoY ~+6%, QoQ ~flat)

### Business Idea

- **Proposed domain (not verified):** dataterminal.ng (TBD)
- **Sector:** Fintech-adjacent / SME SaaS
- **Business model type:** B2B SaaS
- **Stage:** Idea
- **Priority:** High
- **Signal from the data** (**named file**): Sheet **Q3 2025 INTERNET** TOTAL row ~**140.9m** subscriptions; **~+6.05% YoY** vs Q3 2024 column; **~−0.16% QoQ** vs Q2 2025—signals growing annual base but near-term plateau.
- **Problem Identified:** SMEs over-invest in “more data” campaigns when short-run **national** subscription growth is flat QoQ.
- **Target Audience:** Digital agencies, e-commerce SMEs, branch retailers bundling data SIMs.
- **Problem it solves (max 1 sentence):** Calibrates marketing and inventory to **official** internet subscription momentum by quarter.
- **Market Size and Growth Potential:** Broad SME digital economy; differentiation is methodology tied to NBS tables.
- **Estimated daily sales** (range band): ₦10k–₦80k illustrative MRR early stage.
- **Estimated Costs (USD)** (rough band): **$4k–$15k** MVP.
- **Funding Sources:** Micro VC; Founder Institute Nigeria network; revenue reinvestment.
- **Monetization Strategy:** SaaS tiers; paid quarterly **PDF brief** interpreting new workbook drops.
- **Timeline to MVP:** 4–6 months.
- **Regulatory / institutional obstacles (Nigeria-focused):** Clear sourcing of tables; NDPR-compliant handling of any client business data uploaded for modelling.
- **Key Risks and Mitigation:** **Risk:** Correlation vs causation with firm-level sales—**Mitigation:** Frame as **macro guardrail**, not a sales predictor.

### Digital Solution

- **Potential Digital Solution:** Scenario modeller: user inputs segment assumptions; app overlays **national internet YoY/QoQ** from pasted TOTAL rows.
- **No-code / low-code stack:** Glide or Retool + Google Sheets mirror of official TOTALs; optional Python backend later.
- **Landing page platform:** Webflow.
- **Actualization strategy:** Ship a **“QoQ flat callout”** widget bloggers can embed (attributed to NBS file name + period).
- **Competition Analysis:** Global telecom dashboards ignore Nigeria column layout; generic spreadsheet templates lack narrative.
- **How to test viability** (one concrete experiment): Run **A/B** pricing pages with vs without the official **−0.16% QoQ** stat cited (measure trust clicks).
- **Potential Challenges:** Users want forecasts beyond what open data allows.
- **Solutions to those challenges:** Lock outputs to **historical published comparisons** only; label extrapolation clearly as scenario.

### Hardware Solution

Not applicable — planning tool; no device is central to the value proposition.

---

## Idea 3 – Dual-track voice vs data forecaster

### Business Idea

- **Proposed domain (not verified):** twintrack.app (TBD)
- **Sector:** Telecom / Retail ops
- **Business model type:** B2B SaaS
- **Stage:** Idea
- **Priority:** Medium
- **Signal from the data** (**named file**): Same Q3 2025 sheets show **voice** national YoY strongly positive (~**+12%**) while **internet** YoY is moderate (~**+6%**) and QoQ nearly flat—**divergent short-run stories**.
- **Problem Identified:** Distributors stock bundles using a single “telecom growth” mental model.
- **Target Audience:** Airtime/data consolidators, handset retailers, corporate fleet buyers.
- **Problem it solves (max 1 sentence):** Separates **voice-led** and **data-led** planning using the same official workbook structure each quarter.
- **Market Size and Growth Potential:** Nationwide retail SIM/data channel; stickiness if updated every NBS release.
- **Estimated daily sales** (range band): ₦20k–₦120k illustrative wholesale-facing tier.
- **Estimated Costs (USD)** (rough band): **$5k–$18k**.
- **Funding Sources:** Angel; trade association pilots (ASCOMI-style associations—verify); strategic retailer prepayment.
- **Monetization Strategy:** Per-seat SaaS; bulk licence for distributor groups.
- **Timeline to MVP:** 3–4 months for spreadsheet-driven MVP.
- **Regulatory / institutional obstacles (Nigeria-focused):** Avoid implying regulatory filing status; optional collaboration with industry associations for distribution pilots only.
- **Key Risks and Mitigation:** **Risk:** Rapid revision of official tables—**Mitigation:** Versioned imports keyed to **file name + sheet**.

### Digital Solution

- **Potential Digital Solution:** Side-by-side charts: **VOICE sheet TOTAL row** vs **INTERNET sheet TOTAL row** for latest quarter with stored history from user-uploaded workbooks.
- **No-code / low-code stack:** Notion + embedded charts; evolve to React when usage grows.
- **Landing page platform:** Carrd.
- **Actualization strategy:** Offer **free CSV template** matching NBS column order to reduce onboarding friction.
- **Competition Analysis:** Excel power users can replicate; most SMBs will not—position as **time saved + explanation**.
- **How to test viability** (one concrete experiment): **Five distributor interviews** showing Q3 2025 voice vs internet TOTAL extracts only.
- **Potential Challenges:** Manual file uploads each quarter.
- **Solutions to those challenges:** Optional reminder calendar aligned to **NBS publication cadence** (user-maintained dates).

### Hardware Solution

Not applicable — software-only workflow.

---

## Idea 4 – Metro vs national retail heatmaps (Lagos concentration)

### Business Idea

- **Proposed domain (not verified):** metrogsm.ng (TBD)
- **Sector:** Civic tech / Retail analytics
- **Business model type:** Data/Analytics subscription
- **Stage:** Idea
- **Priority:** Medium
- **Signal from the data** (**named file**): **Lagos** rows on Q3 2025 voice and internet sheets carry **multi-million** subscription sub-totals (e.g. voice row ~**21.4m** sub-total column, internet ~**17.7m**) — extreme concentration vs smaller states on the same sheets.
- **Problem Identified:** Chain retailers lack cheap, trusted views of **operator × state** demand from official sources.
- **Target Audience:** Retail expansion leads, bank agency banking rollout planners, metro OOH advertisers.
- **Problem it solves (max 1 sentence):** Supports footprint decisions using **the same state rows** regulators publish, not anecdotal buzz.
- **Market Size and Growth Potential:** Mid-market chains and agencies; expansion possible to other sectors using NBS geographic splits.
- **Estimated daily sales** (range band): ₦25k–₦200k enterprise pilots (illustrative).
- **Estimated Costs (USD)** (rough band): **$8k–$25k** with mapping UX.
- **Funding Sources:** Enterprise pilots; analytics consulting cross-sell.
- **Monetization Strategy:** Seat-based; paid **state packs**.
- **Timeline to MVP:** 4–7 months.
- **Regulatory / institutional obstacles (Nigeria-focused):** Map boundaries must use open map layers; attribute NBS clearly.
- **Key Risks and Mitigation:** **Risk:** Misreading unit labels—**Mitigation:** Copy column headers verbatim from workbook into UI.

### Digital Solution

- **Potential Digital Solution:** Interactive map + table: user selects **voice or internet** sheet; shades states by **Sub Total** column; drill-down to operator columns (MTN, GLO, etc.).
- **No-code / low-code stack:** Mapbox or Leaflet + Papa Parse in a small React app.
- **Landing page platform:** Webflow.
- **Actualization strategy:** Publish **one static infographic** per release: “Lagos share of national voice/internet sub-totals” with cited rows.
- **Competition Analysis:** Private mobility panels are costly; open-stats route is cheaper but labour-intensive without tooling.
- **How to test viability** (one concrete experiment): **Paid discovery** workshop with one retail chain using Q3 2025 sheet only.
- **Potential Challenges:** Geospatial skill gap on buyer side.
- **Solutions to those challenges:** Default exports to **Excel-friendly tables** mirroring NBS layout.

### Hardware Solution

Not applicable — mapping and tables are software-delivered; no dedicated field hardware.

---

## Idea 5 – Operator mix benchmarking for SMEs

### Business Idea

- **Proposed domain (not verified):** opmix.ng (TBD)
- **Sector:** Telecom / Analytics
- **Business model type:** B2B SaaS + API
- **Stage:** Idea
- **Priority:** Medium
- **Signal from the data** (**named file**): Workbook consistently breaks out **MTN, GLO, AIRTEL, EMTS** (and other segments)—national TOTAL rows give operator-scale bases for ratio analysis.
- **Problem Identified:** SMEs guess competitor operator affinity; publishers already ship **structured** operator columns quarterly.
- **Target Audience:** Retailers, fintech airtime resellers, enterprise mobility buyers.
- **Problem it solves (max 1 sentence):** Turns official **operator columns** into simple share charts for a chosen state vs national TOTAL row.
- **Market Size and Growth Potential:** Large reseller ecosystem; API upside for embedded finance apps.
- **Estimated daily sales** (range band): ₦10k–₦100k illustrative blended API+SaaS.
- **Estimated Costs (USD)** (rough band): **$6k–$20k**.
- **Funding Sources:** API revenue; accelerator programmes (verify intake dates).
- **Monetization Strategy:** Freemium charts; paid API keys with rate limits.
- **Timeline to MVP:** 3–5 months.
- **Regulatory / institutional obstacles (Nigeria-focused):** Terms of use for derivative metrics—document as **unofficial index**, cite source file each response.
- **Key Risks and Mitigation:** **Risk:** Misuse for carrier valuation—**Mitigation:** Legal disclaimer; B2B positioning only.

### Digital Solution

- **Potential Digital Solution:** Upload latest workbook → compute operator shares for **TOTAL** and user state row; output PNG + JSON.
- **No-code / low-code stack:** Backend FastAPI microservice; frontend Next.js; Redis cache for parsed sheets.
- **Landing page platform:** Framer.
- **Actualization strategy:** Ship **Postman collection** with sample Q3 2025 parse output for developers.
- **Competition Analysis:** Scraped crowd estimates compete on freshness but lose auditability—**official workbook** anchor is the differentiator.
- **How to test viability** (one concrete experiment): Integrate with **one airtime reseller** dashboard using cached Q3 2025 parse only.
- **Potential Challenges:** Column shifts between workbook versions.
- **Solutions to those challenges:** Header fingerprinting + human confirmation UI when columns move.

### Hardware Solution

Not applicable — API/chart product.

---

## Idea 6 – MNP transparency digest (low porting vs massive bases)

### Business Idea

- **Proposed domain (not verified):** portdigest.ng (TBD)
- **Sector:** Civic tech / Telecom policy
- **Business model type:** B2B subscriptions + public freemium
- **Stage:** Idea
- **Priority:** Medium
- **Signal from the data** (**named file**): **Q3 2025 Porting** sheet shows **1,255** port-in total and **1,255** port-out total for the quarter—small relative to **140m+** internet and **170m+** voice subscription totals on Q3 2025 sheets.
- **Problem Identified:** Analysts and journalists lack a short, neutral narrative each quarter tying **porting** to **subscription scale**.
- **Target Audience:** Policy researchers, telecom reporters, consumer NGOs, investor relations teams.
- **Problem it solves (max 1 sentence):** Puts **porting counts** in context of national subscription bases from the **same publication cycle** (where sheets coexist in one file).
- **Market Size and Growth Potential:** Niche but high-trust; monetise via organisations, not ads alone.
- **Estimated daily sales** (range band): ₦5k–₦40k org subscriptions (illustrative).
- **Estimated Costs (USD)** (rough band): **$2k–$8k** for content-led MVP.
- **Funding Sources:** Media grants; institutional subscriptions; pro bono analyst time.
- **Monetization Strategy:** Paid **PDF + webinar** per release; team licences.
- **Timeline to MVP:** 2–3 months (content + simple site).
- **Regulatory / institutional obstacles (Nigeria-focused):** Neutral tone on carriers; avoid implying NCC endorsement without permission.
- **Key Risks and Mitigation:** **Risk:** Misinterpretation of porting definitions—**Mitigation:** Quote sheet titles and operator rows verbatim.

### Digital Solution

- **Potential Digital Solution:** Quarterly **brief** site: pulls numbers from user-supplied workbook excerpts—charts port-in/out by operator (**MTN, GLO, AIRTEL, EMTS, VTEL** as in Q3 2025 Porting) and juxtaposes **national subscription totals** from voice/internet sheets.
- **No-code / low-code stack:** Ghost or Substack for narrative; Observable Notebook for charts.
- **Landing page platform:** Carrd.
- **Actualization strategy:** Partner with **one university seminar** to validate readability of first brief.
- **Competition Analysis:** Occasional press articles lack consistent methodology—serialized **same-structure** briefs win trust.
- **How to test viability** (one concrete experiment): Publish **one free Q3 2025 brief**; measure institutional email signups **>100** as success threshold.
- **Potential Challenges:** Manual extraction labour.
- **Solutions to those challenges:** Semi-automated parser for Porting sheets only (narrow scope).

### Hardware Solution

Not applicable — research and publishing workflow.

---

## Idea 7 – NBS telecom table normaliser (audit-friendly CSV/API)

### Business Idea

- **Proposed domain (not verified):** nbstechtables.ng (TBD)
- **Sector:** Gov/data infrastructure (private tool)
- **Business model type:** B2B Data/Analytics
- **Stage:** Idea
- **Priority:** Medium
- **Signal from the data** (**named file** + **excerpt metadata**): Inputs bundle references **`Telecoms_Q3_2025.xlsx`** with multiple quarterly sheets—persistent **schema repetition** (states × operators × YoY/QoQ).
- **Problem Identified:** Teams repeatedly clean the same wide layouts for models; errors creep into YoY/QoQ alignment.
- **Target Audience:** Researchers, banks’ economists, startups building Nigeria dashboards.
- **Problem it solves (max 1 sentence):** Deterministic parsing to **long format** with preserved column lineage (sheet name, period, header text).
- **Market Size and Growth Potential:** Small addressable market but high willingness to pay for accuracy.
- **Estimated daily sales** (range band): USD **$100–$800**/month illustrative institutional tier.
- **Estimated Costs (USD)** (rough band): **$10k–$35k** engineering-heavy.
- **Funding Sources:** Pilot contracts; OSS sponsorship; academic licences.
- **Monetization Strategy:** Paid parser runs; on-prem licence for banks.
- **Timeline to MVP:** 5–8 months for robust testing across historical sheets if provided.
- **Regulatory / institutional obstacles (Nigeria-focused):** Redistribution rights of downloaded files—customer brings their own copy; tool processes locally.
- **Key Risks and Mitigation:** **Risk:** Publisher changes layout—**Mitigation:** Contract includes update SLA or community PR workflow.

### Digital Solution

- **Potential Digital Solution:** CLI + desktop Electron **local-first** parser that emits **tidy CSV** + manifest JSON (period, sheet, row hashes).
- **No-code / low-code stack:** Not applicable for core; use Python **pandas/openpyxl** with pytest golden files.
- **Landing page platform:** Simple static GitHub Pages.
- **Actualization strategy:** Publish **open test vectors** from **Q3 2025** TOTAL rows only (non-sensitive aggregates).
- **Competition Analysis:** Generic ETL ignores domain headers; bespoke beats manual cleaning after **two quarters** of use.
- **How to test viability** (one concrete experiment): **Blind test** against three analysts reconciling TOTAL rows—parser must match human consensus **100%**.
- **Potential Challenges:** Edge cells marked `'-'` or blanks as in dumps.
- **Solutions to those challenges:** Explicit **missing-value policy** in manifest.

### Hardware Solution

Not applicable — software parsing pipeline.

---

## Idea 8 – State inclusion index (divergent state YoY vs strong national voice YoY)

### Business Idea

- **Proposed domain (not verified):** statelines.ng (TBD)
- **Sector:** Civic tech / Development analytics
- **Business model type:** Data/Analytics + reports
- **Stage:** Idea
- **Priority:** Medium
- **Signal from the data** (**named file**): **Q3 2025 VOICE** TOTAL shows strong **national YoY** (~**+12%**) while several state rows in earlier quarters/sheets show **negative YoY** values—dispersion across states is visible in the dumped rows (e.g. various states with negative YoY percentages on voice rows).
- **Problem Identified:** Donors and state ICT departments need a repeatable **ranking** of inclusion outcomes grounded in official subscriptions, not anecdotes.
- **Target Audience:** State governments, NGOs, DFIs (where programmes align).
- **Problem it solves (max 1 sentence):** Highlights **which states lag** voice/internet growth vs national momentum using the same quarterly workbook.
- **Market Size and Growth Potential:** Grant-funded pilots; limited classic VC profile unless scaled across indicators beyond telecom.
- **Estimated daily sales** (range band): Project-based **$2k–$30k**/study (illustrative).
- **Estimated Costs (USD)** (rough band): **$7k–$22k** MVP with mapping.
- **Funding Sources:** Development grants; state innovation budgets.
- **Monetization Strategy:** Paid indices + workshops; **open methodology PDF**.
- **Timeline to MVP:** 5–7 months including ethical review template.
- **Regulatory / institutional obstacles (Nigeria-focused):** Avoid implying government partnership; NDPR for any microdata if ever merged with surveys (not in scope here).
- **Key Risks and Mitigation:** **Risk:** Politicised rankings—**Mitigation:** Publish formulas; invite peer review.

### Digital Solution

- **Potential Digital Solution:** Quarterly **index** = f(state YoY voice, state YoY internet) normalised around national TOTAL YoY from the same sheet—visual rank table + change logs.
- **No-code / low-code stack:** R Shiny or Observable for MVP visuals.
- **Landing page platform:** Webflow.
- **Actualisation strategy:** Co-publish with **one civil society** partner to bolster neutrality.
- **Competition Analysis:** Ad-hoc consulting reports lack reproducibility—scripted index wins repeat purchases.
- **How to test viability** (one concrete experiment): **Stakeholder workshop** comparing index rankings to **three** local expert priors—measure Spearman correlation **>0.7** or iterate methodology.
- **Potential Challenges:** Single-indicator bias.
- **Solutions to those challenges:** Disclose limitation; phase **2** add other open datasets when licensed similarly.

### Hardware Solution

Not applicable — policy analytics product unless field surveys are added later (out of scope for this workbook).

---

## Closing note

Regenerate or extend this file when a new **`Telecoms_*.xlsx`** drop replaces totals; keep **sheet names**, **TOTAL rows**, and **period labels** traceable to the publisher’s file.

When you are satisfied with repo changes, **stage, commit, and push** respecting `.gitignore`.
