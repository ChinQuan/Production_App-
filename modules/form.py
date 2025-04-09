import streamlit as st
from datetime import date

def show_form():
    st.header("📋 Add Production Order")

    # Initialize session state if needed
    if "orders" not in st.session_state:
        st.session_state.orders = []

    with st.form("order_form", clear_on_submit=True):
        production_date = st.date_input("Production Date", value=date.today())
        company = st.text_input("Company Name")
        operator = st.text_input("Operator")

        seal_type = st.selectbox("Seal Type", ["Standard Soft", "Standard Hard", "Custom"])
        seal_profile = st.text_input("Enter Seal Profile (e.g., Profile A, Profile B)")

        seals = st.number_input("Number of Seals", min_value=0, step=1)
        production_time = st.number_input("Production Time (Minutes)", min_value=0.0, step=1.0)
        downtime = st.number_input("Downtime (Minutes)", min_value=0.0, step=1.0)
        downtime_reason = st.text_input("Reason for Downtime", placeholder="Enter reason for downtime (if any)")

        submitted = st.form_submit_button("💾 Save Entry")

        if submitted:
            # Validation: if downtime > 0, reason must be provided
            if downtime > 0 and not downtime_reason.strip():
                st.warning("Please provide a reason for the downtime.")
                st.stop()

            # Add to session state
            st.session_state.orders.append({
                "date": str(production_date),
                "company": company,
                "operator": operator,
                "seal_type": seal_type,
                "seal_profile": seal_profile,
                "seals": seals,
                "production_time": production_time,
                "downtime": downtime,
                "downtime_reason": downtime_reason,
            })

            st.success(f"✅ Order for **{company or operator}** added successfully!")
