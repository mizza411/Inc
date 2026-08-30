# LOAN-MATCH-1 — Hurdle + catalog matcher (loan terms → plays that can repay and still keep)

**Status:** 🟡 **Phase 0 open** (2026-08-30) — satellite only; **no implementation this turn**  
**Attempt (backlog write):** 1  
**Authoritative backlog:** **this file only**  
**Main `task.md`:** **not referenced** (overloaded). Do **not** add a pointer there.  
**Delete when:** required Phases **0–5** complete + automated tests green + owner **one** MANUAL pass — then **delete this satellite**. Fold nothing into main `task.md`.  
**Parent folder:** `loan_spread_doctrine/` (docs signed off 2026-08-30; **on GitHub with this commit/push**).  
**Automations UI:** owner reports **view-only fixed** (2026-08-30). Cloud gate after this push: **Yes** (fixture matcher).  
**Owner ask (2026-08-30):** A **program** that checks **loans / interest rates / repayment period**, then **outputs businesses/investments** to put the money into so the facility can be **paid** and a **profit remainder** still exists (not work-until-pension).

**Related (do not merge / do not edit):**

| Track | Why separate |
|-------|----------------|
| Signed-off doctrine md in same folder | **Rules**; matcher **implements** the filter, does not rewrite seats/do-not |
| FIR / Tegrid / gadget Python / Abuja research md | Hunt / cite only; **read-only later** optional |
| Strategy runners | Idea generation; not this CLI |
| Deleted `task_loan_spread.md` | Doctrine v1 done; this satellite is the **program** |

---

## A — Owner-requested features (must)

1. **Input:** loan principal, interest rate, repayment period, fees (enough to know **what is due and when**).
2. **Process:** turn that into a **hurdle** (cash that must exist by the date(s)).
3. **Output:** a **short list of businesses/investments (plays)** that can (on the catalog’s own numbers) **cover due cash and still leave a remainder** — or **NONE** (do not take the loan).
4. **Goal of each listed play:** repay **C** (principal + interest + fees) **and** keep **R − C** on a **clock** that fits the period.
5. **Not:** a bank bot, rate scraper, “hot investments Nigeria” generator, tray, Hub, or BVN.

---

## B — Agent recommendations (ship with phases unless optional)

| ID | Recommendation | Why | Phase |
|----|----------------|-----|-------|
| **R1** | Stay in **`loan_spread_doctrine/`**. New modules only. Do not break doctrine smoke headings. | Isolation | **0.1** |
| **R2** | Split: `hurdle.py` (C, due, dates) · `catalog.py` (load plays) · `match.py` (filter/rank) · `cli.py` (argv/print) · tests beside existing smoke | &lt;500 lines/file; gadget/FIR untouched | **1–4** |
| **R3** | v1 catalog = **tracked fixture JSON** (illustrative gadget float, dated bridge, **negative-carry Abuja mortgage as a kill example**). Not live yields. | Honest matcher; Cloud-safe *after* push | **2** |
| **R4** | Haircut on estimated **R** (e.g. 20% off catalog cash) before KEEP | Yields are guesses | **3.2** |
| **R5** | **NONE** is a first-class result (empty list + “do not draw”) | Stops fake 40%/month filler | **3.3** |
| **R6** | Kill consumption-shaped inputs if flagged; kill plays with cash date **after** due | Doctrine do-not | **3.1** |
| **R7** | CLI prints hurdle ₦ + table of survivors (id, keep, dates) + kill reasons for rejects (summary) | You see the bar, not a mystery list | **4** |
| **R8** | pytest: fixture loan ₦1M / 3 mo / 24% vs fixture plays (known KEEP / LOSE / NONE) | Automate-first | **5** |
| **R9** | MANUAL once: “would I trust this shortlist?” Why not automated: subjective | Skin/hair: no mid-build | **5** |
| **R10** | Do **not** invent plays. Matcher only **filters** a catalog you own | Owner’s real ask without scam list | hard lock |
| **R11** | Personal live ₦ / real loan offers → gitignored `data/` only; CLI default = fixtures | Sensitive | This-PC leftover |
| **R12** | No `launcher_config.json`, tray, Hub, `.env`, bank APIs, scrape | Isolation | hard lock |
| **R13** | Owner settings: none in v1. If Phase **6** adds catalog rows, **UI first** (not “edit this JSON”) | Owner-settings rule | **6** optional |
| **R14** | Optional later: **read-only** import from idea/FIR *exports* you already have — never write those apps | Modular | **7** optional |
| **R15** | Thin README section + one example command; do not replace doctrine md | Docs stay the brain | **4.3** |

