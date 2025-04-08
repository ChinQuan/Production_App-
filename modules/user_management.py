import streamlit as st
import bcrypt
from modules.database import get_connection

# 🔐 AUTHENTICATION
def authenticate_user(username, password):
    if not username or not password:
        return None, None, False

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, password, role FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        conn.close()

        if result:
            db_username, db_password, db_role = result
            if bcrypt.checkpw(password.encode(), db_password.encode()):
                return db_username, db_role, True
        return None, None, False

    except Exception as e:
        st.error(f"Database error: {e}")
        return None, None, False

# 👥 USER MANAGEMENT PANEL
def show_user_management(current_role):
    st.title("👥 User Management")

    if current_role != "Admin":
        st.warning("You do not have permission to access this section.")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, role FROM users")
    users = cursor.fetchall()
    conn.close()

    st.subheader("📋 Existing Users")
    for user in users:
        st.markdown(f"**👤 {user[0]}** — _{user[1]}_")

    st.subheader("➕ Add New User")

    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    new_role = st.selectbox("Role", ["Admin", "Operator"])

    if st.button("Create User"):
        if not new_username or not new_password:
            st.warning("Please provide both username and password.")
        else:
            hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()

            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                               (new_username, hashed_password, new_role))
                conn.commit()
                conn.close()
                st.success(f"✅ User `{new_username}` added successfully.")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"❌ Failed to create user: {e}")
