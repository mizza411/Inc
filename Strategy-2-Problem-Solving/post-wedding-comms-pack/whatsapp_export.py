"""WhatsApp link building and batch export helpers."""

from __future__ import annotations

import urllib.parse

import pandas as pd


def normalize_ng_phone(phone) -> str:
    if phone is None or (isinstance(phone, float) and pd.isna(phone)):
        return ""
    s = str(phone).strip().replace(" ", "").replace("-", "")
    if s.endswith(".0"):
        s = s[:-2]
    if not s:
        return ""
    if s.startswith("+"):
        s = s[1:]
    # Local format: 0803… → 234803…
    if s.startswith("0") and len(s) >= 10:
        s = "234" + s[1:]
    # CSV often drops leading 0 (8031234567) — 10-digit NG mobile
    elif len(s) == 10 and s[0] in "789":
        s = "234" + s
    elif len(s) == 11 and s.startswith("234"):
        pass
    return s


def whatsapp_url(phone: str, message: str) -> str:
    digits = normalize_ng_phone(phone)
    if not digits:
        return ""
    encoded = urllib.parse.quote(message or "")
    return f"https://wa.me/{digits}?text={encoded}"


def build_export_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in df.iterrows():
        message = str(row.get("Message", "") or "")
        phone = row.get("Phone", "")
        rows.append(
            {
                "Name": row.get("Name", ""),
                "Phone": phone,
                "Status": row.get("Status", "Pending"),
                "Message": message,
                "WhatsAppLink": whatsapp_url(phone, message),
            }
        )
    return pd.DataFrame(rows)


def export_copy_text(df: pd.DataFrame) -> str:
    lines: list[str] = []
    for _, row in df.iterrows():
        name = row.get("Name", "")
        message = row.get("Message", "")
        link = row.get("WhatsAppLink", "") or whatsapp_url(
            row.get("Phone", ""), message
        )
        lines.append(f"--- {name} ---")
        lines.append(str(message))
        if link:
            lines.append(link)
        lines.append("")
    return "\n".join(lines).strip()
