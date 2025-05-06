import streamlit as st
import pandas as pd
import io

def show_reports(df):
    st.title("📊 Reports & Export")

    if df.empty:
        st.warning("No data to display. Add some orders to generate report.")
        return

    st.subheader("Current Production Orders")
    st.dataframe(df, use_container_width=True)

    df['Date'] = pd.to_datetime(df['date'], errors='coerce')
    df['Day'] = df['Date'].dt.date

    working_days = df.groupby('Day')['seal_count'].sum()
    avg_daily_production = working_days.mean()

    st.markdown(f"### Avg. Daily Production (Working Days Only): {avg_daily_production:.2f} seals per day")

    avg_daily_production_order = df['seal_count'].sum() / len(df['Day'].unique())
    st.markdown(f"### Avg. Daily Production (Order Dates Only): {avg_daily_production_order:.2f} seals per day")

    # --- Eksport danych ---
    st.subheader("📤 Export Data")

    # CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name='production_data.csv',
        mime='text/csv'
    )

    # Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Orders')
    processed_data = output.getvalue()

    st.download_button(
        label="⬇️ Download Excel",
        data=processed_data,
        file_name='production_data.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
