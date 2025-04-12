import streamlit as st
import bcrypt
from modules.database import get_connection

def show_user_panel():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()

    st.subheader("👥 Existing Users")
    for user in users:
        with st.expander(f"{user[1]} ({user[2]})"):
            current_role = user[2].lower()
            roles = ["admin", "user"]
            if current_role not in roles:
                roles.append(current_role)  # dodaj nietypową rolę, jeśli istnieje

            new_role = st.selectbox(
                f"Role for {user[1]}",
                roles,
                index=roles.index(current_role)
            )

            new_password = st.text_input(
                f"New password for {user[1]} (leave blank to keep current)",
                type="password"
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Update {user[1]}", key=f"update_{user[0]}"):
                    if new_password:
                        hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
                        cursor.execute("UPDATE users SET password=%s, role=%s WHERE id=%s", (hashed, new_role, user[0]))
                    else:
                        cursor.execute("UPDATE users SET role=%s WHERE id=%s", (new_role, user[0]))
                    conn.commit()
                    st.success(f"User {user[1]} updated successfully.")

            with col2:
                if st.button(f"Delete {user[1]}", key=f"delete_{user[0]}"):
                    cursor.execute("DELETE FROM users WHERE id=%s", (user[0],))
                    conn.commit()
                    st.warning(f"User {user[1]} deleted.")
