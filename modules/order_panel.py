import streamlit as st
import pandas as pd
from datetime import datetime
from modules.database import insert_order, get_orders_df

def show_order_panel():
    st.title("📥 Order Panel")

    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.subheader("➕ Add New Completed Order")
        with st.form("order_panel_form"):
            form_col1, form_col2 = st.columns(2)

            with form_col1:
                date = st.date_input("📅 Production Date", value=datetime.today())
                company = st.text_input("🏢 Company Name")
                seal_type = st.selectbox("🧷 Seal Type", ["Standard Hard", "Standard Soft", "Custom"])
                seal_count = st.number_input("🔢 Number of Seals", min_value=0, step=1)

            with form_col2:
                operator = st.text_input("👷 Operator")
                profile = st.text_input("📄 Enter Seal Profile (optional)")
                production_time = st.number_input("⏱️ Production Time (Minutes)", min_value=0.0, step=1.0)

            submitted = st.form_submit_button("✅ Submit Order")
            if submitted:
                new_order = {
                    "date": date,
                    "company": company,
                    "operator": operator,
                    "seal_type": seal_type,
                    "profile": profile,
                    "seal_count": seal_count,
                    "production_time": production_time
                }
                try:
                    insert_order(new_order)
                    st.success("✅ Order added successfully!")
                except Exception as e:
                    st.error(f"❌ Failed to add order:\\n{e}")

    with col2:
        st.subheader("📋 Current Production Orders")
        df = get_orders_df()
        st.dataframe(df)

