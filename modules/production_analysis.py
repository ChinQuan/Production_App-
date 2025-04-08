import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from modules.database import get_connection

def format_time(seconds):
    if seconds < 60:
        return f"{int(seconds)} seconds"
    else:
        minutes = int(seconds // 60)
        remaining_seconds = int(seconds % 60)
        return f"{minutes} minute{'s' if minutes > 1 else ''} {remaining_seconds} seconds"

def calculate_average_time():
    st.header("⏳ Average Production Time Analysis")

    conn = get_connection()
    df = pd.read_sql("SELECT * FROM orders", conn)
    conn.close()

    if df.empty:
        st.write("No data available to calculate average production time.")
        return

    df['date'] = pd.to_datetime(df['date'])

    # 📅 Opcje wyboru przedziału czasowego
    st.sidebar.header("📅 Filter by Date Range")
    date_filter = st.sidebar.selectbox(
        "Select Date Range",
        ["Last Week", "Last Month", "Last Year", "Custom Range"]
    )

    if date_filter == "Last Week":
        start_date = datetime.now() - timedelta(weeks=1)
        end_date = datetime.now()
    elif date_filter == "Last Month":
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
    elif date_filter == "Last Year":
        start_date = datetime.now() - timedelta(days=365)
        end_date = datetime.now()
    else:
        start_date = st.sidebar.date_input("Start Date", value=datetime.now() - timedelta(days=30))
        end_date = st.sidebar.date_input("End Date", value=datetime.now())

    filtered_df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]

    if filtered_df.empty:
        st.write("No data available for the selected date range.")
        return

    st.write(f"Showing data from **{start_date.date()}** to **{end_date.date()}**")

    seal_types = filtered_df['seal_type'].unique()
    results = []

    for seal_type in seal_types:
        type_df = filtered_df[filtered_df['seal_type'] == seal_type]
        total_time = type_df['production_time'].sum()
        total_seals = type_df['seal_count'].sum()
        if total_seals > 0:
            avg_time = (total_time / total_seals) * 60
            results.append([seal_type, format_time(avg_time), 60 / avg_time if avg_time > 0 else 0])

    result_df = pd.DataFrame(results, columns=["Seal Type", "Average Time per Seal", "Seals Produced per Minute"])
    st.table(result_df)
