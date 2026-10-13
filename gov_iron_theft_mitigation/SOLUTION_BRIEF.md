# Government iron theft — tech-led B2G solution brief

**Track ID:** GOV-IRON-THEFT-1  
**Commercial intent:** Monetize — sell to governments (LGs / MDAs)  
**Date:** 2026-10-13  
**Status:** Phase 0 brief frozen (no product scaffold yet)  
**Hard rule:** No content that helps thieves bypass controls  

**Run the solution (start→finish):** [`SOLUTION_PLAYBOOK.md`](SOLUTION_PLAYBOOK.md)  
**Gov-facing pilot proposal (send after filling blanks):** [`GOV_PILOT_PROPOSAL.md`](GOV_PILOT_PROPOSAL.md) — this file stays internal.  
**One-page leave-behind:** [`ONE_PAGER_LEAVE_BEHIND.md`](ONE_PAGER_LEAVE_BEHIND.md)  
**Phase 1 requirements (internal):** [`PHASE_1_REQUIREMENTS.md`](PHASE_1_REQUIREMENTS.md)

---

## 1. Problem framing

Public iron (manhole covers, railings, barricades, poles, similar assets) is stolen because:

| Driver | Plain meaning |
|--------|----------------|
| High scrap value | Cast iron / steel pays at yards even when the asset is public |
| Easy to move | Covers and barriers are detachable and stackable |
| Weak custody chain | After removal, proving ownership at the yard gate is hard |
| Diffuse ownership | Road, water, telecom, LG — many owners, slow joint response |
| Low detection latency | Theft often noticed days later, so recovery is rare |
| Asymmetric risk | Thief gets cash same day. Agency bears injury, flood, and traffic risk |

Core insight from developed-country practice: theft shrinks when **scrap demand is policed as hard as the street asset**, and when **time-to-know** falls from days to minutes.

---

## 2. International practice patterns (guide, not brand copy-paste)

Five layers that usually appear together:

1. **Detection** — sensors on high-risk assets, public reporting, corridor CCTV where power and response exist  
2. **Custody** — who removed metal, why, where it went (works + scrap)  
3. **Scrap-market controls** — licensed yards, refuse unmarked or gov-marked iron, purchase records, inspections  
4. **Marking** — visible and covert marks so a yard or officer can recognize public infrastructure  
5. **Policing coordination** — hotspots, night routes, joint ops with utilities and LG  

Developed-country lesson in one line: make stolen gov iron **hard to cash**, not only hard to lift.

---

## 3. Main chapter — tech to prevent and detect

### 3.1 Detection stack

| Tech | Role | Best use |
|------|------|----------|
| Lift / tilt / open sensors on covers | Instant “this cover moved” alert | Highways, deep chambers, known hotspots |
| Vibration / cut sensors on railings and barriers | Alert on sawing or yank | Bridges, median barriers, site fencing |
| Fixed CCTV + basic motion at corridors | Deterrence and evidence | Night theft routes with power and monitoring |
| Patrol body or vehicle cams on hotspot runs | Evidence when sensors are sparse | LG / police joint nights |
| Crowd report channel (WhatsApp / USSD / simple app) | Humans as sensors city-wide | Everywhere sensors cannot go |

**Design rule:** every alert needs an **owner on call** and a **replace-or-secure SLA**. No orphan alarms.

### 3.2 Prevention / hardening tech

| Tech | Role |
|------|------|
| Locked or retained frames (standards-approved) | Harder lift without tools and time |
| Composite or low-resale covers | Lower melt value, less motive |
| Visible unique ID + covert mark | Yard / police recognition |
| GPS / RFID / NFC tags | Trace if recovered or presented at a yard |
| Contractor digital custody log | Removed metal accounted for on works |

### 3.3 Ops tech (glue)

| Tech | Role |
|------|------|
| Asset register (photo, ID, lat/long, type, last check) | Know what exists before it vanishes |
| Ops dashboard | Report or sensor → ticket → crew → replaced |
| Hotspot map (7 / 30 day) | Where to put next sensors and patrols |
| Shared feed to area command | Police see repeat corridors and yards |

### 3.4 Scrap-market tech (detection at cash-out)

| Tech | Role |
|------|------|
| Licensed dealer digital purchase log | Who sold what ferrous lot, when |
| Yard CCTV at weighbridge / intake | Deterrence and investigation aid |
| Mark / ID lookup for officers at gate | Is this registered public iron? |

Street sensors plus scrap records beat either alone.

### 3.5 System view

