import streamlit as st
import pandas as pd
import plotly.graph_objs as go

def show_charts(df):
    st.title("📈 Charts")

    if df.empty:
        st.warning("No orders to display.")
        return

    st.subheader("🧪 Raw Data Preview")
    st.write(df.head())

    # Filtrowanie po firmie
    if "company" in df.columns:
        selected_company = st.selectbox("Filter by Company", ["All"] + sorted(df["company"].dropna().unique().tolist()))
        if selected_company != "All":
            df = df[df["company"] == selected_company]

    # Konwersja production_time i seal_count do liczbowych
    if "production_time" in df.columns:
        df["production_time"] = pd.to_numeric(df["production_time"], errors="coerce")
    if "seal_count" in df.columns:
        df["seal_count"] = pd.to_numeric(df["seal_count"], errors="coerce")

    # Usuwamy wiersze z pustymi wartościami seal_count
    df = df.dropna(subset=["seal_count"])

    total_orders = len(df)
    total_seals = df["seal_count"].sum()
    avg_time = df["production_time"].mean() if "production_time" in df.columns else None

    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Total Orders", total_orders)
    col2.metric("🧷 Total Seals", total_seals)
    col3.metric("⏱️ Avg. Time", f"{avg_time:.1f} min" if pd.notnull(avg_time) else "N/A")

    if "seal_count" in df.columns and "id" in df.columns:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["id"],
            y=df["seal_count"],
            mode='lines+markers',
            name='Seals'
        ))
        fig.update_layout(title="Seals per Order", xaxis_title="Order ID", yaxis_title="Seals")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 Filtered Production Orders")
    st.dataframe(df)
