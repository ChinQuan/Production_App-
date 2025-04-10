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
tabs = ["Dashboard", "Reports", "Calculator", "Analysis"]
if st.session_state.role == "Admin":
    tabs.append("Edit Orders")

selected_tab = st.selectbox("📁 Navigation", tabs, key="top_nav")

# Show Add Order form in the sidebar
if selected_tab == "Add Order":
    st.sidebar.subheader("📋 Add New Order")
    show_form()  # This will now show in the sidebar

# Load data from database
df = get_orders_df()

# Show column names for debugging
st.write("📋 Data Columns:", df.columns.tolist())

# Display dashboard with KPIs
if selected_tab == "Dashboard":
    st.subheader("📈 Key Production Metrics")
    col1, col2 = st.columns(2)

    if 'date' in df.columns:
        latest_date = df['date'].max()
        orders_today = df[df['date'] == latest_date].shape[0]
    else:
        orders_today = "No data"

    col1.metric("Orders Today", orders_today)
    col2.metric("Average Production Time", "4h 12m")  # Placeholder

    st.markdown("---")
    st.subheader("📊 Charts")
    show_charts(df)

elif selected_tab == "Reports":
    show_reports(df)
elif selected_tab == "Calculator":
    show_calculator(df)
elif selected_tab == "Analysis":
    calculate_average_time(df)
elif selected_tab == "Edit Orders":
    show_edit_orders(df)

