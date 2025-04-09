import streamlit as st
import pandas as pd

def show_reports(df):
    st.title("📊 Reports & Export")

    # Sprawdzamy, czy DataFrame jest pusty
    if df.empty:
        st.warning("No data to display. Add some orders to generate report.")
        return

    # Wyświetlamy tabelę z wszystkimi zamówieniami
    st.subheader("Current Production Orders")
    st.dataframe(df)

    # Upewniamy się, że kolumna 'date' jest w formacie datetime
    df['Date'] = pd.to_datetime(df['date'], errors='coerce')
    df['Day'] = df['Date'].dt.date

    # Średnia produkcja dzienna (Tylko dni robocze)
    working_days = df.groupby('Day')['seal_count'].sum()  # Sumujemy tylko 'seal_count'
    avg_daily_production = working_days.mean()

    st.markdown(f"### Avg. Daily Production (Working Days Only): {avg_daily_production:.2f} seals per day")

    # Średnia produkcja dzienna (Tylko dni z zamówieniami)
    avg_daily_production_order = df['seal_count'].sum() / len(df['Day'].unique())
    st.markdown(f"### Avg. Daily Production (Order Dates Only): {avg_daily_production_order:.2f} seals per day")
