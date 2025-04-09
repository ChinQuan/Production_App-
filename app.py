
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from io import BytesIO

st.set_page_config(page_title="📊 Dashboard", layout="wide")

# Fake session role (for testing)
if "authenticated" not in st.session_state:
    st.session_state.authenticated = True
    st.session_state.username = "admin"
    st.session_state.role = "Admin"

st.sidebar.title("📁 Navigation")
menu = ["📊 Dashboard", "📤 Export", "📝 Edit Orders"] if st.session_state.role == "Admin" else ["📊 Dashboard"]
choice = st.sidebar.radio("Go to:", menu)

# Fake data
df = pd.DataFrame({
    "Order ID": [1, 2, 3],
    "Company": ["Alpha", "Beta", "Gamma"],
    "Operator": ["John", "Anna", "Tom"],
    "Seals": [120, 150, 130],
    "Time (min)": [60, 90, 75],
})

if choice == "📊 Dashboard":
    st.title("📊 Production Dashboard")
    col1, col2, col3 = st.columns(3)
    col1.metric("🧾 Total Orders", len(df))
    col2.metric("🔩 Total Seals", df["Seals"].sum())
    col3.metric("⏱️ Avg. Time", f"{df['Time (min)'].mean():.1f} min")

    st.line_chart(df.set_index("Order ID")["Seals"])

elif choice == "📤 Export":
    st.title("📤 Export Data")
    csv = df.to_csv(index=False).encode('utf-8')
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_data = excel_buffer.getvalue()

    st.download_button("⬇️ Download CSV", csv, "orders.csv", "text/csv")
    st.download_button("⬇️ Download Excel", excel_data, "orders.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

elif choice == "📝 Edit Orders":
    st.title("📝 Edit Orders (Admin Only)")
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=True)
    grid_options = gb.build()
    grid_response = AgGrid(df, gridOptions=grid_options, editable=True, fit_columns_on_grid_load=True)
    st.success("✔️ You can now edit orders directly in the table.")
