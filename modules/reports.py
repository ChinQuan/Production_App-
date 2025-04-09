import streamlit as st
import pandas as pd

def show_reports():
    st.title("📊 Reports & Export")

    df = pd.DataFrame(st.session_state.get("orders", []))
    if df.empty:
        st.warning("No data available.")
        return

    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    excel = df.to_excel(index=False, engine="openpyxl")

    st.download_button("⬇️ Download CSV", csv, "orders.csv", "text/csv")
    st.download_button("⬇️ Download Excel", excel, "orders.xlsx")
# Placeholder for reports.py
