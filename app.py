import streamlit as st
from modules.login import login
from modules.order_panel import show_order_panel
from modules.charts import show_charts
from modules.dashboard import show_dashboard
from modules.user_management import show_user_panel
from modules.database import get_orders_df
from modules.analysis import calculate_average_time
from modules.calculator import show_calculator

def main():
    #st.sidebar.write("🧠 Debug:", st.session_state)

    if not st.session_state.get("username"):
        login()
        return

    role = st.session_state.get("role", "guest")

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Order Panel", "Charts", "Dashboard", "User Management", "Analysis", "Calculator"])

    if page == "Order Panel":
        show_order_panel()
    elif page == "Charts":
        df = get_orders_df()
        show_charts(df)
    elif page == "Dashboard":
        df = get_orders_df()
        show_dashboard(df)
    elif page == "User Management" and role == "admin":
        show_user_panel()
    elif page == "Calculator":
        df = get_orders_df()
        show_calculator(df)
    elif page == "Analysis":
        df = get_orders_df()
        calculate_average_time(df)
    else:
        st.sidebar.warning("You don't have access to this section.")

if __name__ == "__main__":
    main()
