import streamlit as st
from modules.login import login
from modules.order_panel import show_order_panel
from modules.charts import show_charts
from modules.dashboard import show_dashboard
from modules.user_management import show_user_panel
from modules.production_analysis import show_production_analysis
from modules.edit_orders import show_edit_orders

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", [
        "Order Panel", 
        "Charts", 
        "Dashboard", 
        "User Management", 
        "Analysis", 
        "Edit Orders"
    ])

    if "username" not in st.session_state:
        login()

    if "username" in st.session_state:
        role = st.session_state.get("role", "user").lower()

        if page == "Order Panel":
            show_order_panel()
        elif page == "Charts":
            show_charts(df)
        elif page == "Dashboard":
            show_dashboard(df)
        elif page == "User Management":
            if role == "admin":
                show_user_panel()
            else:
                st.sidebar.warning("You don't have access to this section.")
        elif page == "Analysis":
            show_production_analysis()
        elif page == "Edit Orders":
            if role == "admin":
                show_edit_orders()
            else:
                st.sidebar.warning("You don't have access to this section.")
    else:
        st.warning("Please log in to continue.")

if __name__ == "__main__":
    main()
