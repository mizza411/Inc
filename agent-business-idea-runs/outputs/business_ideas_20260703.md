# Nigeria Business Ideas — Multi-Strategy Agent Run

**Generated:** 2026-07-03 (UTC+1)  
**Output file:** `business_ideas_20260703.md` (repo root)  
**Strategies executed:** 5, 6, 7, 9, 11, 12, 13, 14, 15  
**Strategies skipped:** 3, 4 (verbal/network/questionnaire), 8, 10 (retired)  
**Dedup sources:** `past_business_ideas.md`, `business_ideas_20260508.md`, Strategy 5/15 `past_business_ideas.md`, Strategy 15 `business_ideas_20260510.md`

---

## Best ideas (top 5)

| Rank | Idea | One-line rationale |
|------|------|-------------------|
| **1** | **SIMGuard Ledger** | Techpoint reports rising SIM-swap fraud and MTN pushing banks to fund telco-powered security checks — a B2B reconciliation SaaS fits mandatory fraud controls, recurring telco–bank workflows, and your API/integration skills. |
| **2** | **CookSwitch Planner** | Premium Times (2026-07-03) launched a national e-cooking initiative; OWID energy data plus FinTech×Energy niche combo yields a policy-aligned estate rollout tool with clear buyers (developers, DISCOs, clean-cooking NGOs). |
| **3** | **SafeTerminal Proximity** | Same-day Apapa fuel-terminal fire headlines (Premium Times, Vanguard) signal urgent, expensive port-safety risk for haulage firms — a geofenced alert + compliance log MVP is buildable under ~$25k. |
| **4** | **FoodTrace Export Desk** | BusinessDay (2026-07-03) highlights Africa-wide food-safety partnership gaps; AgriTech×FoodSafety combo targets exporters needing audit-ready traceability without repeating prior real-estate or AML ideas. |
| **5** | **SchoolConnect Index** | Peter Obi’s education-investment narrative plus NBS Q3 2025 state internet subscription divergence (Strategy 15 prior run) supports a B2G/B2B school connectivity procurement planner — distinct from past “voice rebound” telecom analytics. |

---

## Ranked ideas (full set)

| Rank | Idea | Primary strategy trace | GUEMF (G/U/E/M/F) | Composite | MVP est. (USD) | Dedup confidence | Founder/operator fit |
|------|------|------------------------|-------------------|-----------|----------------|------------------|----------------------|
| 1 | SIMGuard Ledger | S9 → S12 → S13 | 5/5/4/5/5 | **24** | $12k–$22k | High (novel) | **Strong** — APIs, B2B SaaS |
| 2 | CookSwitch Planner | S5 + S14 + S6 | 5/4/4/4/4 | **21** | $10k–$20k | High | **Strong** — web apps, dashboards |
| 3 | SafeTerminal Proximity | S5 → S12 | 4/5/5/4/4 | **22** | $15k–$28k | High | **Good** — maps, alerts, logistics |
| 4 | FoodTrace Export Desk | S5 + S6 → S13 | 5/4/4/4/3 | **20** | $18k–$30k | High | Moderate — needs domain partners |
| 5 | SchoolConnect Index | S5 + S15 → S12 | 5/4/3/4/4 | **20** | $8k–$18k | Medium-high | **Strong** — data products |
| 6 | RepatriateLink Crisis Desk | S5 | 4/5/3/3/2 | **17** | $12k–$25k | High | Moderate — gov/NGO sales cycles |
| 7 | DigitalHealth Scale Kit | S5 + S6 | 5/4/4/3/3 | **19** | $20k–$30k | Medium | Moderate — health regs |
| 8 | MFB Wind-Down Compliance | S9 | 4/4/4/5/2 | **19** | $15k–$25k | High | **Good** — compliance workflows |
| 9 | LocalPhone Assembly QA | S9 + S7 | 5/3/4/3/2 | **17** | $20k–$30k | High | Weak — hardware-heavy |
| 10 | ClientPulse Async Desk | S11 → S12 | 4/3/3/3/5 | **18** | $5k–$12k | High | **Very strong** — existing dev agency |
| 11 | SolarReadiness Mapper | S14 → S7 | 5/3/4/3/3 | **18** | $12k–$22k | Medium | **Good** — data + energy narrative |
| 12 | SME Digital Ops Passport | S5 + S13 | 4/3/3/3/5 | **18** | $8k–$15k | Low-medium | **Strong** — overlaps SME tooling theme |
| 13 | EMTS Gap Finder | S15 (agent synth.) | 4/3/3/3/4 | **17** | $10k–$18k | Medium | **Good** — telecom data niche |
| 14 | Governance Signal Monitor | S5 + S7 | 3/4/3/2/4 | **16** | $8k–$15k | Medium | **Strong** — lightweight SaaS |

