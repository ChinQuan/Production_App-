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
    # Jeśli użytkownik nie jest zalogowany, pokaż ekran logowania
    if not st.session_state.get("username"):
        login()
        return

    role = st.session_state.get("role", "").lower()
    st.sidebar.title("Nawigacja")

    # Lista dostępnych stron
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

    # Wybór strony
    page_names = list(pages.keys())
    selected_page = st.sidebar.radio("Przejdź do:", page_names)

    # Ładujemy dane tylko raz, jeśli któraś z podstron ich potrzebuje
    df = None
    if selected_page in ["Charts", "Dashboard", "Edit Orders", "Analysis"]:
        df = get_orders_df()

    # Wywołanie odpowiedniej funkcji
    pages[selected_page]()


if __name__ == "__main__":
    main()
