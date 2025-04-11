
import streamlit as st
st.set_page_config(page_title="Production Manager App", layout="wide")

from modules.user_management import authenticate_user
from modules.reports import show_reports
from modules.charts import show_charts
from modules.form import show_form
from modules.calculator import show_calculator
from modules.database import get_orders_df
from modules.analysis import calculate_average_time
from modules.edit_orders import show_edit_orders
from modules.order_panel import show_order_panel

def main():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        username, role = authenticate_user()
        if username:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = role
            st.rerun()
        else:
            st.stop()

    role = st.session_state.get("role", "User")
    st.sidebar.title("Navigation")
    menu = [
        "📥 Order Panel",
        "📈 Charts",
        "📊 Dashboard",
        "Reports",
        "Add Order",
        "Calculator",
        "Analysis",
        "Edit Orders"
    ]
    selected = st.sidebar.radio("Go to", menu)

    if selected == "📥 Order Panel":
        show_order_panel()

    elif selected == "📈 Charts":
        df = get_orders_df()
        show_charts(df)

    elif selected == "📊 Dashboard":
        st.write("🚧 Dashboard placeholder")

    elif selected == "Reports":
        show_reports()

    elif selected == "Add Order":
        show_form()

    elif selected == "Calculator":
        show_calculator()

    elif selected == "Analysis":
        calculate_average_time()

    elif selected == "Edit Orders":
        df = get_orders_df()
        show_edit_orders(df)

if __name__ == "__main__":
    main()
