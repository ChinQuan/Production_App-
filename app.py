import streamlit as st
from modules.login import login  # Import funkcji login z modułu login
from modules.order_panel import show_order_panel
from modules.charts import show_charts
from modules.dashboard import show_dashboard
from modules.user_management import show_user_panel  # Import funkcji do zarządzania użytkownikami

def main():
    # Sprawdzanie, czy użytkownik jest zalogowany
    if not st.session_state.get("username"):
        login()  # Jeśli użytkownik nie jest zalogowany, wywołujemy funkcję login()
        return

    # Gdy użytkownik jest zalogowany, wyświetlamy odpowiedni panel
    role = st.session_state.get("role", "guest")
    
    # Dodawanie różnych zakładek w zależności od roli użytkownika
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Order Panel", "Charts", "Dashboard", "User Management"])

    if page == "Order Panel":
        show_order_panel()
    elif page == "Charts":
        show_charts(df)
    elif page == "Dashboard":
        show_dashboard(df)
    elif page == "User Management" and role == "admin":
        show_user_panel(df)  # Wyświetlenie panelu do zarządzania użytkownikami tylko dla admina
    else:
        st.sidebar.warning("You don't have access to this section.")

if __name__ == "__main__":
    main()
