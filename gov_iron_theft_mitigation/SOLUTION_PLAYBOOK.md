# Public Iron Asset Protect — Solution Playbook

**Track:** GOV-IRON-THEFT-1  
**Audience:** Vendor ops + LGA Works / ICT partners (run the solution)  
**Not this file:** sales one-pager (`ONE_PAGER_LEAVE_BEHIND.md`) or internal design notes (`SOLUTION_BRIEF.md`)  
**Hard rule:** no steps that help thieves bypass controls  

**What this is:** the actual solution from start to finish - Prepare → Prevent → Detect → Respond → Deny cash-out → Learn / scale.

---

## Visuals (read these first)

### End-to-end map

```
                    +------------------ PREPARE ------------------+
                    | sponsor · corridors · register · marks      |
                    | on-call · SLA · yard notice · go-live test  |
                    +----------------------+----------------------+
                                           |
                                           v
                    +------------------ PREVENT ------------------+
                    | harder lift · marks · low-resale materials  |
                    | contractor scrap custody                    |
                    +----------------------+----------------------+
                                           |
                         theft / missing still happens
                                           |
                                           v
         +---------------- DETECT ----------------+
         |  SENSOR          CITIZEN REPORT        |
         |  (tilt/lift)     (WhatsApp / USSD)     |
         |       \                /               |
         |        +---> TICKET <--+               |
         |  (also: device offline warning)        |
         +------------------+---------------------+
                            |
                            v
         +---------------- RESPOND ---------------+
         |  OPS DESK                              |
         |  new -> ack -> assign -> secure/replace|
         |                      -> close          |
         |  Works crew on the street              |
         +---------+------------------+-----------+
                   |                  |
                   v                  v
         +-- DENY CASH-OUT --+   +-- LEARN / SCALE --+
         | yard refuse       |   | day-90 KPIs       |
         | inspect + logs    |   | expand or stop    |
         | police hotspot    |   | next corridor/LGA |
         +-------------------+   +---------+---------+
                                           |
                                           v
                              back to PREPARE (next set)
```

### Street → scrap (why all stages matter)

```
  [COVER / BARRIER] ----steal----> [THIEF] ----sell----> [SCRAP YARD]
         ^                                                  |
         |                                                  |
    PREVENT makes                                          DENY CASH-OUT
    lift harder                                            makes sale hard
         |                                                  |
    DETECT sees                                            RESPOND closes
    the loss fast                                          the hole for people
```

### Who talks to whom

```
  CITIZEN ----report----> OPS DESK <----alert---- SENSOR
                             |
              +--------------+--------------+
              |              |              |
              v              v              v
           WORKS CREW    POLICE LIAISON   YARD INSPECTOR
           (secure)      (hotspot pack)   (refuse / log)
```

---

## Stage 0 — Prepare (days 1–14 of a pilot)

**Done when:** pilot corridors chosen, assets registered and marked, on-call named, yards notified, ops desk users trained.

```
  Sponsor OK
      |
      v
  Pick 20-50 life-safety sites ----> Register + photo + mark
      |                                      |
      v                                      v
  Name on-call + SLA              Issue yard notice
      |                                      |
      +---------------+----------------------+
                      |
                      v
              Train ops users
                      |
                      v
         Go-live: 1 sensor test + 1 fake report
                      |
                      v
                   LIVE PILOT
```

### Steps

1. **Sponsor lock** — Chairman / Works / ICT agree one LGA pilot and a day-90 review date.  
2. **Corridor pick** — Works lists life-safety sites only (deep chambers, highways, flood-prone covers, critical barriers). Cap **20–50** sensorized points for v1.  
3. **Asset register** — For each point: unique ID, type, lat/long, photo, corridor name, public mark string.  
4. **Field mark** — Apply visible ID (and covert mark if used). Export ID list for crews and later yard checks.  
5. **On-call roster** — Named Works responders for nights/weekends. Or vendor first-line triage under MoU. No orphan alarms.  
6. **SLA agreement** — Default targets: alert→ack under 30 minutes (on-call hours). Confirmed missing life-safety→secure/barricade under 4 hours.  
7. **Yard notice** — Licensing / Works issues “refuse unmarked / gov-marked public iron” notice to dealers (template in `packs_static/`).  
8. **Ops access** — Create users: Works dispatcher, crew (limited), ICT admin, liaison read-only. Train ticket flow once.  
9. **Go-live check** — One supervised sensor test + one fake citizen report. Both become tickets and get closed.

### Owners

| Step | Owner |
|------|--------|
| Corridors + crews | LGA Works |
| Users + data rules | LGA ICT + vendor |
| Yard notice issue | Licensing / environment (as applicable) |
| Install sensors + desk | Vendor with Works site access |

### Exit criteria

- [ ] 20–50 assets on register with marks  
- [ ] On-call names published internally  
- [ ] At least one successful sensor test ticket and one report ticket closed  
- [ ] Yard notice distributed  

