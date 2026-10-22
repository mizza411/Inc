# Ask people / ask owners — playbook

**Track:** NET-ASK-REMIND-1  
**Cadence:** Mon / Wed / Fri · **Rotate:** alternate Strategy 3 ↔ Strategy 4  
**Surfaces:** Inc Hub Option B (09:30) · morning `.docx` via project_reminder  
**Rule:** Automation nudges and drafts only. **You** choose whom, talk, and send.

Quick CLI check (from Inc root):

```powershell
python -m network_ask_reminder today
python -m network_ask_reminder openers --mode both
```

---

## 1. Ritual (every cadence day)

1. Nudge appears (Hub modal and/or this doc opens).
2. Confirm today mode: **S3 network** or **S4 owners** (`today` CLI or Hub bullets).
3. Pick **1–3 people** (judgment only — never auto-picked).
4. Ask in person / call / WhatsApp — paste an opener if helpful.
5. Write what you heard (role, not phone).
6. Log it; optionally open Problem ID / Strategy folders later.

Goal per hit: **at least one real conversation**, not a perfect interview.

---

## 2. Flow (nudge → ask → log → formulate)

```
  Mon/Wed/Fri
  Hub 09:30 and/or morning .docx
           |
           v
     +-----+-----+
     | rotate S3 |
     |   <-> S4  |
     +--+--+--+--+
        |     |
     S3 ask  S4 ask
   (network) (owners)
        |     |
        +--+--+
           |
           v
   log-add (no phones in git)
           |
           v
   optional: Problem ID / S3 / S4 tools
           |
           v
   later: idea formulation (agent / tables)
```

---

## 3. Strategy 3 day — network (people you know)

**Who (examples — you decide):** classmates, coworkers, friends with side hustles, family in business, church/mosque contacts you already talk to, alumni, neighbors who run something small.

**Avoid:** cold-blasting strangers; scraping contact lists into the repo; pressure if someone is clearly busy or uncomfortable.

### Openers (copy/paste — you send)

1. Hey — quick one: what’s the most annoying or expensive problem in your work or side hustle right now?
2. I’m collecting real business problems (not pitching). What’s broken or slow for you every week?
3. If a simple digital tool could remove one headache, what would it fix?

Also fine: shorter in-person version — “What’s the most frustrating part of how you work lately?”

### What to write down

| Field | Keep |
|-------|------|
| Role / context | e.g. “classmate — freelancing” (no phone) |
| Problem | one sentence |
| Frequency / urgency | daily / weekly / rare · high / med / low |
| Current workaround | how they cope today |
| Would they pay? | yes / maybe / no / unknown |

### After the chat

```powershell
python -m network_ask_reminder log-add --mode s3 --notes "one-line problem" --role "classmate"
```

More depth later: Strategy 3 folder  
`Business-Idea-Formulation-Strategy-3-Network-Based-Problem-Identification/`

---

## 4. Strategy 4 day — business owners

**Who (examples):** shop / kiosk / POS operators, service SMEs (salon, repairs, logistics), market traders you already buy from, landlords / agents you deal with, any owner who trusts you enough for a short ask.

**Consent first:** explain you are learning what owners struggle with; they can refuse; questionnaire is optional.

### Openers (copy/paste — you send)

1. Hi — I’m learning what owners struggle with. What’s the hardest ops problem this week?
2. No sales pitch: what takes too much time or money to run your business day-to-day?
3. Would you mind a short questionnaire on business challenges? Totally optional — 5 minutes.

### Live questions (if no form)

Use any 2–3 of these (from Strategy 4 template):

- Biggest challenge right now?
- What process takes too much time?
- What do you spend too much money on?
- What tool do you wish existed?
- What manual task would you automate?

### Questionnaire / survey pointers (optional)

- Strategy 4 template: `Business-Idea-Formulation-Strategy-4-Business-Owner-Problem-Collection/questionnaire_template.txt`
- Google Doc template (Drive): linked from Strategy 4 playbook / README
- Problem ID live survey (if useful): Hub → Problem identification → live site

Never force a form. A spoken answer logged in your words is enough for this habit.

### What to write down

Same table as S3, plus: industry / shop type · whether they saw a questionnaire · consent noted as “yes/no” (no signature file required for habit v1).

### After the chat

```powershell
python -m network_ask_reminder log-add --mode s4 --notes "one-line problem" --role "kiosk owner"
```

---

## 5. After-ask checklist

1. **Log immediately** (while fresh):

```powershell
cd C:\dev\Inc
python -m network_ask_reminder log-add --mode s3 --notes "..." --role "..."
# or --mode s4
python -m network_ask_reminder status
```

2. **No PII in git:** no phone numbers, full legal names if sensitive, home addresses, or chat exports. Role + problem only. Local `data/ask_log.jsonl` is gitignored.

3. **When to open Problem ID:** if the person wants a structured survey, or you want a durable anonymous response — Hub → Problem identification. Do not change survey schema for this habit.

4. **When to open Strategy folders:** when you have 3+ related problems and want the collector / ChatGPT table flow — not required every cadence day.

5. **Opener file:** Hub **Start** also writes `network_ask_reminder/data/last_openers.txt` and copies to clipboard.

---

## 6. Risks and stop-rules

| Risk | What to do |
|------|------------|
| Feels spammy | Cap at 1–3 asks per cadence day; prefer people you already greet |
| Awkward / “are you selling?” | Lead with “not pitching”; stop if they pull back |
| PII leak into git/chat | Role + problem only; never paste phones into Cursor |
| Over-collecting, under-acting | Prefer logging + later formulation over endless interviews |
| Confusing with Macrodroid / Drive macros | Legacy Google/Macrodroid setup may still exist for S3/S4 Drive docs — this Inc/PR habit is the **primary** nudge now; Drive macros are optional parallel |

**Stop if:** someone asks you to stop contacting them; or you are using the habit to avoid shipping other money tracks.

---

## 7. Related paths

| Path | Role |
|------|------|
| `network_ask_reminder/` | This habit (config, CLI, Hub, docx) |
| Strategy 3 folder | Network collection tooling |
| Strategy 4 folder | Owner questionnaire collection |
| `problem_identification_tool/` | Optional survey sink |
| `.cursor/rules/task_net_ask_remind.md` | Backlog |

Regenerate this Word file after edits:

```powershell
python -m network_ask_reminder build-docx
```
