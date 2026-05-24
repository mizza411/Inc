"""
Automated research and fact-checking for YouTube scripts.

Gathers lightweight sources (Wikipedia + trend context) and flags script
claims that lack supporting evidence in those sources.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from urllib.parse import quote
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)

CREDIBLE_SEED_SOURCES = [
    {
        "title": "Our World in Data",
        "url": "https://ourworldindata.org/",
        "snippet": "Global statistics and research charts for fact-backed commentary.",
        "source_type": "statistics",
        "credibility_score": 0.9,
    },
    {
        "title": "Nigeria Bureau of Statistics",
        "url": "https://www.nigerianstat.gov.ng/",
        "snippet": "Official Nigerian economic and social indicators.",
        "source_type": "official",
        "credibility_score": 0.95,
    },
    {
        "title": "BBC News Africa",
        "url": "https://www.bbc.com/news/world/africa",
        "snippet": "Regional news coverage for current-events context.",
        "source_type": "news",
        "credibility_score": 0.85,
    },
]


@dataclass
class ResearchSource:
    title: str
    url: str
    snippet: str
    source_type: str
    credibility_score: float


@dataclass
class FactCheckItem:
    claim: str
    status: str
    supporting_sources: List[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class ResearchReport:
    topic: str
    sources: List[ResearchSource]
    fact_checks: List[FactCheckItem]
    fact_checking_status: str
    research_quality_score: float
    generated_at: datetime

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["generated_at"] = self.generated_at.isoformat()
        return data


class ResearchEngine:
    """Gather sources and run heuristic fact-checks on generated scripts."""

    def __init__(self, exports_dir: Optional[Path] = None):
        base = Path(__file__).resolve().parent.parent
        self.exports_dir = exports_dir or base / "exports"

    def analyze_topic(
        self,
        topic: str,
        script_data: Optional[Dict[str, Any]] = None,
        extra_sources: Optional[List[Dict[str, Any]]] = None,
    ) -> ResearchReport:
        sources = self._gather_sources(topic, extra_sources)
        fact_checks = self.fact_check_script(script_data or {}, sources)
        status = self._overall_status(fact_checks)
        quality = self._research_quality(sources, fact_checks)

        return ResearchReport(
            topic=topic,
            sources=sources,
            fact_checks=fact_checks,
            fact_checking_status=status,
            research_quality_score=quality,
            generated_at=datetime.now(),
        )

    def fact_check_script(
        self,
        script_data: Dict[str, Any],
        sources: List[ResearchSource],
    ) -> List[FactCheckItem]:
        claims = self._extract_claims(script_data)
        if not claims:
            return [
                FactCheckItem(
                    claim="No explicit factual claims detected in script.",
                    status="needs_review",
                    notes="Add statistics, dates, or cited statements for stronger verification.",
                )
            ]

        corpus = " ".join(s.snippet.lower() for s in sources)
        results: List[FactCheckItem] = []

        for claim in claims:
            keywords = self._keywords(claim)
            matched = [s.title for s in sources if any(k in s.snippet.lower() for k in keywords)]
            if len(keywords) >= 2 and sum(1 for k in keywords if k in corpus) >= 2:
                status = "verified"
                notes = "Claim keywords appear in gathered source snippets."
            elif matched:
                status = "partial"
                notes = "Some overlap with sources; manual review recommended."
            else:
                status = "unsupported"
                notes = "No supporting snippet found; revise claim or add sources."

            results.append(
                FactCheckItem(
                    claim=claim,
                    status=status,
                    supporting_sources=matched,
                    notes=notes,
                )
            )

        return results

    def export_report(self, report: ResearchReport) -> Path:
        self.exports_dir.mkdir(parents=True, exist_ok=True)
        stamp = report.generated_at.strftime("%Y%m%d_%H%M%S")
        safe_topic = re.sub(r"[^\w\-]+", "_", report.topic.lower())[:40]
        path = self.exports_dir / f"research_{safe_topic}_{stamp}.json"
        path.write_text(json.dumps(report.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
        return path

    def _gather_sources(
        self,
        topic: str,
        extra_sources: Optional[List[Dict[str, Any]]] = None,
    ) -> List[ResearchSource]:
        sources: List[ResearchSource] = []

        for seed in CREDIBLE_SEED_SOURCES:
            sources.append(ResearchSource(**seed))

        wiki = self._fetch_wikipedia_summary(topic)
        if wiki:
            sources.append(wiki)

        if extra_sources:
            for item in extra_sources:
                sources.append(
                    ResearchSource(
                        title=item.get("title", "External source"),
                        url=item.get("url", ""),
                        snippet=item.get("snippet", item.get("query", "")),
                        source_type=item.get("source_type", "external"),
                        credibility_score=float(item.get("credibility_score", 0.7)),
                    )
                )

        return sources

    def _fetch_wikipedia_summary(self, topic: str) -> Optional[ResearchSource]:
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(topic.replace(' ', '_'))}"
            req = Request(url, headers={"User-Agent": "Inc-YouTube-Automation/1.0"})
            with urlopen(req, timeout=8) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            extract = payload.get("extract") or ""
            if not extract:
                return None
            return ResearchSource(
                title=payload.get("title", topic),
                url=payload.get("content_urls", {}).get("desktop", {}).get("page", ""),
                snippet=extract[:500],
                source_type="wikipedia",
                credibility_score=0.75,
            )
        except Exception as exc:
            logger.debug("Wikipedia lookup failed for %s: %s", topic, exc)
            return None

    def _extract_claims(self, script_data: Dict[str, Any]) -> List[str]:
        parts: List[str] = []
        for key in ("hook", "introduction", "conclusion", "call_to_action"):
            if script_data.get(key):
                parts.append(str(script_data[key]))
        main = script_data.get("main_content", [])
        if isinstance(main, list):
            parts.extend(str(p) for p in main)
        elif main:
            parts.append(str(main))

        text = " ".join(parts)
        sentences = re.split(r"(?<=[.!?])\s+", text)
        claims: List[str] = []

        for sentence in sentences:
            s = sentence.strip()
            if len(s) < 40:
                continue
            if re.search(r"\d+|percent|million|billion|according to|study|research|data shows", s, re.I):
                claims.append(s[:240])
            if len(claims) >= 8:
                break

        return claims

    def _keywords(self, text: str) -> List[str]:
        words = re.findall(r"[a-zA-Z]{5,}", text.lower())
        stop = {"about", "their", "there", "which", "would", "could", "should", "because"}
        return [w for w in words if w not in stop][:8]

    def _overall_status(self, fact_checks: List[FactCheckItem]) -> str:
        if not fact_checks:
            return "pending"
        statuses = {f.status for f in fact_checks}
        if statuses <= {"verified"}:
            return "verified"
        if "unsupported" in statuses:
            return "flagged"
        return "partial"

    def _research_quality(
        self,
        sources: List[ResearchSource],
        fact_checks: List[FactCheckItem],
    ) -> float:
        source_score = min(1.0, len(sources) / 5.0) * 0.5
        if not fact_checks:
            return round(source_score, 2)
        verified_ratio = sum(1 for f in fact_checks if f.status == "verified") / len(fact_checks)
        return round(source_score + verified_ratio * 0.5, 2)
