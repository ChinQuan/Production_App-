# modules/admin_management.py

import streamlit as st
import psycopg2
import bcrypt

# Funkcja połączenia z bazą danych PostgreSQL
def get_connection():
    conn = psycopg2.connect(
        host=st.secrets['postgres']['host'],
        database=st.secrets['postgres']['database'],
        user=st.secrets['postgres']['user'],
        password=st.secrets['postgres']['password'],
        port=st.secrets['postgres']['port']
    )
    return conn

# Funkcja do dodawania nowego użytkownika (Admin lub Operator)
def add_user(username, password, role):
    conn = get_connection()
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
        (username, hashed_password, role)
    )
    conn.commit()
    conn.close()
    st.success(f"✅ Użytkownik {username} z rolą {role} został dodany pomyślnie!")

# Wyświetlenie interfejsu do tworzenia użytkownika
def show_user_creation():
    st.title("Zarządzanie użytkownikami")

    st.sidebar.header("Dodaj Nowego Użytkownika")
    new_username = st.sidebar.text_input("Nazwa użytkownika", key="new_username")
    new_password = st.sidebar.text_input("Hasło", type="password", key="new_password")
    role = st.sidebar.selectbox("Wybierz rolę", ("Admin", "Operator"), key="user_role")

    if st.sidebar.button("Dodaj Użytkownika", key="add_user_button"):
        if new_username and new_password:
            add_user(new_username, new_password, role)
        else:
            st.error("❌ Wprowadź nazwę użytkownika, hasło i rolę")
