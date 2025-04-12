import streamlit as st
from modules.database import get_orders_df
from modules.charts import show_charts
from modules.dashboard import show_dashboard
from modules.order_panel import show_order_panel
from modules.analysis import show_analysis, calculate_average_time
from modules.user_management import show_user_management

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Order Panel", "Charts", "Dashboard", "Analysis", "User Management"])

    if page == "Order Panel":
        show_order_panel()

    elif page == "Charts":
        df = get_orders_df()
        show_charts(df)

    elif page == "Dashboard":
        df = get_orders_df()
        show_dashboard(df)

    elif page == "Analysis":
        df = get_orders_df()
        calculate_average_time(df)
        show_analysis(df)  # Jeśli show_analysis potrzebuje df – jeśli nie, usuń argument

    elif page == "User Management":
        show_user_management()

    else:
        st.sidebar.warning("You don't have access to this section.")

if __name__ == "__main__":
    main()
