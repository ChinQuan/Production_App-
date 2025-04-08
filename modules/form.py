import streamlit as st
import pandas as pd
from datetime import datetime
from modules.database import get_connection

def show_form():
    st.title("➕ Add New Order")

    with st.form("order_form"):
        date = st.date_input("Date", value=datetime.today())
        company = st.text_input("Company")
        operator = st.text_input("Operator")
        seal_type = st.text_input("Seal Type")
        profile = st.text_input("Profile")
        seal_count = st.number_input("Number of Seals", min_value=1)
        production_time = st.number_input("Production Time (minutes)", min_value=0)
        downtime = st.number_input("Downtime (minutes)", min_value=0)
        downtime_reason = st.text_input("Downtime Reason", value="-")

        submitted = st.form_submit_button("Save Order")

        if submitted:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO orders (date, company, operator, seal_type, profile, seal_count, production_time, downtime, downtime_reason)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (date, company, operator, seal_type, profile, seal_count, production_time, downtime, downtime_reason))
                conn.commit()
                cursor.close()
                conn.close()
                st.success("✅ Order successfully saved.")
            except Exception as e:
                st.error(f"❌ Error saving order: {e}")

def show_home():
    st.title("📋 Order List")

    try:
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM orders ORDER BY date DESC", conn)
        conn.close()

        if df.empty:
            st.info("No orders in the database.")
        else:
            st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Error loading order data: {e}")
