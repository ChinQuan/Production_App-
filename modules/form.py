import streamlit as st
from modules.database import get_connection

def show_form():
    st.sidebar.subheader("📋 Add New Order")

    conn = get_connection()
    cursor = conn.cursor()

    date = st.sidebar.date_input("Date")
    company = st.sidebar.text_input("Company")
    operator = st.sidebar.text_input("Operator")
    seal_type = st.sidebar.text_input("Seal Type")
    profile = st.sidebar.text_input("Profile")
    seal_count = st.sidebar.number_input("Seal Count", min_value=1, step=1)
    production_time = st.sidebar.number_input("Production Time", min_value=0.0)
    downtime = st.sidebar.number_input("Downtime", min_value=0.0)
    downtime_reason = st.sidebar.text_input("Downtime Reason")
    
    if st.sidebar.button("Add Order"):
        cursor.execute(
            "INSERT INTO orders (date, company, operator, seal_type, profile, seal_count, production_time, downtime, downtime_reason) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (date, company, operator, seal_type, profile, seal_count, production_time, downtime, downtime_reason)
        )
        conn.commit()
        st.sidebar.success("Order added successfully.")
    
    cursor.close()
    conn.close()
