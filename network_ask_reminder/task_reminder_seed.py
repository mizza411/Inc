"""
AUTO-NAR-05 — optional Task Reminder recurring seed.

SKIPPED (Phase 4, 2026-08-08): Task Reminder JSON layout / upsert API path is not
clear enough to seed safely without risking other tasks. Prefer:
  - Inc Hub schedule (Phase 3) + project_reminder is_document open (AUTO-NAR-04)
Revisit only with an explicit owner-approved tasks.json schema path.
"""

SKIP_REASON = (
    "Task Reminder seed deferred — unclear safe upsert path; "
    "Hub schedule + PR docx open cover the habit nudge."
)


def seed_status() -> str:
    return f"SKIPPED: {SKIP_REASON}"
