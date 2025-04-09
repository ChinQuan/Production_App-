
import streamlit as st
import pandas as pd

# Domyślni użytkownicy
def load_users():
    return {
        "admin": {"password": "admin123", "role": "Admin"},
        "user": {"password": "user123", "role": "Operator"},
    }

def authenticate_user():
    if "users" not in st.session_state:
        st.session_state.users = load_users()

    st.title("🔐 Login")

    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("➡️ Login"):
        if username in st.session_state.users and st.session_state.users[username]["password"] == password:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = st.session_state.users[username]["role"]
            st.success(f"✅ Welcome, {username} ({st.session_state.role})")
        else:
            st.error("❌ Invalid credentials. Please try again.")

    return (
        st.session_state.get("username"),
        st.session_state.get("role"),
        st.session_state.get("authenticated", False),
    )

def show_user_management():
    st.title("👥 User Management")

    if "users" not in st.session_state:
        st.session_state.users = load_users()

    st.subheader("➕ Add New User")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    new_role = st.selectbox("Role", ["Admin", "Operator"])

    if st.button("➕ Create User"):
        if new_username in st.session_state.users:
            st.warning("⚠️ User already exists.")
        else:
            st.session_state.users[new_username] = {
                "password": new_password,
                "role": new_role
            }
            st.success(f"✅ User `{new_username}` added as {new_role}")

    st.subheader("📋 Existing Users")
    users_df = pd.DataFrame([
        {"Username": u, "Role": info["role"]}
        for u, info in st.session_state.users.items()
    ])
    st.table(users_df)
