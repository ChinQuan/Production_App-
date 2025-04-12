import streamlit as st
from modules.order_panel import show_order_panel
from modules.charts import show_charts
from modules.dashboard import show_dashboard
from modules.analysis import show_analysis
from modules.user_management import show_user_management
from modules.database import get_orders_df, get_current_user_role
from modules.auth import check_authentication
from modules.edit_orders import show_edit_orders
from modules.activity_log import show_activity_log

def main():
    st.set_page_config(page_title="Production Management App", layout="wide")

    if not check_authentication():
        st.stop()

    role = get_current_user_role()
    df = get_orders_df()

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Order Panel", "Charts", "Dashboard", "Analysis", "User Management", "Edit Orders", "Activity Log"])

    if role == "admin":
        if page == "Order Panel":
            show_order_panel()
        elif page == "Charts":
            show_charts(df)
        elif page == "Dashboard":
            show_dashboard(df)
        elif page == "Analysis":
            show_analysis()
        elif page == "User Management":
            show_user_management()
        elif page == "Edit Orders":
            show_edit_orders()
        elif page == "Activity Log":
            show_activity_log()
    else:
        if page in ["Order Panel", "Charts", "Dashboard", "Analysis"]:
            if page == "Order Panel":
                show_order_panel()
            elif page == "Charts":
                show_charts(df)
            elif page == "Dashboard":
                show_dashboard(df)
            elif page == "Analysis":
                show_analysis()
        else:
            st.sidebar.warning("You don't have access to this section.")

if __name__ == "__main__":
    main()
