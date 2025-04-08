import streamlit as st
import pandas as pd
import plotly.express as px
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
    st.header("⏳ Advanced Production Analysis")

    conn = get_connection()
    df = pd.read_sql("SELECT * FROM orders", conn)
    conn.close()

    if df.empty:
        st.write("No data available to calculate average production time.")
        return

    df['date'] = pd.to_datetime(df['date'])

    # 📅 Filter by Date Range
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

    # 📊 Produktywność operatorów
    with st.expander("📊 Productivity by Operator"):
        operator_df = filtered_df.groupby('operator')[['seal_count', 'production_time']].sum().reset_index()

        # 🔥 Sprawdzanie danych wejściowych
        st.write("### Dane dotyczące operatorów")
        st.dataframe(operator_df)

        # Obliczanie UPM na podstawie minut
        operator_df['UPM'] = operator_df['seal_count'] / operator_df['production_time']

        # Wizualizacja wykresu
        fig1 = px.bar(operator_df, x='operator', y='UPM', title='Operator Productivity (UPM)')
        st.plotly_chart(fig1)

    # 📅 Produkcja na przestrzeni czasu
    with st.expander("📈 Production Over Time"):
        time_df = filtered_df.groupby('date')['seal_count'].sum().reset_index()
        fig2 = px.line(time_df, x='date', y='seal_count', title='Production Over Time')
        st.plotly_chart(fig2)

    # 🏢 Produkcja per firma
    with st.expander("🏢 Production by Company"):
        company_df = filtered_df.groupby('company')['seal_count'].sum().reset_index()
        fig3 = px.pie(company_df, names='company', values='seal_count', title='Production by Company')
        st.plotly_chart(fig3)

    # 🔩 Produkcja per typ uszczelki
    with st.expander("🔩 Production by Seal Type"):
        seal_type_df = filtered_df.groupby('seal_type')['seal_count'].sum().reset_index()
        fig4 = px.bar(seal_type_df, x='seal_type', y='seal_count', title='Production by Seal Type')
        st.plotly_chart(fig4)

    # ⛔ Analiza przestojów
    with st.expander("⛔ Downtime Analysis"):
        downtime_df = filtered_df.groupby('downtime_reason')['downtime'].sum().reset_index()
        fig5 = px.bar(downtime_df, x='downtime_reason', y='downtime', title='Downtime Reasons')
        st.plotly_chart(fig5)

    st.success("📊 Analysis successfully completed")
