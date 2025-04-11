
import streamlit as st
import pandas as pd
import plotly.express as px

def show_charts(df):
    st.title("📈 Charts Overview")

    if df.empty:
        st.warning("No production data available.")
        return

    # Konwersja daty i filtrowanie tylko na dni robocze
    df["date"] = pd.to_datetime(df["date"])
    df["weekday"] = df["date"].dt.day_name()
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    df = df[df["weekday"].isin(weekdays)]

    # Wykres 1: Produkcja dzienna
    daily_prod = df.groupby("date")["seal_count"].sum().reset_index()
    fig1 = px.line(daily_prod, x="date", y="seal_count", title="📅 Daily Seal Production (Weekdays Only)",
                   markers=True, labels={"seal_count": "Seal Count", "date": "Date"})
    st.plotly_chart(fig1, use_container_width=True)

    # Wykres 2: Produkcja wg firmy (łącznie)
    if "company" in df.columns:
        seal_by_company = df.groupby("company")["seal_count"].sum().reset_index()
        fig2 = px.bar(seal_by_company, x="company", y="seal_count",
                      title="🏢 Total Seal Production by Company", text_auto=True)
        st.plotly_chart(fig2, use_container_width=True)

    # Wykres 3: Produkcja wg typu uszczelek (łącznie)
    if "seal_type" in df.columns:
        seal_by_type = df.groupby("seal_type")["seal_count"].sum().reset_index()
        fig3 = px.bar(seal_by_type, x="seal_type", y="seal_count",
                      title="🧷 Total Seal Production by Type", text_auto=True, color="seal_type")
        st.plotly_chart(fig3, use_container_width=True)

    # Wykres 4: Produkcja wg operatora
    if "operator" in df.columns:
        seals_by_operator = df.groupby("operator")["seal_count"].sum().reset_index()
        fig4 = px.bar(seals_by_operator, x="operator", y="seal_count",
                      title="👷 Total Seal Production by Operator", text_auto=True)
        st.plotly_chart(fig4, use_container_width=True)
