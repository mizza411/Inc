#!/usr/bin/env python3
"""Fetch RSS/OWID/S1 discovery/S6/S7 inputs for agent formulation runs (strategies 1, 5, 6, 7, 9, 14; optional 15)."""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

RUN_DIR = Path(__file__).resolve().parent
REPO_ROOT = RUN_DIR.parent
INPUTS_DIR = RUN_DIR / "inputs"
INPUTS_DIR.mkdir(parents=True, exist_ok=True)

STRATEGY_1_DIR = REPO_ROOT / "Strategy-1-Business-Variation"
STRATEGY_1_SCRIPT = STRATEGY_1_DIR / "business_variation_collector.py"

RSS = {
    "nairametrics": "https://nairametrics.com/feed/",
    "businessday": "https://businessday.ng/feed/",
    "punch": "https://punchng.com/feed/",
    "vanguard": "https://www.vanguardngr.com/feed/",
    "premium_times": "https://www.premiumtimesng.com/feed/",
    "techpoint": "https://techpoint.africa/feed/",
    "financial_nigeria": "https://financialnigeria.com/rss.xml",
}

OWID_TOPICS = [
    ("internet-users", "https://ourworldindata.org/internet"),
    ("renewable-energy", "https://ourworldindata.org/renewable-energy"),
]

STARTUPLIST_STARTUPS_URL = "https://www.startuplist.africa/startups"
PRODUCT_HUNT_FEED = "https://www.producthunt.com/feed"


def strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text or "").strip()


def build_strategy1_discovery(
    *,
    rss: Optional[list] = None,
    startup_directory: Optional[dict] = None,
    trending: Optional[dict] = None,
) -> dict:
    """
    Strategy 1 fetch block (§11 Phase C): no seed_businesses.json.

    Primary path = agent-native web research with citeable URLs.
    Optional discovery_leads are soft hints from RSS / Product Hunt / StartupList
    already fetched in this run — never treat as proven complaints.
    Soft-fail: never raises; empty leads still return usable guidance.
    """
    leads: list[dict] = []
    try:
        for block in rss or []:
            if not isinstance(block, dict) or block.get("error"):
                continue
            source = block.get("source") or "rss"
            for article in (block.get("articles") or [])[:5]:
                if not isinstance(article, dict):
                    continue
                title = (article.get("title") or "").strip()
                link = (article.get("link") or "").strip()
                if not title or not link:
                    continue
                leads.append(
                    {
                        "kind": "news_headline",
                        "source": source,
                        "title": title[:200],
                        "url": link,
                        "published": article.get("published") or "",
                        "use": "optional_lead_only",
                    }
                )
        if isinstance(trending, dict):
            for product in (trending.get("products") or [])[:8]:
                if not isinstance(product, dict):
                    continue
                title = (product.get("title") or product.get("name") or "").strip()
                link = (product.get("link") or "").strip()
                if not title:
                    continue
                leads.append(
                    {
                        "kind": "trending_product",
                        "source": trending.get("source") or "product_hunt",
                        "title": title[:200],
                        "url": link,
                        "published": product.get("published") or "",
                        "use": "optional_lead_only",
                    }
                )
        if isinstance(startup_directory, dict) and startup_directory.get("url"):
            leads.append(
                {
                    "kind": "startup_directory",
                    "source": startup_directory.get("source") or "startuplist_africa",
                    "title": "StartupList Africa startups index (filter Nigeria + sector)",
                    "url": startup_directory.get("url"),
                    "published": "",
                    "use": "optional_lead_only",
                }
            )
    except Exception as ex:
        return {
            "status": "error",
            "primary": "agent_native_web_research",
            "error": str(ex),
            "formula": "Successful Business + Recurring Complaint = Profitable Variation",
            "discovery_leads": [],
            "note": "Continue agent run; web-discover S1 businesses + complaints with URLs.",
        }

    # Cap leads; prefer diversity already roughly ordered news → PH → directory
    slim = leads[:20]
    status = "ok" if slim else "agent_web_research_only"
    return {
        "status": status,
        "primary": "agent_native_web_research",
        "formula": "Successful Business + Recurring Complaint = Profitable Variation",
        "requirements": [
            "Cite success_url (or equivalent) for the successful business",
            "Cite complaint source_url (http/https) with title/quote/date when available",
            "Differentiate variation — not Strategy 6 niche-combo or Strategy 7 trending-adapt alone",
        ],
        "forbidden": [
            "seed_businesses.json / archived example_complaints",
            "strategy_1_seeds (removed)",
            "AI-invented gaps without URLs",
        ],
        "discovery_leads_count": len(slim),
        "discovery_leads": slim,
        "note": (
            "discovery_leads are optional starting points from this fetch only. "
            "Agent must verify online and cite real complaint/success URLs. "
            "CLI: business_variation_collector.py --non-interactive --inputs "
            "fixtures/sample_inputs.json"
        ),
    }


