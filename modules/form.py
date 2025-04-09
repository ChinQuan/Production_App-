import streamlit as st
import pandas as pd
from modules.database import insert_order
from datetime import datetime

def show_form():
    st.title("➕ Add New Order")

    tab1, tab2 = st.tabs(["📋 Form", "📈 Preview"])

    with tab1:
        left, right = st.columns([2, 3])

        with left:
            with st.form("order_form"):
                date = st.date_input("Date", value=datetime.today())
                company = st.text_input("Company")
                operator = st.text_input("Operator")
                seal_type = st.selectbox("Seal Type", ["Standard Hard", "Standard Soft", "Custom"])
                seal_count = st.number_input("Seal Count", min_value=0, step=1)
                production_time = st.number_input("Production Time (minutes)", min_value=0, step=1)

                submitted = st.form_submit_button("Add Order")
                if submitted:
                    new_order = {
                        "date": date,
                        "company": company,
                        "operator": operator,
                        "seal_type": seal_type,
                        "seal_count": seal_count,
                        "production_time": production_time
                    }
                    try:
                        insert_order(new_order)
                        st.success("✅ Order added successfully!")
                    except Exception as e:
                        st.error(f"❌ Failed to add order:\n{e}")

        with right:
            st.info("You can use this panel later for charts, order preview or validations.")

    with tab2:
        st.write("📄 You can preview existing orders here (future feature).")
