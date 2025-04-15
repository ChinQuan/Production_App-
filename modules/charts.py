import streamlit as st
import pandas as pd
import plotly.express as px

def show_charts(df):
    st.title("📈 Charts Overview")

    if df.empty:
        st.warning("No production data available.")
        return

    df["date"] = pd.to_datetime(df["date"])
    df["weekday"] = df["date"].dt.day_name()
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    df = df[df["weekday"].isin(weekdays)]

    # Daily production
    daily_prod = df.groupby("date")["seal_count"].sum().reset_index()
    fig1 = px.line(daily_prod, x="date", y="seal_count", title="📅 Daily Seal Production (Weekdays Only)",
                   markers=True, labels={"seal_count": "Seal Count", "date": "Date"})
    st.plotly_chart(fig1, use_container_width=True)

    # Total by company (case-insensitive)
    if "company" in df.columns:
        df['company_normalized'] = df['company'].str.lower()
        seal_by_company = df.groupby('company_normalized')["seal_count"].sum().reset_index()
        first_names = df.groupby('company_normalized')['company'].first().reset_index()
        seal_by_company = seal_by_company.merge(first_names, on='company_normalized')
        seal_by_company = seal_by_company.rename(columns={'company': 'company_display'})

        fig2 = px.bar(
            seal_by_company,
            x="company_display",
            y="seal_count",
            title="🏢 Total Seal Production by Company",
            labels={"seal_count": "Seal Count", "company_display": "Company"}
        )
        st.plotly_chart(fig2, use_container_width=True)