def run_strategy1_noninteractive(
    inputs_path: Optional[str] = None,
    timeout_sec: int = 60,
) -> dict:
    """Optional: run Strategy 1 collector non-interactively via URL-cited --inputs."""
    if not STRATEGY_1_SCRIPT.exists():
        return {"status": "script_missing", "path": str(STRATEGY_1_SCRIPT)}

    fixture = STRATEGY_1_DIR / "fixtures" / "sample_inputs.json"
    inputs = Path(inputs_path) if inputs_path else fixture
    if not inputs.is_file():
        return {"status": "no_inputs_file", "path": str(inputs)}

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    try:
        proc = subprocess.run(
            [
                sys.executable,
                str(STRATEGY_1_SCRIPT),
                "--non-interactive",
                "--inputs",
                str(inputs),
            ],
            cwd=str(STRATEGY_1_DIR),
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            env=env,
        )
        return {
            "status": "ok" if proc.returncode == 0 else "failed",
            "inputs": str(inputs),
            "returncode": proc.returncode,
            "stdout_tail": (proc.stdout or "")[-1500:],
            "stderr_tail": (proc.stderr or "")[-800:],
        }
    except subprocess.TimeoutExpired as ex:
        return {
            "status": "timeout",
            "timeout_sec": timeout_sec,
            "stdout_tail": (ex.stdout or "")[-1500:] if ex.stdout else "",
            "stderr_tail": (ex.stderr or "")[-800:] if ex.stderr else "",
        }
    except Exception as ex:
        return {"status": "error", "error": str(ex)}


def fetch_rss():
    try:
        import feedparser
    except ImportError:
        return [{"error": "feedparser not installed"}]

    results = []
    for name, url in RSS.items():
        try:
            feed = feedparser.parse(url)
            articles = []
            for entry in feed.entries[:10]:
                articles.append(
                    {
                        "title": entry.get("title", ""),
                        "summary": strip_html(
                            entry.get("summary", "") or entry.get("description", "")
                        )[:400],
                        "link": entry.get("link", ""),
                        "published": entry.get("published", ""),
                    }
                )
            results.append(
                {"source": name, "feed": url, "count": len(articles), "articles": articles}
            )
        except Exception as ex:
            results.append({"source": name, "feed": url, "error": str(ex)})
    return results


def fetch_owid_snippets():
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        return [{"error": "requests/beautifulsoup4 not installed"}]

    headers = {"User-Agent": "Mozilla/5.0 (compatible; IncStrategyBot/1.0)"}
    out = []
    for topic, url in OWID_TOPICS:
        try:
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            text = " ".join(soup.get_text().split())
            out.append(
                {
                    "topic": topic,
                    "url": url,
                    "status": response.status_code,
                    "snippet": text[:2500],
                }
            )
        except Exception as ex:
            out.append({"topic": topic, "url": url, "error": str(ex)})
    return out


def fetch_strategy6_startup_directory():
    """Strategy 6: StartupList Africa snippet (Nigeria-focused startup directory)."""
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        return {"status": "skipped", "error": "requests/beautifulsoup4 not installed"}

    headers = {"User-Agent": "Mozilla/5.0 (compatible; IncStrategyBot/1.0)"}
    try:
        response = requests.get(STARTUPLIST_STARTUPS_URL, headers=headers, timeout=25)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = " ".join(soup.get_text().split())
        nigeria_hits = []
        for token in text.split():
            if token.lower() in ("nigeria", "nigerian", "lagos", "abuja"):
                nigeria_hits.append(token)
        return {
            "source": "startuplist_africa",
            "url": STARTUPLIST_STARTUPS_URL,
            "status": response.status_code,
            "snippet": text[:3500],
            "nigeria_keyword_count": len(nigeria_hits),
            "note": "Filter Nigeria + sector on site; Crunchbase optional legacy fallback.",
        }
    except Exception as ex:
        return {
            "source": "startuplist_africa",
            "url": STARTUPLIST_STARTUPS_URL,
            "status": "error",
            "error": str(ex),
        }


def fetch_strategy7_trending():
    """Strategy 7: Product Hunt RSS (global trending products; adapt for Nigeria)."""
    try:
        import feedparser
    except ImportError:
        return {"status": "skipped", "error": "feedparser not installed"}

    try:
        feed = feedparser.parse(PRODUCT_HUNT_FEED)
        products = []
        for entry in feed.entries[:15]:
            products.append(
                {
                    "title": entry.get("title", ""),
                    "summary": strip_html(
                        entry.get("summary", "") or entry.get("description", "")
                    )[:300],
                    "link": entry.get("link", ""),
                    "published": entry.get("published", ""),
                }
            )
        return {
            "source": "product_hunt",
            "feed": PRODUCT_HUNT_FEED,
            "count": len(products),
            "products": products,
            "note": "Adapt for Nigeria with niche combo; Crunchbase screenshot optional legacy.",
        }
    except Exception as ex:
        return {
            "source": "product_hunt",
            "feed": PRODUCT_HUNT_FEED,
            "status": "error",
            "error": str(ex),
        }


