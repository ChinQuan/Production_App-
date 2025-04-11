import streamlit as st
import bcrypt
from modules.database import get_connection

def login():
    st.sidebar.title("🔐 Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    login_btn = st.sidebar.button("Login")

    if login_btn:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password, role FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        conn.close()

        if result and bcrypt.checkpw(password.encode(), result[0].encode()):
            st.sidebar.success(f"✅ Logged in as {username}")
            st.sidebar.write(f"🛡 Role: {result[1]}")
            return username, result[1]
        else:
            st.sidebar.error("❌ Invalid username or password")

    return None, None
