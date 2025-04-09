import streamlit as st
from datetime import date

def show_form():
    st.header("📝 Add Production Order")

    with st.form("order_form"):
        production_date = st.date_input("Production Date", value=date.today())
        company = st.text_input("Company Name")
        operator = st.text_input("Operator")

        seal_type = st.selectbox("Seal Type", [
            "STANDARD SOFT", "STANDARD HARD", "CUSTOM SOFT",
            "CUSTOM HARD", "SPECIAL", "V-RINGS", "STACK"
        ])

        if seal_type == "STACK":
            seal_profile = st.text_input("Stack Composition (e.g., 1x Type A + 2x Type B)", key="stack_profile")
        else:
            seal_profile = st.text_input("Enter Seal Profile (e.g., Profile A, Profile B)", key="standard_profile")

        seals = st.number_input("Number of Seals", min_value=0, step=1)
        production_time = st.number_input("Production Time (Minutes)", min_value=0.0, step=1.0)
        downtime = st.number_input("Downtime (Minutes)", min_value=0.0, step=1.0)
        downtime_reason = st.text_input("Reason for Downtime") if downtime > 0 else ""

        submitted = st.form_submit_button("💾 Save Entry")

        if submitted:
            if not company or not operator:
                st.error("Company and Operator fields are required.")
                st.stop()

            if seal_type == "STACK" and not seal_profile:
                st.error("Please specify the stack composition.")
                st.stop()

            if downtime > 0 and not downtime_reason:
                st.warning("You entered downtime minutes but no reason. Please consider adding a reason.")

            # Store entry in session_state (simulate saving)
            if "orders" not in st.session_state:
                st.session_state.orders = []

            st.session_state.orders.append({
                "date": str(production_date),
                "company": company,
                "operator": operator,
                "seal_type": seal_type,
                "seal_profile": seal_profile,
                "seals": seals,
                "time_min": production_time,
                "downtime": downtime,
                "reason": downtime_reason,
            })

            st.success(f"✅ Order for {operator} saved successfully!")
