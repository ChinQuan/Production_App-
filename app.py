# Modular structure placeholder
import streamlit as st
from modules.user_management import authenticate_user
from modules.reports import show_reports
from modules.charts import show_charts
from modules.production_analysis import show_analysis
from modules.form import show_form
from modules.edit_orders import show_edit_orders

st.set_page_config(page_title="Production App", layout="wide")

def main():
    st.sidebar.title("Navigation")
    menu = ["Dashboard", "Reports", "Add Order", "Edit Orders"]
    choice = st.sidebar.radio("Go to", menu)

    if choice == "Dashboard":
        show_charts()
    elif choice == "Reports":
        show_reports()
    elif choice == "Add Order":
        show_form()
    elif choice == "Edit Orders":
        show_edit_orders()

if __name__ == '__main__':
    main()
