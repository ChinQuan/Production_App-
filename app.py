import streamlit as st
st.set_page_config(page_title="Production Manager App", layout="wide")
from modules.user_management import authenticate_user
from modules.reports import show_reports
from modules.charts import show_charts
from modules.form import show_form
from modules.calculator import show_calculator
from modules.database import get_orders_df
from modules.analysis import calculate_average_time
from modules.edit_orders import show_edit_orders

# Set page config


# User authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    username, role = authenticate_user()
    if username:
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.role = role
        st.rerun()
    else:
        st.stop()

# Main layout
st.title("📊 Production Manager App")
st.markdown("---")

# Top navigation bar
tabs = ["Dashboard", "Reports", "Add Order", "Calculator", "Analysis"]
if st.session_state.role == "Admin":
    tabs.append("Edit Orders")

selected_tab = st.selectbox("📁 Nawigacja", tabs, key="top_nav")

# Load data from database
df = get_orders_df()

# Display dashboard with KPIs
if selected_tab == "Dashboard":
    st.subheader("📈 Kluczowe metryki produkcyjne")
    col1, col2, col3 = st.columns(3)
    col1.metric("Zlecenia dziś", df[df['data'] == df['data'].max()].shape[0])
    col2.metric("Średni czas realizacji", "4h 12m")  # Placeholder
    col3.metric("Całkowity koszt", f"{df['koszt'].sum():,.0f} zł")
    
    st.markdown("---")
    st.subheader("📊 Wykresy")
    show_charts(df)

elif selected_tab == "Reports":
    show_reports(df)
elif selected_tab == "Add Order":
    show_form()
elif selected_tab == "Calculator":
    show_calculator(df)
elif selected_tab == "Analysis":
    calculate_average_time(df)
elif selected_tab == "Edit Orders":
    show_edit_orders(df)

