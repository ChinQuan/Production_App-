import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def format_time(seconds):
    if seconds < 60:
        return f"{int(seconds)} seconds"
    else:
        minutes = int(seconds // 60)
        remaining_seconds = int(seconds % 60)
        return f"{minutes} minute{'s' if minutes > 1 else ''} {remaining_seconds} seconds"

def calculate_average_time(df):
    st.header("⏳ Average Production Time Analysis")

    if df.empty:
        st.write("No data available to calculate average production time.")
        return

    # Sprawdzamy, czy kolumna 'date' istnieje w danych
    if 'date' not in df.columns:
        st.write("Date column not found in data.")
        return

    # Upewniamy się, że kolumna 'date' jest w formacie datetime
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Sprawdzamy, czy kolumna 'seal_type' istnieje w danych
    if 'seal_type' not in df.columns:
        st.write("Seal Type column not found in data.")
        return

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

    # Przypisujemy odpowiednie kolumny
    seal_types = filtered_df['seal_type'].unique()
    average_times = {}

    for seal_type in seal_types:
        filtered_type_df = filtered_df[filtered_df['seal_type'] == seal_type]
        total_time = filtered_type_df['production_time'].sum()  # Używamy production_time
        total_seals = filtered_type_df['seal_count'].sum()  # Używamy seal_count

        if total_seals > 0:
            avg_time = (total_time / total_seals) * 60
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

    companies = filtered_df['company'].unique()
    company_times = {}

    for company in companies:
        filtered_company_df = filtered_df[filtered_df['company'] == company]
        total_time = filtered_company_df['production_time'].sum()
        total_seals = filtered_company_df['seal_count'].sum()

        if total_seals > 0:
            avg_time = (total_time / total_seals) * 60
            seals_per_minute = 60 / avg_time if avg_time > 0 else 0
            company_times[company] = (format_time(avg_time), seals_per_minute)
        else:
            company_times[company] = (None, None)

    st.subheader("📊 By Company")
    company_df = pd.DataFrame(
        [(company, avg[0], avg[1]) for company, avg in company_times.items()],
        columns=['Company', 'Average Time per Seal', 'Seals Produced per Minute (UPM)']
    )
    st.table(company_df)

    operators = filtered_df['operator'].unique()
    operator_times = {}

    for operator in operators:
        filtered_operator_df = filtered_df[filtered_df['operator'] == operator]
        total_time = filtered_operator_df['production_time'].sum()
        total_seals = filtered_operator_df['seal_count'].sum()

        if total_seals > 0:
            avg_time = (total_time / total_seals) * 60
            seals_per_minute = 60 / avg_time if avg_time > 0 else 0
            operator_times[operator] = (format_time(avg_time), seals_per_minute)
        else:
            operator_times[operator] = (None, None)

    st.subheader("📊 By Operator")
    operator_df = pd.DataFrame(
        [(operator, avg[0], avg[1]) for operator, avg in operator_times.items()],
        columns=['Operator', 'Average Time per Seal', 'Seals Produced per Minute (UPM)']
    )
    st.table(operator_df)