```
                    +------------------+
                    | PUBLIC REPORT    |
                    | WhatsApp/USSD/app|
                    +--------+---------+
                             |
   +----------+       +------v------+       +----------------+
   | SENSORS  |------>| OPS DESK /  |------>| CREW: secure / |
   | tilt/vib |       | DASHBOARD   |       | replace (SLA)  |
   | + CCTV   |       +------+------+       +--------+-------+
   +----------+              |                       |
                             v                       v
                      +--------------+        +--------------+
                      | HOTSPOT MAP  |        | ASSET REG +  |
                      | + police MoU |        | ID / RFID    |
                      +------+-------+        +------+-------+
                             |                       |
                             v                       v
                      +--------------------------------------+
                      | SCRAP GATE: license, log, CCTV, ID   |
                      | lookup — hard to cash stolen iron    |
                      +--------------------------------------+
```

---

## 4. Nigeria / gov-fit options

### Near-term (weeks to about 3 months)

1. Asset register + photo IDs for top risk corridors  
2. WhatsApp / USSD “missing cover” → ticket list / map  
3. Pilot **20–50** sensorized covers (life-safety sites only) with a named night responder  
4. Paint / stamp codes + yard notice (unmarked or gov-marked iron refused)  
5. Weekly hotspot printout for LG works + area command  

### Medium-term (about 6–24 months)

1. Expand sensors only where alert→response rate is proven  
2. Shared dashboard across LG / works / water / police liaison  
3. Licensed yards: mandatory digital ferrous purchase logs + intake CCTV  
4. RFID / NFC on new stock + lookup for inspectors  
5. Composite / low-resale covers on new installs where standards allow  
6. Selective corridor CCTV on proven hotspots (power + retention policy)  

---

## 5. Commercial offer (B2G — sell to governments)

**Positioning:** managed **detect + prove + respond** package. Government keeps arrest powers, scrap licensing, and street policing.

| Package slice | What government buys | What the vendor delivers |
|---------------|----------------------|--------------------------|
| Detect | Alerts when high-risk assets move | Sensor pilot + report channel |
| Prove | This metal is ours | Marking + asset register + optional RFID / NFC |
| Respond | Missing → crew ticket → replaced | Ops dashboard + SLA workflows |
| Deter cash-out | Advice and SOPs for yards (gov enforces) | Playbooks, training, inspection checklists |
| Prove ROI | Fewer open holes / faster replace | Hotspot + SLA reports for directors |

**First-sale wedge:** one LGA pilot — 20–50 life-safety covers + report channel + dashboard + weekly hotspot pack for works and area command.

**You do not sell:** arrest powers, scrap licensing, or street policing. You sell the system that makes those work.

---

## 6. Recommendations (owners + risks)

| ID | Action | Owner | Risk if weak |
|----|--------|-------|--------------|
| T1 | Life-safety sensor pilot + 24h on-call | LG works + ICT (vendor supports) | Alarms with no crew = wasted spend |
| T2 | Report channel + dashboard MVP | LG ICT / digital unit + vendor | Detection stays days-late |
| T3 | Mark + register before mass IoT | Inventory / roads | Gadgets with no proof of ownership |
| T4 | Scrap log + yard inspections | Licensing + police | Thieves still cash out same night |
| T5 | Police hotspot pack from dashboard | Area command | Sensors without deterrence |
| T6 | One LGA end-to-end pilot, then scale | State / LG lead | Nationwide tech with no ops muscle |

### Commercial risks

| Risk | Mitigation |
|------|------------|
| Sensors with no night responder | Contract includes named on-call + SLA, or vendor staffs first-line triage |
| Procurement slow | Pilot MoU / innovation route, fixed price, clear KPI |
| “We already have CCTV” | Sell time-to-replace + register + scrap SOP, not cameras alone |
| Liability if someone falls in a hole | Contract: gov owns assets / response. Vendor owns software / uptime |

---

## 7. Explicitly out of scope

- Anything that helps thieves bypass sensors, cameras, locks, tags, or yard checks  
- Lock picking, sensor blind spots, evasion routes, how yards evade inspections  
- Cloning a foreign “smart manhole” brand as the product  

---

## 8. Layout and next phases

**Folder:** `gov_iron_theft_mitigation/` at Inc root (brief + later offer pack). No Hub card, tray, or auto-launch unless owner opts in later.

| Phase | Goal |
|-------|------|
| **0** | This brief frozen on disk — done |
| **1** | Requirements + one-LGA pilot scope + acceptance criteria — done (`PHASE_1_REQUIREMENTS.md`) |
| **2a** | Gov pilot proposal — done (owner fills blanks) |
| **2b** | One-page leave-behind — done (fee blank in repo) |
| **3** | Scaffold `iron_protect` — done (2026-10-13) |
| **4** | Ops UI + WhatsApp stub + smokes — done (2026-10-13) |

---

## 9. Done-when (Phase 0)

- [x] Problem framing written  
- [x] International patterns in plain language  
- [x] Tech prevention and detection as main chapter  
- [x] Nigeria near-term vs medium-term options  
- [x] B2G recommendations with owners and risks  
- [x] Out-of-scope / no bypass rule stated  
- [x] Commercial intent recorded (sell to governments)  
