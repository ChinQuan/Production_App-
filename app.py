import streamlit as st
from modules.user_management import authenticate_user
from modules.reports import show_reports
from modules.charts import show_charts
from modules.form import show_form
from modules.user_admin import show_user_management
from modules.calculator import show_calculator
from modules.database import get_orders_df
from modules.analysis import calculate_average_time

def main():
    st.set_page_config(page_title="Production Manager App", layout="wide")

    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        username, role = authenticate_user()
        if username:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = role
            st.experimental_rerun()
        else:
            st.stop()

    role = st.session_state.get("role", "User")
    st.sidebar.title("Navigation")
    menu = ["Dashboard", "Reports", "Add Order", "Calculator", "Analysis"]
    if role == "Admin":
        menu.extend(["User Management", "Edit Orders"])

    choice = st.sidebar.radio("Go to", menu)

    df = get_orders_df()

    if choice == "Dashboard":
        show_charts()
    elif choice == "Reports":
        show_reports()
    elif choice == "Add Order":
        show_form()
    elif choice == "Calculator":
        show_calculator(df)
    elif choice == "Analysis":
        calculate_average_time(df)
    elif choice == "User Management" and role == "Admin":
        show_user_management()
    elif choice == "Edit Orders" and role == "Admin":
        st.warning("🛠 Edit Orders view coming soon.")

if __name__ == "__main__":
    main()
