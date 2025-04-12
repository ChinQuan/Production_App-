import streamlit as st
from modules.order_panel import show_order_panel
from modules.charts import show_charts
from modules.dashboard import show_dashboard
from modules.analysis import calculate_average_time
from modules.user_management import show_user_panel
from modules.database import get_orders_df, get_current_user_role
from modules.auth import check_authentication
from modules.edit_orders import show_edit_orders


def main():
    st.set_page_config(page_title="Production App", layout="wide")

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        check_authentication()
        return

    role = get_current_user_role()
    page = st.sidebar.selectbox("Select Page", [
        "Order Panel", "Charts", "Dashboard", "Analysis", "Edit Orders", "Activity Log"])

    if role == "admin":
        df = get_orders_df()
        if page == "Order Panel":
            show_order_panel()
        elif page == "Charts":
            show_charts(df)
        elif page == "Dashboard":
            show_dashboard(df)
        elif page == "Analysis":
            calculate_average_time(df)
        elif page == "Edit Orders":
            show_edit_orders()
        elif page == "Activity Log":
            show_activity_log()
    else:
        if page in ["Order Panel", "Charts", "Dashboard", "Analysis"]:
            df = get_orders_df()
            if page == "Order Panel":
                show_order_panel()
            elif page == "Charts":
                show_charts(df)
            elif page == "Dashboard":
                show_dashboard(df)
            elif page == "Analysis":
                calculate_average_time(df)
        else:
            st.sidebar.warning("You don't have access to this section.")

if __name__ == "__main__":
    main()
