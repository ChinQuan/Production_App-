import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def format_time(seconds):
    if seconds < 60:
        return f"{int(seconds)} seconds"
    else:
        minutes = int(seconds // 60)
        remaining_seconds = int(seconds % 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} {remaining_seconds} seconds"

def calculate_average_time(df):
    # Convert production_time from minutes to seconds
    df['production_time'] = df['production_time'] * 60
    st.header("⏳ Average Production Time Analysis")

    if df.empty:
        st.write("No data available to calculate average production time.")
        return

    if 'date' not in df.columns:
        st.write("Date column not found in data.")
        return

    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    st.sidebar.header("🗓 Filter by Date Range")
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

    st.markdown("""<style>
    table td, table th {
        text-align: center !important;
    }
    </style>""", unsafe_allow_html=True)

    # By Seal Type
    seal_types = filtered_df['seal_type'].unique()
    average_times = {}

    for seal_type in seal_types:
        filtered_type_df = filtered_df[filtered_df['seal_type'] == seal_type]
        total_time = filtered_type_df['production_time'].sum()
        total_seals = filtered_type_df['seal_count'].sum()

        if total_seals > 0:
            avg_time = total_time / total_seals
            seals_per_minute = 60 / avg_time if avg_time > 0 else 0
            average_times[seal_type] = (format_time(avg_time), seals_per_minute)
        else:
            average_times[seal_type] = (None, None)

    st.subheader("📊 By Seal Type")
    result_df = pd.DataFrame(
        [(seal_type, avg[0], avg[1]) for seal_type, avg in average_times.items()],
        columns=['Seal Type', 'Average Time per Seal', 'Seals Produced per Minute (UPM)']
    )
    st.table(result_df)

    # By Company (case-insensitive grouping)
    filtered_df['company_normalized'] = filtered_df['company'].str.lower()
    grouped_companies = filtered_df.groupby('company_normalized')

    company_times = {}
    for company_norm, group in grouped_companies:
        total_time = group['production_time'].sum()
        total_seals = group['seal_count'].sum()
        if total_seals > 0:
            avg_time = total_time / total_seals
            seals_per_minute = (total_seals / total_time) * 60 if total_time else 0
            display_name = group['company'].iloc[0]
            company_times[display_name] = (format_time(avg_time), seals_per_minute)
        else:
            display_name = group['company'].iloc[0]
            company_times[display_name] = (None, None)

    st.subheader("📊 By Company")
    company_df = pd.DataFrame(
        [(company, avg[0], avg[1]) for company, avg in company_times.items()],
        columns=['Company', 'Average Time per Seal', 'Seals Produced per Minute (UPM)']
    )
    st.table(company_df)

    # By Operator (case-insensitive grouping)
    filtered_df['operator_normalized'] = filtered_df['operator'].str.lower()
    grouped = filtered_df.groupby('operator_normalized')

    operator_times = {}
    for operator_norm, group in grouped:
        total_time = group['production_time'].sum()
        total_seals = group['seal_count'].sum()
        if total_seals > 0:
            avg_time = total_time / total_seals
            seals_per_minute = (total_seals / total_time) * 60 if total_time else 0
            display_name = group['operator'].iloc[0]
            operator_times[display_name] = (format_time(avg_time), seals_per_minute)
        else:
            display_name = group['operator'].iloc[0]
            operator_times[display_name] = (None, None)

    st.subheader("📊 By Operator")
    operator_df = pd.DataFrame(
        [(operator, avg[0], avg[1]) for operator, avg in operator_times.items()],
        columns=['Operator', 'Average Time per Seal', 'Seals Produced per Minute (UPM)']
    )
    st.table(operator_df)


