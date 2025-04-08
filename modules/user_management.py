# modules/user_management.py

import streamlit as st
import psycopg2
import bcrypt


def get_connection():
    conn = psycopg2.connect(
        host=st.secrets['postgres']['host'],
        database=st.secrets['postgres']['database'],
        user=st.secrets['postgres']['user'],
        password=st.secrets['postgres']['password'],
        port=st.secrets['postgres']['port']
    )
    return conn


def authenticate_user():
    st.sidebar.subheader("🔑 Logowanie")
    username = st.sidebar.text_input("Nazwa użytkownika")
    password = st.sidebar.text_input("Hasło", type="password")

    if st.sidebar.button("Zaloguj"):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT username, password, role FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()

            if result:
                db_username, hashed_password, role = result
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    st.success(f"✅ Zalogowano pomyślnie jako {role} - {username}")
                    return username, role, True
                else:
                    st.sidebar.error("❌ Nieprawidłowe hasło.")
            else:
                st.sidebar.error("❌ Użytkownik nie istnieje.")

            cursor.close()
            conn.close()
        except Exception as e:
            st.sidebar.error(f"❌ Wystąpił błąd podczas logowania: {e}")
    return None, None, False
    