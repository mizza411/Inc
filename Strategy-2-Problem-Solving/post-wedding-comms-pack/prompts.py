"""Prompt and static template builders for guest and vendor messages."""

from __future__ import annotations


def _clean(value) -> str:
    if value is None or (isinstance(value, float) and str(value) == "nan"):
        return ""
    return str(value).strip()


def build_guest_prompt(row: dict, couple_names: str = "we") -> str:
    name = _clean(row.get("Name"))
    gift = _clean(row.get("GiftOrSpray"))
    relationship = _clean(row.get("Relationship"))
    event = _clean(row.get("EventAttended"))

    parts = [
        f"Write a warm, personal wedding thank-you message from {couple_names} to {name}.",
        "Keep it 2–4 sentences, suitable for WhatsApp.",
        "Tone: grateful, Nigerian wedding context, not overly formal.",
    ]
    if relationship:
        parts.append(f"Their relationship to the couple: {relationship}.")
    if gift:
        parts.append(f"Mention their gift or spray contribution: {gift}.")
    if event:
        parts.append(f"They attended: {event}.")
    parts.append("Do not include placeholders; write the final message only.")
    return " ".join(parts)


def build_vendor_thank_you(row: dict, couple_names: str = "we") -> str:
    name = _clean(row.get("Name"))
    role = _clean(row.get("Role"))
    notes = _clean(row.get("Notes"))
    base = (
        f"Dear {name},\n\n"
        f"Thank you so much for your wonderful work as our {role or 'vendor'} at our wedding. "
        f"Your professionalism made our day special.\n\n"
        f"With gratitude,\n{couple_names}"
    )
    if notes:
        base = base.replace(
            "Your professionalism made our day special.",
            f"Your professionalism made our day special. {notes}",
        )
    return base


def build_vendor_review_request(row: dict, couple_names: str = "we") -> str:
    name = _clean(row.get("Name"))
    role = _clean(row.get("Role"))
    link = _clean(row.get("ReviewLink"))
    msg = (
        f"Hi {name}, hope you are well! We loved having you as our {role or 'vendor'}. "
        f"If you have a moment, a short review would mean a lot to us"
    )
    if link:
        msg += f": {link}"
    msg += f". Thank you again! — {couple_names}"
    return msg
