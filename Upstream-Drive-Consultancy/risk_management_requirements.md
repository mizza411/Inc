# Risk management consultancy requirements (Line D)

**Company:** Upstream Drive Consultancy  
**Task:** UDC-1 · Phase 2b  
**Date:** 2026-09-24  
**Who it is for:** You, before selling Line **D**.  
**Pair with:** `offer_lines.md` · `company_requirements.md` · `sources.md`  
**Not this file:** Cert stamps (Line A). Test methods (Line B). Monthly watch ops (Line C). Physical guard SaaS. Legal advice.

Line D helps a **named decision-owner** see risks, choose treatments, and own residual risk — in plain language. Upstream does **not** carry the client’s residual risk.

---

## 1. What you sell

| Shape | You deliver | Done when |
|-------|-------------|-----------|
| **Risk picture (project)** | Scope, context, risk register (or equivalent list), ranked priorities, treatment options mapped to owner decisions | Owner can name top risks and what they will do / accept / transfer |
| **Risk refresh (retained)** | Periodic update of the register against agreed triggers (e.g. new system, new vendor, tender, incident) | Calendar or trigger met; delta note left with owner |
| **Decision support** | Short options note: treat via Line A / B / C, insurance, process change, or accept — with who decides | Owner signs or emails a clear choice (accept / treat / defer) |

You may align treatments to Upstream Lines **A–C** (prep, authorised test, watch). You may point at building / DC research for **physical** context in writing. You do not become their guard company or their certifier by selling D.

---

## 2. Minimum method (keep it thin)

Use a short, repeatable loop. Framework names (e.g. ISO 31000 **pattern**) are optional labels — **not** a claim that Upstream is ISO-certified or that the client is.

| Step | Plain meaning | Artefact |
|------|---------------|----------|
| 1. Context | What the business does; what is in / out of scope | One-page context |
| 2. Identify | What can go wrong for that scope (IT, data, vendors, continuity — Nigeria-first) | Risk list |
| 3. Analyse | How bad / how likely in owner language (not fake precision) | Columns on the list |
| 4. Evaluate | What needs a decision now vs later | Rank / heat or simple High–Med–Low |
| 5. Treat | Options: avoid, reduce, transfer, accept — link A/B/C where useful | Treatment table |
| 6. Own | Named person accepts residual risk | Sign-off or email on file |
| 7. Review | When to look again | Trigger list + next date |

**Do not** invent decimal “risk scores” that pretend science. **Do not** promise “no incidents if you hire us.”

---

## 3. Nigeria-first risk themes (starter menu)

Use only what fits the client. Mark unknowns **check this**.

| Theme | Why it shows up | Typical treatment pointers |
|-------|-----------------|----------------------------|
| Power / continuity | Grid unreliability for many firms; diesel and UPS discipline | Continuity plan; vendor SLAs; building operator clauses — not Upstream running generators |
| Personal data / NDPA | Act + GAID; filings; processor chains | Line **A** prep; contracts; retention — not “NDPR certified” |
| Cyber access | Wrong login, wrong change, silent copy | Line **A** controls; Line **B** only with letter; Line **C** watch if list exists |
| Vendor / third party | Outsourced IT, cloud, DPCO, guards | Clause packs; who holds keys; exit |
| People / privilege | Shared admin, no leave backup | Access hygiene; lean roles on client side |
| Fraud / payment | Where money or cards touch systems | PCI readiness (**A**); scoped test (**B**) if authorised |
| Single site / Lagos concentration | Site loss pattern in DC research | Multi-site or colo choice — advisory only |

Physical hall Tier claims: use **Tier‑4–class** teaching language; never stamp a hall Tier IV unless verified (`sources.md`).

---

## 4. What must exist before first Line D invoice

On top of `company_requirements.md` shared floor:

| # | Requirement |
|---|-------------|
| 1 | Named **decision-owner** (who accepts residual risk) — not only an IT contact |
| 2 | Written scope: in / out (systems, sites, processes, vendors) |
| 3 | Contract that says Upstream advises; client owns residual risk; no incident guarantee |
| 4 | PI that covers advisory / risk consultancy (**check this** wording) |
| 5 | Delivery person identified (see `lean_roles.md`) — risk facilitator ≠ authorised tester by default |
| 6 | Clear handoff if treatment needs A, B, or C (separate contract / letter) |

---

## 5. Refusals (Line D)

| Do not | Why |
|--------|-----|
| Sell D as a certificate or “you are compliant” | That is stamp language — Line A handoff |
| Sell D as a penetration test or monthly watch | Wrong line shape |
| Carry or insure their residual risk by brochure claim | Risk transfer needs real insurance / contract — not markdown |
| Run their SOC or fix live systems under a “risk” fee | Separate paper if ever |
| Physical security-as-a-service | Company lock |
| Attack methods in the risk report | Same rule as Line B brochures |
| Invoice D before this file existed and was owner-read | Pack lock from Phase 2a |

---

## 6. Who pays

| Buyer pain | Buy D when |
|------------|------------|
| Board / exec wants a clear risk picture before spending on ISO / test / watch | Scope is fuzzy; they need priorities first |
| Tender asks for a risk assessment alongside security questionnaire | Deliver picture + point to A for evidence build |
| After an incident or near-miss | Refresh register; do not pretend the incident report is a cert |
| Expanding vendors or a new product line | Context changed; old list is stale |

If they only want a gap list against ISO/NDPA/PCI, that may be **A**, not D. If they only want alerts answered, that is **C**.

---

## 7. Lean delivery (pointer)

One strong facilitator can open D. Authorised testing skill and weekday watch triage are **different** seats — see `lean_roles.md` (Phase 2c). Do not pretend one junior does A+B+C+D alone.

---

## 8. Related

| Doc | Role |
|-----|------|
| `offer_lines.md` | Line D in the menu |
| `sources.md` | Citations and check-this |
| [`../dc-security-nigeria-research/start_it_security_as_service_ng.md`](../dc-security-nigeria-research/start_it_security_as_service_ng.md) | A–C product map |
| [`../dc-security-nigeria-research/ict_technical_roles.md`](../dc-security-nigeria-research/ict_technical_roles.md) | Keep / hire / clause + automate (building view) |
