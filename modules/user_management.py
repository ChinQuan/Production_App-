import streamlit as st
import psycopg2
import bcrypt

def login():
    st.sidebar.subheader("🔐 Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    login_button = st.sidebar.button("Login")

    if login_button:
        config = st.secrets["postgres"]
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user and bcrypt.checkpw(password.encode(), user[2].encode()):
                st.session_state["username"] = user[1]
                st.session_state["role"] = user[3]
                st.sidebar.success(f"✅ Logged in as {user[1]}")
                st.rerun()
            else:
                st.sidebar.error("❌ Invalid username or password.")
        except Exception as e:
            st.sidebar.error(f"Database error: {e}")
        finally:
            cursor.close()
            conn.close()

    if "username" in st.session_state:
        st.sidebar.success(f"✅ Logged in as {st.session_state['username']}")
        st.sidebar.button("Logout", on_click=lambda: st.session_state.clear())
        # 👇 Debug role
        st.sidebar.write("🛡️ Role:", st.session_state.get("role"))
