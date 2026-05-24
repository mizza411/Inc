"""Tests for launch content batch (Phase 4.2)."""

from pathlib import Path

from core.launch_batch import LAUNCH_TOPICS, LaunchBatchRunner
from main import YouTubeBusinessSystem


def test_launch_topics_meet_minimum():
    assert len(LAUNCH_TOPICS) >= 10


def test_launch_batch_dry_run_plans_enough_videos():
    system = YouTubeBusinessSystem()
    runner = LaunchBatchRunner(system, exports_dir=Path("exports/launch_batches"))
    manifest = runner.run(count=12, dry_run=True, use_trends=True)

    assert manifest.dry_run is True
    assert manifest.planned_count >= 10
    assert manifest.success_count == 0
    assert Path(manifest.export_path).is_file()


def test_launch_batch_plan_deduplicates():
    system = YouTubeBusinessSystem()
    runner = LaunchBatchRunner(system)
    planned = runner.plan_topics(count=20, use_trends=False)

    topics = [p["topic"].lower() for p in planned]
    assert len(topics) == len(set(topics))
