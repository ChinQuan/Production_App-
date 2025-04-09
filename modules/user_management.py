# modules/user_management.py
import streamlit as st

def authenticate_user():
    st.title("🔐 Login")

    username = st.text_input("🧑 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("➡️ Login"):
        if "users" in st.session_state and username in st.session_state.users:
            if st.session_state.users[username]["password"] == password:
                role = st.session_state.users[username]["role"]
                st.success(f"✅ Welcome, {username} ({role})")
                return username, role
            else:
                st.error("❌ Incorrect password.")
        else:
            st.error("❌ User not found.")
        return None, None  # Always return two values on failure

    return None, None  # If login button not clicked yet

def show_user_management():
    st.header("👥 User Management")

    if "users" not in st.session_state:
        st.session_state.users = {
            "admin": {"password": "admin", "role": "Admin"},
            "operator": {"password": "operator", "role": "Operator"}
        }

    with st.expander("➕ Add New User"):
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        new_role = st.selectbox("Role", ["Admin", "Operator"])
        if st.button("Add User"):
            if new_username in st.session_state.users:
                st.warning("⚠️ User already exists.")
            else:
                st.session_state.users[new_username] = {
                    "password": new_password,
                    "role": new_role
                }
                st.success(f"✅ User '{new_username}' added.")

    with st.expander("🗑 Remove User"):
        users_list = list(st.session_state.users.keys())
        user_to_remove = st.selectbox("Select User", users_list)
        if st.button("Remove User"):
            if user_to_remove in st.session_state.users:
                del st.session_state.users[user_to_remove]
                st.success(f"🗑 User '{user_to_remove}' removed.")

