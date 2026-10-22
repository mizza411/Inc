# Public Iron Asset Protect

**Status:** prospect  
**Added:** 2026-10-22  
**Source run:** not from a daily formulation dump — owner track **GOV-IRON-THEFT-1** under `../gov_iron_theft_mitigation/`  
**Related research (optional pointer only — do not move files):** `../gov_iron_theft_mitigation/` (`SOLUTION_PLAYBOOK.md`, `GOV_PILOT_PROPOSAL.md`, `ONE_PAGER_LEAVE_BEHIND.md`, `iron_protect/` ops MVP, `media/` video previs)

> Graduation into `Started-Businesses/` requires **explicit user approval**. Agents must not auto-graduate this file.

## Problem

Local governments and MDAs lose manhole covers, railings, and roadside barricades to scrap theft. Citizens often notice days later. Open chambers cause injury and flood risk. Stolen iron is still easy to sell at yards. Councils need faster detection, clearer ownership marks, a Works response loop, and scrap-gate friction, not cameras alone.

## Why this is a prospect

- **Urgent / expensive / frequent:** life-safety holes and repeat corridor losses cost replacements, liability, and trust
- Fits Nigeria now: scrap demand for ferrous metal stays strong, Works response is often slow, and yard cash-out is weakly checked
- Fits B2G operator path: sell a **90-day one-LGA pilot** (detect + ticket + respond + yard packs), keep police and licensing with government
- Commercial intent locked: **monetize, sell to LGs / MDAs**. Original offer, not a cloned foreign smart-cover brand
- Working pack already exists: playbook, gov proposal, leave-behind, stdlib ops desk + WhatsApp webhook stub, Phase 3–4 smokes green
- **Hard rule:** no content that helps thieves bypass sensors, locks, marks, or yard checks

## MVP sketch

- **Scope:** One-LGA pilot — register and mark **20–50** life-safety assets, citizen report channel (WhatsApp-first), sensor alerts on the pilot set, ops tickets (ack → assign → secure/replace → close), weekly hotspot pack for Works + police liaison, yard notice + inspection checklist, day-90 KPI report
- **Est. cost (USD):** software MVP already scaffolded (stdlib). Pilot fee and hardware kit quoted per LGA (fee blanks stay on proposal / local quote, not invented here). Overall build target remains within the usual ≤ ~$30k software band unless hardware volume expands
- **Platforms:** web ops desk (`app_web.py` / `/ops`), WhatsApp/webhook ingest stub, optional USSD later. No Hub / tray / auto-launch unless owner opts in
- **Target:** one LGA Works + ICT sponsor first, then expand corridors / second LGA after day-90 scorecard
- **Regulatory / role notes:** Council owns assets and street response. Vendor owns software/uptime and packs. Police and scrap licensing stay with competent authorities

## Next validation

| Date | Action | Done? |
|------|--------|-------|
| 2026-10-29 | Fill leave-behind / proposal blanks (LGA name, vendor contact, pilot fee in local quote) | [ ] |
| 2026-11-12 | Book 45-minute Works + ICT meeting for one named LGA (corridors + on-call names) | [ ] |
| 2026-11-26 | MoU or written pilot approval path clear, or park / pivot decision | [ ] |

## Notes

- Run the solution: `../gov_iron_theft_mitigation/SOLUTION_PLAYBOOK.md` (Prepare → Prevent → Detect → Respond → Deny cash-out → Learn/scale)
- Sell pack: `GOV_PILOT_PROPOSAL.md`, `ONE_PAGER_LEAVE_BEHIND.md`
- Media previs: `media/VIDEO_PRODUCTION_PACKAGE.md`, `media/chatgpt_workflow_storyboard.jpg` (mock Day-90 numbers are illustrative only)
- Funding sibling: `public-iron-asset-protect-funding.md` (blanks only in tracked file)
- Do not graduate to `Started-Businesses/` until the owner explicitly approves
- Do not merge with FIR site reports, Tegrid GTM, or SME workshop loss-prevention