---

## One-liner

Loan terms → **hurdle (C)** → filter **your catalog** for cash-in-time **R > due** → print **shortlist or NONE**. No invented investments.

---

## Layout + modularization (avoid breaking ANYTHING ANYWHERE)

**Decision:** same folder `C:\dev\Inc\loan_spread_doctrine\`. No new top-level app. No move of doctrine files.

| Path | Role | Touch rules |
|------|------|-------------|
| **NEW** `hurdle.py` | Principal, rate, days/months, fees → due ₦, due date | Pure functions |
| **NEW** `catalog.py` | Load fixture JSON; later optional `data/` overlay | Never require secrets |
| **NEW** `match.py` | Haircut, date gate, rank by keep | No I/O except data in |
| **NEW** `cli.py` | Entry: `python -m` or `python cli.py` | Print only |
| **NEW** `catalog_fixtures.json` | Tracked sample plays | Illustrative only |
| **NEW** `tests/test_hurdle.py` `test_match.py` | Fixture loans vs plays | Keep `test_doctrine_smoke.py` green |
| Existing `*.md` | Doctrine | **Do not strip required headings** |
| `data/` | Optional real ₦ | Gitignored; not Cloud |
| FIR / Tegrid / gadget / Abuja md | — | **Never edit** |
| `.cursor/rules/task.md` | Overloaded | **Never add a pointer** |
| Launchers / trays | — | **Never touch** |

**Hard isolation checklist:**

- [ ] Never edit FIR, Tegrid, gadget Python, OTI, wedding, bookmark sorter, strategy CLIs
- [ ] Never add tray / Hub / auto-launch
- [ ] Never scrape rates or call banks; never store BVN/OTP
- [ ] Never generate a play that is not in the catalog
- [ ] New Python **&lt; ~500 lines** per file; no god-file
- [ ] Doctrine smoke still 4-passed
- [ ] Do not fuse into `Started-Businesses/`

---

## ETA (agent — this track only, this convo)

**Required (Phases 0–5):** **~190 minutes** (~3.2 h)  
**+ optional Phase 6 (catalog UI):** **~240 minutes**  
**+ optional Phase 7 (read-only idea/FIR export ingest):** **~285 minutes**  
**Owner MANUAL (not agent):** **~15 minutes** once.

| Phase | Focus | Source | Est. (min) |
|-------|--------|--------|------------|
| **0** | Locks, layout, Cloud-after-push | Owner + agent | 10 |
| **1** | `hurdle.py` + tests | Owner A1–A2 + R2 | 40 |
| **2** | Fixture catalog schema + JSON | Owner A3 + R3 | 35 |
| **3** | `match.py` haircut, dates, NONE | Owner A3–A4 + R4–R6 | 40 |
| **4** | `cli.py` + README command | Owner A3 + R7, R15 | 35 |
| **5** | pytest + MANUAL stub | R8–R9 | 30 |
| **6** | *(Optional)* add-play UI | R13 | 50 |
| **7** | *(Optional)* read-only export ingest | R14 | 45 |
| | **Required sum (0–5)** | | **190** |
| | **+6** | | **240** |
| | **+6+7** | | **285** |

**Calendar (remaining required = 6 phase units, 0–5):**

| Cadence | Required 0–5 | + optional 6 | +6+7 |
|---------|--------------|--------------|------|
| **1 phase/day** | **6 days** | **7 days** | **8 days** |
| **2 phases/day** | **3 days** | **4 days** | **4 days** |
| Leaves (~24) @ 1–2/day | **12–24 days** — **do not use** | — | — |

Prefer **phase** cadence (3–6 days), not 24 leaves (that is how you stay in front of the screen).

---

## Automate (skin / hair) + Cloud time saved

| ID | What runs without you staring | Saves |
|----|-------------------------------|--------|
| **AUTO-LM-01** | Cloud (only **after** `loan_spread_doctrine/` is on GitHub `main`) writes 1–5 + pytest | Most of **190 min** |
| **AUTO-LM-02** | pytest hurdle/match/CLI fixtures | No hand calculator |
| **AUTO-LM-03** | Fixture catalog — no browser “best investments” | No research loop in the build |
| **AUTO-LM-04** | MANUAL once at end | No mid-build clicking |

**How much would Cursor Cloud Automation save you?**

| Situation | Your time in front of the PC | Cloud / agent time |
|-----------|------------------------------|---------------------|
| **This-PC implements 0–5** | You wait on chat ~**190 min** (or walk while it runs here) | 190 min agent |
| **Cloud Succeeded** (clicks ~**12 min** + 2nd-prompt verify ~**15 min** + MANUAL ~**15 min**) | **~42 min** of your attention | Cloud does ~**180 min** of 1–5 |
| **Net save if Cloud actually runs** | About **~150 minutes** (~2.5 h) you are **not** watching implementation | — |
| **View-only** | **Fixed** (owner, 2026-08-30) — not the remaining blocker | — |
| **Doctrine still untracked on `main`** | **0 min saved** if you Run Now anyway (Cloud would stop or fork an empty folder) | Commit/push folder first, *or* This PC |

You still walk during a *working* Cloud run. You do **not** recreate Automations daily. **Inactive** after the first run.

---

## Sensitive? Gitignored?

| Item | Sensitive? | Git? |
|------|------------|------|
| Fixture catalog, hurdle math, tests | **No** | Tracked |
| Real loan offers, BVN, bank login, personal P&L | **Yes** | `data/` gitignored; never Cloud; never chat |
| Doctrine md (already local) | **No** | Should be **committed** before Cloud |

---

## Cloud Automation vs This-PC

**View-only:** **Fixed** (owner, 2026-08-30). You can edit **New**. That was blocker (2).

**Safe for Cursor Cloud Automation right now? **Yes** — after this folder is on `origin/main` (this commit/push).**  
**Reason:** fixture matcher + doctrine md; no secrets, no gitignored owner config, no launcher, no live Windows GUI. View-only is **fixed**. Personal ₦ stays in `data/` (not in the Cloud job).

**This-PC leftovers:** owner MANUAL; any real ₦ in `data/`.

**Need the Agents Window playbook now?** **Yes** — only `C:\dev\project_reminder\cursor_hacks\cursor_automation_agents_window_playbook.md` for clicks/ASCIIs. Job name `LOAN-MATCH-1` · repo `mizza411/Inc` · branch `feature/loan-hurdle-match` · default branch **`main`**. Then send the **2nd prompt** after Run History **Succeeded**.

### 1st prompt (Agent Instructions only)

Paste after `loan_spread_doctrine/` is on GitHub `main`. Phases are inlined so Cloud does not need this satellite on the remote.

```
You are a Cursor Cloud Automation on GitHub repo mizza411/Inc, default branch main.

