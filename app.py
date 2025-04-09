import streamlit as st
st.set_page_config(page_title="Production Manager App", layout="wide")

from modules.user_management import authenticate_user
from modules.reports import show_reports
from modules.charts import show_charts
from modules.form import show_form
from modules.calculator import show_calculator
from modules.database import get_orders_df
from modules.analysis import calculate_average_time
from modules.edit_orders import show_edit_orders  # Dodane tutaj

def main():
    # Authentication
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

    role = st.session_state.get("role", "User")
    st.sidebar.title("Navigation")
    menu = [
        "📈 Charts","Dashboard", "Reports", "Add Order", "Calculator", "Analysis"]
    if role == "Admin":
        menu.append("Edit Orders")

    choice = st.sidebar.radio("Go to", menu)

    df = get_orders_df()

    if choice == "Dashboard":
        show_charts(df)
    elif choice == "Reports":
        show_reports(df)
    elif choice == "Add Order":
        show_form()
    elif choice == "Calculator":
        show_calculator(df)
    elif choice == "Analysis":
        calculate_average_time(df)
    elif choice == "Edit Orders" and role == "Admin":
        show_edit_orders(df)

if __name__ == "__main__":
    main()

