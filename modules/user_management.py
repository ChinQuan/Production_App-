import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
import bcrypt

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
                try:
                    if bcrypt.checkpw(password.encode(), user["password"].encode()):
                        role = user["role"]
                        st.success(f"✅ Welcome, {username} ({role})")
                        return username, role
                except ValueError:
                    if password == user["password"]:
                        role = user["role"]
                        st.success(f"✅ Welcome, {username} ({role})")
                        return username, role

            st.error("Invalid username or password")

        except Exception as e:
            st.error(f"Database connection failed: {e}")
