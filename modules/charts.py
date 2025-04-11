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

    # Total by company
    if "company" in df.columns:
        seal_by_company = df.groupby("company")["seal_count"].sum().reset_index()
        fig2 = px.bar(seal_by_company, x="company", y="seal_count",
                      title="🏢 Total Seal Production by Company", text_auto=True)
        st.plotly_chart(fig2, use_container_width=True)

    # Total by seal type
    if "seal_type" in df.columns:
        seal_by_type = df.groupby("seal_type")["seal_count"].sum().reset_index()
        fig3 = px.bar(seal_by_type, x="seal_type", y="seal_count",
                      title="🧷 Total Seal Production by Type", text_auto=True, color="seal_type")
        st.plotly_chart(fig3, use_container_width=True)

        # Top 5 most produced types
        top5_types = seal_by_type.sort_values("seal_count", ascending=False).head(5)
        fig_top5 = px.bar(top5_types, x="seal_type", y="seal_count",
                          title="🏆 Top 5 Most Produced Seal Types", text_auto=True, color="seal_type")
        st.plotly_chart(fig_top5, use_container_width=True)

    # Production by operator
    if "operator" in df.columns:
        seals_by_operator = df.groupby("operator")["seal_count"].sum().reset_index()
        fig4 = px.bar(seals_by_operator, x="operator", y="seal_count",
                      title="👷 Total Seal Production by Operator", text_auto=True)
        st.plotly_chart(fig4, use_container_width=True)

        # Average production time per operator
        df["avg_time_per_seal"] = df["production_time"] / df["seal_count"]
        avg_time = df.groupby("operator")["avg_time_per_seal"].mean().reset_index()
        fig_avg = px.bar(avg_time, x="operator", y="avg_time_per_seal",
                         title="⏱️ Avg. Production Time per Seal by Operator",
                         text_auto=".2f", labels={"avg_time_per_seal": "Avg. Time (min)"})
        st.plotly_chart(fig_avg, use_container_width=True)

    # Weekly production
    df["week"] = df["date"].dt.strftime("%Y-%U")
    weekly_prod = df.groupby("week")["seal_count"].sum().reset_index()
    fig_week = px.bar(weekly_prod, x="week", y="seal_count",
                      title="📅 Weekly Seal Production", text_auto=True)
    st.plotly_chart(fig_week, use_container_width=True)
