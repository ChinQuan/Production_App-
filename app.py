import streamlit as st

# 🔑 Page configuration - MUST be the very first Streamlit command!
st.set_page_config(page_title="Production Manager App", layout="wide")


import bcrypt
from modules.user_management import show_user_management, authenticate_user  # Importowanie funkcji do logowania
from modules.import_data import show_import_data
from modules.form import show_form
from modules.reports import show_reports
from modules.charts import show_charts
from modules.database import execute_query
import psycopg2


def main():
    st.sidebar.title("Production Manager App")
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None

    if not st.session_state.authenticated:
        username, authenticated = authenticate_user()
        if authenticated:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.experimental_rerun()
        else:
            st.sidebar.error("❌ Błędne dane logowania. Spróbuj ponownie.")
    else:
        st.sidebar.success(f"✅ Zalogowany jako: {st.session_state.username}")
        menu = ["Formularz", "Raporty", "Wykresy", "Użytkownicy", "Import danych", "Wyloguj"]
        choice = st.sidebar.selectbox("Nawigacja", menu)

        if choice == "Formularz":
            show_form("form_tab")  # Przekazywanie unikalnej nazwy zakładki
        elif choice == "Raporty":
            show_reports()
        elif choice == "Wykresy":
            show_charts()
        elif choice == "Użytkownicy":
            show_user_management()
        elif choice == "Import danych":
            show_import_data()
        elif choice == "Wyloguj":
            st.session_state.authenticated = False
            st.session_state.username = None
            st.experimental_rerun()


if __name__ == "__main__":
    main()
