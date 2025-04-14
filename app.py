import streamlit as st

st.write("🔥 App is loading...")

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
    if not st.session_state.get("username"):
        st.write("🧾 Showing login screen...")
        login()
        return

    role = st.session_state.get("role", "").lower()
    st.sidebar.title("Nawigacja")

    df = None
    pages = {
        "Order Panel": show_order_panel,
        "Charts": lambda: show_charts(df),
        "Dashboard": lambda: show_dashboard(df),
        "Edit Orders": lambda: show_edit_orders(df),
        "Analysis": lambda: calculate_average_time(df),
        "Calculator": show_calculator,
    }

    if role == "admin":
        pages["User Management"] = show_user_panel

    selected_page = st.sidebar.radio("Przejdź do:", list(pages.keys()))
    st.write(f"🔀 Page selected: {selected_page}")

    if selected_page in ["Charts", "Dashboard", "Edit Orders", "Analysis"]:
        st.write("📥 Loading data from database...")
        df = get_orders_df()

    pages[selected_page]()

if __name__ == "__main__":
    main()
