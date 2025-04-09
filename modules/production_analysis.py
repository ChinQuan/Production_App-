import streamlit as st
import pandas as pd

def show_analysis():
    st.subheader("📈 Production Analysis")

    df = pd.DataFrame({
        "Company": ["Alpha", "Beta", "Gamma"],
        "Seals": [120, 150, 130],
        "Time (min)": [60, 90, 75],
    })

    avg_time = df["Time (min)"].mean()
    total_seals = df["Seals"].sum()

    st.metric("⏱️ Avg Production Time", f"{avg_time:.1f} min")
    st.metric("🧷 Total Seals", total_seals)
# Placeholder for production_analysis.py
