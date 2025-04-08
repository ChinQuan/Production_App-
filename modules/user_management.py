import streamlit as st
import bcrypt
from modules.database import get_connection

def authenticate_user():
    st.sidebar.title("🔐 Login")

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    # Zmienna do kontrolowania stanu logowania
    login_button_pressed = st.sidebar.button("Login")

    # Domyślnie nic nie robi — zwraca brak danych
    if not login_button_pressed:
        return None, None, False

    if not username or not password:
        st.error("❌ Please fill in both fields.")
        return None, None, False

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password, role FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        conn.close()

        if result:
            hashed_password, role = result
            if bcrypt.checkpw(password.encode(), hashed_password.encode()):
                return username, role, True
            else:
                st.error("❌ Incorrect password.")
        else:
            st.error("❌ User not found.")
    except Exception as e:
        st.error(f"⚠️ Login error: {e}")

    return None, None, False

