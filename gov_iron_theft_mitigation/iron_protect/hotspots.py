"""Weekly hotspot pack export for Works / liaison."""

from __future__ import annotations

import csv
import io
from collections import Counter
from datetime import datetime, timedelta, timezone

from .assets import AssetRegister
from .tickets import TicketService


class HotspotPack:
    def __init__(self, assets: AssetRegister, tickets: TicketService) -> None:
        self.assets = assets
        self.tickets = tickets

    def build(self, *, days: int = 7) -> dict:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        recent = [
            t
            for t in self.tickets.list()
            if _parse(t.created_at) >= cutoff
        ]
        by_corridor: Counter[str] = Counter()
        open_vs_closed = {"open": 0, "closed": 0}
        top_assets: Counter[str] = Counter()

        asset_corridor = {
            a.asset_id: a.corridor
            for a in self.assets.list(include_training=True)
        }
        for t in recent:
            corridor = asset_corridor.get(t.asset_id or "", "unmatched")
            by_corridor[corridor] += 1
            if t.state == "closed":
                open_vs_closed["closed"] += 1
            else:
                open_vs_closed["open"] += 1
            if t.asset_id:
                top_assets[t.asset_id] += 1

        return {
            "days": days,
            "generated_at": datetime.now(timezone.utc)
            .replace(microsecond=0)
            .isoformat(),
            "counts_by_corridor": dict(by_corridor),
            "open_vs_closed": open_vs_closed,
            "top_locations": top_assets.most_common(10),
            "ticket_count": len(recent),
        }

    def to_markdown(self, *, days: int = 7) -> str:
        pack = self.build(days=days)
        lines = [
            f"# Hotspot pack (last {pack['days']} days)",
            "",
            f"Generated: {pack['generated_at']}",
            f"Tickets in window: {pack['ticket_count']}",
            "",
            "## Open vs closed",
            f"- Open: {pack['open_vs_closed']['open']}",
            f"- Closed: {pack['open_vs_closed']['closed']}",
            "",
            "## By corridor",
        ]
        for corridor, count in sorted(
            pack["counts_by_corridor"].items(), key=lambda x: (-x[1], x[0])
        ):
            lines.append(f"- {corridor}: {count}")
        lines.extend(["", "## Top asset IDs"])
        for asset_id, count in pack["top_locations"]:
            lines.append(f"- {asset_id}: {count}")
        lines.append("")
        lines.append(
            "_Pack for Works and liaison only. No bypass or defeat detail._"
        )
        return "\n".join(lines) + "\n"

    def to_csv(self, *, days: int = 7) -> str:
        pack = self.build(days=days)
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["section", "key", "value"])
        writer.writerow(["meta", "days", pack["days"]])
        writer.writerow(["meta", "generated_at", pack["generated_at"]])
        for corridor, count in pack["counts_by_corridor"].items():
            writer.writerow(["corridor", corridor, count])
        writer.writerow(
            ["open_vs_closed", "open", pack["open_vs_closed"]["open"]]
        )
        writer.writerow(
            ["open_vs_closed", "closed", pack["open_vs_closed"]["closed"]]
        )
        for asset_id, count in pack["top_locations"]:
            writer.writerow(["top_asset", asset_id, count])
        return buf.getvalue()


def _parse(iso: str) -> datetime:
    return datetime.fromisoformat(iso.replace("Z", "+00:00"))
