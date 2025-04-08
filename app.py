import streamlit as st
st.set_page_config(page_title="Production Manager App", layout="wide")
import pandas as pd

from modules.user_management import authenticate_user, show_user_management
from modules.import_data import show_import_data
from modules.reports import show_reports
from modules.charts import show_charts
from modules.production_analysis import calculate_average_time
from modules.database import get_connection
from modules.form import show_form, show_home
from modules.admin_edit_orders import show_admin_edit_orders


def main():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.role = None

    if st.sidebar.button("Log out"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.role = None
        st.experimental_rerun()

    if not st.session_state.authenticated:
        authenticate_user()
        st.stop()  # <-- kluczowe, by zatrzymać kod, dopóki user się nie zaloguje

    st.sidebar.success(f"Logged in as: {st.session_state.username} ({st.session_state.role})")

    tabs = ["Add Order", "Reports", "Charts", "User Management"]
    if st.session_state.role == "admin":
        tabs.append("Admin Edit Orders")

    selected_tab = st.selectbox("Select View", tabs)

    if selected_tab == "Add Order":
        show_form()
    elif selected_tab == "Reports":
        show_reports()
    elif selected_tab == "Charts":
        show_charts()
    elif selected_tab == "User Management":
        show_user_management()
    elif selected_tab == "Admin Edit Orders" and st.session_state.role == "admin":
        show_admin_edit_orders()


if __name__ == "__main__":
    main()
