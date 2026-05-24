# YouTube Automation — CLI Reference

Run all commands from the `youtube/` folder:

```powershell
cd Strategy-2-Problem-Solving\Content-Automation\youtube
python main.py <command> [options]
```

## Quick start

| Goal | Command |
|------|---------|
| Check system health | `python main.py status` |
| Create one video | `python main.py create "Afrobeats" music` |
| Plan launch queue | `python main.py launch --dry-run` |
| Run health alerts | `python main.py monitor` |
| Run all tests | `python main.py test` |

---

## Core commands

### `demo`
Runs a short demonstration of language blending, song analysis, trends, and script generation.

```powershell
python main.py demo
```

### `status`
Prints JSON system status: settings, component readiness, monetization checklist.

```powershell
python main.py status
```

### `create <topic> [context]`
Full pipeline for one video:
1. Language blends  
2. Trending songs + topics  
3. Script + research + subtitles  
4. Video assembly  
5. Performance tracking (SQLite)

```powershell
python main.py create "Lagos Tech Startups" technology
python main.py create "Afrobeats" music
```

**Contexts:** `music`, `culture`, `food`, `technology`, `lifestyle`, etc.

---

## Batch & launch (Phase 4)

### `batch <topic1,topic2,...> [context]`
Creates multiple videos and exports a manifest to `exports/launch_batches/`.

```powershell
python main.py batch "Topic A,Topic B,Topic C" culture
```

### `launch [count] [--dry-run]`
Launch content batch using 12 curated Nigerian-culture topics (+ trend enrichment).

```powershell
python main.py launch --dry-run    # plan only, no creation
python main.py launch 12           # create 12 videos (~30–45 min)
```

Manifest: `exports/launch_batches/launch_*.json`

---

## Phase 3 features

### `trends`
Trending topic analysis (Google Trends when available, offline fallback otherwise).

```powershell
python main.py trends
```

Export: `exports/trending_topics_*.json`

### `performance [summary|import]`
Content quality and performance summary from SQLite.

```powershell
python main.py performance
python main.py performance import exports/youtube_metrics.json
```

### `schedule plan [days] | list | run-due [--dry-run]`
Content calendar from trending topics.

```powershell
python main.py schedule plan 14
python main.py schedule list
python main.py schedule run-due --dry-run
python main.py schedule run-due
```

### `dashboard`
Generates HTML analytics dashboard.

```powershell
python main.py dashboard
# Then: python -m http.server 8000
# Open: http://localhost:8000/web/analytics_dashboard.html
```

### `research <topic>`
Research and fact-check for a topic (builds script first).

```powershell
python main.py research "Nigeria economy"
```

### `subtitles <topic>`
Generate SRT + WebVTT subtitle files only.

```powershell
python main.py subtitles Afrobeats
```

Output: `exports/subtitles/*.srt` and `*.vtt`

---

## Monitoring & testing (Phase 4)

### `monitor`
Checks schedule misses, quality drops, and launch batch failures.

```powershell
python main.py monitor
```

- Exit code `0` = healthy  
- Exit code `1` = critical or warning alerts  
- Report: `exports/monitoring/monitoring_report_*.json`

### `test`
E2E smoke test + full pytest suite (17+ tests).

```powershell
python main.py test
```

---

## Other commands

### `report [folder]`
Exports a comprehensive system JSON report.

```powershell
python main.py report reports
```

---

## Data locations

| Path | Purpose |
|------|---------|
| `data/youtube_business.db` | Videos, schedule, analytics (gitignored) |
| `exports/` | JSON exports, subtitles, manifests (gitignored) |
| `web/analytics_dashboard.html` | Generated dashboard |
| `output/` | Assembled video metadata |

---

## Requirements

Minimal Phase 3 install:

```powershell
pip install -r requirements-phase3-minimal.txt
```

Full install:

```powershell
pip install -r requirements.txt
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Unicode/emoji errors on Windows | Commands auto-reconfigure UTF-8 in `main()` |
| Google Trends timeout | Offline fallback topics used automatically |
| `monitor` exit code 1 | Review `exports/monitoring/` report; run overdue schedule slots |
| SQLite locked on Windows | Close DB connections; avoid deleting temp DB while open |

See also: [LAUNCH_CHECKLIST.md](LAUNCH_CHECKLIST.md)