*GUEMF scale: 1 = weak, 5 = strong. Composite = sum of five scores (max 25).*

---

## Execution summary

| Strategy | Status | Data freshness | Notes |
|----------|--------|----------------|-------|
| **5** News extraction | **Partial — agent synthesis** | RSS fetched **2026-07-03 ~17:03** | `agent_strategy_run_20260630.py` → `agent_strategy_inputs_20260703_170310.json`. Feeds: BusinessDay, Punch, Vanguard, Premium Times (35 headlines). **Nairametrics feed returned 0 articles** (empty/blocked). Script `news_problem_extractor.py` not run (blocks on `input()`). |
| **6** Niche combination | **Agent synthesis** | Static niche list in repo + news context | `startup_niche_combiner.py` not run (interactive). Combinations derived from script’s `common_niches` + Jul 2026 headlines. Crunchbase scrape not attempted (login wall likely). |
| **7** Trending startup adaptation | **Agent synthesis** | Public trend patterns (2026) | `trending_startup_adapter.py` requires Crunchbase screenshot + `input()`. Agent adapted global patterns (enterprise AI agents, climate ops, local manufacturing) to Nigeria. |
| **9** Financial news | **Partial — RSS + synthesis** | Techpoint **2026-07-03**; Nairametrics/Financial Nigeria feeds **0 articles** | `financial_news_extractor.py` not run (interactive). Techpoint RSS used as financial/tech proxy. |
| **11** Personal problems | **Agent synthesis** | `Started-Businesses/software-development.md` | `personal_problem_converter.py` not run (interactive). Problems inferred from documented agency delivery/follow-up pain points. |
| **12** GUEMF filtering | **Agent synthesis** | Applied to candidate problems above | `problem_filter.py` not run (interactive). Scores computed in this file’s ranked table. |
| **13** Multi-source analysis | **Agent synthesis** | News + OWID + Strategy 15 figures | `multisource_analyzer.py` not run (SimilarWeb API / manual inputs). Cross-source synthesis performed here. |
| **14** Global data (OWID) | **Partial — fetch OK** | OWID pages fetched **2026-07-03** | Internet, renewable-energy, energy topics OK. `financial-inclusion` and `electricity` URLs **404**. `global_trend_adapter.py` not run (interactive). |
| **15** Nigeria open data | **Partial — validation only** | NBS telecom Q3 2025 (prior audited run) | `--non-interactive --inputs nigeria_inputs.json`: **UnicodeEncodeError** on Windows cp1252; retry with `PYTHONIOENCODING=utf-8` **hung** at `offer_cursor_copy_block` (clipboard prompt). **Read-only import** validated 1 record; synthesis uses figures from `business_ideas_20260510.md` / `_telecoms_q3_dump.txt`, not new XLSX parse this session. |
| **3, 4, 8, 10** | **Skipped** | — | Per instructions (verbal/retired). |

**Blockers (no code changes made):** Interactive `input()` / clipboard gates in Strategies 5–7, 9, 11–14; Strategy 15 Windows console encoding + post-run clipboard helper hang; Nairametrics RSS empty; Strategy 15 inputs JSON still contains placeholder indicator and binary XLSX payload instead of clean excerpt.

