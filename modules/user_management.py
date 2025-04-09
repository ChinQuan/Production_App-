import streamlit as st

# Sztuczna baza użytkowników (do testów prezentacyjnych)
USERS = {
    "admin": {"password": "admin123", "role": "Admin"},
    "user": {"password": "user123", "role": "Operator"},
}

def authenticate_user():
    st.title("🔐 Login")

    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    login_btn = st.button("➡️ Login")

    if login_btn:
        if username in USERS and USERS[username]["password"] == password:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = USERS[username]["role"]
            st.success(f"✅ Welcome, {username} ({st.session_state.role})")
        else:
            st.error("❌ Invalid credentials. Please try again.")

    return (
        st.session_state.get("username"),
        st.session_state.get("role"),
        st.session_state.get("authenticated", False),
    )

def show_user_management():
    st.subheader("👥 User Management Panel")
    st.info("This is a placeholder – real functionality could connect to a user database.")
# Placeholder for user_management.py
