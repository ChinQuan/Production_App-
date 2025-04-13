import streamlit as st
from modules.login import login
from modules.order_panel import show_order_panel
from modules.charts import show_charts
from modules.dashboard import show_dashboard
from modules.user_management import show_user_panel
from modules.database import get_orders_df
from modules.analysis import calculate_average_time
from modules.calculator import show_calculator
from modules.edit_orders import show_edit_orders

def main():
    # Debug:
    # st.sidebar.write("🧠 Debug:", st.session_state)

    if not st.session_state.get("username"):
        login()
        return

    role = st.session_state.get("role", "guest")

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", [
        "Order Panel",
        "Charts",
        "Dashboard",
        "Edit Orders",
        "User Management",
        "Analysis",
        "Calculator"
    ])

    if page == "Order Panel":
        show_order_panel()

    elif page == "Charts":
        df = get_orders_df()
        show_charts(df)

    elif page == "Dashboard":
        df = get_orders_df()
        show_dashboard(df)

    elif page == "Edit Orders":
        df = get_orders_df()
        show_edit_orders(df)

    elif page == "User Management":  # ⚠️ admin check temporarily disabled
        show_user_panel()

    elif page == "Analysis":
        df = get_orders_df()
        calculate_average_time(df)

    elif page == "Calculator":
        show_calculator()

if __name__ == "__main__":
    main()
