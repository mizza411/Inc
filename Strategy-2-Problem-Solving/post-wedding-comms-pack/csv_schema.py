"""CSV column validation and normalization for guest and vendor lists."""

from __future__ import annotations

import pandas as pd

GUEST_REQUIRED = ("Name", "Phone")
GUEST_OPTIONAL = ("GiftOrSpray", "Relationship", "Email", "EventAttended")
VENDOR_REQUIRED = ("Name", "Phone", "Role")
VENDOR_OPTIONAL = ("Email", "ReviewLink", "Notes")

STATUS_PENDING = "Pending"
STATUS_SENT = "Sent"
STATUS_SKIPPED = "Skipped"
STATUSES = (STATUS_PENDING, STATUS_SENT, STATUS_SKIPPED)

# Keep phone/name columns as strings when reading CSV (pandas drops leading 0 otherwise)
CSV_DTYPE = {"Name": str, "Phone": str, "Role": str, "Email": str}


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [str(c).strip() for c in out.columns]
    return out


def validate_guest_csv(df: pd.DataFrame) -> tuple[pd.DataFrame | None, str | None]:
    df = _normalize_columns(df)
    missing = [c for c in GUEST_REQUIRED if c not in df.columns]
    if missing:
        # Legacy: Name + Email only (email path still works)
        if "Name" in df.columns and "Email" in df.columns and "Phone" not in df.columns:
            df["Phone"] = ""
            return prepare_guest_df(df), None
        return None, f"Guest CSV must include columns: {', '.join(GUEST_REQUIRED)}"
    return prepare_guest_df(df), None


def prepare_guest_df(df: pd.DataFrame) -> pd.DataFrame:
    df = _normalize_columns(df)
    for col in GUEST_REQUIRED + GUEST_OPTIONAL:
        if col not in df.columns:
            df[col] = ""
    if "Status" not in df.columns:
        df["Status"] = STATUS_PENDING
    if "Message" not in df.columns:
        df["Message"] = ""
    df["Status"] = df["Status"].apply(
        lambda s: s if s in STATUSES else STATUS_PENDING
    )
    return df


def validate_vendor_csv(df: pd.DataFrame) -> tuple[pd.DataFrame | None, str | None]:
    df = _normalize_columns(df)
    missing = [c for c in VENDOR_REQUIRED if c not in df.columns]
    if missing:
        return None, f"Vendor CSV must include columns: {', '.join(VENDOR_REQUIRED)}"
    return prepare_vendor_df(df), None


def prepare_vendor_df(df: pd.DataFrame) -> pd.DataFrame:
    df = _normalize_columns(df)
    for col in VENDOR_REQUIRED + VENDOR_OPTIONAL:
        if col not in df.columns:
            df[col] = ""
    if "Status" not in df.columns:
        df["Status"] = STATUS_PENDING
    if "Message" not in df.columns:
        df["Message"] = ""
    df["Status"] = df["Status"].apply(
        lambda s: s if s in STATUSES else STATUS_PENDING
    )
    return df
