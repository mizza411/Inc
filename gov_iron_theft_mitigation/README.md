# Public Iron Asset Protect (GOV-IRON-THEFT-1)

B2G pilot stack: detect missing public iron, ticket Works response, export hotspot packs.  
Sell to LGs / MDAs. **No thief-bypass content.**

## Docs

| File | Audience |
|------|----------|
| `SOLUTION_BRIEF.md` | Internal design |
| `GOV_PILOT_PROPOSAL.md` | Gov proposal (owner fills blanks) |
| `PHASE_1_REQUIREMENTS.md` | F1–F12 acceptance criteria |
| `MANUAL_TEST.md` | Owner once at sign-off |

## Run (Phase 3–4)

```powershell
cd C:\dev\Inc\gov_iron_theft_mitigation
python run_demo.py
python -m unittest discover -s tests -v
python app_web.py
# Ops desk:  http://127.0.0.1:8765/ops
# Webhook:   POST /webhooks/whatsapp  header X-Stub-Token: iron-protect-pilot-stub
```

Stdlib only. No Hub card, tray, or auto-launch unless you opt in later.

## Package layout

`iron_protect/` — assets, tickets, ingest_*, hotspots, kpis, auth_roles, packs_static, whatsapp_webhook, web_ui, store, service
