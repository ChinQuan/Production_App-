import streamlit as st
import datetime

def show_form():
    st.title("🧾 Add Production Order")

    if "orders" not in st.session_state:
        st.session_state.orders = []

    with st.form("order_form"):
        production_date = st.date_input("Production Date", datetime.date.today())
        company = st.text_input("Company Name")
        operator = st.text_input("Operator")

        seal_type = st.selectbox("Seal Type", [
            "STANDARD SOFT",
            "STANDARD HARD",
            "CUSTOM SOFT",
            "CUSTOM HARD",
            "SPECIAL",
            "V-RINGS",
            "STACK"
        ])

        # Show extra input if STACK is selected
        stack_components = ""
        if seal_type == "STACK":
            stack_components = st.text_input("Enter Stack Components (e.g., 1x Type A + 2x Type B)")

        seal_profile = st.text_input("Enter Seal Profile (e.g., Profile A, Profile B)")
        seals = st.number_input("Number of Seals", min_value=0, step=1)
        production_time = st.number_input("Production Time (Minutes)", min_value=0.0, step=1.0)
        downtime = st.number_input("Downtime (Minutes)", min_value=0.0, step=1.0)
        downtime_reason = st.text_input("Reason for Downtime") if downtime > 0 else ""

        submitted = st.form_submit_button("Save Entry")

        if submitted:
            st.session_state.orders.append({
                "date": str(production_date),
                "company": company,
                "operator": operator,
                "seal_type": seal_type,
                "seal_profile": seal_profile,
                "stack_info": stack_components,
                "seals": seals,
                "production_time": production_time,
                "downtime": downtime,
                "downtime_reason": downtime_reason
            })
            st.success(f"Order for {operator} saved successfully!")
