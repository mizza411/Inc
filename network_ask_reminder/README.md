# network_ask_reminder — NET-ASK-REMIND-1

Habit tool: nudge you **Mon / Wed / Fri** to ask **people around you (Strategy 3)** or **business owners (Strategy 4)** for problems, then log answers locally.

**Authoritative backlog:** `.cursor/rules/task_net_ask_remind.md`  
**Locks (Phase 0):** surfaces **both** (Inc Hub + project_reminder) · rotate **alternate S3↔S4** · capture **local log + pointers**  
**Status:** Phase **5** playbook ✅ · Phase 6 = owner asks + one `MANUAL_TEST` pass

## Surfaces

| Surface | What |
|---------|------|
| **Inc Hub** | Pinned **Ask people / owners (S3+S4)** · schedule `network_ask_mwf` 09:30 M/W/F |
| **project_reminder** | Additive `ask_people_ask_owners_playbook` (`is_document`) opens `.docx` on boot |

## Hub (Phase 3)

- Pillar **Problem identification** → pinned **Ask people / owners (S3+S4)**
- Schedule **`network_ask_mwf`**: Mon/Wed/Fri **09:30** → Option B Hub modal (tray must be running)
- **Start** → open playbook + copy openers (you still send). **Not now** dismisses.

## Files


| File | Role |
|------|------|
| `ask_people_ask_owners_playbook.md` / `.docx` | Full ritual playbook (Phase 5) |
| `config.example.json` | Cadence / rotate / surfaces schema (**AUTO-NAR-01**) |
| `hub_nudge.py` | **AUTO-NAR-03** Hub modal copy + Start |
| `build_docx.py` / `pr_launcher.py` | **AUTO-NAR-08/04** pandoc + PR launcher validate |
| `task_reminder_seed.py` | **AUTO-NAR-05** skipped (documented) |
| `config_loader.py` / `rotate.py` / `ask_log.py` / `status_report.py` / `openers.py` / `isolation.py` / `cli.py` | Phase 2 automation |
| `MANUAL_TEST.md` | Owner-only steps (**MAN-NAR-***) |
| `data/` | Ask logs (gitignored `*.jsonl`) |

## CLI (from Inc root)

```powershell
python -m network_ask_reminder validate-config
python -m network_ask_reminder today
python -m network_ask_reminder today --date 2026-08-12
python -m network_ask_reminder log-add --mode s3 --notes "problem summary" --role "classmate"
python -m network_ask_reminder status
python -m network_ask_reminder openers --mode both
python -m network_ask_reminder isolation-check
```

Optional: copy `config.example.json` → `config.json` (gitignored) for local overrides.

```powershell
python -m network_ask_reminder build-docx
python -m network_ask_reminder build-docx --check
python -m network_ask_reminder validate-pr-launcher
python -m network_ask_reminder task-reminder-seed-status
```

Or:

```powershell
pandoc network_ask_reminder/ask_people_ask_owners_playbook.md -o network_ask_reminder/ask_people_ask_owners_playbook.docx
```

## Smokes

```powershell
python -m unittest network_ask_reminder.tests.test_phase2_smoke network_ask_reminder.tests.test_phase3_smoke network_ask_reminder.tests.test_phase4_smoke -v
```

## Do not touch (isolation)

- Tegrid / FIR / OTI / Land Sales OS / gadget ops / bookmark sorter
- Strategy 1/5/12/15 CLIs · `run_all_strategies` Run ALL membership for S3/S4
- Problem ID questionnaire schema
- Auto-DM / scrape contacts / send WhatsApp for the user
- Detached OS toasts; prefer Hub Option B + PR `is_document` open (Phases 3–4)

## Related

- Strategy 3: `Business-Idea-Formulation-Strategy-3-Network-Based-Problem-Identification/`
- Strategy 4: `Business-Idea-Formulation-Strategy-4-Business-Owner-Problem-Collection/`
- Optional capture: `problem_identification_tool/`