---

## Idea details

### 1. SIMGuard Ledger — Telco–bank SIM-security cost recovery (S9, S12, S13)

- **Problem:** Techpoint (2026-07-03): *“As SIM-swap fraud rises, MTN wants banks to pay for telecom-powered security checks.”* Banks and telcos lack a shared audit trail for who pays for verification steps after fraud incidents.
- **Solution:** B2B SaaS ledger: incident ID → telco API check log → cost allocation rules → monthly settlement statements for compliance teams.
- **Target:** Tier-2 banks, fintech issuers, telco enterprise partnerships.
- **MVP cost:** $12k–$22k (API integrations, RBAC, reporting).
- **Regulatory:** CBN payment/consumer protection; NDPA for subscriber metadata; partner-only data flows.
- **Commercial viability:** High if one pilot bank signs — recurring reconciliation revenue.
- **Dedup:** No match in `past_business_ideas.md` or `business_ideas_20260508.md` (distinct from card spend controls / AML baseline).
- **Founder fit:** Strong for a Python/JS agency building fintech integrations.

### 2. CookSwitch Planner — E-cooking estate rollout (S5, S14, S6 FinTech×Energy)

- **Problem:** Premium Times (2026-07-03): Federal government e-cooking initiative to reduce firewood/polluting fuels; estates and developers lack ROI models for wiring + appliance mix.
- **Solution:** Web planner: unit count → load model → tariff scenario → capex/opex vs LPG baseline; export PDF for DISCO/estate approvals.
- **Target:** Estate developers, facility managers, clean-cooking NGOs, mini-grid operators.
- **MVP cost:** $10k–$20k.
- **Regulatory:** NERC/DISCO connection rules; SON for appliances; align with national clean-cooking policy docs.
- **Commercial viability:** Medium-high — policy tailwind; sales via developer partnerships.
- **Dedup:** High — not in past lists (differs from diesel/grid estate ideas).
- **Founder fit:** Strong — dashboard + PDF automation.

### 3. SafeTerminal Proximity — Port fuel-terminal incident alerts (S5, S12)

- **Problem:** Premium Times & Vanguard (2026-07-03): Fire at Apapa fuel terminal; haulage firms need provable geofence avoidance and insurer-ready incident logs.
- **Solution:** Mobile/web geofence alerts around registered high-risk terminals; driver acknowledgment; fleet compliance export.
- **Target:** Tanker fleets, freight forwarders, port insurers.
- **MVP cost:** $15k–$28k (maps, SMS/WhatsApp, fleet admin).
- **Regulatory:** NPA/port safety coordination; NDPA location data.
- **Commercial viability:** Medium — niche but high willingness-to-pay after incidents.
- **Dedup:** High — not port-terminal specific in prior files.
- **Founder fit:** Good — logistics + mapping stack.

### 4. FoodTrace Export Desk — Africa food-safety traceability (S5, S6 AgriTech×FoodSafety, S13)

- **Problem:** BusinessDay (2026-07-03): Experts urge stronger government–private food-safety partnerships across Africa; Nigerian exporters struggle to prove chain-of-custody.
- **Solution:** Batch QR + cold-chain checklist SaaS; exporter dashboard for audit packets (farm → processor → port).
- **Target:** Food exporters, aggregators, NAFDAC-facing QA consultants.
- **MVP cost:** $18k–$30k.
- **Regulatory:** NAFDAC, SON export requirements; NDPA.
- **Commercial viability:** Medium — needs pilot exporter; sticky if certification-linked.
- **Dedup:** High — avoids real-estate transparency repeats.
- **Founder fit:** Moderate — needs food-industry champion.

### 5. SchoolConnect Index — State-level internet vs school need (S5, S15, S12)

