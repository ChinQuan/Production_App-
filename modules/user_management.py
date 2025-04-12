import streamlit as st
from modules.database import get_all_users, update_user, delete_user, create_user

def show_user_panel():
    st.title("🧑‍💼 User Management Panel")

    users = get_all_users()

    st.subheader("👥 Existing Users")
    for user in users:
        with st.expander(f"{user[1]} ({user[2]})"):
            new_role = st.selectbox(f"Role for {user[1]}", ["admin", "user"], index=["admin", "user"].index(user[2]), key=f"role_{user[0]}")
            new_password = st.text_input(f"New password for {user[1]} (leave empty to keep current)", type="password", key=f"pass_{user[0]}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Update {user[1]}", key=f"update_{user[0]}"):
                    success = update_user(user[0], new_role, new_password if new_password else None)
                    if success:
                        st.success(f"✅ User {user[1]} updated.")
                        st.rerun()
            with col2:
                if st.button(f"Delete {user[1]}", key=f"delete_{user[0]}"):
                    success = delete_user(user[0])
                    if success:
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
            success = create_user(new_username, new_user_password, new_user_role)
            if success:
                st.success(f"✅ User {new_username} created.")
                st.rerun()

