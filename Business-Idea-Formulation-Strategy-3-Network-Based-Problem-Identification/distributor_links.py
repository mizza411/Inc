#!/usr/bin/env python3
"""
Strategy 3 — Paid distributor link generator (Phase B1).

Creates unique survey links with ref/UTM tracking for people you pay to
share the ill_pay_to_v1 survey. Does not modify network_problem_collector.py.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

DEFAULT_BASE_URL = (
    "https://mizza411.github.io/Inc/problem_identification_tool/web/index.html"
)
DEFAULT_SURVEY_ID = "ill_pay_to_v1"
REGISTRY_FILENAME = "distributor_registry.json"
TEMPLATES_FILENAME = "distributor_message_templates.txt"
OUTREACH_PREFIX = "distributor_outreach_"


def slugify(name: str) -> str:
    """Turn a display name into a stable ref id (e.g. 'Jane Doe' -> 'jane_doe')."""
    slug = name.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    slug = slug.strip("_")
    return slug or "distributor"


def build_distributor_link(
    distributor_id: str,
    base_url: str = DEFAULT_BASE_URL,
    survey_id: str = DEFAULT_SURVEY_ID,
    utm_medium: str = "strategy3",
    utm_campaign: str = "ill_pay_to",
) -> str:
    """Build a tracked survey URL. ref + utm_source both map to the distributor."""
    params = {
        "survey": survey_id,
        "ref": distributor_id,
        "utm_source": distributor_id,
        "utm_medium": utm_medium,
        "utm_campaign": utm_campaign,
    }
    return f"{base_url}?{urlencode(params)}"


class DistributorLinkManager:
    def __init__(self, strategy_dir: Path | None = None):
        self.strategy_dir = strategy_dir or Path(__file__).resolve().parent
        self.registry_path = self.strategy_dir / REGISTRY_FILENAME
        self.templates_path = self.strategy_dir / TEMPLATES_FILENAME

    def _empty_registry(self) -> dict[str, Any]:
        return {
            "version": 1,
            "survey_base_url": DEFAULT_BASE_URL,
            "survey_id": DEFAULT_SURVEY_ID,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "distributors": [],
        }

    def load_registry(self) -> dict[str, Any]:
        if not self.registry_path.exists():
            return self._empty_registry()
        with open(self.registry_path, encoding="utf-8") as handle:
            data = json.load(handle)
        if "distributors" not in data:
            data["distributors"] = []
        return data

    def save_registry(self, data: dict[str, Any]) -> None:
        data["generated_at"] = datetime.now(timezone.utc).isoformat()
        with open(self.registry_path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False)

    def add_distributor(
        self,
        name: str,
        channel: str = "",
        payout_terms: str = "",
        industry: str = "",
        notes: str = "",
        distributor_id: str | None = None,
    ) -> dict[str, Any]:
        registry = self.load_registry()
        dist_id = distributor_id or slugify(name)
        link = build_distributor_link(
            dist_id,
            base_url=registry.get("survey_base_url", DEFAULT_BASE_URL),
            survey_id=registry.get("survey_id", DEFAULT_SURVEY_ID),
        )

        existing = next(
            (d for d in registry["distributors"] if d["id"] == dist_id),
            None,
        )
        record = {
            "id": dist_id,
            "name": name.strip(),
            "channel": channel.strip(),
            "industry": industry.strip(),
            "payout_terms": payout_terms.strip(),
            "notes": notes.strip(),
            "link": link,
            "responses_tracked": existing["responses_tracked"] if existing else 0,
            "status": existing.get("status", "active") if existing else "active",
            "added_at": existing["added_at"] if existing else datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

        if existing:
            registry["distributors"] = [
                record if d["id"] == dist_id else d for d in registry["distributors"]
            ]
        else:
            registry["distributors"].append(record)

        self.save_registry(registry)
        return record

    def list_distributors(self) -> list[dict[str, Any]]:
        return self.load_registry().get("distributors", [])

    def load_message_templates(self) -> str:
        if not self.templates_path.exists():
            raise FileNotFoundError(f"Templates file not found: {self.templates_path}")
        return self.templates_path.read_text(encoding="utf-8")

    def render_outreach(self, distributor: dict[str, Any]) -> str:
        """Fill distributor_message_templates.txt for one distributor."""
        template = self.load_message_templates()
        replacements = {
            "{distributor_name}": distributor.get("name", ""),
            "{your_name}": "[Your name]",
            "{link}": distributor.get("link", ""),
            "{payout_terms}": distributor.get("payout_terms", "[payout terms]"),
            "{channel}": distributor.get("channel", ""),
        }
        rendered = template
        for key, value in replacements.items():
            rendered = rendered.replace(key, value)
        return rendered

    def generate_outreach_file(
        self,
        distributor_ids: list[str] | None = None,
    ) -> Path:
        distributors = self.list_distributors()
        if distributor_ids:
            id_set = set(distributor_ids)
            distributors = [d for d in distributors if d["id"] in id_set]

        if not distributors:
            raise ValueError("No distributors in registry. Add one with --add first.")

        parts = [
            "Strategy 3 — Paid distributor outreach messages",
            f"Generated: {datetime.now(timezone.utc).isoformat()}",
            "",
        ]
        for dist in distributors:
            parts.append("=" * 60)
            parts.append(f"To: {dist['name']} via {dist.get('channel') or 'your channel'}")
            parts.append(f"Ref id: {dist['id']}")
            parts.append(f"Link: {dist['link']}")
            parts.append("=" * 60)
            parts.append(self.render_outreach(dist).strip())
            parts.append("")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = self.strategy_dir / f"{OUTREACH_PREFIX}{timestamp}.txt"
        out_path.write_text("\n".join(parts), encoding="utf-8")
        return out_path


def cmd_add(args: argparse.Namespace) -> int:
    manager = DistributorLinkManager()
    record = manager.add_distributor(
        name=args.name,
        channel=args.channel or "",
        payout_terms=args.payout or "",
        industry=args.industry or "",
        notes=args.notes or "",
        distributor_id=args.id,
    )
    print(f"Added distributor: {record['name']} ({record['id']})")
    print(f"Link: {record['link']}")
    print(f"Registry: {manager.registry_path}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    manager = DistributorLinkManager()
    distributors = manager.list_distributors()
    if not distributors:
        print("No distributors yet. Run: python distributor_links.py add --name \"Contact Name\"")
        return 0
    for dist in distributors:
        print(f"- {dist['name']} ({dist['id']})")
        print(f"  Channel: {dist.get('channel') or 'n/a'}")
        print(f"  Payout: {dist.get('payout_terms') or 'n/a'}")
        print(f"  Link: {dist['link']}")
        print(f"  Responses tracked: {dist.get('responses_tracked', 0)}")
    return 0


def cmd_link(args: argparse.Namespace) -> int:
    dist_id = args.id or slugify(args.name)
    url = build_distributor_link(dist_id)
    print(url)
    return 0


def cmd_outreach(args: argparse.Namespace) -> int:
    manager = DistributorLinkManager()
    ids = args.ids.split(",") if args.ids else None
    out_path = manager.generate_outreach_file(distributor_ids=ids)
    print(f"Outreach messages saved to: {out_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Strategy 3 paid distributor link generator (Phase B1)",
    )
    sub = parser.add_subparsers(dest="command")

    add_p = sub.add_parser("add", help="Register a distributor and generate their link")
    add_p.add_argument("--name", required=True, help="Distributor display name")
    add_p.add_argument("--channel", help="WhatsApp, LinkedIn, Email, etc.")
    add_p.add_argument("--payout", help="e.g. 500 NGN per qualified response")
    add_p.add_argument("--industry", help="Optional industry / network niche")
    add_p.add_argument("--notes", help="Optional internal notes")
    add_p.add_argument("--id", help="Override ref slug (default: slugified name)")
    add_p.set_defaults(func=cmd_add)

    list_p = sub.add_parser("list", help="List registered distributors")
    list_p.set_defaults(func=cmd_list)

    link_p = sub.add_parser("link", help="Print a one-off link without saving to registry")
    link_p.add_argument("--name", help="Name to slugify for ref id")
    link_p.add_argument("--id", help="Explicit ref id")
    link_p.set_defaults(func=cmd_link)

    out_p = sub.add_parser("outreach", help="Generate outreach messages from templates")
    out_p.add_argument(
        "--ids",
        help="Comma-separated distributor ids (default: all in registry)",
    )
    out_p.set_defaults(func=cmd_outreach)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
