
import streamlit as st
import bcrypt
from modules.database import get_connection

def show_user_panel():
    st.title("🧑‍💼 User Management Panel")

    # Load all users
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users ORDER BY id")
    users = cursor.fetchall()
    conn.close()

    st.subheader("👥 Existing Users")
    for user in users:
        with st.expander(f"{user[1]} ({user[2]})"):
            new_role = st.selectbox(f"Role for {user[1]}", ["admin", "user"], index=["admin", "user"].index(user[2]), key=f"role_{user[0]}")
            new_password = st.text_input(f"New password for {user[1]} (leave empty to keep current)", type="password", key=f"pass_{user[0]}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Update {user[1]}", key=f"update_{user[0]}"):
                    conn = get_connection()
                    cursor = conn.cursor()
                    if new_password:
                        hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
                        cursor.execute("UPDATE users SET role = %s, password = %s WHERE id = %s", (new_role, hashed_pw, user[0]))
                    else:
                        cursor.execute("UPDATE users SET role = %s WHERE id = %s", (new_role, user[0]))
                    conn.commit()
                    conn.close()
                    st.success(f"✅ User {user[1]} updated.")
                    st.rerun()
            with col2:
                if st.button(f"Delete {user[1]}", key=f"delete_{user[0]}"):
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM users WHERE id = %s", (user[0],))
                    conn.commit()
                    conn.close()
                    st.warning(f"🗑️ User {user[1]} deleted.")
                    st.rerun()

    st.subheader("➕ Add New User")
    new_username = st.text_input("New Username")
    new_user_password = st.text_input("New Password", type="password")
    new_user_role = st.selectbox("Role", ["user", "admin"])
    if st.button("Create User"):
        if not new_username or not new_user_password:
            st.error("❗ Please enter both username and password.")
        else:
            hashed_pw = bcrypt.hashpw(new_user_password.encode(), bcrypt.gensalt()).decode()
            conn = get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (new_username, hashed_pw, new_user_role))
                conn.commit()
                st.success(f"✅ User {new_username} created.")
                st.rerun()
            except Exception as e:
                st.error(f"⚠️ Error: {e}")
            finally:
                conn.close()
