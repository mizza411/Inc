"""CLI for network_ask_reminder (Phase 2)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .ask_log import append_ask
from .build_docx import main as build_docx_main
from .config_loader import ConfigError, load_config
from .isolation import run_isolation_checks
from .openers import generate_openers
from .pr_launcher import validate_pr_launcher
from .rotate import day_prompt, parse_date
from .status_report import compute_status, format_status
from .task_reminder_seed import seed_status


def _add_config_arg(p: argparse.ArgumentParser) -> None:
    p.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to config JSON (default: config.json or config.example.json)",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m network_ask_reminder",
        description="NET-ASK-REMIND-1 habit tooling (config, rotate, log, status, openers)",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_val = sub.add_parser("validate-config", help="AUTO-NAR-01 load+validate config")
    _add_config_arg(p_val)

    p_today = sub.add_parser("today", help="AUTO-NAR-02 show today's mode + prompt")
    _add_config_arg(p_today)
    p_today.add_argument("--date", default=None, help="YYYY-MM-DD (default: today)")

    p_log = sub.add_parser("log-add", help="AUTO-NAR-06 append ask to JSONL log")
    _add_config_arg(p_log)
    p_log.add_argument("--mode", required=True, choices=("s3", "s4"))
    p_log.add_argument("--notes", required=True)
    p_log.add_argument("--role", default="", help="Role/context only — no phone numbers")
    p_log.add_argument("--log", type=Path, default=None, help="Override log path")

    p_status = sub.add_parser("status", help="AUTO-NAR-07 last-asked / streak / today")
    _add_config_arg(p_status)
    p_status.add_argument("--date", default=None, help="YYYY-MM-DD for 'today' view")
    p_status.add_argument("--log", type=Path, default=None)

    p_op = sub.add_parser("openers", help="AUTO-NAR-10 print copy-paste openers (no send)")
    _add_config_arg(p_op)
    p_op.add_argument("--mode", choices=("s3", "s4", "both"), default="both")
    p_op.add_argument("--out", type=Path, default=None, help="Optional write path")

    sub.add_parser("isolation-check", help="AUTO-NAR-09 path / cross-link isolation")

    p_docx = sub.add_parser("build-docx", help="AUTO-NAR-08 pandoc md→docx")
    p_docx.add_argument("--check", action="store_true", help="Validate existing docx only")

    sub.add_parser("validate-pr-launcher", help="AUTO-NAR-04 project_reminder launcher entry")
    sub.add_parser("task-reminder-seed-status", help="AUTO-NAR-05 skip status")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.cmd == "isolation-check":
            errors = run_isolation_checks()
            if errors:
                print("FAIL isolation-check:")
                for e in errors:
                    print(f"  - {e}")
                return 1
            print("OK isolation-check")
            return 0

        if args.cmd == "build-docx":
            return build_docx_main(["--check"] if args.check else [])

        if args.cmd == "validate-pr-launcher":
            errors = validate_pr_launcher()
            if errors:
                print("FAIL validate-pr-launcher:")
                for e in errors:
                    print(f"  - {e}")
                return 1
            print("OK validate-pr-launcher")
            return 0

        if args.cmd == "task-reminder-seed-status":
            print(seed_status())
            return 0

        cfg = load_config(args.config if hasattr(args, "config") else None)

        if args.cmd == "validate-config":
            print("OK validate-config")
            print(f"  rotate_mode={cfg['rotate_mode']}")
            print(f"  cadence.days={cfg['cadence']['days']}")
            print(f"  cadence.local_time={cfg['cadence']['local_time']}")
            return 0

        if args.cmd == "today":
            d = parse_date(args.date)
            dp = day_prompt(cfg, d)
            print(f"date: {d.isoformat()}")
            print(f"day: {dp.day_key}")
            print(f"cadence_day: {dp.is_cadence_day}")
            print(f"mode: {dp.mode}")
            print(f"prompt:\n{dp.prompt_text}")
            return 0

        if args.cmd == "log-add":
            row = append_ask(
                cfg,
                mode=args.mode,
                notes=args.notes,
                role=args.role,
                log_path=args.log,
            )
            print("OK log-add")
            print(row)
            return 0

        if args.cmd == "status":
            d = parse_date(args.date)
            report = compute_status(cfg, today=d, log_path=args.log)
            print(format_status(report))
            return 0

        if args.cmd == "openers":
            text = generate_openers(cfg, args.mode)
            if args.out:
                args.out.parent.mkdir(parents=True, exist_ok=True)
                args.out.write_text(text + "\n", encoding="utf-8")
                print(f"OK openers wrote {args.out}")
            else:
                print(text)
            return 0

        print(f"unknown command: {args.cmd}", file=sys.stderr)
        return 2
    except (ConfigError, ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
