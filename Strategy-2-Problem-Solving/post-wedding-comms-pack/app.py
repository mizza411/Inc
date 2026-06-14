"""Post-Wedding Comms Pack — Streamlit MVP (P0)."""

from __future__ import annotations

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from csv_schema import (
    CSV_DTYPE,
    STATUS_PENDING,
    STATUS_SENT,
    STATUS_SKIPPED,
    STATUSES,
    prepare_guest_df,
    prepare_vendor_df,
    validate_guest_csv,
    validate_vendor_csv,
)
from email_send import send_thank_you_email
from generation import generate_message
from prompts import build_guest_prompt, build_vendor_review_request, build_vendor_thank_you
from whatsapp_export import build_export_dataframe, export_copy_text

load_dotenv()

st.set_page_config(page_title="Post-Wedding Comms Pack", layout="wide")
st.title("Post-Wedding Comms Pack (MVP)")
st.caption("WhatsApp-first guest thank-yous and vendor wrap-up — review before sending.")

if "couple_names" not in st.session_state:
    st.session_state.couple_names = "We"
if "guest_df" not in st.session_state:
    st.session_state.guest_df = None
if "vendor_df" not in st.session_state:
    st.session_state.vendor_df = None

st.session_state.couple_names = st.sidebar.text_input(
    "Sign-off names (e.g. Ada & Emeka)",
    value=st.session_state.couple_names,
)


def _status_summary(df: pd.DataFrame) -> None:
    if df is None or df.empty:
        return
    counts = df["Status"].value_counts()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total", len(df))
    c2.metric("Pending", int(counts.get(STATUS_PENDING, 0)))
    c3.metric("Sent", int(counts.get(STATUS_SENT, 0)))
    c4.metric("Skipped", int(counts.get(STATUS_SKIPPED, 0)))


def _render_checklist(df: pd.DataFrame, key_prefix: str) -> pd.DataFrame:
    updated_rows = []
    filter_status = st.selectbox(
        "Filter by status",
        ["All"] + list(STATUSES),
        key=f"{key_prefix}_filter",
    )
    for i, row in df.iterrows():
        if filter_status != "All" and row.get("Status") != filter_status:
            continue
        with st.expander(f"{row.get('Name', 'Recipient')} — {row.get('Status', STATUS_PENDING)}"):
            new_status = st.selectbox(
                "Status",
                STATUSES,
                index=list(STATUSES).index(row.get("Status", STATUS_PENDING)),
                key=f"{key_prefix}_status_{i}",
            )
            message = st.text_area(
                "Message",
                value=str(row.get("Message", "") or ""),
                key=f"{key_prefix}_msg_{i}",
                height=120,
            )
            phone = row.get("Phone", "")
            if phone:
                st.caption(f"Phone: {phone}")
            email = row.get("Email", "")
            if email:
                st.caption(f"Email: {email}")
            updated = row.to_dict()
            updated["Status"] = new_status
            updated["Message"] = message
            updated_rows.append((i, updated))
    out = df.copy()
    for idx, data in updated_rows:
        for col, val in data.items():
            out.at[idx, col] = val
    return out


