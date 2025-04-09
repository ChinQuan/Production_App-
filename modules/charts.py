import streamlit as st
import plotly.graph_objs as go

def show_charts(df):
    st.title("📊 Production Dashboard")

    if df.empty:
        st.warning("No orders to display.")
        return

    total_orders = len(df)
    total_seals = df["seal_count"].sum()
    avg_time = df["production_time"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Total Orders", total_orders)
    col2.metric("🧷 Total Seals", total_seals)
    col3.metric("⏱️ Avg. Time", f"{avg_time:.1f} min")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["seal_count"],
        mode='lines+markers',
        name='Seals'
    ))
    fig.update_layout(title="Seals per Order", xaxis_title="Order", yaxis_title="Seals")
    st.plotly_chart(fig, use_container_width=True)
