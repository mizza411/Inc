"""Single-session Streamlit AppTest smoke for P0 UI (MANUAL_TEST §A/C/E/F).

Run: python test_streamlit_p0.py
      python -m unittest test_streamlit_p0 -v

One app session avoids repeated cold starts (which caused hangs/flakes).
Export download buttons are not in AppTest 1.58 — see test_p0_flow.py for CSV/links.
"""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from whatsapp_export import build_export_dataframe

_ENV = {
    "PAYMENTS_DISABLED": "1",
    "PAYSTACK_SECRET_KEY": "",
    "LLM_PROVIDER": "deepseek",
    "DEEPSEEK_API_KEY": "",
    "LLM_API_KEY": "",
    "OPENAI_API_KEY": "",
    "NGPT_API_KEY": "",
}


def _run_app():
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=15)
    at.run()
    if at.exception:
        raise AssertionError(f"App load failed: {at.exception[0].value}")
    return at


def _upload(at, key: str, filename: str, content: bytes) -> None:
    for fu in at.file_uploader:
        if fu.key == key:
            fu.upload(filename, content, "text/csv")
            return
    raise AssertionError(f"Missing uploader {key!r}")


def _selectbox(tab, key: str):
    for sb in tab.selectbox:
        if sb.key == key:
            return sb
    raise AssertionError(f"Missing selectbox {key!r}")


def _metrics(tab) -> dict[str, str]:
    return {m.label: str(m.value) for m in tab.metric}


def run_p0_ui_smoke() -> None:
    """All P0 UI checks in one Streamlit session."""
    guest_csv = (ROOT / "samples" / "guests_sample.csv").read_bytes()
    vendor_csv = (ROOT / "samples" / "vendors_sample.csv").read_bytes()
    legacy_csv = b"Name,Email\nTest User,test@example.com\n"

    at = _run_app()
    guests = at.tabs[0]
    vendors = at.tabs[1]

    # §A — guest upload + metrics
    _upload(at, "guest_upload", "guests_sample.csv", guest_csv)
    at.run()
    assert not at.exception, at.exception
    success = [s.value for s in at.success]
    assert any("Loaded 3 guests" in v for v in success), success
    guests = at.tabs[0]
    m = _metrics(guests)
    assert m.get("Total") == "3", m
    assert m.get("Pending") == "3", m
    assert "Generate guest messages (AI)" in [b.label for b in guests.button]

    # §C — message edit persists
    guests.text_area[0].set_value("Custom thank-you for Grace").run()
    at.run()
    guests = at.tabs[0]
    assert guests.text_area[0].value == "Custom thank-you for Grace"
    guests.text_area[1].set_value("Other guest").run()
    at.run()
    guests = at.tabs[0]
    assert guests.text_area[0].value == "Custom thank-you for Grace"

    # §C — filter + export link format (logic assertion)
    _selectbox(guests, "guest_filter").select("Pending").run()
    at.run()
    guests = at.tabs[0]
    assert _selectbox(guests, "guest_filter").value == "Pending"
    raw = pd.read_csv(ROOT / "samples" / "guests_sample.csv", dtype={"Name": str, "Phone": str})
    export_df = build_export_dataframe(
        raw.assign(Message=["Hi"] * 3, Status=["Pending"] * 3)
    )
    assert export_df["WhatsAppLink"].iloc[0].startswith("https://wa.me/234")

    # §C — status widgets accept values
    _selectbox(guests, "guest_status_0").select("Sent").run()
    at.run()
    guests = at.tabs[0]
    assert _selectbox(guests, "guest_status_0").value == "Sent"

    # §E — legacy CSV (new session state: re-upload overwrites guest list)
    _upload(at, "guest_upload", "legacy.csv", legacy_csv)
    at.run()
    assert any("Loaded 1 guests" in v for v in [s.value for s in at.success])
    guests = at.tabs[0]
    guests.button[1].click()
    at.run()
    guests = at.tabs[0]
    errors = [e.value for e in guests.error]
    assert any("SENDGRID" in e.upper() or "SENDER_EMAIL" in e.upper() for e in errors), errors

    # §F — vendors
    _upload(at, "vendor_upload", "vendors_sample.csv", vendor_csv)
    at.run()
    assert any("Loaded 2 vendors" in v for v in [s.value for s in at.success])
    vendors = at.tabs[1]
    assert _metrics(vendors).get("Total") == "2"
    vendors.button[0].click()
    at.run()
    assert any("Thank-you templates applied" in v for v in [s.value for s in at.success])
    vendors = at.tabs[1]
    vendors.button[1].click()
    at.run()
    assert any("Review-request templates applied" in v for v in [s.value for s in at.success])


class StreamlitP0SmokeTest(unittest.TestCase):
    def test_p0_ui_smoke_single_session(self):
        with patch.dict(os.environ, _ENV, clear=False):
            run_p0_ui_smoke()


if __name__ == "__main__":
    with patch.dict(os.environ, _ENV, clear=False):
        try:
            run_p0_ui_smoke()
            print("OK: Streamlit P0 UI smoke passed")
        except AssertionError as exc:
            print(f"FAILED: {exc}")
            raise SystemExit(1) from exc
