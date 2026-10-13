# GOV-IRON-THEFT-1 — Phase 1 requirements (one-LGA pilot)

**Track:** GOV-IRON-THEFT-1  
**Date:** 2026-10-13  
**Audience:** Internal (build + sales prep). Not a gov send-file.  
**Aligns with:** `GOV_PILOT_PROPOSAL.md` KPIs and 90-day scope  
**Owner fills LGA blanks** on the proposal separately. This file stays generic.  
**Hard rule:** no content that helps thieves bypass controls  
**Build rule:** Phase 1 = requirements only. No product scaffold until Phase 3 OK.

Cloud-safe: yes (tracked docs only).

---

## A. Requirements

### A1. App / product requirements

| Item | Decision for v1 pilot |
|------|------------------------|
| Who it is for | LGA Works + ICT operators, with read packs for police liaison |
| Core problem | Public iron stolen or missing, detected late, hard to prove and close out |
| Must-have | Asset register, citizen report intake, sensor alerts for pilot set, ticket → assign → close, weekly hotspot export, KPI counters |
| Nice-to-have (not pilot blockers) | RFID lookup UI, USSD (WhatsApp-first OK), map tiles offline pack, automated yard API |
| Platforms | Web ops dashboard (desktop-first). Mobile browser OK. WhatsApp for public report. No tray / Hub unless owner opts later |
| Offline vs online | Dashboard online. Field photo capture may queue if signal drops, then sync |
| Data storage | Vendor-hosted or Council-hosted per MoU. No personal owner money/IDs in repo. Pilot data retention in MoU |
| Auth | Named Council users + vendor admin. Role: Works dispatcher, Works crew (limited), ICT admin, read-only liaison |

### A2. Feature requirements (acceptance criteria)

| ID | Feature | Done when |
|----|---------|-----------|
| F1 | **Asset register** | Operator can create/edit an asset with: unique ID, type (cover / railing / barricade / other), lat/long or map pin, photo, corridor label, install/check date. List filters by corridor and status (present / missing / secured). |
| F2 | **Marking support** | Each asset shows its public ID string for stencil / tag. Export CSV of IDs + locations for field team. |
| F3 | **Citizen report channel** | Public can submit missing-asset report via WhatsApp (or documented USSD later) with free text + location. Creates a ticket linked to nearest asset if matched, else unmatched queue. |
| F4 | **Sensor alert intake** | Pilot devices (20–50) can create a ticket of type `sensor_alert` with asset ID + timestamp. Failed device heartbeat visible as `device_offline` (ops visibility only, not a thief guide). |
| F5 | **Ops tickets** | Ticket states: new → acknowledged → assigned → secured / replaced / false_alarm / closed. Assignee and timestamps recorded. |
| F6 | **On-call acknowledgement** | From `sensor_alert` or life-safety report, time-to-acknowledge is measurable. Dashboard shows unacked alerts older than threshold. |
| F7 | **Crew outcome** | Works user can mark secured (temporary barricade) or replaced, with optional photo. Closes or advances ticket per rules. |
| F8 | **Weekly hotspot pack** | One-click or scheduled export: counts by corridor, open vs closed, top locations, last 7 days. PDF or markdown + CSV. Safe for liaison (no bypass detail). |
| F9 | **Yard engagement pack** | Static docs downloadable: yard notice template + inspection checklist (Council enforces). Not a live integration in Phase 3 MVP unless scoped later. |
| F10 | **KPI dashboard** | Shows the Phase 1 KPI set below for the pilot window. Day-90 snapshot exportable. |
| F11 | **Roles / access** | ICT can add/disable users. Liaison role cannot edit tickets. Audit log of login and ticket state changes. |
| F12 | **Training mode** | Sample corridor with fake assets for demo without touching live pilot data. |

### A3. Pilot scope bounds (one LGA)

| Bound | Value |
|-------|--------|
| Duration | 90 days from go-live |
| Sensorized assets | 20–50 life-safety points, chosen with Works |
| Geography | One LGA (name on proposal, not required in this file) |
| Report channel | WhatsApp-first for pilot |
| Crews | Council Works (vendor does not replace covers unless MoU says otherwise) |
| Scale | No city-wide rollout in pilot contract |

### A4. KPIs (must match proposal defaults unless MoU annex changes them)

| KPI | Default target | How measured |
|-----|----------------|--------------|
| Alert → Works acknowledgement | Under 30 minutes in on-call hours | `acked_at - alert_at` on sensor tickets |
| Confirmed missing life-safety → secure / barricade | Under 4 hours (or stricter Works SLA) | `secured_at - confirmed_missing_at` |
| Public reports closed with outcome | At least 90% | Closed tickets / all public-report tickets |
| Orphan sensor alerts | Under 5% | Alerts never acknowledged / all sensor alerts |
| Day-90 briefing delivered | Yes | Report file accepted by sponsor |

### A5. Task / delivery requirements

| Item | Requirement |
|------|-------------|
| Dependencies | MoU or written pilot approval, Works corridor list, on-call names, SIM/power plan for sensors |
| Risks | Orphan alarms, procurement delay, WhatsApp number abuse, sensor power loss |
| Testing | Automated tests for ticket state machine + KPI math before UI polish. Manual only for WhatsApp live and field install |
| Rollout | Days 1–14 setup, 15–75 operate, 76–90 KPI freeze (see proposal) |
| Out of scope | Police replacement, scrap licensing product, bypass/defeat content, Hub/tray/auto-launch, cloning foreign brands |

### A6. Assumptions (non-blocking)

1. Council provides site access and a Works dispatcher account within 14 days of kick-off.  
2. Sensor hardware vendor or kit is chosen in Phase 3 design (this phase does not lock a brand).  
3. English UI for v1. Local-language WhatsApp auto-replies can be Phase 4+.  
4. Pricing stays on owner-filled proposal / local quote, not in this file.  

### A7. Open questions (non-blocking for Phase 1 done)

1. Preferred host: vendor cloud vs Council premises?  
2. WhatsApp Business API vs shared phone + manual intake for first pilot?  
3. Does ICT require NITDA / data-residency wording in MoU?  

---

## B. Module plan (for Phase 3 — do not build yet)

Keep files under ~500 lines. Suggested split when scaffolding starts:

| Module | Responsibility |
|--------|----------------|
| `assets` | Register CRUD, ID export |
| `tickets` | State machine, assignees, timestamps |
| `ingest_reports` | WhatsApp/webhook → ticket |
| `ingest_sensors` | Device alert → ticket (no defeat docs) |
| `hotspots` | Weekly pack export |
| `kpis` | Counters aligned to section A4 |
| `auth_roles` | Users and roles |
| `packs_static` | Yard notice + checklist files |

---

## C. Phase 1 done-when

- [x] Product / feature / delivery requirements written  
- [x] Acceptance criteria per feature (F1–F12)  
- [x] Pilot bounds and KPIs aligned to `GOV_PILOT_PROPOSAL.md`  
- [x] Out of scope and hard rule restated  
- [x] Module plan listed without scaffolding code  
- [x] Owner confirmed they fill LGA / contact / fee blanks on the proposal themselves  

**Phase 1 complete.** Next authorized build step is Phase 3 only after owner OK (Phase 2b pricing optional in parallel).
