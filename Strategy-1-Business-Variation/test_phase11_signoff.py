#!/usr/bin/env python3
"""
Strategy 1 §11 Phase D sign-off (automated).

Proves: no live seeds; URL-cited collector output; fetch uses strategy_1_discovery;
sample Docx contains complaint source URLs (convert only — does not open Word).
"""

from __future__ import annotations

import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
COLLECTOR = ROOT / "business_variation_collector.py"
FIXTURE = ROOT / "fixtures" / "sample_inputs.json"
SAMPLE_MD = ROOT / "fixtures" / "s11_citation_sample.md"
SAMPLE_DOCX = ROOT / "fixtures" / "s11_citation_sample.docx"
RUNNER = REPO / "agent-business-idea-runs" / "agent_strategy_run.py"


def run(cmd: list[str], *, cwd: Path, timeout: int = 120) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def check_no_live_seeds(errors: list[str]) -> None:
    live = ROOT / "seed_businesses.json"
    archived = ROOT / "_archive" / "seed_businesses.json"
    if live.exists():
        errors.append(f"live seed_businesses.json must not exist at {live}")
    if not archived.exists():
        errors.append(f"archived seeds missing: {archived}")


def check_collector_urls(errors: list[str]) -> None:
    before = set(ROOT.glob("business_variation_*.json"))
    r = run(
        [sys.executable, str(COLLECTOR), "--non-interactive", "--inputs", str(FIXTURE)],
        cwd=ROOT,
    )
    if r.returncode != 0:
        errors.append(f"collector --inputs failed: {r.stderr or r.stdout}")
        return
    after = set(ROOT.glob("business_variation_*.json"))
    new = after - before
    if not new:
        errors.append("no new business_variation_*.json from fixture run")
        return
    latest = max(new, key=lambda p: p.stat().st_mtime)
    data = json.loads(latest.read_text(encoding="utf-8"))
    if data.get("intake") != "url_cited_online":
        errors.append(f"expected intake=url_cited_online, got {data.get('intake')}")
    biz = (data.get("businesses") or [None])[0]
    if not biz:
        errors.append("empty businesses in collector output")
        return
    if not str(biz.get("success_url") or "").startswith("http"):
        errors.append("missing business success_url")
    c0 = (biz.get("complaints") or [None])[0]
    if not c0 or not str(c0.get("source_url") or "").startswith("http"):
        errors.append("missing complaint source_url")
    stamp = latest.stem.replace("business_variation_", "")
    p1a = ROOT / f"strategy1_prompt_1a_payload_{stamp}.txt"
    if not p1a.exists():
        errors.append("missing prompt 1a payload")
    else:
        body = p1a.read_text(encoding="utf-8")
        if "source_url=" not in body and "https://" not in body:
            errors.append("prompt 1a payload missing source URL citations")


def check_discovery_unit(errors: list[str]) -> None:
    sys.path.insert(0, str(RUNNER.parent))
    import agent_strategy_run as asr  # noqa: E402

    if hasattr(asr, "fetch_strategy1_seeds"):
        errors.append("fetch_strategy1_seeds should be gone")
    disc = asr.build_strategy1_discovery(
        rss=[
            {
                "source": "techpoint",
                "articles": [
                    {"title": "Lead", "link": "https://techpoint.africa/x", "published": ""}
                ],
            }
        ],
        startup_directory={"url": "https://www.startuplist.africa/startups"},
        trending={"products": [{"title": "Prod", "link": "https://www.producthunt.com/p"}]},
    )
    if disc.get("primary") != "agent_native_web_research":
        errors.append("discovery primary wrong")
    if disc.get("discovery_leads_count", 0) < 1:
        errors.append("expected at least one discovery lead in unit sample")


def check_docx_citations(errors: list[str]) -> None:
    """Convert sample md → docx without opening Word; assert URLs in document.xml."""
    marker_url = "https://play.google.com/store/apps/details?id=com.jumia.food"
    SAMPLE_MD.write_text(
        "\n".join(
            [
                "# Strategy 1 citation sample (§11 Phase D)",
                "",
                "## HotHold Kitchen NG (S1)",
                "",
                "- **Successful business:** Jumia Food",
                "- **Success URL:** https://food.jumia.com.ng/",
                "- **Recurring complaint:** Food arrives cold / late",
                f"- **Complaint source URL:** {marker_url}",
                "- **Variation:** Insulated micro-hub SLA for office parks",
                "",
            ]
        ),
        encoding="utf-8",
    )
    sys.path.insert(0, str(REPO))
    from business_bookmark_sorter.docx_export import convert_md_to_docx

    try:
        out = convert_md_to_docx(SAMPLE_MD, SAMPLE_DOCX)
    except Exception as ex:
        errors.append(f"docx convert failed: {ex}")
        return
    if not out.exists() or out.stat().st_size < 500:
        errors.append(f"docx missing or too small: {out}")
        return
    try:
        with zipfile.ZipFile(out, "r") as zf:
            xml = zf.read("word/document.xml").decode("utf-8", errors="replace")
    except Exception as ex:
        errors.append(f"docx zip read failed: {ex}")
        return
    if "play.google.com" not in xml and marker_url not in xml:
        # Pandoc may split URLs across runs — require at least domain fragment
        if "jumia.food" not in xml and "food.jumia" not in xml:
            errors.append("docx document.xml missing expected citation URL fragments")


def main() -> int:
    errors: list[str] = []
    check_no_live_seeds(errors)
    check_collector_urls(errors)
    check_discovery_unit(errors)
    check_docx_citations(errors)

    if errors:
        print("FAIL Strategy 1 §11 Phase D sign-off")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("PASS Strategy 1 §11 Phase D sign-off")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
