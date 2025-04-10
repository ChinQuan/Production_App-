import bcrypt
# modules/user_management.py
import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor

# 🔐 User authentication using PostgreSQL
def authenticate_user():
    st.title("🔐 Login")

    username = st.text_input("🧑 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("➡️ Login"):
        config = st.secrets["postgres"]
        try:
            conn = psycopg2.connect(
                host=config["host"],
                database=config["database"],
                user=config["user"],
                password=config["password"],
                port=config["port"],
                sslmode=config["sslmode"]
            )
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            conn.close()

            if user:
                if bcrypt.checkpw(password.encode(), user["password"].encode()):  # ⚠️ You can switch to bcrypt here later
                    role = user["role"]
                    st.success(f"✅ Welcome, {username} ({role})")
                    return username, role
                else:
                    st.error("❌ Incorrect password.")
            else:
                st.error("❌ User not found.")
        except Exception as e:
            st.error(f"Database error: {e}")

    return None, None

# 🧑‍💼 Optional: user management interface (add/remove users)
def show_user_management():
    st.header("👥 User Management")

    config = st.secrets["postgres"]
    conn = psycopg2.connect(
        host=config["host"],
        database=config["database"],
        user=config["user"],
        password=config["password"],
        port=config["port"],
        sslmode=config["sslmode"]
    )
    cursor = conn.cursor()

    with st.expander("➕ Add New User"):
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        new_role = st.selectbox("Role", ["Admin", "Operator"])

        if st.button("Add User"):
            cursor.execute("SELECT * FROM users WHERE username = %s", (new_username,))
            existing = cursor.fetchone()
            if existing:
                st.warning("⚠️ User already exists.")
            else:
                cursor.execute(
                    "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                    (new_username, new_password, new_role)
                )
                conn.commit()
                st.success(f"✅ User '{new_username}' added.")

    with st.expander("🗑 Remove User"):
        cursor.execute("SELECT username FROM users")
        user_list = [row[0] for row in cursor.fetchall()]
        user_to_remove = st.selectbox("Select User", user_list)

        if st.button("Remove User"):
            cursor.execute("DELETE FROM users WHERE username = %s", (user_to_remove,))
            conn.commit()
            st.success(f"🗑 User '{user_to_remove}' removed.")

    cursor.close()
    conn.close()
