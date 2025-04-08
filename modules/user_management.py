import streamlit as st
import psycopg2
import bcrypt
from modules.database import get_connection

def authenticate_user():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
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
                st.error("❌ Invalid password.")
        else:
            st.error("❌ User not found.")

    return None, None, False

def show_user_management(role):
    st.title("👥 User Management")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, role FROM users")
    users = cursor.fetchall()
    conn.close()

    st.subheader("📋 Existing Users")
    for user in users:
        st.write(f"👤 {user[0]} - {user[1]}")

    st.subheader("➕ Add New User")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    new_role = st.selectbox("Role", ["Admin", "Operator"])

    if st.button("Create User"):
        hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                       (new_username, hashed_password, new_role))
        conn.commit()
        conn.close()
        st.success("✅ User created successfully.")
        st.experimental_rerun()

    st.subheader("🗑️ Delete User")
    user_to_delete = st.text_input("Enter username to delete")
    if st.button("Delete"):
        if user_to_delete != "admin":
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE username = %s", (user_to_delete,))
            conn.commit()
            conn.close()
            st.success("✅ User deleted.")
            st.experimental_rerun()
        else:
            st.warning("⚠️ Cannot delete the main admin user.")