- **Problem:** Vanguard (2026-07-03): Education crisis needs investment not policy churn; NBS Q3 2025 data shows state-level internet subscription divergence (prior Strategy 15 audit: national internet ~140.9m, ~+6% YoY, ~flat QoQ; Lagos ~17.7m internet subs).
- **Solution:** Map state NBS internet growth ranks against open school counts (UBEC/NBS where available) → prioritized LGAs for connectivity procurement briefs.
- **Target:** State education boards, edtech NGOs, tower/fibre vendors.
- **MVP cost:** $8k–$18k.
- **Regulatory:** Public procurement; accurate sourcing disclaimers (not NBS-endorsed).
- **Commercial viability:** Medium — B2G cycles; strong grant narrative.
- **Dedup:** Medium-high — distinct from Strategy 15 “voice rebound” / “MNP digest” past ideas.
- **Founder fit:** Strong — data product from open tables.

### 6. RepatriateLink Crisis Desk — Diaspora evacuation coordination (S5)

- **Problem:** BusinessDay (2026-07-03): FG evacuated 593 Nigerians from South Africa; xenophobia coverage across Vanguard/Punch.
- **Solution:** Crisis registry: citizen intake → flight manifest workflow → consular status portal for families (B2G licensed).
- **MVP cost:** $12k–$25k.
- **Commercial viability:** Lower frequency; high urgency when active.
- **Dedup:** High.
- **Founder fit:** Moderate — gov procurement heavy.

### 7. DigitalHealth Scale Kit — ADHS interoperability layer (S5, S6 HealthTech×Logistics)

- **Problem:** BusinessDay: Africa struggles to scale digital health beyond pilots (ADHS 2026).
- **Solution:** Lightweight FHIR-friendly patient referral + lab result routing between clinic systems.
- **MVP cost:** $20k–$30k.
- **Dedup:** Medium — health staffing ideas exist in Strategy 5 past list; this is interoperability not recruitment.
- **Founder fit:** Moderate — health domain advisors needed.

### 8. MFB Wind-Down Compliance — Post-licence-revocation toolkit (S9)

- **Problem:** Techpoint: CBN revoked 46 microfinance bank licences — wind-down, depositor comms, and reporting spikes.
- **Solution:** Workflow templates + regulator checklist tracker for affected MFBs/consultants.
- **MVP cost:** $15k–$25k.
- **Dedup:** High.
- **Founder fit:** Good — document/workflow automation.

### 9. LocalPhone Assembly QA — Domestic smartphone ambition (S9, S7)

- **Problem:** Techpoint: Nigeria wants local smartphone manufacturing, not imports only.
- **Solution:** QC traceability for assembly lines (IMEI batch, component sourcing log).
- **MVP cost:** $20k–$30k; hardware adjacency.
- **Dedup:** High.
- **Founder fit:** Weak without factory partner.

### 10. ClientPulse Async Desk — Agency client follow-up (S11, S12)

- **Problem:** From `software-development.md`: clients go quiet; ethical follow-up needs async options (Loom, one-question pings, trained staff contact).
- **Solution:** Lightweight CRM for Nigerian dev agencies: delivery milestones → templated async check-ins → support window alerts.
- **MVP cost:** $5k–$12k.
- **Dedup:** High.
- **Founder fit:** **Very strong** — dogfood for existing software business.

### 11. SolarReadiness Mapper — Renewable transition estates (S14, S7)

- **Problem:** OWID: fossil fuels dominate; Nigeria e-cooking + global renewable shift create estate-level planning gap.
- **Solution:** Rooftop solar + battery sizing vs grid outage hours; links to CookSwitch scenarios.
- **MVP cost:** $12k–$22k.
- **Dedup:** Medium — energy ideas exist but not this OWID+e-cooking combo.
- **Founder fit:** Good.

### 12. SME Digital Ops Passport — Tooling confidence gap (S5, S13)

- **Problem:** Vanguard/Mastercard SME playbook: digital tools turn ambition into reality, but 40m MSMEs lack integrated ops stack.
- **Solution:** Readiness scan → recommended tool bundle (payments, inventory, tax) with implementation checklist.
- **MVP cost:** $8k–$15k.
- **Dedup:** Low-medium — crowded SME space; differentiate via Nigeria-specific bundles.
- **Founder fit:** Strong.

