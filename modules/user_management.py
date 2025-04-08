import streamlit as st
import json
import os
import hashlib

USERS_FILE = "users.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)

def authenticate_user():
    st.sidebar.title("🔐 Login")

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    users = load_users()
    hashed_password = hash_password(password)

    if st.sidebar.button("Login"):
        if username in users and users[username]["password"] == hashed_password:
            st.success("✅ Login successful")
            return username, users[username]["role"], True
        else:
            st.error("❌ Login failed: invalid credentials")

    return None, None, False

def show_user_management(role):
    st.header("👥 User Management")

    users = load_users()
    st.subheader("📋 User List")
    user_list = [[user, users[user]["role"]] for user in users]
    st.json(user_list)

    st.subheader("➕ Add New User")

    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    new_role = st.selectbox("Role", ["Admin", "Operator"])

    if st.button("Create User"):
        if new_username in users:
            st.warning("⚠️ This username already exists.")
        else:
            users[new_username] = {
                "password": hash_password(new_password),
                "role": new_role
            }
            save_users(users)
            st.success(f"✅ User `{new_username}` created successfully.")
            st.experimental_rerun()
