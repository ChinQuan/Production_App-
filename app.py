import streamlit as st
st.set_page_config(page_title="Production Manager App", layout="wide")
from modules.user_management import authenticate_user
from modules.reports import show_reports
from modules.charts import show_charts
from modules.form import show_form
from modules.calculator import show_calculator
from modules.user_admin import show_user_admin
from modules.average_production import show_avg_production_time



# Sidebar navigation
st.sidebar.title("📊 Menu")
page = st.sidebar.radio("Go to", ["Home", "Production Charts", "Calculator", "User Management", "Reports", "Average Production Time"])

# User authentication
auth_result = authenticate_user()
if auth_result:
    username, role = auth_result

    # Sidebar info
    st.sidebar.success(f"Logged in as {username} ({role})")
    if st.sidebar.button("Logout"):
        st.cache_data.clear()
        st.rerun()

    # Navigation logic
    if page == "Home":
        st.title("🏠 Production Data Overview")
    elif page == "Production Charts":
        show_charts()
    elif page == "Calculator":
        show_calculator()
    elif page == "User Management":
        if role == "admin":
            show_user_admin()
        else:
            st.warning("You do not have access to this page.")
    elif page == "Reports":
        show_reports()
    elif page == "Average Production Time":
        show_avg_production_time()
else:
    st.warning("Please log in to access the app.")
