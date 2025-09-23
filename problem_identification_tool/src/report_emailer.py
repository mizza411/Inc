#!/usr/bin/env python3
"""
Email Summary Report Generator
Generates a concise summary of recent responses and emails it to stakeholders.
Requires SMTP credentials in config/sharing_config.json
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'config', 'sharing_config.json')


def load_json(path: str) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def format_summary(problems: List[Dict[str, Any]], analytics: Dict[str, Any]) -> Dict[str, str]:
    """Create text and HTML summary strings."""
    total = len(problems)
    categories: Dict[str, int] = {}
    severities: Dict[int, int] = {}

    for p in problems:
        categories[p.get('category', 'unknown')] = categories.get(p.get('category', 'unknown'), 0) + 1
        try:
            sev = int(p.get('severity', 5))
        except Exception:
            sev = 5
        severities[sev] = severities.get(sev, 0) + 1

    top_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]
    sev_order = [str(i) for i in range(1, 11)]

    lines = [
        f"Report generated: {datetime.now().isoformat()}",
        f"Total problems identified: {total}",
        f"Most common categories: {', '.join([f'{k} ({v})' for k,v in top_categories]) if top_categories else '—'}",
        "Severity distribution (1-10): " + ", ".join([f"{s}:{severities.get(int(s),0)}" for s in sev_order])
    ]

    text = "\n".join(lines)

    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height:1.6; color:#333;">
      <h2>Problem Identification - Summary Report</h2>
      <p><strong>Report generated:</strong> {datetime.now().isoformat()}</p>
      <ul>
        <li><strong>Total problems identified:</strong> {total}</li>
        <li><strong>Most common categories:</strong> {', '.join([f'{k} ({v})' for k,v in top_categories]) if top_categories else '—'}</li>
        <li><strong>Severity distribution (1-10):</strong> {', '.join([f"{s}:{severities.get(int(s),0)}" for s in sev_order])}</li>
      </ul>
    </body>
    </html>
    """

    return {"text": text, "html": html}


def send_email(subject: str, text_body: str, html_body: str, recipients: List[str], smtp_config: Dict[str, Any]):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = smtp_config['sender_email']
    msg['To'] = ", ".join(recipients)

    part1 = MIMEText(text_body, 'plain')
    part2 = MIMEText(html_body, 'html')
    msg.attach(part1)
    msg.attach(part2)

    with smtplib.SMTP(smtp_config['smtp_server'], smtp_config['smtp_port']) as server:
        server.starttls()
        if smtp_config.get('sender_email') and smtp_config.get('sender_password'):
            server.login(smtp_config['sender_email'], smtp_config['sender_password'])
        server.sendmail(smtp_config['sender_email'], recipients, msg.as_string())


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate and email a summary report of identified problems.')
    parser.add_argument('--days', type=int, default=7, help='Include problems from the last N days (default: 7)')
    parser.add_argument('--to', nargs='*', help='Override recipient emails')
    parser.add_argument('--print', action='store_true', help='Print the report instead of sending email')
    args = parser.parse_args()

    problems_path = os.path.join(DATA_DIR, 'problems.json')
    analytics_path = os.path.join(DATA_DIR, 'analytics.json')

    problems_data = load_json(problems_path)
    analytics_data = load_json(analytics_path)
    config = load_json(CONFIG_FILE)

    cutoff = datetime.now() - timedelta(days=args.days)
    recent_problems = [p for p in problems_data.get('problems', []) if datetime.fromisoformat(p.get('timestamp', datetime.min.isoformat())) >= cutoff]

    summary = format_summary(recent_problems, analytics_data)

    if args.print:
        print(summary['text'])
        return

    recipients = args.to if args.to else config.get('email_lists', {}).get('contacts', [])
    if not recipients:
        print('No recipients configured. Use --print to view the report or add contacts in config/sharing_config.json')
        return

    smtp_config = config.get('email', {})
    subject = f"Problem Identification - {len(recent_problems)} problems in last {args.days} days"
    send_email(subject, summary['text'], summary['html'], recipients, smtp_config)
    print('Summary report emailed successfully.')

if __name__ == '__main__':
    main()
