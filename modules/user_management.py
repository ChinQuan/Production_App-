import streamlit as st
import bcrypt
from modules.database import get_connection

def authenticate_user():
    st.sidebar.title("🔐 Login")

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login") and username and password:
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
                st.error("❌ Incorrect password")
                return None, None, False
        else:
            st.error("❌ User not found")
            return None, None, False

    return None, None, False


