"""End-to-end system tests for Phase 4.1 (full create pipeline)."""

from __future__ import annotations

import time
from pathlib import Path

import pytest

from core.performance_tracker import ContentPerformanceTracker
from core.subtitle_generator import SubtitleGenerator
from main import YouTubeBusinessSystem


@pytest.fixture
def system(tmp_path: Path) -> YouTubeBusinessSystem:
    """YouTube system with isolated DB and export paths for E2E runs."""
    sys = YouTubeBusinessSystem()
    sys.subtitle_generator = SubtitleGenerator(output_dir=tmp_path / "subtitles")
    sys.performance_tracker = ContentPerformanceTracker(db_path=tmp_path / "e2e_youtube.db")
    sys.video_assembler.assets_path = str(tmp_path / "assets")
    return sys


def test_create_complete_video_e2e(system: YouTubeBusinessSystem, tmp_path: Path):
    result = system.create_complete_video(
        "Afrobeats E2E Test",
        context="music",
        target_minutes=8,
    )

    assert result["success"] is True, result.get("error")
    assert result["video_title"]
    assert result["estimated_duration"] >= 8
    assert len(result["language_blends"]) >= 1
    assert len(result["trending_songs"]) >= 1

    research = result["research"]
    assert research["topic"] == "Afrobeats E2E Test"
    assert research["research_quality_score"] >= 0

    subtitles = result["subtitles"]
    assert len(subtitles["cues"]) >= 1
    assert Path(subtitles["srt_path"]).is_file()
    assert Path(subtitles["vtt_path"]).is_file()

    assembled = result["assembled_video"]
    assert assembled.total_duration > 0
    assert assembled.segments

    tracking = result.get("performance_tracking")
    assert tracking is not None
    assert tracking["video_id"] > 0
    assert tracking["validation_score"] > 0

    system.performance_tracker.db.close()


def test_generate_content_batch_e2e(system: YouTubeBusinessSystem, monkeypatch):
    monkeypatch.setattr(time, "sleep", lambda *_args, **_kwargs: None)

    results = system.generate_content_batch(
        ["Batch Topic One", "Batch Topic Two"],
        context="culture",
    )

    assert len(results) == 2
    assert all(r["success"] for r in results), [r.get("error") for r in results]


def test_schedule_run_due_dry_run(system: YouTubeBusinessSystem):
    system.content_scheduler.generate_plan(days_ahead=7)
    due = system.content_scheduler.run_due(
        lambda topic, ctx, mins: system.create_complete_video(topic, ctx, target_minutes=mins),
        dry_run=True,
    )
    assert isinstance(due, list)


def test_system_status_after_e2e(system: YouTubeBusinessSystem):
    status = system.get_system_status()
    checklist = status["monetization_checklist"]

    assert checklist["8+ minute videos"] is True
    assert checklist["High-effort content"] is True
    assert status["components"]["video_assembler"] == "ready"
