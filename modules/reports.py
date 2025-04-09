import streamlit as st
import pandas as pd
from io import BytesIO

def show_reports():
    st.title("📊 Reports & Export")

    # Dane przykładowe – do prezentacji
    df = pd.DataFrame({
        "Order ID": [1, 2, 3],
        "Company": ["Alpha", "Beta", "Gamma"],
        "Operator": ["John", "Anna", "Tom"],
        "Seals": [120, 150, 130],
        "Time (min)": [60, 90, 75],
    })

    st.dataframe(df)

    # Eksport CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download CSV", data=csv, file_name="report.csv", mime="text/csv")

    # Eksport Excel
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_data = excel_buffer.getvalue()
    st.download_button("⬇️ Download Excel", data=excel_data, file_name="report.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
# Placeholder for reports.py
