import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(__file__))

from modules.login import login
from modules.order_panel import show_order_panel
from modules.charts import show_charts
from modules.dashboard import show_dashboard
from modules.production_analysis import calculate_average_time
from modules.user_management import show_user_panel
from modules.database import get_orders_df

def main():
    if not st.session_state.get("username"):
        login()
        return

    role = st.session_state.get("role", "guest")

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Order Panel", "Charts", "Dashboard", "Analysis", "User Management"])

    if page == "Order Panel":
        show_order_panel()
    elif page == "Charts":
        show_charts()
    elif page == "Dashboard":
        show_dashboard()
    elif page == "Analysis":
        df = get_orders_df()
        calculate_average_time(df)
    elif page == "User Management" and role.lower() == "admin":
        show_user_panel()
    else:
        st.sidebar.warning("You don't have access to this section.")

if __name__ == "__main__":
    main()

