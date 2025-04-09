import streamlit as st
import pandas as pd
import plotly.graph_objs as go

def show_charts():
    st.title("📊 Production Dashboard")

    # Dane testowe – można podmienić na realne
    df = pd.DataFrame({
        "Order ID": [1, 2, 3],
        "Company": ["Alpha", "Beta", "Gamma"],
        "Seals": [120, 150, 130],
        "Time (min)": [60, 90, 75],
    })

    total_orders = len(df)
    total_seals = df["Seals"].sum()
    avg_time = df["Time (min)"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Total Orders", total_orders)
    col2.metric("🧷 Total Seals", total_seals)
    col3.metric("⏱️ Avg. Time", f"{avg_time:.1f} min")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Order ID"],
        y=df["Seals"],
        mode='lines+markers',
        name='Seals'
    ))
    fig.update_layout(title="Seals per Order", xaxis_title="Order ID", yaxis_title="Seals")
    st.plotly_chart(fig, use_container_width=True)
# Placeholder for charts.py