def _guest_tab() -> None:
    st.subheader("Guest gratitude")
    st.markdown(
        "Upload CSV with **Name**, **Phone** (+ optional **GiftOrSpray**, "
        "**Relationship**, **Email**, **EventAttended**). Legacy **Name + Email** still works."
    )
    uploaded = st.file_uploader("Guest list CSV", type=["csv"], key="guest_upload")
    if uploaded is not None:
        raw = pd.read_csv(uploaded, dtype=CSV_DTYPE)
        prepared, err = validate_guest_csv(raw)
        if err:
            st.error(err)
        else:
            st.session_state.guest_df = prepared
            st.success(f"Loaded {len(prepared)} guests.")

    df = st.session_state.guest_df
    if df is None or df.empty:
        st.info("Upload a guest CSV to begin.")
        return

    _status_summary(df)

    if st.button("Generate guest messages (AI)", key="gen_guest"):
        progress = st.progress(0.0)
        couple = st.session_state.couple_names
        errors: list[str] = []
        for n, (i, row) in enumerate(df.iterrows()):
            prompt = build_guest_prompt(row.to_dict(), couple_names=couple)
            msg, err = generate_message(prompt)
            if err:
                errors.append(f"{row.get('Name')}: {err}")
            else:
                df.at[i, "Message"] = msg
            progress.progress((n + 1) / len(df))
        st.session_state.guest_df = df
        progress.empty()
        if errors:
            st.warning("Some messages failed:\n" + "\n".join(errors[:5]))
        else:
            st.success("Guest messages generated. Review below before exporting.")

    df = _render_checklist(st.session_state.guest_df, "guest")
    st.session_state.guest_df = df

    export_df = build_export_dataframe(df)
    st.download_button(
        "Download export CSV (messages + WhatsApp links)",
        data=export_df.to_csv(index=False).encode("utf-8"),
        file_name="guest_comms_export.csv",
        mime="text/csv",
        key="guest_csv_dl",
    )
    st.download_button(
        "Download copy-paste text",
        data=export_copy_text(export_df).encode("utf-8"),
        file_name="guest_comms_whatsapp.txt",
        mime="text/plain",
        key="guest_txt_dl",
    )

    if st.button("Send email to guests with Email column (optional)", key="guest_email"):
        sent = 0
        failures: list[str] = []
        for _, row in df.iterrows():
            email = str(row.get("Email", "") or "").strip()
            if not email:
                continue
            ok, err = send_thank_you_email(
                email,
                "Thank You for Celebrating With Us!",
                str(row.get("Message", "") or ""),
            )
            if ok:
                sent += 1
            else:
                failures.append(f"{row.get('Name')}: {err}")
        if sent:
            st.success(f"Sent {sent} emails.")
        if failures:
            st.error("\n".join(failures[:5]))


def _vendor_tab() -> None:
    st.subheader("Vendor wrap-up")
    st.markdown(
        "Upload CSV with **Name**, **Phone**, **Role** "
        "(+ optional **Email**, **ReviewLink**, **Notes**)."
    )
    uploaded = st.file_uploader("Vendor list CSV", type=["csv"], key="vendor_upload")
    if uploaded is not None:
        raw = pd.read_csv(uploaded, dtype=CSV_DTYPE)
        prepared, err = validate_vendor_csv(raw)
        if err:
            st.error(err)
        else:
            st.session_state.vendor_df = prepared
            st.success(f"Loaded {len(prepared)} vendors.")

    df = st.session_state.vendor_df
    if df is None or df.empty:
        st.info("Upload a vendor CSV to begin.")
        return

    _status_summary(df)
    couple = st.session_state.couple_names
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Apply thank-you template to all", key="vendor_thanks"):
            for i, row in df.iterrows():
                df.at[i, "Message"] = build_vendor_thank_you(row.to_dict(), couple_names=couple)
            st.session_state.vendor_df = df
            st.success("Thank-you templates applied.")
    with col2:
        if st.button("Apply review-request template to all", key="vendor_review"):
            for i, row in df.iterrows():
                df.at[i, "Message"] = build_vendor_review_request(
                    row.to_dict(), couple_names=couple
                )
            st.session_state.vendor_df = df
            st.success("Review-request templates applied.")

    df = _render_checklist(st.session_state.vendor_df, "vendor")
    st.session_state.vendor_df = df

    export_df = build_export_dataframe(df)
    st.download_button(
        "Download vendor export CSV",
        data=export_df.to_csv(index=False).encode("utf-8"),
        file_name="vendor_comms_export.csv",
        mime="text/csv",
        key="vendor_csv_dl",
    )
    st.download_button(
        "Download vendor copy-paste text",
        data=export_copy_text(export_df).encode("utf-8"),
        file_name="vendor_comms_whatsapp.txt",
        mime="text/plain",
        key="vendor_txt_dl",
    )


guest_tab, vendor_tab = st.tabs(["Guests", "Vendors"])
with guest_tab:
    _guest_tab()
with vendor_tab:
    _vendor_tab()
