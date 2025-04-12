import streamlit as st
import bcrypt
from modules.database import get_connection

def show_user_panel():
    conn = get_connection()
    cursor = conn.cursor()

    st.header("👨‍💼 User Management Panel")

    # --- Add new user section ---
    st.subheader("➕ Add New User")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    new_role = st.selectbox("Role", ["admin", "user", "operator"])

    if st.button("Create User"):
        if new_username and new_password:
            # Check if user exists
            cursor.execute("SELECT * FROM users WHERE username = %s", (new_username,))
            if cursor.fetchone():
                st.error("User already exists.")
            else:
                hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
                cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                               (new_username, hashed_pw, new_role))
                conn.commit()
                st.success(f"User '{new_username}' created successfully!")
        else:
            st.warning("Please fill in both username and password.")

    st.divider()

    # --- Existing users section ---
    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()
    st.subheader("👥 Existing Users")

    for user in users:
        with st.expander(f"{user[1]} ({user[2]})"):
            current_role = user[2].lower()
            roles = ["admin", "user", "operator"]
            if current_role not in roles:
                roles.append(current_role)

            new_role = st.selectbox(
                f"Role for {user[1]}", roles, index=roles.index(current_role), key=f"role_{user[0]}"
            )

            new_password = st.text_input(
                f"New password for {user[1]} (leave blank to keep current)", type="password", key=f"pw_{user[0]}"
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Update {user[1]}", key=f"update_{user[0]}"):
                    if new_password:
                        hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
                        cursor.execute("UPDATE users SET password=%s, role=%s WHERE id=%s",
                                       (hashed, new_role, user[0]))
                    else:
                        cursor.execute("UPDATE users SET role=%s WHERE id=%s", (new_role, user[0]))
                    conn.commit()
                    st.success(f"User {user[1]} updated successfully.")

            with col2:
                if st.button(f"Delete {user[1]}", key=f"delete_{user[0]}"):
                    cursor.execute("DELETE FROM users WHERE id=%s", (user[0],))
                    conn.commit()
                    st.warning(f"User {user[1]} deleted.")
