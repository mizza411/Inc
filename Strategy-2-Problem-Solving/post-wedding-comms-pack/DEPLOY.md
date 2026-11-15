# Deploy — Post-Wedding Comms Pack

**Goal:** Public landing + hosted Streamlit app URL for IG bio / Phase 0b.  
**Keep `PAYMENTS_DISABLED=1` until Phase 0b go** (≥2 couples yes to ₦10k).

---

## A — Landing (GitHub Pages)

Repo already includes static files under `landing/`.

**Expected URL after `main` is on GitHub Pages** (same pattern as Problem ID):

`https://mizza411.github.io/Inc/Strategy-2-Problem-Solving/post-wedding-comms-pack/landing/`

### Before sharing (privacy)

**Do not put your WhatsApp number in chat, commits, or public `config.js`.**

**Step-by-step:** [`landing/SET_CONTACT_URL.md`](./landing/SET_CONTACT_URL.md) (Google Form recipe + mailto / IG).

1. Edit committed `landing/config.js` with a **non-phone** contact only:
   - `CONTACT_URL` — Google Form, `mailto:…`, or Instagram `https://ig.me/m/yourhandle`
   - `APP_URL` — Streamlit Cloud URL (fill after section B)
2. Optional **local-only** WhatsApp tests: copy `config.local.js.example` → `config.local.js` (gitignored), set `WHATSAPP_E164` on your machine only.
3. Commit + push (when you choose) — confirm `config.local.js` is **not** staged.
4. Open the Pages URL; confirm **Request access** opens your Form / mailto / IG.

**Local preview:** open `landing/index.html` in a browser (or any static server).

---

## B — Streamlit Cloud (app host)

1. [share.streamlit.io](https://share.streamlit.io) → **New app**
2. Repo: your Inc fork/remote · Branch: `main`
3. Main file path:

   `Strategy-2-Problem-Solving/post-wedding-comms-pack/app.py`

4. **Secrets** (App settings → Secrets) — paste TOML:

```toml
LLM_PROVIDER = "deepseek"
DEEPSEEK_API_KEY = "sk-..."
PAYMENTS_DISABLED = "1"
PAYSTACK_AMOUNT_KOBO = "1000000"
# After Phase 0b go only:
# PAYSTACK_SECRET_KEY = "sk_live_..."
# PAYMENTS_DISABLED = "0"
```

5. Deploy → copy the `*.streamlit.app` URL into `landing/config.js` → `APP_URL`.
6. Re-push landing config (or edit on Pages) so “Open the app” works.

**Webhook (optional for v1):** `webhook_server.py` needs a separate host (Railway/Render). Sidebar “Verify reference” works without webhook for early pilots.

---

## C — Gate checklist (from `LAUNCH_PLAN.md`)

| Step | Owner |
|------|--------|
| `python run_automated_tests.py` green | Agent / you |
| Short `MANUAL_TEST.md` §B + §D | You (once) |
| Landing live + WhatsApp number set | You + this folder |
| Streamlit URL live | You (Cloud secrets) |
| Then IG + Phase 0b DMs | You |

Do **not** create the public IG page until landing (or app) URL is ready.
