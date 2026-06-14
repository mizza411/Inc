"""Non-Streamlit smoke test for guest + vendor CSV flow (P0)."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from csv_schema import validate_guest_csv, validate_vendor_csv
from prompts import build_guest_prompt, build_vendor_review_request, build_vendor_thank_you
from whatsapp_export import build_export_dataframe, export_copy_text, normalize_ng_phone


def main() -> int:
    errors: list[str] = []
    samples = ROOT / "samples"

    # Guest flow
    guest_path = samples / "guests_sample.csv"
    if not guest_path.exists():
        errors.append(f"Missing {guest_path}")
    else:
        gdf, gerr = validate_guest_csv(pd.read_csv(guest_path, dtype={"Name": str, "Phone": str}))
        if gerr or gdf is None:
            errors.append(f"Guest validation: {gerr}")
        else:
            if len(gdf) != 3:
                errors.append(f"Expected 3 guests, got {len(gdf)}")
            phone = normalize_ng_phone("08031234567")
            if phone != "2348031234567":
                errors.append(f"Phone normalize failed: {phone}")
            prompt = build_guest_prompt(gdf.iloc[0].to_dict(), couple_names="Ada & Emeka")
            if "Grace" not in prompt or "50000" not in prompt:
                errors.append("Guest prompt missing expected fields")
            gexport = build_export_dataframe(gdf.assign(Message=["Hi Grace", "Hi Tunde", "Hi Amaka"]))
            if "WhatsAppLink" not in gexport.columns or not gexport["WhatsAppLink"].iloc[0].startswith("https://wa.me/234"):
                errors.append(f"Guest WhatsApp export links invalid: {gexport['WhatsAppLink'].iloc[0]}")
            txt = export_copy_text(gexport)
            if "Auntie Grace" not in txt:
                errors.append("Guest copy-paste export missing name")

    # Legacy Name + Email CSV
    legacy = pd.DataFrame({"Name": ["Diaspora Ben"], "Email": ["ben@example.com"]})
    leg_df, leg_err = validate_guest_csv(legacy)
    if leg_err or leg_df is None or "Phone" not in leg_df.columns:
        errors.append(f"Legacy CSV failed: {leg_err}")

    # Vendor flow
    vendor_path = samples / "vendors_sample.csv"
    if not vendor_path.exists():
        errors.append(f"Missing {vendor_path}")
    else:
        vdf, verr = validate_vendor_csv(pd.read_csv(vendor_path, dtype={"Name": str, "Phone": str, "Role": str}))
        if verr or vdf is None:
            errors.append(f"Vendor validation: {verr}")
        else:
            if len(vdf) != 2:
                errors.append(f"Expected 2 vendors, got {len(vdf)}")
            row = vdf.iloc[0].to_dict()
            thanks = build_vendor_thank_you(row, couple_names="Ada & Emeka")
            review = build_vendor_review_request(row, couple_names="Ada & Emeka")
            if "Photographer" not in thanks or "review" not in review.lower():
                errors.append("Vendor templates missing expected content")
            vexport = build_export_dataframe(
                vdf.assign(Message=[thanks, build_vendor_thank_you(vdf.iloc[1].to_dict(), "Ada & Emeka")])
            )
            if vexport.empty or not vexport["WhatsAppLink"].iloc[0]:
                errors.append("Vendor export failed")

    if errors:
        print("FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("OK: guest + vendor CSV flow passed")
    print(f"  Guests: {len(gdf)} rows, export columns: {list(gexport.columns)}")
    print(f"  Vendors: {len(vdf)} rows, sample link: {gexport['WhatsAppLink'].iloc[0][:40]}...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