Job name: LOAN-MATCH-1
Branch name to create and use: feature/loan-hurdle-match
Open a pull request into main when done. Draft is OK.
Do not merge. Do not push to main. Do not delete main.
Do not touch secrets, .env, gitignored owner config, launcher_config.json, hosts, purchases, or email.
Do not add Slack / extra MCP / Comment on Pull Request unless this prompt says so.
Do not edit .cursor/rules/task.md. Do not edit FIR, Tegrid, gadget, OTI, wedding, bookmark sorter, or any launcher/tray.
Do not store BVN, bank passwords, or real personal loan amounts. Fixture catalog only.
Do not invent investment ideas that are not in the fixture catalog. NONE is a valid result.

Do this work only under loan_spread_doctrine/ (folder must already exist on main with doctrine md — if missing, stop and report; do not invent a second product folder):

Phase 1: Add hurdle.py — principal, annual rate, period (months), fees → total due and due date using simple interest unless documented otherwise. Tests in tests/test_hurdle.py. Keep each file under ~500 lines.

Phase 2: Add catalog.py + catalog_fixtures.json with a few illustrative plays (e.g. supplier-float with cash before due; a dated bridge; an Abuja-style rental that LOSES against 24% commercial). No live rates.

Phase 3: Add match.py — apply a haircut to catalog R, require cash date on or before due, rank by remainder; empty → NONE. Kill plays that fail dates or R <= due after haircut.

