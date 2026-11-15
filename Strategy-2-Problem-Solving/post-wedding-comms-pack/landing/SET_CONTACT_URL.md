# Set CONTACT_URL (no WhatsApp in chat or git)

**Goal:** Make **Request access** on the landing page open a public, non-phone contact method.  
**File to edit:** `landing/config.js` → `CONTACT_URL`  
**Do not** put a phone number in that file or in Cursor chat.

---

## Pick one (2–5 minutes)

### Option A — Google Form (recommended for Phase 0b)

**Privacy lock (2026-07-30 / this thread):** Do **not** create the Form under your **personal** Google account if your real name would show to respondents. Prefer a **brand Google account** whose display name is `Post-Wedding Comms Pack` (or similar). Alternatives: product IG as `CONTACT_URL`, or brand mailto — never personal Gmail Form / personal-name mailto.

1. Open [Google Forms](https://forms.google.com) while signed into the **brand** account → blank form.
2. Title: `Post-Wedding Comms Pack — early access`
3. Add questions (short answer / multiple choice):

| # | Question | Type |
|---|----------|------|
| 1 | First name | Short answer |
| 2 | City (Abuja / Lagos / other) | Short answer |
| 3 | Approx. guest count | Short answer |
| 4 | Would you pay ₦10,000 flat for self-serve thank-you drafts + WhatsApp export? | Multiple choice: Yes / No / Maybe |
| 5 | Prefer self-serve app or ₦15k done-for-you drafts? | Multiple choice |
| 6 | How should we reply? (email or IG handle — optional) | Short answer |

4. **Send** → copy the link (`https://forms.gle/...` or `docs.google.com/forms/...`).
5. Paste into `config.js`:

```js
CONTACT_URL: "https://forms.gle/PASTE_YOUR_LINK_HERE",
```

6. Save. Open `landing/index.html` locally → click **Request access** → confirm the form opens.

### Option B — mailto (no Form)

```js
CONTACT_URL: "mailto:YOUR_EMAIL@example.com?subject=ACCESS%20%E2%80%94%20Post-Wedding%20Comms%20Pack",
```

Use an email you are OK having in a public GitHub Pages file.

### Option C — Instagram DM

```js
CONTACT_URL: "https://ig.me/m/YOUR_HANDLE",
```

Only after the IG account exists (per `LAUNCH_PLAN.md`: after landing/host).

---

## What “done” looks like

```js
window.PWCP_LANDING = {
  CONTACT_URL: "https://forms.gle/....",  // non-empty
  WHATSAPP_E164: "",                      // stay empty in committed file
  APP_URL: "",                            // later, after Streamlit
};
```

Landing button **Request access** opens that URL. No phone required.

---

## Optional: wire it via chat without sharing a phone

If you want the agent to edit `config.js` for you, reply with **only** the public Form / mailto / IG URL (never a phone number).  
Or edit the file yourself and say “CONTACT_URL set” when finished.
