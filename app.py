import streamlit as st

# 🔑 Page configuration - MUST be the very first Streamlit command!
st.set_page_config(page_title="Production Manager App", layout="wide")


import bcrypt
from modules.user_management import show_user_management
from modules.import_data import show_import_data
from modules.form import show_form
from modules.reports import show_reports
from modules.charts import show_charts
from modules.database import execute_query
import psycopg2


# ✅ Function to establish a database connection


def main():
    st.sidebar.title("Production Manager App")
    menu = ["Formularz", "Raporty", "Wykresy", "Użytkownicy", "Import danych"]
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


if __name__ == "__main__":
    main()
