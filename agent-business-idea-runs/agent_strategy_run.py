#!/usr/bin/env python3
"""Fetch RSS/OWID inputs for agent formulation runs (strategies 5, 9, 14; optional 15)."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

RUN_DIR = Path(__file__).resolve().parent
REPO_ROOT = RUN_DIR.parent
INPUTS_DIR = RUN_DIR / "inputs"
INPUTS_DIR.mkdir(parents=True, exist_ok=True)

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


def strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text or "").strip()


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

    import os

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
        description="Fetch agent formulation inputs (RSS, OWID; optional Strategy 15)."
    )
    parser.add_argument(
        "--fetch-only",
        action="store_true",
        help="RSS + OWID only; skip Strategy 15 subprocess (recommended for agent runs).",
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
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    out_path = INPUTS_DIR / f"agent_strategy_inputs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    payload: dict = {
        "generated_at": datetime.now().isoformat(),
        "strategies_skipped": [3, 4, 8, 10],
        "strategy_5_9_rss": fetch_rss(),
        "strategy_14_owid": fetch_owid_snippets(),
    }

    run_s15 = args.with_strategy15 and not args.fetch_only
    if run_s15:
        payload["strategy_15_run"] = run_strategy15(timeout_sec=args.strategy15_timeout)
    else:
        payload["strategy_15_run"] = {"status": "skipped", "reason": "use --with-strategy15 to enable"}

    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {out_path}")

    for block in payload["strategy_5_9_rss"]:
        if "articles" in block:
            print(f"\n=== {block['source']} ({block.get('count', len(block['articles']))} headlines) ===")
            for article in block["articles"][:5]:
                print(f"  - {article['title'][:100]}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