---

## Stage 1 — Prevent (ongoing, starts in Prepare)

**Done when:** stealing takes more time/risk, scrap motive is lower on new stock, works scrap cannot vanish quietly.

```
  BEFORE                         AFTER PREVENT
  ======                         =============
  loose cover                    retained/locked frame (where allowed)
  no ID                          visible + covert mark
  iron = high scrap pay          new stock = lower resale where possible
  works scrap "disappears"       contractor must log / return metal
```

### Controls (use all that fit local standards)

| Control | What it does |
|---------|----------------|
| Retained / locked frames (standards-approved) | Harder casual lift |
| Visible + covert marks | Ownership proof at street and yard |
| Low-resale / composite covers on **new** installs | Less melt value |
| Contractor custody clause | Removed metal logged or returned |
| Public awareness on report channel | Citizens become early sensors |

### Owners

| Control | Owner |
|---------|--------|
| Frame / material standards | Works + engineering |
| Marking on live assets | Works + vendor |
| Contract clauses | Procurement / project managers |

### Exit criteria (steady state)

- [ ] New installs follow agreed material / frame rules where allowed  
- [ ] Every pilot asset has a public mark on the register  
- [ ] Active works contracts in pilot corridors include scrap custody language  

---

## Stage 2 — Detect (live after go-live)

**Done when:** a missing or disturbed asset creates a ticket within minutes (sensors) or within the report SLA (citizens).

```
   STREET                         OPS
   ======                         ===
   Cover lifts ----sensor------>  ticket: sensor_alert
   Citizen sees hole             ticket: public_report
        \----WhatsApp/USSD---->/     (match nearest asset if lat/lon)
   Device goes quiet ------>     ticket: device_offline
   Camera (optional) ------>     evidence only (still open a ticket)
```

### Channels

1. **Sensor / tilt / cut alerts** on the pilot set → ticket `sensor_alert`.  
2. **Citizen report** (WhatsApp first, USSD optional) → ticket `public_report`, matched to nearest asset when location is sent.  
3. **Device offline** → ticket `device_offline` so silence is visible to ops (not a bypass guide).  
4. **Optional corridor CCTV** only where power and a watcher exist - evidence support, not a replacement for tickets.

### Ops rule

Every detection path must open a ticket. No “we saw it on CCTV” with no Works assignment.

### Owners

| Channel | Owner |
|---------|--------|
| Sensors + heartbeat | Vendor ops |
| Citizen channel number / bot | Vendor + ICT |
| CCTV (if any) | LGA / police as already owned |

### Exit criteria

- [ ] Sensor alerts create tickets with asset ID and timestamp  
- [ ] Citizen reports create tickets (matched or unmatched queue)  
- [ ] Offline devices appear on ops list  

---

## Stage 3 — Respond (every ticket)

**Done when:** life-safety openings are secured fast, tickets reach a closed outcome, KPIs are honest.

### Ticket path

```
                         +-- false_alarm -------------------+
                         |                                  |
                         v                                  v
   new ----> acknowledged ----> assigned ----> secured ----> closed
                                      |            ^
                                      +--> replaced +
```

```
  CLOCK A                         CLOCK B
  alert -> ack                    missing -> secure
  (target < 30 min on-call)       (target < 4 hours)
```

### Crew play (life safety first)

1. **Acknowledge** so the alert is not an orphan.  
2. **Assign** a crew or shift lead.  
3. **Secure** the hole/barrier gap (barricade, temporary cover) before perfect replacement if needed.  
4. **Replace** under Works rules. Photo optional on close.  
5. **Close** with outcome. Unmatched citizen reports get investigated or closed with reason.

### Who may edit tickets

Works dispatcher, Works crew, ICT admin, vendor admin. Liaison is read-only (hotspot packs only).

### Owners

| Action | Owner |
|--------|--------|
| Ack / assign / close | Works dispatcher |
| Physical secure / replace | Works crew |
| Escalation if SLA breach | Works lead + vendor triage |

### Exit criteria (per serious ticket)

- [ ] Acknowledged inside SLA when on-call  
- [ ] Secured or replaced with timestamp  
- [ ] Closed with outcome (not left forever in `new`)  

---

## Stage 4 — Deny cash-out (parallel to Detect / Respond)

**Done when:** selling stolen public iron is risky at licensed yards, and police/liaison get useful hotspot packs.

```
  STOLEN IRON ----try to sell----> SCRAP YARD GATE
                                       |
                         +-------------+-------------+
                         |             |             |
                         v             v             v
                      NOTICE        INSPECT        REFUSE
                   (already out)   (checklist)   (unmarked /
                                                gov-marked)
                                       |
                                       v
                              WEEKLY HOTSPOT PACK
                              Works + Area Command
```

### Loop

