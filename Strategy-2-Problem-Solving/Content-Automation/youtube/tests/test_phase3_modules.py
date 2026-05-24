"""Integration tests for Phase 3 modules (3.1–3.5)."""

import json
from pathlib import Path

from core.analytics_dashboard import AnalyticsDashboard
from core.content_scheduler import ContentScheduler
from core.performance_tracker import ContentPerformanceTracker
from core.research_engine import ResearchEngine
from core.script_generator import ScriptGenerator
from core.topic_analyzer import TrendingTopicAnalyzer
from main import YouTubeBusinessSystem, _parse_uploads_per_week


def test_parse_uploads_per_week():
    assert _parse_uploads_per_week("3x per week") == 3
    assert _parse_uploads_per_week("") == 3


def test_topic_analyzer_offline_report():
    analyzer = TrendingTopicAnalyzer()
    report = analyzer.analyze()

    assert len(report.top_picks) >= 1
    assert report.confidence_score > 0
    terms = analyzer.topic_terms(report)
    assert isinstance(terms, list)
    assert len(terms) >= 1


def test_research_engine_analyze_topic():
    engine = ResearchEngine()
    script_data = {
        "title": "Nigeria economy overview",
        "hook": "Nigeria has one of the largest economies in Africa.",
        "introduction": "We review recent trends and data points.",
        "main_content": ["Population growth affects infrastructure demand."],
        "conclusion": "Stay informed with verified sources.",
        "call_to_action": "Like and subscribe.",
    }
    report = engine.analyze_topic("Nigeria economy", script_data)

    assert report.topic == "Nigeria economy"
    assert len(report.sources) >= 1
    assert 0 <= report.research_quality_score <= 1
    assert report.fact_checking_status in ("verified", "partial", "flagged", "pending")


def test_research_export(tmp_path: Path):
    engine = ResearchEngine(exports_dir=tmp_path)
    report = engine.analyze_topic("Lagos tech", {"title": "Lagos tech"})
    path = engine.export_report(report)

    assert Path(path).is_file()
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    assert data["topic"] == "Lagos tech"


def test_performance_tracker_summary(tmp_path: Path):
    db_path = tmp_path / "test_youtube.db"
    tracker = ContentPerformanceTracker(db_path=db_path)
    summary = tracker.get_summary()

    assert "database" in summary
    assert "content_quality" in summary
    tracker.db.close()


def test_content_scheduler_plan(tmp_path: Path):
    db_path = tmp_path / "sched.db"
    scheduler = ContentScheduler(db_path=db_path, uploads_per_week=2)
    created = scheduler.generate_plan(days_ahead=7)

    assert len(created) >= 1
    upcoming = scheduler.list_upcoming(limit=5)
    assert isinstance(upcoming, list)
    scheduler.db.close()


def test_analytics_dashboard_html(tmp_path: Path):
    db_path = tmp_path / "dash.db"
    web_dir = tmp_path / "web"
    exports_dir = tmp_path / "exports"

    dashboard = AnalyticsDashboard(db_path=db_path)
    dashboard.web_dir = web_dir
    dashboard.exports_dir = exports_dir

    out = dashboard.generate_html()
    html = Path(out).read_text(encoding="utf-8")

    assert "<html" in html
    assert "YouTube Automation Analytics" in html
    assert "<motion" not in html.lower()
    dashboard.close()


def test_system_status_all_components_ready():
    system = YouTubeBusinessSystem()
    status = system.get_system_status()

    assert status["status"] in ("operational", "warning")
    components = status["components"]
    for key in (
        "topic_analyzer",
        "performance_tracker",
        "content_scheduler",
        "analytics_dashboard",
        "research_engine",
        "subtitle_generator",
    ):
        assert components[key] == "ready"
