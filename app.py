import streamlit as st
from modules.login import login
from modules.order_panel import show_order_panel
from modules.charts import show_charts
from modules.dashboard import show_dashboard
from modules.calculator import show_calculator
from modules.production_analysis import show_analysis
from modules.edit_orders import show_edit_orders
from modules.user_panel import show_user_panel
from modules.database import get_connection

import pandas as pd

def load_data():
    conn = get_connection()
    query = "SELECT * FROM production_data"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def main():
    st.set_page_config(page_title="Production Manager App", layout="wide")

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.role = ""

    if not st.session_state.authenticated:
        username, role = login()
        if username:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = role
        else:
            st.stop()

    st.sidebar.success(f"Logged in as {st.session_state.username} ({st.session_state.role})")

    df = load_data()

    selected = st.sidebar.radio("Go to", [
        "Dashboard",
        "Charts",
        "Order Panel",
        "Calculator",
        "Analysis",
        "Edit Orders",
        "User Management" if st.session_state.role == "Admin" else ""
    ])

    if selected == "Dashboard":
        show_dashboard()
    elif selected == "Charts":
        show_charts(df)
    elif selected == "Order Panel":
        show_order_panel(df)
    elif selected == "Calculator":
        show_calculator()
    elif selected == "Analysis":
        show_analysis(df)
    elif selected == "Edit Orders":
        show_edit_orders(df)
    elif selected == "User Management" and st.session_state.role == "Admin":
        show_user_panel()

if __name__ == "__main__":
    main()
