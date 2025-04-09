import streamlit as st
import pandas as pd
from modules.user_management import authenticate_user, show_user_management
from modules.form import show_form
from modules.reports import show_reports
from modules.charts import show_charts
from modules.edit_orders import show_edit_orders

st.set_page_config(page_title="Production Manager", layout="wide")

def main():
    # Inicjalizacja sesji
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.role = None

    # Wylogowanie
    if st.sidebar.button("🚪 Logout"):
        for key in ["authenticated", "username", "role"]:
            st.session_state.pop(key, None)
        st.rerun()

    # Logowanie
    if not st.session_state.authenticated:
        username, role, authenticated = authenticate_user()
        if authenticated:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = role
            st.rerun()
        else:
            st.stop()

    role = st.session_state.role
    username = st.session_state.username

    # Pasek boczny
    st.sidebar.markdown(f"## 👋 Hello, `{username}` ({role})")
    menu = ["Dashboard", "Reports", "Add Order", "Edit Orders"]
    if role == "Admin":
        menu.append("User Management")

    choice = st.sidebar.radio("Go to:", menu)

    # Nawigacja
    if choice == "Dashboard":
        show_charts()
    elif choice == "Reports":
        show_reports()
    elif choice == "Add Order":
        show_form()
    elif choice == "Edit Orders":
        show_edit_orders()
    elif choice == "User Management":
        show_user_management()

if __name__ == "__main__":
    main()