1. **Notice** already issued in Prepare.  
2. **Inspect** yards on a schedule (checklist in `packs_static/`).  
3. **Refuse** unmarked gov-looking lots and gov-marked pieces.  
4. **Record** purchases where law requires.  
5. **Weekly hotspot pack** from ops (counts by corridor, open vs closed, top asset IDs) → Works + Area Command liaison.  
6. **Follow up** repeat corridors and repeat yards together.

### Boundary

Vendor supplies packs, checklists, and mark lists. **Council and police enforce.** Vendor does not arrest or license.

### Owners

| Action | Owner |
|--------|--------|
| Inspections / licence action | Licensing + police |
| Hotspot pack generation | Vendor ops / Works ICT |
| Patrol decisions | Area Command |

### Exit criteria

- [ ] At least one inspection cycle completed in the pilot window  
- [ ] Weekly packs issued while pilot is live  
- [ ] Mark list available to inspectors (CSV / print)  

---

## Stage 5 — Learn and scale (days 76–90, then beyond)

**Done when:** day-90 scorecard is honest, and the next corridor or LGA decision is evidence-based.

```
                 DAY-90 SCORECARD
                        |
        +---------------+---------------+
        |               |               |
        v               v               v
   KPIs green      Alerts OK        Whole loop weak
   response OK     response weak
        |               |               |
        v               v               v
   Expand sensors  Fix on-call      Stop or redesign
   next corridor   before devices   (do not scale fail)
```

### Scorecard (defaults)

| KPI | Target |
|-----|--------|
| Alert → Works ack | Under 30 min on-call |
| Confirmed missing → secure | Under 4 hours |
| Public reports closed with outcome | At least 90% |
| Orphan sensor alerts | Under 5% |
| Day-90 briefing delivered | Yes |

### Decisions

| Result | Action |
|--------|--------|
| KPIs mostly green | Expand sensors on proven corridors, keep same response model |
| Alerts good, response weak | Fix on-call / crews before buying more devices |
| Response good, yards still absorbing metal | Intensify Stage 4 with licensing / police |
| Whole loop weak | Stop or redesign - do not “scale failure” |

### Owners

Day-90 briefing: vendor drafts, Works / ICT / sponsor accept. Scale spend: LGA sponsor.

### Exit criteria

- [ ] Written day-90 report with KPI table and recommendation  
- [ ] Go / adjust / stop decision recorded  

---

## Roles at a glance

| Party | Owns in the solution |
|-------|----------------------|
| LGA Works | Corridors, crews, secure/replace, SLAs |
| LGA ICT | Accounts, hosting preference, data retention with vendor |
| Licensing / environment | Yard notices and inspections |
| Police / Area Command | Patrols, investigation, yard enforcement support |
| Vendor | Sensors, report intake, ops desk, packs, training, KPI report |

---

## Daily / weekly rhythm (live pilot)

```
  CONTINUOUS     sensor / citizen ---> ticket ---> respond
       |
  DAILY          sweep unacked + open life-safety
       |
  WEEKLY         hotspot pack + offline device check
       |
  MONTHLY        yard inspection sample + mark list refresh
       |
  DAY 90         scorecard ---> expand / fix / stop
```

| Cadence | Action |
|---------|--------|
| Continuous | Sensors + citizen reports → tickets |
| Every alert | Ack → assign → secure/replace → close |
| Daily | Review unacked / open life-safety tickets |
| Weekly | Hotspot pack to Works + liaison. Spot-check offline devices |
| Monthly | Yard inspection sample + mark-list refresh |
| Day 90 | Full scorecard and scale decision |
---

## Tooling map (what software does vs humans)

| Stage | Software helps | Humans still must |
|-------|----------------|-------------------|
| Prepare | Asset register, user roles | Pick sites, paint marks, name on-call |
| Prevent | ID export, custody templates | Install frames/materials, write contracts |
| Detect | Sensor ingest, WA/webhook stub, tickets | Watch optional CCTV, maintain power/SIM |
| Respond | State machine, SLA clocks, photos ref | Drive to site, barricade, replace |
| Deny cash-out | Hotspot export, static yard packs | Inspect yards, refuse lots, prosecute |
| Learn | KPI snapshot | Decide budget and next LGA |

Ops desk entry (when running locally): `python app_web.py` → `/ops`.  
Automated checks: `python -m unittest discover -s tests -v`.

---

## Explicitly out of this playbook

- How to defeat sensors, locks, marks, cameras, or yard checks  
- City-wide install on day one without a working response roster  
- Vendor replacing police or scrap regulators  

---

## Related files

| File | Use |
|------|-----|
| This playbook | **Run** the solution |
| `GOV_PILOT_PROPOSAL.md` / `ONE_PAGER_LEAVE_BEHIND.md` | **Sell** the pilot |
| `PHASE_1_REQUIREMENTS.md` | Feature acceptance for build |
| `SOLUTION_BRIEF.md` | Design background |
| `MANUAL_TEST.md` | Owner sign-off leftovers (live WA / field hardware) |
