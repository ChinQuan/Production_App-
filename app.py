# app.py

import streamlit as st
from modules.user_management import authenticate_user
from modules.admin_management import show_user_creation

def main():
    st.set_page_config(page_title="Production App", page_icon="⚙️", layout="wide")
    username, role, authenticated = authenticate_user()

    if authenticated:
        if role == 'Admin':
            st.sidebar.success("👑 Panel Admina")
            show_user_creation()
            st.write("### Funkcje dostępne dla Admina")
            st.write("- Dodawanie i zarządzanie użytkownikami")
            st.write("- Generowanie raportów")
            st.write("- Zarządzanie danymi produkcyjnymi")

        elif role == 'Operator':
            st.sidebar.success("🔧 Panel Operatora")
            st.write("### Funkcje dostępne dla Operatora")
            st.write("- Przeglądanie raportów")
            st.write("- Analiza danych produkcyjnych")

    else:
        st.write("## Proszę się zalogować z odpowiednimi uprawnieniami")


if __name__ == "__main__":
    main()
    