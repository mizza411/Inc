"""
Static analytics dashboard generator for the YouTube automation pipeline.

Reads SQLite metrics and writes a self-contained HTML dashboard under web/.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from database.youtube_schema import YouTubeDatabase

logger = logging.getLogger(__name__)


class AnalyticsDashboard:
    """Build a local HTML dashboard from tracked content and performance data."""

    def __init__(self, db_path: Optional[Union[str, Path]] = None):
        base = Path(__file__).resolve().parent.parent
        self.db_path = Path(db_path or base / "data" / "youtube_business.db")
        self.web_dir = base / "web"
        self.exports_dir = base / "exports"
        self.db = YouTubeDatabase(str(self.db_path))

    def collect_data(self) -> Dict[str, Any]:
        """Gather all dashboard metrics from the database."""
        return {
            "generated_at": datetime.now().isoformat(),
            "database": str(self.db_path),
            "content_quality": self.db.get_content_quality_summary(),
            "performance_totals": self.db.get_performance_totals(),
            "business_metrics": self.db.get_business_metrics_summary(),
            "schedule_summary": self.db.get_schedule_summary(),
            "recent_videos": self.db.list_videos(limit=15),
            "top_performing_videos": self.db.get_top_performing_videos(limit=10),
            "upcoming_schedule": self.db.list_schedule(
                status="planned",
                from_date=datetime.now().date().isoformat(),
                limit=15,
            ),
            "monetization_ready": self.db.get_monetization_ready_videos()[:10],
        }

    def generate_html(
        self,
        output_path: Optional[Union[str, Path]] = None,
    ) -> Path:
        """Render dashboard HTML and return the output path."""
        data = self.collect_data()
        out = Path(output_path or self.web_dir / "analytics_dashboard.html")
        out.parent.mkdir(parents=True, exist_ok=True)

        html = self._render_page(data)
        out.write_text(html, encoding="utf-8")
        logger.info("Analytics dashboard written to %s", out)

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = self.exports_dir / f"analytics_snapshot_{stamp}.json"
        self.exports_dir.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")

        return out

    def close(self) -> None:
        self.db.close()

    def _render_page(self, data: Dict[str, Any]) -> str:
        quality = data.get("content_quality") or {}
        perf = data.get("performance_totals") or {}
        schedule = data.get("schedule_summary") or {}

        kpis = [
            ("Videos tracked", _fmt_num(quality.get("video_count"))),
            ("Avg quality score", _fmt_score(quality.get("avg_quality"))),
            ("Planned slots", _fmt_num(schedule.get("planned", 0))),
            ("Total views (latest)", _fmt_num(perf.get("total_views"))),
        ]

        kpi_cards = "".join(
            '<div class="kpi"><label>{label}</label><strong>{value}</strong></div>'.format(
                label=_esc(label), value=value
            )
            for label, value in kpis
        )

        sections = [
            _section_table(
                "Recent videos",
                ["ID", "Title", "Niche", "Status", "Quality"],
                data.get("recent_videos") or [],
                lambda r: [
                    r.get("id"),
                    r.get("title"),
                    r.get("content_niche"),
                    r.get("status"),
                    _fmt_score(r.get("high_effort_score")),
                ],
            ),
            _section_table(
                "Upcoming schedule",
                ["Date", "Topic", "Niche", "Status"],
                data.get("upcoming_schedule") or [],
                lambda r: [
                    r.get("scheduled_date"),
                    r.get("topic_title"),
                    r.get("content_niche"),
                    r.get("status"),
                ],
            ),
            _section_table(
                "Top performing (latest metrics)",
                ["Title", "Views", "Likes", "Watch time (min)"],
                data.get("top_performing_videos") or [],
                lambda r: [
                    r.get("title"),
                    r.get("views"),
                    r.get("likes"),
                    r.get("watch_time_minutes"),
                ],
            ),
            _section_table(
                "Monetization-ready drafts",
                ["Title", "Score", "Duration (min)", "Niche"],
                data.get("monetization_ready") or [],
                lambda r: [
                    r.get("title"),
                    _fmt_score(r.get("high_effort_score")),
                    r.get("actual_duration_minutes"),
                    r.get("content_niche"),
                ],
            ),
        ]

        body = "\n    ".join(sections)
        generated = _esc(data.get("generated_at", ""))
        db_name = _esc(Path(str(data.get("database", ""))).name)

        return (
            "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
            "  <meta charset=\"UTF-8\">\n"
            "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
            "  <title>YouTube Automation Analytics Dashboard</title>\n"
            "  <style>\n"
            "    :root { --card: #1e293b; --text: #f8fafc; --muted: #94a3b8; --accent: #38bdf8; }\n"
            "    * { box-sizing: border-box; margin: 0; padding: 0; }\n"
            "    body { font-family: Segoe UI, system-ui, sans-serif; "
            "background: linear-gradient(160deg, #0f172a, #1e3a5f); "
            "color: var(--text); min-height: 100vh; padding: 24px 16px; }\n"
            "    .wrap { max-width: 1100px; margin: 0 auto; }\n"
            "    header { margin-bottom: 24px; }\n"
            "    h1 { font-size: 1.6rem; margin-bottom: 6px; }\n"
            "    .sub { color: var(--muted); font-size: 0.9rem; }\n"
            "    .kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); "
            "gap: 12px; margin-bottom: 24px; }\n"
            "    .kpi { background: var(--card); border-radius: 12px; padding: 16px; border: 1px solid #334155; }\n"
            "    .kpi label { display: block; color: var(--muted); font-size: 0.75rem; text-transform: uppercase; }\n"
            "    .kpi strong { font-size: 1.5rem; margin-top: 6px; display: block; }\n"
            "    section { background: var(--card); border-radius: 12px; padding: 16px; "
            "border: 1px solid #334155; margin-bottom: 16px; }\n"
            "    h2 { font-size: 1rem; margin-bottom: 12px; color: var(--accent); }\n"
            "    table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }\n"
            "    th, td { text-align: left; padding: 8px 6px; border-bottom: 1px solid #334155; }\n"
            "    th { color: var(--muted); font-weight: 600; }\n"
            "    .empty { color: var(--muted); font-style: italic; padding: 8px 0; }\n"
            "  </style>\n</head>\n<body>\n"
            "  <div class=\"wrap\">\n"
            "    <header>\n"
            "      <h1>YouTube Automation Analytics</h1>\n"
            f"      <p class=\"sub\">Generated {generated} · DB: {db_name}</p>\n"
            "    </header>\n"
            f"    <div class=\"kpis\">{kpi_cards}</div>\n"
            f"    {body}\n"
            "  </div>\n</body>\n</html>"
        )


def _section_table(title: str, headers: List[str], rows: List[Dict], row_fn) -> str:
    if not rows:
        return f'<section><h2>{escape(title)}</h2><p class="empty">No data yet.</p></section>'

    head = "".join(f"<th>{escape(h)}</th>" for h in headers)
    body_rows = []
    for row in rows:
        cells = row_fn(row)
        tds = "".join(f"<td>{escape(str(c if c is not None else ''))}</td>" for c in cells)
        body_rows.append(f"<tr>{tds}</tr>")

    return (
        f"<section><h2>{escape(title)}</h2>"
        f"<table><thead><tr>{head}</tr></thead>"
        f"<tbody>{''.join(body_rows)}</tbody></table></section>"
    )


def _esc(value: Any) -> str:
    return escape(str(value if value is not None else ""))


def _fmt_num(value: Any) -> str:
    if value is None:
        return "0"
    try:
        n = float(value)
        return f"{int(n):,}" if n == int(n) else f"{n:,.1f}"
    except (TypeError, ValueError):
        return "0"


def _fmt_score(value: Any) -> str:
    if value is None:
        return "-"
    try:
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        return "-"
