import streamlit as st
import pandas as pd

def show_reports(df):
    st.title("📊 Reports & Export")

    if df.empty:
        st.warning("No data to display. Add some orders to generate report.")
        return

    # Example of a simple report table
    st.subheader("Current Production Orders")
    st.dataframe(df)

    # Calculate and show the average daily production (Working days only)
    df['Date'] = pd.to_datetime(df['date'])
    df['Day'] = df['Date'].dt.date

    # Avg. Daily Production (Working Days Only)
    working_days = df.groupby('Day').sum()
    avg_daily_production = working_days['seal_count'].mean()
    
    st.markdown(f"### Avg. Daily Production (Working Days Only): {avg_daily_production:.2f} seals per day")

    # Avg. Daily Production (Order Dates Only)
    avg_daily_production_order = df['seal_count'].sum() / len(df['Day'].unique())
    st.markdown(f"### Avg. Daily Production (Order Dates Only): {avg_daily_production_order:.2f} seals per day")

    )
