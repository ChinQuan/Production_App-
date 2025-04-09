# modules/form.py

import streamlit as st
import datetime
from modules.database import insert_order

def show_form():
    st.header("➕ Add New Production Order")

    with st.form("order_form", clear_on_submit=True):
        production_date = st.date_input("Production Date", value=datetime.date.today())
        company = st.text_input("Company")
        operator = st.text_input("Operator")
        
        seal_type = st.selectbox("Seal Type", [
            "STANDARD SOFT", "STANDARD HARD",
            "CUSTOM SOFT", "CUSTOM HARD",
            "SPECIAL", "V-RINGS", "STACK"
        ])

        seal_profile = ""
        if seal_type == "STACK":
            seal_profile = st.text_area("Stack Composition (e.g. 1xA + 2xB)", height=100)
        else:
            seal_profile = st.text_input("Seal Profile")

        seals = st.number_input("Seal Count", min_value=1, step=1)
        production_time = st.number_input("Production Time (in minutes)", min_value=1)
        downtime = st.number_input("Downtime (in minutes)", min_value=0)
        downtime_reason = st.text_area("Downtime Reason (if any)")

        submitted = st.form_submit_button("Submit")

    if submitted:
        if not company or not operator:
            st.error("Company and Operator fields are required.")
            st.stop()

        if seal_type == "STACK" and not seal_profile:
            st.error("Please specify the stack composition.")
            st.stop()

        if downtime > 0 and not downtime_reason:
            st.warning("You entered downtime minutes but no reason. Please consider adding a reason.")

        try:
            insert_order(
                production_date=str(production_date),
                company=company,
                operator=operator,
                seal_type=seal_type,
                seal_profile=seal_profile,
                seals=seals,
                production_time=production_time,
                downtime=downtime,
                reason=downtime_reason,
            )
            st.success(f"✅ Order for {operator} saved to the database!")
        except Exception as e:
            st.error(f"❌ Failed to save order:\n\n{e}")
