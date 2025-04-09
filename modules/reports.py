import streamlit as st
import pandas as pd
from io import BytesIO

def show_reports():
    st.title("📊 Reports & Export")

    # Wczytanie danych z CSV
    try:
        df = pd.read_csv("orders.csv")
    except FileNotFoundError:
        st.warning("Brak danych do wyświetlenia. Dodaj zamówienia, aby wygenerować raport.")
        return

    st.dataframe(df)

    # Eksport do CSV
    csv = df.to_csv(index=False).encode("utf-8")

    # Eksport do Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Orders")
    excel_data = output.getvalue()

    # Przyciski pobierania
    st.download_button(
        "⬇️ Download CSV", 
        data=csv, 
        file_name="orders.csv", 
        mime="text/csv"
    )

    st.download_button(
        "⬇️ Download Excel", 
        data=excel_data, 
        file_name="orders.xlsx", 
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
