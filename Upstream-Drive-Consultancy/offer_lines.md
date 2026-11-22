# Offer lines — Upstream Drive Consultancy

**Company:** Upstream Drive Consultancy  
**Task:** UDC-1 · Phase 2a  
**Date:** 2026-09-24  
**Who it is for:** You, deciding what the firm sells under one name.  
**Pair with:** `company_requirements.md` (floor before invoice).  
**Maps to research:** IT SecaaS Offers A–C in `dc-security-nigeria-research/`; **D** is Upstream’s risk line (detail in Phase 2b).

```
  UPSTREAM DRIVE CONSULTANCY
  ┌──────────────────────────────────────────────┐
  │  A  Cert prep + training                     │
  │  B  Authorised testing (letter first)        │
  │  C  Monthly IT watch                         │
  │  D  Risk management consultancy              │
  └──────────────────────────────────────────────┘
           ≠ Physical security-as-a-service
```

---

## Line map (1:1 with SecaaS + risk)

| Line | Shape | You deliver | You do **not** deliver | Research detail |
|------|-------|-------------|-------------------------|-----------------|
| **A — Certs & training** | Project (+ workshops) | Gap list, policies, evidence tracker, training; handoff to who stamps | The ISO / PCI / Commission stamp itself | [`start_it_security_as_service_ng.md` §7 Offer A](../dc-security-nigeria-research/start_it_security_as_service_ng.md) |
| **B — Authorised testing** | Project + **written letter** | Scoped report on named systems and dates | Attack how-tos; access without a letter; “you are certified” | [`start_it_security_as_service_ng.md` §8 Offer B](../dc-security-nigeria-research/start_it_security_as_service_ng.md) |
| **C — IT watch** | Monthly | Acknowledge alerts on a named list in sold hours; tell their named person | Physical patrol; free monthly break-in; fixing servers unless a separate contract | [`start_it_security_as_service_ng.md` §9 Offer C](../dc-security-nigeria-research/start_it_security_as_service_ng.md) |
| **D — Risk management** | Project or retained advice | Risk picture, priorities, treatment options, decision support for a named owner | Owning their residual risk; guaranteeing no incident; replacing their board | `risk_management_requirements.md` (Phase **2b**) |

---

## A — Certifications, readiness, and training

**v1 targets (lock):** ISO/IEC 27001 · Nigeria Data Protection Act readiness · PCI DSS readiness.

| Done when | Notes |
|-----------|--------|
| Written gap list against one named target | Client can see what is missing |
| Policies / lists / evidence a reviewer will ask for | Evidence-room coaching OK |
| Training with agenda + attendance + expectations sheet | Workshop ≠ certificate |
| Handoff names who stamps | Not Upstream unless a later lock + licence says so |

**Who pays (examples):** tender / bank wants ISO or questionnaire; NDPC filing prep; acquirer raised PCI.

**Do not say:** “We certified you,” “NDPR certified,” “we are your QSA / DPCO” unless listed/licensed.

---

## B — Authorised testing

**Hard rule:** Written authorisation for **named systems** and **named dates** before any access. Default **observe-only**. This pack **stops before any test method**.

| Must be in the letter | Why |
|-----------------------|-----|
| Both legal names; systems in / out | Scope fence |
| Calendar and hours | Excess access = same problem as no letter |
| Observe-only vs change | Default observe-only |
| Stop-now person + phone | Kill switch |
| Copy / retention / delete; report ownership | Evidence hygiene |
| “We are not issuing a security certificate” | Separate from Offer A |

**Company add-ons:** letter filed before access; PI that names authorised testing; practice environment **you own**.

**Do not say:** “licensed to hack”; sell “they will not see it was us”; fold a test into Line C’s monthly fee.

Cybercrimes Act s.6 (and related) — business boundary only; counsel reads the letter template (**check this**). Possible CNII: do not start on a casual letter.

---

## C — Monthly IT watch

| In the fee | Out of fee (unless second contract) |
|------------|-------------------------------------|
| Named systems; alert types; hours; acknowledge time | Build a programme from zero |
| Who you call; what you will not do | Issue a certificate |
| Note to their named person in business words | One-off test; fix servers yourself |

**Hours:** weekday window first (one triage + leave backup). Longer day / all-week only when people, power, and second path exist. Do not print “24/7” for one phone in bed.

**Data:** logs often hold personal data — NDPA processor terms; retention; breach notice **to client** so they can meet Commission clocks (**check this** counsel).

A monthly invoice is **not** authorisation to access — contract or attached letter must name systems and watch tooling.

---

## D — Risk management consultancy

**Status in this pack:** requirements live in `risk_management_requirements.md` (Phase 2b).

---

## Who pays (shared picture)

| Buyer pain | Buy |
|------------|-----|
| Bank / foreign customer / tender wants ISO or security questionnaire | **A** |
| Commission filing or privacy programme with no internal team | **A** |
| Acquirer raised PCI DSS | **A** (and maybe **B** after level is clear) |
| Board or tender wants a scoped test of systems they own | **B** |
| Named systems + someone to answer alerts in named hours | **C** |
| Board / exec needs a clear risk picture and treatment choices | **D** |

---

## Order of opening the company

1. Open **A** (NDPA prep → ISO prep → PCI readiness). Training sits here.  
2. Add **B** only with a letter checklist counsel has seen (**check this**). Observe-only default.  
3. Add **C** weekday watch only for a client whose list already exists. All-week last.  
4. Add **D** using `risk_management_requirements.md` (named decision-owner; client owns residual risk).  
5. Later options in A: DPCO licence; never claim QSA until the PCI council lists you.

---

## Explicit: not physical security as a service

| In this product | Out of this product |
|-----------------|---------------------|
| Policies, access lists, system alerts, authorised tests of **computer** systems | Guarding a gate, staffing a desk with a radio as the product |
| Advising that a hall needs cameras / badges (words on a page) | Operating their guard force or CCTV centre for a monthly fee |
| Pointing at building docs for who hires guards | Claiming “we are your physical SecaaS” |

If a buyer wants physical security as a service, that is a different company with different licences. **Check this** before you ever offer it.

---

## Related

| Doc | Role |
|-----|------|
| `company_requirements.md` | Floor before first invoice |
| `risk_management_requirements.md` | Line D detail (Phase 2b) |
| `lean_roles.md` | Who delivers each line (Phase 2c) |
| [`../dc-security-nigeria-research/start_it_security_as_service_ng.md`](../dc-security-nigeria-research/start_it_security_as_service_ng.md) | SecaaS cover |
