"""Optional SendGrid email delivery (legacy / diaspora path)."""

from __future__ import annotations

import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_thank_you_email(to_email: str, subject: str, body: str) -> tuple[bool, str | None]:
    api_key = os.getenv("SENDGRID_API_KEY")
    sender = os.getenv("SENDER_EMAIL")
    if not api_key or not sender:
        return False, "Missing SENDGRID_API_KEY or SENDER_EMAIL in .env file."
    if not to_email or str(to_email).strip() == "":
        return False, "No email address for this recipient."

    message = Mail(
        from_email=sender,
        to_emails=str(to_email).strip(),
        subject=subject,
        plain_text_content=body,
    )
    try:
        sg = SendGridAPIClient(api_key)
        sg.send(message)
        return True, None
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)
