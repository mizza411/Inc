#!/usr/bin/env python3
"""Fetch RSS/OWID/S1/S6/S7 inputs for agent formulation runs (strategies 1, 5, 6, 7, 9, 14; optional 15)."""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

RUN_DIR = Path(__file__).resolve().parent
REPO_ROOT = RUN_DIR.parent
INPUTS_DIR = RUN_DIR / "inputs"
INPUTS_DIR.mkdir(parents=True, exist_ok=True)

STRATEGY_1_DIR = REPO_ROOT / "Strategy-1-Business-Variation"
STRATEGY_1_SEEDS = STRATEGY_1_DIR / "seed_businesses.json"
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


def fetch_strategy1_seeds() -> dict:
    """
    Strategy 1: load local seed_businesses.json (no network).
    Soft-fail: never raises; agent can still synthesize if status != ok.
    """
    if not STRATEGY_1_SEEDS.exists():
        return {
            "status": "missing",
            "path": str(STRATEGY_1_SEEDS),
            "error": "seed_businesses.json not found",
            "note": "Synthesize complaint→variation from Nigeria market leaders; mark status synthesized.",
        }
    try:
        data = json.loads(STRATEGY_1_SEEDS.read_text(encoding="utf-8"))
        businesses = data.get("businesses") if isinstance(data, dict) else None
        if not isinstance(businesses, list):
            return {
                "status": "error",
                "path": str(STRATEGY_1_SEEDS),
                "error": "invalid seeds file (missing businesses list)",
            }
        slim = []
        for b in businesses[:12]:
            if not isinstance(b, dict):
                continue
            slim.append(
                {
                    "id": b.get("id"),
                    "name": b.get("name"),
                    "category": b.get("category"),
                    "example_complaints": (b.get("example_complaints") or [])[:6],
                }
            )
        return {
            "status": "ok",
            "source": "seed_businesses.json",
            "path": str(STRATEGY_1_SEEDS),
            "formula": "Successful Business + Recurring Complaint = Profitable Variation",
            "business_count": len(slim),
            "businesses": slim,
            "note": (
                "Not Strategy 6 (niche combo) or Strategy 7 (trending adapt). "
                "Optional subprocess: business_variation_collector.py "
                "--non-interactive --seed-ids jumia_food,bolt"
            ),
        }
    except Exception as ex:
        return {
            "status": "error",
            "path": str(STRATEGY_1_SEEDS),
            "error": str(ex),
            "note": "Continue agent run; synthesize Strategy 1 ideas and mark status synthesized.",
        }


def run_strategy1_noninteractive(
    seed_ids: str = "jumia_food,bolt",
    timeout_sec: int = 60,
) -> dict:
    """Optional: run Strategy 1 collector non-interactively (default off in fetch)."""
    if not STRATEGY_1_SCRIPT.exists():
        return {"status": "script_missing", "path": str(STRATEGY_1_SCRIPT)}

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    try:
        proc = subprocess.run(
            [
                sys.executable,
                str(STRATEGY_1_SCRIPT),
                "--non-interactive",
                "--seed-ids",
                seed_ids,
            ],
            cwd=str(STRATEGY_1_DIR),
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            env=env,
        )
        return {
            "status": "ok" if proc.returncode == 0 else "failed",
            "seed_ids": seed_ids,
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
        help="RSS + OWID + S1 seeds + S6/S7; skip Strategy 15 subprocess (recommended).",
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
        help="Also run Strategy 1 collector --non-interactive --seed-ids (optional).",
    )
    parser.add_argument(
        "--strategy1-seed-ids",
        default="jumia_food,bolt",
        metavar="IDS",
        help="Seed ids for --with-strategy1-run (default: jumia_food,bolt).",
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

    payload: dict = {
        "generated_at": datetime.now().isoformat(),
        "strategies_skipped": [2, 3, 4, 8, 10],
        "strategy_1_seeds": fetch_strategy1_seeds(),
        "strategy_5_9_rss": fetch_rss(),
        "strategy_6_startup_directory": fetch_strategy6_startup_directory(),
        "strategy_7_trending": fetch_strategy7_trending(),
        "strategy_14_owid": fetch_owid_snippets(),
    }

    if args.with_strategy1_run:
        payload["strategy_1_run"] = run_strategy1_noninteractive(
            seed_ids=args.strategy1_seed_ids,
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

    s1 = payload.get("strategy_1_seeds") or {}
    print(
        f"\n=== strategy_1_seeds ({s1.get('status')}) "
        f"businesses={s1.get('business_count', 0)} ==="
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
