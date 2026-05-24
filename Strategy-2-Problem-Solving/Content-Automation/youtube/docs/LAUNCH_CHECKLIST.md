# YouTube Channel Launch Checklist

Use this checklist before publishing your first batch of automated faceless videos.

**Project folder:** `Strategy-2-Problem-Solving/Content-Automation/youtube`  
**Channel (default):** Nigerian Vibes & Vibes

---

## Pre-launch (1–2 days before)

### System verification
- [ ] Run `python main.py status` — all components show `ready`
- [ ] Run `python main.py test` — full suite passes
- [ ] Run `python main.py monitor` — no critical/warning alerts

### Content planning
- [ ] Run `python main.py trends` — review trending topics export
- [ ] Run `python main.py launch --dry-run` — confirm 10+ video queue
- [ ] Run `python main.py schedule plan 14` — fill content calendar

### Quality gates (YouTube monetization)
- [ ] Videos target **8+ minutes** (default in settings)
- [ ] High-effort validation enabled (`quality_validation_enabled: true`)
- [ ] Research + fact-check step runs for each video
- [ ] Subtitles (SRT/VTT) generated for each video

---

## Launch day — content creation

### Option A: Curated launch batch (recommended)
```powershell
cd Strategy-2-Problem-Solving\Content-Automation\youtube
python main.py launch 12
```
- [ ] Confirm manifest in `exports/launch_batches/launch_*.json`
- [ ] Verify `success_count` matches planned videos
- [ ] Review failed entries (if any) and re-run individual topics:
  ```powershell
  python main.py create "<failed topic>" culture
  ```

### Option B: Custom batch
```powershell
python main.py batch "Topic 1,Topic 2,Topic 3,..." music
```

### After go-live
- [ ] Run `python main.py go-live` — dashboard + performance snapshot + launch report
- [ ] Run `python main.py performance` — videos tracked in SQLite
- [ ] Run `python main.py dashboard` — open HTML dashboard
- [ ] Run `python main.py monitor` — confirm no pipeline failures

---

## Upload preparation (manual YouTube steps)

For each created video, gather from exports/outputs:
- [ ] Script title and description (from create result / DB)
- [ ] SRT subtitle file (`exports/subtitles/*.srt`)
- [ ] Thumbnail path (from assembled video metadata)
- [ ] Tags: nigerian, yoruba, culture, trending (defaults in pipeline)

Upload schedule suggestion (matches 3×/week default):
- [ ] Week 1: 3 videos (Mon / Wed / Fri)
- [ ] Week 2: 3 videos
- [ ] Week 3: 3 videos
- [ ] Week 4: 3+ videos

Use `python main.py schedule list` to align with planned slots.

---

## Post-launch monitoring (weekly)

- [ ] `python main.py monitor` — schedule misses, quality drops
- [ ] `python main.py performance` — quality scores trending up
- [ ] `python main.py dashboard` — review recent videos table
- [ ] Import YouTube Studio metrics when available:
  ```powershell
  python main.py performance import <metrics.json>
  ```

---

## Monetization readiness (Phase 4.6 prep)

Before applying for YouTube Partner Program:
- [ ] 1,000+ subscribers (manual YouTube milestone)
- [ ] 4,000+ watch hours in last 12 months
- [ ] 8+ minute average on published videos
- [ ] Original commentary (language blending satisfies this)
- [ ] Consistent upload cadence (3×/week target)

Checklist from system:
```powershell
python main.py status
```
Review `monetization_checklist` in JSON output.

---

## Emergency rollback

If batch creation fails mid-run:
1. Check `exports/launch_batches/*.json` for failed index/topic
2. Run `python main.py monitor` for alert details
3. Re-create failed topics individually with `create`
4. Re-run `python main.py test` before next batch

---

## Related docs

- [CLI_REFERENCE.md](CLI_REFERENCE.md) — all commands
- [faceless_video_strategy.md](faceless_video_strategy.md) — content strategy
- [youtube_monetization_research.md](youtube_monetization_research.md) — monetization requirements

**Last updated:** Phase 4.4 (2026-05-24)
