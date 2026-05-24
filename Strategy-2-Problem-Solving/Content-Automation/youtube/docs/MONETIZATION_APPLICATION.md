# YouTube Partner Program — Application Guide

Apply for monetization after your channel meets YouTube's thresholds and your pipeline produces eligible content.

## Automated checks

```powershell
python main.py monetization init-metrics   # create data/monetization_metrics.json
python main.py monetization check          # full readiness report
python main.py monetization --metrics path/to/metrics.json
```

Report export: `exports/monetization/monetization_application_*.json`

## YouTube Partner Program thresholds

| Requirement | Target |
|-------------|--------|
| Subscribers | 1,000 |
| Public watch hours (12 months) | 4,000 |
| Content policies | No active strikes |
| 2-Step Verification | Required on Google account |

## Pipeline content requirements (automated)

The system enforces:
- **8+ minute** scripts/videos (`min_video_length` ≥ 480 seconds)
- **High-effort validation** enabled
- **Research + subtitles** on each `create` run
- **Quality score ≥ 0.8** for monetization-eligible drafts in SQLite

Check system config:
```powershell
python main.py status   # see monetization_checklist
```

## Weekly workflow

1. Create/upload videos from launch batch (`python main.py launch`)
2. Update `data/monetization_metrics.json` from YouTube Studio → Analytics
3. Run `python main.py monetization check`
4. Run `python main.py monitor` for pipeline health
5. When report shows **READY TO APPLY**, apply in YouTube Studio → **Earn**

## Manual application steps (YouTube Studio)

1. Sign in to [YouTube Studio](https://studio.youtube.com)
2. Go to **Earn** → **Apply** for the YouTube Partner Program
3. Accept terms and link **AdSense** (or create account)
4. Wait for review (typically days to weeks)
5. After approval, enable ads on eligible videos

## Metrics file format

Copy from example:
```powershell
copy data\monetization_metrics.example.json data\monetization_metrics.json
```

```json
{
  "subscribers": 1200,
  "watch_hours_12mo": 4500,
  "channel_url": "https://youtube.com/@yourchannel",
  "two_factor_enabled": true,
  "application_submitted": false,
  "adsense_linked": false
}
```

## Related docs

- [youtube_monetization_research.md](youtube_monetization_research.md) — background research
- [LAUNCH_CHECKLIST.md](LAUNCH_CHECKLIST.md) — pre-launch steps
- [CLI_REFERENCE.md](CLI_REFERENCE.md) — all commands

**Phase 4.6** — Last updated 2026-05-24
