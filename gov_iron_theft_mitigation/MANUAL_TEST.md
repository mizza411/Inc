# MANUAL_TEST — Public Iron Asset Protect (GOV-IRON-THEFT-1)

Automate-first. Agent runs smokes during build. You run this **once** at solution-complete sign-off.

## Already automated (do not re-test manually)

- Phase 3 domain: assets, tickets, roles, sensors, KPIs, hotspots, static packs  
  (`tests/test_phase3_smoke.py`)
- Phase 4: WhatsApp stub parse (flat + nested), stub token check  
- Phase 4 HTTP: `/health` phase 4, `/ops` HTML, `POST /webhooks/whatsapp` create ticket, bad token 401  
  (`tests/test_phase4_smoke.py`)

## Manual leftovers

### M1 — Live WhatsApp Business API (not the stub)

- **Why not automated:** real Meta / WA Business credentials and Council phone policy  
- Steps: point production webhook at a secured endpoint (not the stub token) → send a real location message → confirm ticket  
- Expected: ticket appears for Works within agreed SLA  
- **Waive** until a live WA number is provisioned  

### M2 — Field sensor install on a real cover

- **Why not automated:** physical site, power, Works access  
- Steps: install one pilot device with Works → supervised lift test → acknowledge on `/ops`  
- Expected: alert ticket, hole secured per Works rules  
- **Waive** until hardware pilot  

### M3 — Ops desk visual glance (optional)

- **Why not automated:** subjective layout readability  
- Steps: `python app_web.py` → open `http://127.0.0.1:8765/ops` → seed asset → simulate WA → advance ticket  
- Expected: tables update, flash messages readable on desktop and phone-width window  

## Sign-off

- [ ] Automated Phase 3 + 4 suites green on this machine  
- [ ] M1 live WA (or waived)  
- [ ] M2 field sensor (or waived)  
- [ ] M3 optional glance  

**Ready for single manual pass — run `MANUAL_TEST.md`** when you treat the pilot software MVP as solution-complete (hardware/WA still may be waived).
