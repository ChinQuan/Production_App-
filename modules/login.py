import streamlit as st
import bcrypt
from modules.database import get_user_by_username

def login():
    st.sidebar.title("🔐 Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    login_btn = st.sidebar.button("Login")

    if login_btn:
        user = get_user_by_username(username)

        if user and bcrypt.checkpw(password.encode(), user["password"].encode()):
            st.session_state["username"] = username
            st.session_state["role"] = user["role"]
            st.rerun()
        else:
            st.sidebar.error("❌ Invalid username or password")

    if "username" in st.session_state:
        st.sidebar.success(f"✅ Logged in as {st.session_state['username']}")
        st.sidebar.write(f"🛡 Role: {st.session_state.get('role')}")
