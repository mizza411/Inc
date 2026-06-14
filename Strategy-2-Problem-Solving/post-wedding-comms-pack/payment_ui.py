"""Streamlit sidebar — Paystack unlock flow."""

from __future__ import annotations

import streamlit as st

from paystack_client import default_amount_kobo, initialize_transaction, payments_configured
from unlock import is_unlocked, payments_required, try_unlock_with_reference


def _amount_ngn_display() -> str:
    kobo = default_amount_kobo()
    return f"₦{kobo // 100:,}"


def handle_query_reference(session: dict) -> None:
    ref = st.query_params.get("reference") or st.query_params.get("trxref")
    if not ref or not payments_required():
        return
    if session.get("_verified_query_ref") == ref:
        return
    ok, err = try_unlock_with_reference(ref)
    if ok:
        session["unlocked"] = True
        session["unlocked_reference"] = ref
        session["payment_reference"] = ref
        session["_verified_query_ref"] = ref
        st.sidebar.success("Payment verified — unlocked for this session.")
    elif err:
        st.sidebar.error(err)


def render_payment_sidebar(session: dict) -> bool:
    st.sidebar.subheader("Unlock")
    if not payments_required():
        st.sidebar.info("Payments disabled (dev mode). All features unlocked.")
        return True

    handle_query_reference(session)

    if is_unlocked(session):
        ref = session.get("unlocked_reference", "")
        st.sidebar.success(f"Unlocked {ref}".strip())
        return True

    st.sidebar.caption(f"One-time unlock per wedding — {_amount_ngn_display()}")
    email = st.sidebar.text_input("Your email", key="paystack_email")
    if st.sidebar.button("Get Paystack payment link", key="pay_init"):
        if not email.strip():
            st.sidebar.error("Enter your email first.")
        else:
            init, err = initialize_transaction(email.strip())
            if err:
                st.sidebar.error(err)
            else:
                session["pending_reference"] = init["reference"]
                st.sidebar.link_button(
                    "Pay with Paystack →",
                    init["authorization_url"],
                    type="primary",
                )
                st.sidebar.caption(f"Reference: `{init['reference']}`")

    ref_in = st.sidebar.text_input(
        "Already paid? Paste reference",
        value=session.get("pending_reference", ""),
        key="paystack_ref_input",
    )
    if st.sidebar.button("Verify payment", key="pay_verify"):
        ok, err = try_unlock_with_reference(ref_in)
        if ok:
            session["unlocked"] = True
            session["unlocked_reference"] = ref_in.strip()
            session["payment_reference"] = ref_in.strip()
            st.sidebar.success("Verified — you can use all features.")
            st.rerun()
        else:
            st.sidebar.error(err or "Verification failed.")

    return False


def require_unlock(session: dict) -> bool:
    if is_unlocked(session):
        return True
    st.warning(f"Unlock required ({_amount_ngn_display()} one-time) — use the sidebar to pay or verify.")
    return False
