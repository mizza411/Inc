"""
Launch content batch planner and runner (Phase 4.2).

Builds a 10+ video launch queue from curated topics plus optional trend picks,
runs the full create pipeline, and exports a JSON manifest.
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import asdict, dataclass, is_dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from core.content_scheduler import NICHE_TO_CONTEXT

logger = logging.getLogger(__name__)

# Curated launch lineup — Nigerian culture / monetization-friendly niches
LAUNCH_TOPICS: List[Dict[str, str]] = [
    {"topic": "Afrobeats Global Rise", "context": "music"},
    {"topic": "Lagos Nightlife Culture", "context": "culture"},
    {"topic": "Nollywood Streaming Boom", "context": "culture"},
    {"topic": "Nigerian Tech Startups", "context": "technology"},
    {"topic": "Jollof Wars Taste and Culture", "context": "food"},
    {"topic": "Yoruba Phrases Going Viral", "context": "culture"},
    {"topic": "Super Eagles Fan Culture", "context": "culture"},
    {"topic": "Cost of Living Nigeria Explained", "context": "culture"},
    {"topic": "Diaspora Remittance Impact", "context": "culture"},
    {"topic": "Afrobeats Dance Trends", "context": "music"},
    {"topic": "Nigerian Wedding Traditions", "context": "culture"},
    {"topic": "Pidgin English Evolution", "context": "culture"},
]


@dataclass
class LaunchBatchManifest:
    batch_id: str
    created_at: str
    dry_run: bool
    requested_count: int
    planned_count: int
    success_count: int
    failure_count: int
    topics: List[Dict[str, Any]]
    export_path: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class LaunchBatchRunner:
    """Plan and execute the YouTube channel launch content batch."""

    def __init__(
        self,
        system: Any,
        exports_dir: Optional[Union[str, Path]] = None,
        min_videos: int = 10,
    ):
        base = Path(__file__).resolve().parent.parent
        self.system = system
        self.exports_dir = Path(exports_dir or base / "exports" / "launch_batches")
        self.min_videos = max(10, min_videos)

    def plan_topics(self, count: int = 12, use_trends: bool = True) -> List[Dict[str, str]]:
        """Merge curated launch topics with trend-based video ideas."""
        target = max(count, self.min_videos)
        planned: List[Dict[str, str]] = []
        seen: set[str] = set()

        def add(topic: str, context: str) -> None:
            key = topic.strip().lower()
            if key and key not in seen:
                seen.add(key)
                planned.append({"topic": topic.strip(), "context": context})

        for item in LAUNCH_TOPICS:
            add(item["topic"], item["context"])

        if use_trends and getattr(self.system, "topic_analyzer", None):
            try:
                report = self.system.topic_analyzer.analyze()
                for idea in report.video_ideas:
                    category = idea.get("category", "general")
                    context = NICHE_TO_CONTEXT.get(category, "culture")
                    add(idea.get("title") or idea.get("topic", ""), context)
                for pick in report.top_picks:
                    context = NICHE_TO_CONTEXT.get(pick.category, "culture")
                    add(pick.query, context)
            except Exception as exc:
                logger.warning("Trend enrichment skipped for launch batch: %s", exc)

        return planned[:target]

    def run(
        self,
        count: int = 12,
        dry_run: bool = False,
        delay_seconds: int = 5,
        use_trends: bool = True,
    ) -> LaunchBatchManifest:
        """Plan and optionally execute the launch batch."""
        planned = self.plan_topics(count=count, use_trends=use_trends)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        batch_id = f"launch_{stamp}"

        entries: List[Dict[str, Any]] = []
        success_count = 0
        failure_count = 0

        if dry_run:
            for i, item in enumerate(planned, 1):
                entries.append(
                    {
                        "index": i,
                        "topic": item["topic"],
                        "context": item["context"],
                        "status": "planned",
                    }
                )
        else:
            for i, item in enumerate(planned, 1):
                logger.info("Launch batch %s/%s: %s", i, len(planned), item["topic"])
                result = self.system.create_complete_video(
                    item["topic"],
                    item["context"],
                    target_minutes=8,
                )
                entry = self._manifest_entry(i, item, result)
                entries.append(entry)
                if result.get("success"):
                    success_count += 1
                else:
                    failure_count += 1
                if i < len(planned) and delay_seconds > 0:
                    time.sleep(delay_seconds)

        export_path = self._export(batch_id, dry_run, count, planned, entries, success_count, failure_count)
        return LaunchBatchManifest(
            batch_id=batch_id,
            created_at=datetime.now().isoformat(),
            dry_run=dry_run,
            requested_count=count,
            planned_count=len(planned),
            success_count=success_count,
            failure_count=failure_count,
            topics=entries,
            export_path=str(export_path),
        )

    def _manifest_entry(
        self,
        index: int,
        item: Dict[str, str],
        result: Dict[str, Any],
    ) -> Dict[str, Any]:
        entry: Dict[str, Any] = {
            "index": index,
            "topic": item["topic"],
            "context": item["context"],
            "success": bool(result.get("success")),
            "status": "created" if result.get("success") else "failed",
        }
        if result.get("success"):
            entry.update(
                {
                    "video_title": result.get("video_title"),
                    "estimated_duration": result.get("estimated_duration"),
                    "subtitle_cues": len((result.get("subtitles") or {}).get("cues", [])),
                    "research_quality": (result.get("research") or {}).get("research_quality_score"),
                    "performance_video_id": (result.get("performance_tracking") or {}).get("video_id"),
                    "srt_path": (result.get("subtitles") or {}).get("srt_path"),
                }
            )
        else:
            entry["error"] = result.get("error")
        return entry

    def _export(
        self,
        batch_id: str,
        dry_run: bool,
        count: int,
        planned: List[Dict[str, str]],
        entries: List[Dict[str, Any]],
        success_count: int,
        failure_count: int,
    ) -> Path:
        self.exports_dir.mkdir(parents=True, exist_ok=True)
        path = self.exports_dir / f"{batch_id}.json"
        payload = {
            "batch_id": batch_id,
            "created_at": datetime.now().isoformat(),
            "dry_run": dry_run,
            "requested_count": count,
            "planned_count": len(planned),
            "success_count": success_count,
            "failure_count": failure_count,
            "topics": entries,
        }
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        logger.info("Launch batch manifest exported to %s", path)
        return path

    @staticmethod
    def _json_safe(value: Any) -> Any:
        if is_dataclass(value):
            return asdict(value)
        if isinstance(value, datetime):
            return value.isoformat()
        return value
