import streamlit as st
import pandas as pd
import psycopg2
import bcrypt

def show_user_panel():
    st.title("👥 User Management")

    if st.session_state.get("role") != "admin":
        st.error("❌ Access denied. This section is only for administrators.")
        return

    # 🔐 Connection copied from database.py
    config = st.secrets["postgres"]
    conn = psycopg2.connect(**config)
    cursor = conn.cursor()

    # ➕ ADD USER
    st.subheader("➕ Add New User")
    with st.form("add_user_form"):
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        new_role = st.selectbox("Role", ["admin", "operator"])
        submitted = st.form_submit_button("Create User")

        if submitted:
            if new_username and new_password:
                hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
                cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                               (new_username, hashed_pw, new_role))
                conn.commit()
                st.success(f"✅ User '{new_username}' created.")
            else:
                st.warning("Please fill in all fields.")

    st.divider()

    # 📋 VIEW USERS
    st.subheader("📋 Current Users")
    try:
        users_df = pd.read_sql("SELECT id, username, role FROM users ORDER BY id", conn)
        st.dataframe(users_df, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Failed to fetch users: {e}")
        return

    # 🔁 RESET PASSWORD
    st.subheader("🔁 Reset Password")
    with st.form("reset_pw_form"):
        user_to_reset = st.selectbox("Select user", users_df["username"].tolist())
        new_pw = st.text_input("New Password", type="password")
        reset_submitted = st.form_submit_button("Reset Password")

        if reset_submitted:
            if new_pw:
                hashed_pw = bcrypt.hashpw(new_pw.encode(), bcrypt.gensalt()).decode()
                cursor.execute("UPDATE users SET password=%s WHERE username=%s", (hashed_pw, user_to_reset))
                conn.commit()
                st.success(f"🔐 Password updated for '{user_to_reset}'")
            else:
                st.warning("Please enter a new password.")

    # ❌ DELETE USER
    st.subheader("❌ Delete User")
    with st.form("delete_user_form"):
        user_to_delete = st.selectbox("Select user to delete", users_df["username"].tolist())
        if user_to_delete == st.session_state["username"]:
            st.warning("⚠️ You cannot delete yourself.")
        else:
            delete_submitted = st.form_submit_button("Delete User")
            if delete_submitted:
                cursor.execute("DELETE FROM users WHERE username=%s", (user_to_delete,))
                conn.commit()
                st.success(f"🗑️ User '{user_to_delete}' deleted.")

    cursor.close()
    conn.close()
