import streamlit as st
import pandas as pd
import plotly.express as px

def show_dashboard(df):
    st.title("📊 Production Dashboard")

    if df.empty:
        st.warning("No data available.")
        return

    df["date"] = pd.to_datetime(df["date"])
    df["week"] = df["date"].dt.isocalendar().week
    df["year"] = df["date"].dt.year
    df["weekday"] = df["date"].dt.day_name()

    # ---------------------------
    # 🔍 Filters
    # ---------------------------
    with st.sidebar:
        st.header("📅 Filters")
        date_range = st.date_input("Select date range", [df["date"].min(), df["date"].max()])
        selected_operator = st.selectbox("Select operator", ["All"] + sorted(df["operator"].dropna().unique().tolist()))
        selected_company = st.selectbox("Select company", ["All"] + sorted(df["company"].dropna().unique().tolist()))

    filtered_df = df.copy()
    if len(date_range) == 2:
        filtered_df = filtered_df[(filtered_df["date"] >= pd.to_datetime(date_range[0])) & (filtered_df["date"] <= pd.to_datetime(date_range[1]))]
    if selected_operator != "All":
        filtered_df = filtered_df[filtered_df["operator"] == selected_operator]
    if selected_company != "All":
        filtered_df = filtered_df[filtered_df["company"] == selected_company]

    # ---------------------------
    # 🧮 KPIs
    # ---------------------------
    today = pd.Timestamp.today().normalize()
    this_week = today.isocalendar().week

    orders_today = filtered_df[filtered_df["date"] == today]
    seals_today = orders_today["seal_count"].sum()
    avg_time_today = (orders_today["production_time"] / orders_today["seal_count"]).mean()

    orders_this_week = filtered_df[filtered_df["week"] == this_week]
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

    # ---------------------------
    # 📈 Weekly Production Trend
    # ---------------------------
    weekly_trend = filtered_df.groupby(["year", "week"])["seal_count"].sum().reset_index()
    weekly_trend["label"] = weekly_trend["year"].astype(str) + "-W" + weekly_trend["week"].astype(str)
    fig_weekly = px.line(weekly_trend, x="label", y="seal_count", title="📈 Weekly Seal Production Trend", markers=True)
    st.plotly_chart(fig_weekly, use_container_width=True)

    # ---------------------------
    # 💡 Insights & Alerts
    # ---------------------------
    st.subheader("⚠️ Alerts")
    overall_avg = (filtered_df["production_time"] / filtered_df["seal_count"]).mean()
    if pd.notnull(avg_time_today) and avg_time_today > overall_avg * 1.3:
        st.error("⚠️ Production time today is significantly higher than average!")

    # ---------------------------
    # 📊 Best Day of the Week
    # ---------------------------
    st.subheader("📅 Best Production Day")
    weekday_prod = filtered_df.groupby("weekday")["seal_count"].sum().reindex([
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ])
    best_day = weekday_prod.idxmax()
    st.info(f"📌 Best day for production: **{best_day}**")

    fig_weekday = px.bar(weekday_prod.reset_index(), x="weekday", y="seal_count",
                         title="📊 Total Production by Weekday", labels={"seal_count": "Seal Count"})
    st.plotly_chart(fig_weekday, use_container_width=True)

    # ---------------------------
    # 🏆 Top Operator This Week
    # ---------------------------
    st.subheader("🏆 Top Operator This Week")
    top_op = orders_this_week.groupby("operator")["seal_count"].sum().sort_values(ascending=False)
    if not top_op.empty:
        st.success(f"🥇 Top operator: **{top_op.idxmax()}** with **{top_op.max()}** seals")

    fig_top_op = px.bar(top_op.reset_index(), x="operator", y="seal_count",
                        title="🏗️ Operator Performance This Week", labels={"seal_count": "Seal Count"})
    st.plotly_chart(fig_top_op, use_container_width=True)

    # ---------------------------
    # 📝 Notes
    # ---------------------------
    st.subheader("📝 Notes")
    user_notes = st.text_area("Add your notes for today:", "")
    if user_notes:
        st.write("✅ Note saved (not persistent):")
        st.info(user_notes)

