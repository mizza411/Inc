"""
Trending topic analysis for YouTube content planning.

Fetches rising search topics (Google Trends via pytrends when available) and
produces ranked topic ideas with Nigerian/cultural angle suggestions for scripts.
"""

from __future__ import annotations

import json
import logging
import random
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

DEFAULT_SEED_KEYWORDS = [
    "afrobeats",
    "nigerian music",
    "lagos",
    "nollywood",
    "naira",
    "super eagles",
    "jollof",
    "tech startup nigeria",
]


@dataclass
class TrendingTopic:
    """A single trending topic candidate for video content."""

    query: str
    source: str
    region: str
    score: float
    category: str = "general"
    related_queries: List[str] = field(default_factory=list)


@dataclass
class TopicAnalysisReport:
    """Aggregated trending topic analysis."""

    topics: List[TrendingTopic]
    top_picks: List[TrendingTopic]
    video_ideas: List[Dict[str, str]]
    regions_checked: List[str]
    used_live_data: bool
    analysis_timestamp: datetime
    confidence_score: float

    def to_dict(self) -> Dict:
        data = asdict(self)
        data["analysis_timestamp"] = self.analysis_timestamp.isoformat()
        return data


class TrendingTopicAnalyzer:
    """Discover trending topics for faceless YouTube scripts (music, culture, news-adjacent)."""

    def __init__(
        self,
        geo_primary: str = "NG",
        geo_fallback: str = "US",
        seed_keywords: Optional[List[str]] = None,
        max_topics: int = 15,
    ):
        self.geo_primary = geo_primary
        self.geo_fallback = geo_fallback
        self.seed_keywords = seed_keywords or list(DEFAULT_SEED_KEYWORDS)
        self.max_topics = max_topics

    def analyze(self) -> TopicAnalysisReport:
        """Run topic discovery; uses live Trends when possible, else curated fallback."""
        logger.info("Starting trending topic analysis (geo=%s)...", self.geo_primary)

        topics: List[TrendingTopic] = []
        regions_checked: List[str] = []
        used_live = False

        live_topics, regions = self._fetch_google_trends()
        if live_topics:
            topics.extend(live_topics)
            regions_checked.extend(regions)
            used_live = True

        if len(topics) < 3:
            topics.extend(self._fallback_topics())
            regions_checked.append("fallback_curated")

        topics = self._dedupe_and_rank(topics)[: self.max_topics]
        top_picks = topics[: min(5, len(topics))]
        video_ideas = self.suggest_video_ideas(top_picks)
        confidence = 0.85 if used_live else 0.55

        return TopicAnalysisReport(
            topics=topics,
            top_picks=top_picks,
            video_ideas=video_ideas,
            regions_checked=sorted(set(regions_checked)),
            used_live_data=used_live,
            analysis_timestamp=datetime.now(),
            confidence_score=confidence,
        )

    def suggest_video_ideas(self, topics: List[TrendingTopic]) -> List[Dict[str, str]]:
        """Turn topics into faceless-video pitch lines (English–Yoruba channel angle)."""
        ideas: List[Dict[str, str]] = []
        templates = [
            "Why {query} is everywhere right now (Nigerian take)",
            "Sha, let's break down {query} for the diaspora",
            "Omo — {query} explained with culture + context",
            "{query}: what it means for Nigeria this week",
        ]

        for topic in topics[:8]:
            template = random.choice(templates)
            title = template.format(query=topic.query.title())
            ideas.append(
                {
                    "title": title,
                    "topic": topic.query,
                    "category": topic.category,
                    "hook_angle": f"Trending in {topic.region} via {topic.source}",
                }
            )
        return ideas

    def export_report(self, report: TopicAnalysisReport, exports_dir: Optional[Path] = None) -> Path:
        """Write analysis JSON under youtube/exports/."""
        base = exports_dir or Path(__file__).resolve().parent.parent / "exports"
        base.mkdir(parents=True, exist_ok=True)
        stamp = report.analysis_timestamp.strftime("%Y%m%d_%H%M%S")
        path = base / f"trending_topics_{stamp}.json"
        with path.open("w", encoding="utf-8") as f:
            json.dump(report.to_dict(), f, indent=2, ensure_ascii=False)
        logger.info("Exported topic analysis to %s", path)
        return path

    def topic_terms(self, report: TopicAnalysisReport, limit: int = 8) -> List[str]:
        """Flat list of topic strings for script generator / tags."""
        terms: List[str] = []
        for t in report.top_picks:
            terms.append(t.query)
            terms.extend(t.related_queries[:2])
        return list(dict.fromkeys(terms))[:limit]

    def _fetch_google_trends(self) -> tuple[List[TrendingTopic], List[str]]:
        topics: List[TrendingTopic] = []
        regions: List[str] = []

        try:
            from pytrends.request import TrendReq
        except ImportError:
            logger.warning("pytrends not installed; skipping live Google Trends")
            return topics, regions

        pytrends = TrendReq(hl="en-US", tz=60)

        for geo in (self.geo_primary, self.geo_fallback):
            try:
                df = pytrends.trending_searches(pn=geo)
                if df is not None and not df.empty:
                    regions.append(geo)
                    for row in df.head(10).itertuples(index=False):
                        query = str(row[0]).strip()
                        if query:
                            topics.append(
                                TrendingTopic(
                                    query=query,
                                    source="google_trends_trending_searches",
                                    region=geo,
                                    score=9.0 - len(topics) * 0.1,
                                    category=self._guess_category(query),
                                )
                            )
            except Exception as exc:
                logger.debug("trending_searches %s failed: %s", geo, exc)

        for keyword in self.seed_keywords[:4]:
            related = self._related_queries_safe(pytrends, keyword, self.geo_primary)
            if related is None:
                related = self._related_queries_safe(pytrends, keyword, self.geo_fallback)
            if related is not None and not related.empty:
                regions.append(self.geo_primary)
                for _, row in related.head(5).iterrows():
                    q = str(row.get("query", row.iloc[0])).strip()
                    if q:
                        topics.append(
                            TrendingTopic(
                                query=q,
                                source=f"google_trends_related:{keyword}",
                                region=self.geo_primary,
                                score=7.5,
                                category=self._guess_category(q),
                                related_queries=[keyword],
                            )
                        )
            time.sleep(0.5)

        return topics, regions

    def _related_queries_safe(self, pytrends, keyword: str, geo: str):
        try:
            pytrends.build_payload([keyword], timeframe="today 3-m", geo=geo)
            bundle = pytrends.related_queries().get(keyword)
            if bundle and bundle.get("top") is not None and not bundle["top"].empty:
                return bundle["top"]
        except Exception as exc:
            logger.debug("related_queries %s/%s: %s", keyword, geo, exc)
        return None

    def _fallback_topics(self) -> List[TrendingTopic]:
        """Offline defaults when Trends is unavailable (rate limits, no network)."""
        samples = [
            ("afrobeats new releases", "music"),
            ("cost of living nigeria", "news"),
            ("remote work lagos", "lifestyle"),
            ("nollywood streaming", "entertainment"),
            ("nigerian tech startups", "technology"),
            ("super eagles news", "sports"),
            ("yoruba culture trends", "culture"),
            ("diaspora remittance", "finance"),
        ]
        return [
            TrendingTopic(
                query=q,
                source="curated_fallback",
                region="NG",
                score=6.0 - i * 0.2,
                category=cat,
            )
            for i, (q, cat) in enumerate(samples)
        ]

    def _dedupe_and_rank(self, topics: List[TrendingTopic]) -> List[TrendingTopic]:
        seen: Dict[str, TrendingTopic] = {}
        for t in topics:
            key = t.query.lower().strip()
            if not key:
                continue
            existing = seen.get(key)
            if existing is None or t.score > existing.score:
                seen[key] = t
        return sorted(seen.values(), key=lambda x: x.score, reverse=True)

    def _guess_category(self, query: str) -> str:
        q = query.lower()
        if any(w in q for w in ("song", "music", "afro", "artist", "album")):
            return "music"
        if any(w in q for w in ("movie", "nollywood", "show", "celebrity")):
            return "entertainment"
        if any(w in q for w in ("naira", "price", "fuel", "economy", "inflation")):
            return "news"
        if any(w in q for w in ("football", "super eagles", "sport", "match")):
            return "sports"
        if any(w in q for w in ("tech", "startup", "phone", "app")):
            return "technology"
        return "general"


def run_cli_analysis() -> TopicAnalysisReport:
    """CLI helper: analyze and export, return report."""
    analyzer = TrendingTopicAnalyzer()
    report = analyzer.analyze()
    analyzer.export_report(report)
    return report
