import streamlit as st
import pandas as pd
import bcrypt
from modules.database import get_connection

def authenticate_user(username_input, password_input):
    if not username_input or not password_input:
        return None, None, False

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, password, role FROM users WHERE username = %s", (username_input,))
        result = cursor.fetchone()
        conn.close()

        if result:
            db_username, db_password, db_role = result
            if bcrypt.checkpw(password_input.encode(), db_password.encode()):
                return db_username, db_role, True
            else:
                return None, None, False
        else:
            return None, None, False
    except Exception as e:
        st.error(f"Database error: {e}")
        return None, None, False

def show_user_management(current_role):
    if current_role != "Admin":
        st.warning("⚠️ Only admins can manage users.")
        return

    st.title("👥 User Management")

    conn = get_connection()
    cursor = conn.cursor()

    users = pd.read_sql("SELECT id, username, role FROM users ORDER BY id", conn)

    st.subheader("📋 Current Users")
    st.dataframe(users)

    st.divider()

    st.subheader("➕ Add New User")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    new_role = st.selectbox("Role", ["Admin", "Operator"])

    if st.button("Add User"):
        if new_username and new_password:
            hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                (new_username, hashed_pw, new_role)
            )
            conn.commit()
            st.success("✅ User added successfully.")
            st.experimental_rerun()
        else:
            st.error("Please fill in all fields.")

    st.divider()

    st.subheader("❌ Delete User")
    usernames = users['username'].tolist()
    user_to_delete = st.selectbox("Select user to delete", usernames)

    if st.button("Delete Selected User"):
        if user_to_delete:
            cursor.execute("DELETE FROM users WHERE username = %s", (user_to_delete,))
            conn.commit()
            st.success(f"✅ User '{user_to_delete}' deleted.")
            st.experimental_rerun()

    conn.close()

