
import streamlit as st
import pandas as pd
import plotly.express as px

def show_charts(df):
    st.title("📈 Charts Overview")

    if df.empty:
        st.warning("No production data available.")
        return

    # Konwersja daty
    df["date"] = pd.to_datetime(df["date"])
    df["weekday"] = df["date"].dt.day_name()

    # Filtrowanie tylko na dni robocze (pon-pt)
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    df = df[df["weekday"].isin(weekdays)]

    # Wykres liniowy: dzienna produkcja
    daily_prod = df.groupby("date")["seal_count"].sum().reset_index()
    fig1 = px.line(daily_prod, x="date", y="seal_count", title="📅 Daily Seal Production (Weekdays Only)",
                   markers=True, labels={"seal_count": "Seal Count", "date": "Date"})
    st.plotly_chart(fig1, use_container_width=True)

    # Produkcja wg firmy i seal_type
    if "company" in df.columns and "seal_type" in df.columns:
        seal_by_company_type = df.groupby(["company", "seal_type"])["seal_count"].sum().reset_index()
        fig2 = px.bar(seal_by_company_type, x="company", y="seal_count", color="seal_type",
                      title="🏭 Seal Production by Company and Type", barmode="group")
        st.plotly_chart(fig2, use_container_width=True)

    # Produkcja wg operatora
    if "operator" in df.columns:
        seals_by_operator = df.groupby("operator")["seal_count"].sum().reset_index()
        fig3 = px.bar(seals_by_operator, x="operator", y="seal_count",
                      title="👷 Total Seal Production by Operator")
        st.plotly_chart(fig3, use_container_width=True)
