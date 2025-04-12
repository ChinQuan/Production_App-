import streamlit as st
from modules.order_panel import show_order_panel
from modules.charts import show_charts
from modules.dashboard import show_dashboard
from modules.user_management import show_user_panel
from modules.production_analysis import show_production_analysis
from modules.database import get_orders_df

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Order Panel", "Charts", "Dashboard", "Analysis", "User Management"])

    df = get_orders_df()  # <- to jest kluczowe

    if page == "Order Panel":
        show_order_panel()
    elif page == "Charts":
        show_charts(df)  # <- przekazanie df
    elif page == "Dashboard":
        show_dashboard(df)  # <- przekazanie df
    elif page == "Analysis":
        show_production_analysis(df)  # <- przekazanie df
    elif page == "User Management":
        if "role" in st.session_state and st.session_state["role"].lower() == "admin":
            show_user_panel()
        else:
            st.sidebar.warning("You don't have access to this section.")

if __name__ == "__main__":
    main()
