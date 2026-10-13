"""HTML fragments for the Phase 4 ops desk (stdlib, no templates engine)."""

from __future__ import annotations

import html
from typing import Any


def page(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --bg: #e8eef2;
      --ink: #1a2b33;
      --accent: #0b6e4f;
      --card: #f7fafb;
      --line: #b7c5cc;
    }}
    body {{
      margin: 0;
      font-family: "Segoe UI", "IBM Plex Sans", sans-serif;
      background:
        radial-gradient(ellipse at top left, #d5e4ea, transparent 55%),
        linear-gradient(160deg, var(--bg), #dfe8e4 70%);
      color: var(--ink);
      min-height: 100vh;
    }}
    header {{
      padding: 1.25rem 1.5rem 0.5rem;
      border-bottom: 1px solid var(--line);
      background: rgba(247,250,251,0.85);
    }}
    header h1 {{
      margin: 0;
      font-size: 1.45rem;
      letter-spacing: 0.02em;
    }}
    header p {{ margin: 0.35rem 0 0; max-width: 40rem; }}
    nav a {{
      margin-right: 1rem;
      color: var(--accent);
      font-weight: 600;
    }}
    main {{ padding: 1rem 1.5rem 2rem; }}
    .grid {{
      display: grid;
      gap: 1rem;
      grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
    }}
    section {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 4px;
      padding: 0.9rem 1rem;
    }}
    section h2 {{ margin: 0 0 0.6rem; font-size: 1.05rem; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 0.92rem; }}
    th, td {{
      text-align: left;
      padding: 0.35rem 0.4rem;
      border-bottom: 1px solid var(--line);
      vertical-align: top;
    }}
    label {{ display: block; margin: 0.4rem 0 0.15rem; font-size: 0.85rem; }}
    input, select, textarea, button {{
      font: inherit;
      padding: 0.35rem 0.45rem;
      width: 100%;
      box-sizing: border-box;
    }}
    button {{
      margin-top: 0.65rem;
      background: var(--accent);
      color: #fff;
      border: 0;
      cursor: pointer;
      width: auto;
      min-height: 2.5rem;
      padding: 0.45rem 0.9rem;
    }}
    button:hover {{ filter: brightness(1.05); }}
    .flash {{
      background: #e3f2ea;
      border: 1px solid #9ccbb5;
      padding: 0.5rem 0.75rem;
      margin-bottom: 1rem;
    }}
    .muted {{ color: #4d5f68; font-size: 0.85rem; }}
    code {{ background: #eef3f5; padding: 0.1rem 0.25rem; }}
  </style>
</head>
<body>
  <header>
    <h1>Public Iron Asset Protect</h1>
    <p>Ops desk for one-LGA pilot — detect, ticket, secure. No bypass tooling.</p>
    <nav>
      <a href="/ops" title="Open ops desk">Ops</a>
      <a href="/health" title="Service health JSON">Health</a>
      <a href="/hotspots.md" title="Download hotspot markdown">Hotspots</a>
      <a href="/kpis" title="KPI JSON">KPIs</a>
    </nav>
  </header>
  <main>
    {body}
  </main>
</body>
</html>
"""


def ops_body(
    *,
    flash: str,
    tickets: list[dict[str, Any]],
    assets: list[dict[str, Any]],
    kpis: dict[str, Any],
) -> str:
    flash_html = (
        f'<div class="flash" role="status">{html.escape(flash)}</div>'
        if flash
        else ""
    )
    ticket_rows = []
    for t in tickets:
        ticket_rows.append(
            "<tr>"
            f"<td>{html.escape(str(t.get('ticket_id')))}</td>"
            f"<td>{html.escape(str(t.get('kind')))}</td>"
            f"<td>{html.escape(str(t.get('state')))}</td>"
            f"<td>{html.escape(str(t.get('asset_id') or '—'))}</td>"
            f"<td>{html.escape(str(t.get('text') or '')[:80])}</td>"
            "</tr>"
        )
    if not ticket_rows:
        ticket_rows.append('<tr><td colspan="5">No tickets yet.</td></tr>')

    asset_rows = []
    for a in assets:
        asset_rows.append(
            "<tr>"
            f"<td>{html.escape(str(a.get('asset_id')))}</td>"
            f"<td>{html.escape(str(a.get('corridor')))}</td>"
            f"<td>{html.escape(str(a.get('status')))}</td>"
            f"<td>{html.escape(str(a.get('public_mark')))}</td>"
            "</tr>"
        )
    if not asset_rows:
        asset_rows.append('<tr><td colspan="4">No assets — seed from form.</td></tr>')

    kpi_bits = "".join(
        f"<li><strong>{html.escape(k)}</strong>: {html.escape(str(v))}</li>"
        for k, v in kpis.items()
    )

    return f"""
{flash_html}
<div class="grid">
  <section>
    <h2>KPIs</h2>
    <ul>{kpi_bits}</ul>
    <p class="muted">Targets: ack under 30 min, secure under 4 h, reports closed 90%+.</p>
  </section>
  <section>
    <h2>Simulate WhatsApp report</h2>
    <form method="post" action="/ops/simulate-wa" title="Submit simulated citizen report">
      <label for="message_id">Message id</label>
      <input id="message_id" name="message_id" required title="Unique message id"/>
      <label for="text">Text</label>
      <textarea id="text" name="text" rows="3" required title="Report text">Cover missing</textarea>
      <label for="lat">Lat (optional)</label>
      <input id="lat" name="lat" title="Latitude"/>
      <label for="lon">Lon (optional)</label>
      <input id="lon" name="lon" title="Longitude"/>
      <button type="submit" title="Create ticket from simulated WhatsApp">Create report ticket</button>
    </form>
    <p class="muted">Webhook JSON: <code>POST /webhooks/whatsapp</code> with header
    <code>X-Stub-Token: iron-protect-pilot-stub</code></p>
  </section>
  <section>
    <h2>Advance ticket</h2>
    <form method="post" action="/ops/transition" title="Change ticket state">
      <label for="ticket_id">Ticket id</label>
      <input id="ticket_id" name="ticket_id" required title="Ticket id"/>
      <label for="new_state">New state</label>
      <select id="new_state" name="new_state" title="Next ticket state">
        <option>acknowledged</option>
        <option>assigned</option>
        <option>secured</option>
        <option>replaced</option>
        <option>false_alarm</option>
        <option>closed</option>
      </select>
      <label for="actor">Actor user</label>
      <input id="actor" name="actor" value="disp1" title="Acting user id"/>
      <button type="submit" title="Apply ticket transition">Update ticket</button>
    </form>
  </section>
  <section>
    <h2>Seed demo asset</h2>
    <form method="post" action="/ops/seed-asset" title="Add a demo cover to the register">
      <label for="asset_id">Asset id</label>
      <input id="asset_id" name="asset_id" value="PILOT-1" title="Asset id"/>
      <label for="corridor">Corridor</label>
      <input id="corridor" name="corridor" value="pilot-corridor" title="Corridor name"/>
      <label for="alat">Lat</label>
      <input id="alat" name="lat" value="9.05" title="Asset latitude"/>
      <label for="alon">Lon</label>
      <input id="alon" name="lon" value="7.49" title="Asset longitude"/>
      <button type="submit" title="Save demo asset">Save asset</button>
    </form>
  </section>
</div>
<section style="margin-top:1rem">
  <h2>Tickets</h2>
  <table>
    <thead><tr><th>Id</th><th>Kind</th><th>State</th><th>Asset</th><th>Text</th></tr></thead>
    <tbody>{''.join(ticket_rows)}</tbody>
  </table>
</section>
<section style="margin-top:1rem">
  <h2>Assets</h2>
  <table>
    <thead><tr><th>Id</th><th>Corridor</th><th>Status</th><th>Mark</th></tr></thead>
    <tbody>{''.join(asset_rows)}</tbody>
  </table>
</section>
"""