### 13. EMTS Gap Finder — Fixed-wireless underserved states (S15 agent synth.)

- **Problem:** NBS Q3 2025 workbook shows operator columns (MTN, GLO, AIRTEL, EMTS); some states negative voice YoY while national voice +12% YoY — fixed/mobile wireless gaps for enterprise sites.
- **Solution:** State×operator anomaly alerts for ISP sales teams targeting underserved LGAs.
- **MVP cost:** $10k–$18k.
- **Dedup:** Medium — related to but not duplicate of past Strategy 15 heatmap/benchmark ideas.
- **Founder fit:** Good for telecom data niche.

### 14. Governance Signal Monitor — Institutional trust analytics (S5, S7)

- **Problem:** Punch PFIPC scandal coverage; enterprises need vendor/gov-contract risk signals without building full OSINT teams.
- **Solution:** Curated news + filing alert feed with severity tags for procurement teams.
- **MVP cost:** $8k–$15k.
- **Dedup:** Medium.
- **Founder fit:** Strong for automation shop.

---

## Cross-cutting assessment

| Criterion | Summary |
|-----------|---------|
| **Commercial viability** | Top tier (SIMGuard, CookSwitch, SafeTerminal) have identifiable B2B buyers and recurring use cases. Crisis/gov ideas (RepatriateLink) are impactful but lumpy revenue. |
| **MVP ≤ ~$30k** | All ideas scoped at or below ~$30k except upper-bound fleet/port builds; ClientPulse and SchoolConnect are leanest. |
| **Regulatory fit** | Fintech/telco (SIMGuard), port safety (SafeTerminal), NAFDAC food trace, NERC energy, NDPA data handling flagged per idea; none require unreleased licences for MVP pilots. |
| **Dedup confidence** | Deliberately avoided repeats from grid/diesel estates, AI deepfake fraud, real-estate transparency, stablecoin adoption, voice rebound analytics, MNP digest, and `business_ideas_20260508.md` domains. Medium risk on SME digital tooling (crowded). |
| **Founder/operator fit** | Software development agency profile aligns best with **SIMGuard**, **ClientPulse**, **CookSwitch**, **SchoolConnect**, **Governance Signal** — API-heavy B2B SaaS and internal dogfooding. |

---

## Suggested next validation steps

| Date | Action | Owner |
|------|--------|-------|
| **2026-07-07** | 5 customer discovery calls: 2 bank fraud ops, 2 estate facility managers, 1 haulage fleet dispatcher (SIMGuard, CookSwitch, SafeTerminal hypotheses). | Founder |
| **2026-07-10** | Re-fetch Nairametrics + Financial Nigeria feeds; if still empty, add manual headline paste or NewsAPI key to agent runner (future session — requires script change approval). | Agent/founder |
| **2026-07-12** | Strategy 15: replace `nigeria_inputs.json` statistical excerpt with clean Q3 2025 TOTAL-row text from `Telecoms_Q3_2025.xlsx`; re-run `--non-interactive` with `PYTHONIOENCODING=utf-8` and skip clipboard step (code change) or import-only validation path. | Founder |
| **2026-07-14** | Build 2-page landing + waitlist for **SIMGuard Ledger** and **CookSwitch Planner**; measure signup conversion. | Founder |
| **2026-07-21** | 30-day pilot LOI target: one bank/fintech partner for SIM cost ledger **or** one estate for e-cooking ROI PDF. | Founder |
| **2026-08-01** | GUEMF re-score top 3 after discovery; kill or pivot ideas scoring &lt;17 composite. | Founder |

---

*Agent run attempt **1** for this requirement. Automated inputs: `agent_strategy_inputs_20260703_170310.json`. No existing strategy scripts, configs, or `task.md` files were modified.*
