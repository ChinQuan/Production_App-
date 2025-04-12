import streamlit as st

from modules.order_panel import show_order_panel
from modules.charts import show_charts
from modules.dashboard import show_dashboard
from modules.analysis import calculate_average_time
from modules.user_management import show_user_panel
from modules.database import get_orders_df
from modules.edit_orders import show_edit_orders

def main():
    st.set_page_config(layout="wide")
    st.title("Order Management")

    menu = ["Dashboard", "Order Panel", "Charts", "Edit Orders", "Users"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "Dashboard":
        show_dashboard()
    elif choice == "Order Panel":
        show_order_panel()
    elif choice == "Charts":
        show_charts()
    elif choice == "Edit Orders":
        show_edit_orders()
    elif choice == "Users":
        show_user_panel()

if __name__ == "__main__":
    main()