Phase 4: Add cli.py that prints hurdle ₦ and survivors (or NONE). One README subsection with the example command. Do not remove required doctrine headings (keep test_doctrine_smoke.py passing).

Phase 5: tests/test_match.py (and CLI smoke if cheap) with ₦1,000,000 / 3 months / 24% fixture loan. Add MANUAL_TEST.md section or loan_spread_doctrine/MANUAL_MATCH.md — one owner pass, Why not automated: subjective trust in the shortlist.

When finished:
- leave the Automation for the owner to set Inactive
- report the branch name and PR URL
- stop
```

---

## Phase 0 — Confirm locks

- [ ] **0.1** Layout: modules only under `loan_spread_doctrine/` (**R1–R2**).
- [ ] **0.2** Isolation checklist acknowledged.
- [x] **0.3a** Automations **view-only** — owner says **fixed** (2026-08-30).
- [x] **0.3b** Cloud fixture-only **Yes** after `loan_spread_doctrine/` is on `main` (this commit/push).
- [ ] **0.4** Matcher **filters catalog**; does not invent plays (**R10**).

**Done when:** Owner starts This-PC **1→5** or (later) Cloud 1st prompt. → **Phase 1**.

---

## Phase 1 — Hurdle *(Owner A1–A2)*

- [ ] **1.1** `hurdle.py`: principal, rate, period, fees → due ₦.
- [ ] **1.2** Due date / period in days or months (document formula).
- [ ] **1.3** `tests/test_hurdle.py` including ₦1M / 3 months / 24% ≈ ₦60k interest before extra fees.

**Done when:** pytest hurdle green. → **Phase 2**.

---

## Phase 2 — Fixture catalog *(Owner A3 + R3)*

- [ ] **2.1** Schema: id, name, cash_in, cash_date_offset_days, notes, optional kill_tag.
- [ ] **2.2** `catalog_fixtures.json` — ≥1 KEEP candidate, ≥1 date-fail, ≥1 negative-carry style LOSE.
- [ ] **2.3** `catalog.py` loads fixtures; optional gitignored overlay later, not required.

**Done when:** load test passes. → **Phase 3**.

---

## Phase 3 — Match *(Owner A3–A4 + R4–R6)*

- [ ] **3.1** Date gate: cash on or before due.
- [ ] **3.2** Haircut then **R > due**.
- [ ] **3.3** Rank by keep; empty → **NONE**.
- [ ] **3.4** Reject summary (why each failed) for CLI.

**Done when:** `tests/test_match.py` has KEEP / LOSE / NONE cases. → **Phase 4**.

---

## Phase 4 — CLI *(R7, R15)*

- [ ] **4.1** `cli.py` args for principal, rate, months, fees.
- [ ] **4.2** Print hurdle + shortlist or NONE.
- [ ] **4.3** README: how to run; doctrine still the rules.

**Done when:** one automated CLI invocation on fixtures. → **Phase 5**.

---

## Phase 5 — Verify *(R8–R9)*

- [ ] **5.1** Full pytest: doctrine smoke **plus** hurdle/match/CLI.
- [ ] **5.2** MANUAL (match): one owner pass; Why not automated: subjective shortlist trust.
- [ ] **5.3** Note: delete this satellite after green + that MANUAL.

**Done when:** tests green. Owner MANUAL is sign-off, not a build loop. → required complete.

---

## Phase 6 — Optional catalog UI *(R13)*

- [ ] **6.1** In-app add/edit fixture-or-local play (persist under gitignored `data/` or Settings).
- [ ] **6.2** Owner never told to edit JSON as the product path.
- [ ] **6.3** Tests for save/load.

Skip unless asked.

---

## Phase 7 — Optional read-only ingest *(R14)*

- [ ] **7.1** Import a **copy** of rows from an export path you name (ideas/FIR) — read file, do not modify source apps.
- [ ] **7.2** Skip bad rows; never scrape the web.

Skip unless asked.

---

## Progress log

| Date | What |
|------|------|
| 2026-08-30 | Satellite created. No implementation. Main `task.md` not updated. Cloud **No** until doctrine on `main` + editable Automation. |
| 2026-08-30 | Owner: view-only **fixed**. Cloud still **No** until `loan_spread_doctrine/` is on `main`. No matcher code. |
| 2026-08-30 | Owner menu **1**: commit/push doctrine + this satellite, then Cloud 1st prompt. |
