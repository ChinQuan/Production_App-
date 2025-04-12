
import streamlit as st
import pandas as pd
import plotly.express as px

def show_dashboard(df):
    st.title("📊 Production Dashboard")

    if df.empty:
        st.warning("No data available.")
        return

    df["date"] = pd.to_datetime(df["date"])
    today = pd.Timestamp.today().normalize()
    this_week = today.isocalendar().week
    df["week"] = df["date"].dt.isocalendar().week
    df["year"] = df["date"].dt.year

    # 🧮 KPI
    orders_today = df[df["date"] == today]
    seals_today = orders_today["seal_count"].sum()
    avg_time_today = (orders_today["production_time"] / orders_today["seal_count"]).mean()

    orders_this_week = df[df["week"] == this_week]
    seals_this_week = orders_this_week["seal_count"].sum()
    avg_time_week = (orders_this_week["production_time"] / orders_this_week["seal_count"]).mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Orders Today", len(orders_today))
    col2.metric("🔧 Seals Today", int(seals_today))
    col3.metric("⏱️ Avg. Time/Seal Today", f"{avg_time_today:.1f} min" if pd.notnull(avg_time_today) else "N/A")

    col4, col5, col6 = st.columns(3)
    col4.metric("🗓️ Orders This Week", len(orders_this_week))
    col5.metric("🧩 Seals This Week", int(seals_this_week))
    col6.metric("⏳ Avg. Time/Seal This Week", f"{avg_time_week:.1f} min" if pd.notnull(avg_time_week) else "N/A")

    # 📈 Trend tygodniowy
    weekly_trend = df.groupby(["year", "week"])["seal_count"].sum().reset_index()
    weekly_trend["label"] = weekly_trend["year"].astype(str) + "-W" + weekly_trend["week"].astype(str)
    fig = px.bar(weekly_trend, x="label", y="seal_count", title="📈 Weekly Seal Production Trend")
    st.plotly_chart(fig, use_container_width=True)

    # 🏆 Top firma / operator
    st.subheader("🏆 Top Performers")

    col7, col8 = st.columns(2)

    if "company" in df.columns:
        top_company = df.groupby("company")["seal_count"].sum().reset_index().sort_values(by="seal_count", ascending=False).head(1)
        if not top_company.empty:
            col7.success(f"🏭 Top Company: {top_company.iloc[0]['company']} ({int(top_company.iloc[0]['seal_count'])} seals)")

    if "operator" in df.columns:
        top_operator = df.groupby("operator")["seal_count"].sum().reset_index().sort_values(by="seal_count", ascending=False).head(1)
        if not top_operator.empty:
            col8.info(f"👷 Top Operator: {top_operator.iloc[0]['operator']} ({int(top_operator.iloc[0]['seal_count'])} seals)")

    # 🧹 Braki
    st.subheader("⚠️ Missing Data Alerts")
    missing = []
    if df["seal_type"].isnull().any():
        missing.append("Seal Type")
    if df["production_time"].isnull().any():
        missing.append("Production Time")
    if missing:
        st.error("Missing values in: " + ", ".join(missing))
    else:
        st.success("✅ No missing critical fields!")


    # 📈 Avg. Daily Production (Mon–Fri)
    working_days_df = df[df["date"].dt.weekday < 5]
    daily_totals = working_days_df.groupby("date")["seal_count"].sum()
    avg_daily_production = daily_totals.mean()
    st.metric("📊 Avg. Daily Seal Production (Weekdays)", f"{avg_daily_production:.1f} seals")

