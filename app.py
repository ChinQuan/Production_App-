import streamlit as st
import pandas as pd

from modules.user_management import authenticate_user, show_user_management
from modules.reports import show_reports
from modules.charts import show_charts
from modules.form import show_form
from modules.calculator import show_calculator
from modules.database import get_orders_df

def main():
    st.set_page_config(page_title="Production Manager App", layout="wide")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.role = None

    if st.sidebar.button("🚪 Logout"):
        for key in ["authenticated", "username", "role"]:
            st.session_state.pop(key, None)
        st.experimental_rerun()

    if not st.session_state.authenticated:
        username, role, authenticated = authenticate_user()
        if authenticated:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = role
        else:
            st.warning("🔒 Please log in to access the app.")
            return
    else:
        username = st.session_state.username
        role = st.session_state.role

    st.sidebar.markdown(f"## 👤 Logged in as {role}: `{username}`")

    menu = ["Add Order", "Reports", "Charts", "Calculator"]
    if role == "Admin":
        menu.extend(["User Management", "Edit Orders"])

    choice = st.sidebar.radio("📂 Navigation", menu)

    df = get_orders_df()  # załaduj dane produkcyjne z bazy lub session_state

    if choice == "Add Order":
        show_form()
    elif choice == "Reports":
        show_reports()
    elif choice == "Charts":
        show_charts()
    elif choice == "Calculator":
        show_calculator(df)
    elif choice == "User Management" and role == "Admin":
        show_user_management()
    elif choice == "Edit Orders" and role == "Admin":
        st.warning("🛠 Edit Orders view coming soon.")

if __name__ == "__main__":
    main()