def run_strategy15(timeout_sec: int = 120) -> dict:
    s15 = REPO_ROOT / "Business-Idea-Formulation-Strategy-15-Nigeria-National-Open-Data"
    script = s15 / "nigeria_national_open_data.py"
    if not script.exists():
        return {"status": "script_missing"}

    inputs = s15 / "nigeria_inputs.json"
    if not inputs.exists():
        inputs = s15 / "nigeria_inputs_validated.json"
    if not inputs.exists():
        return {"status": "no_inputs_file"}

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    try:
        proc = subprocess.run(
            [
                sys.executable,
                str(script),
                "--non-interactive",
                "--inputs",
                str(inputs),
            ],
            cwd=str(s15),
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            env=env,
        )
        return {
            "status": "ok" if proc.returncode == 0 else "failed",
            "returncode": proc.returncode,
            "stdout_tail": proc.stdout[-2000:] if proc.stdout else "",
            "stderr_tail": proc.stderr[-1000:] if proc.stderr else "",
        }
    except subprocess.TimeoutExpired as ex:
        return {
            "status": "timeout",
            "timeout_sec": timeout_sec,
            "stdout_tail": (ex.stdout or "")[-2000:] if ex.stdout else "",
            "stderr_tail": (ex.stderr or "")[-1000:] if ex.stderr else "",
        }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Fetch agent formulation inputs (RSS, OWID, S1 seeds, S6/S7; optional Strategy 1/15 runs)."
        )
    )
    parser.add_argument(
        "--fetch-only",
        action="store_true",
        help="RSS + OWID + S1 status + S6/S7; skip Strategy 15 subprocess (recommended).",
    )
    parser.add_argument(
        "--with-strategy15",
        action="store_true",
        help="Also run Strategy 15 subprocess (may hang on clipboard prompts).",
    )
    parser.add_argument(
        "--strategy15-timeout",
        type=int,
        default=120,
        metavar="SEC",
        help="Strategy 15 subprocess timeout (default: 120).",
    )
    parser.add_argument(
        "--with-strategy1-run",
        action="store_true",
        help="Also run Strategy 1 collector --non-interactive --inputs (optional).",
    )
    parser.add_argument(
        "--strategy1-inputs",
        default=None,
        metavar="PATH",
        help="URL-cited inputs JSON for --with-strategy1-run (default: Strategy 1 fixtures/sample_inputs.json).",
    )
    parser.add_argument(
        "--strategy1-timeout",
        type=int,
        default=60,
        metavar="SEC",
        help="Strategy 1 subprocess timeout (default: 60).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    out_path = INPUTS_DIR / f"agent_strategy_inputs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    rss = fetch_rss()
    startup_directory = fetch_strategy6_startup_directory()
    trending = fetch_strategy7_trending()
    owid = fetch_owid_snippets()

    payload: dict = {
        "generated_at": datetime.now().isoformat(),
        "strategies_skipped": [2, 3, 4, 8, 10],
        "strategy_5_9_rss": rss,
        "strategy_6_startup_directory": startup_directory,
        "strategy_7_trending": trending,
        "strategy_14_owid": owid,
        "strategy_1_discovery": build_strategy1_discovery(
            rss=rss,
            startup_directory=startup_directory,
            trending=trending,
        ),
    }

    if args.with_strategy1_run:
        payload["strategy_1_run"] = run_strategy1_noninteractive(
            inputs_path=args.strategy1_inputs,
            timeout_sec=args.strategy1_timeout,
        )
    else:
        payload["strategy_1_run"] = {
            "status": "skipped",
            "reason": "use --with-strategy1-run to enable non-interactive collector",
        }

    run_s15 = args.with_strategy15 and not args.fetch_only
    if run_s15:
        payload["strategy_15_run"] = run_strategy15(timeout_sec=args.strategy15_timeout)
    else:
        payload["strategy_15_run"] = {"status": "skipped", "reason": "use --with-strategy15 to enable"}

    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out_path}")

    s1 = payload.get("strategy_1_discovery") or {}
    print(
        f"\n=== strategy_1_discovery ({s1.get('status')}) "
        f"leads={s1.get('discovery_leads_count', 0)} "
        f"primary={s1.get('primary')} ==="
    )

    for block in payload["strategy_5_9_rss"]:
        if "articles" in block:
            print(
                f"\n=== {block['source']} "
                f"({block.get('count', len(block['articles']))} headlines) ==="
            )
            for article in block["articles"][:5]:
                print(f"  - {article['title'][:100]}")

    s7 = payload.get("strategy_7_trending", {})
    if s7.get("products"):
        print(f"\n=== product_hunt ({s7.get('count', 0)} products) ===")
        for product in s7["products"][:5]:
            print(f"  - {product['title'][:100]}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
