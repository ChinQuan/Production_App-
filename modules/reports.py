import streamlit as st
import pandas as pd
from modules.database import get_connection

def show_reports():
    st.title("📊 Reports")

    conn = get_connection()
    df = pd.read_sql("SELECT * FROM orders", conn)
    conn.close()

    if df.empty:
        st.warning("No data available to generate reports.")
        return

    df['date'] = pd.to_datetime(df['date'])

    st.subheader("Filtered Data")
    start_date = st.date_input("Start Date", value=pd.to_datetime("2022-01-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime("today"))

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    st.write(filtered_df)

    st.subheader("📈 Production Statistics")
    total_seals = filtered_df['seal_count'].sum()
    total_orders = len(filtered_df)
    avg_production_time = filtered_df['production_time'].mean()

    st.metric("Total Seals Produced", total_seals)
    st.metric("Total Orders", total_orders)
    st.metric("Average Production Time", f"{avg_production_time:.2f} hours" if avg_production_time else "N/A")
