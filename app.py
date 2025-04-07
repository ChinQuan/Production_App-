import streamlit as st
import bcrypt
from modules.user_management import show_user_management
from modules.import_data import show_import_data
from modules.form import show_form
from modules.reports import show_reports
from modules.charts import show_charts
from modules.database import execute_query
import psycopg2

# 🔑 Page configuration - MUST be at the top!
st.set_page_config(page_title="Production Manager App", layout="wide")

# ✅ Function to establish a database connection
def get_connection():
    return psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        database=st.secrets["postgres"]["database"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"],
        port=st.secrets["postgres"]["port"],
        sslmode=st.secrets["postgres"]["sslmode"]
    )

# ✅ Login function - improved to work with bcrypt
def login(username, password):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT username, password, role FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            return {"Username": user[0], "Role": user[2]}
        return None

    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None

menu = ["Home", "Form", "Reports", "Charts", "User Management", "Import Data"]
choice = st.sidebar.selectbox("Select Menu", menu)

# 🌟 Login Interface
if st.session_state.user is None:
    st.sidebar.title("🔑 Login")
    username = st.sidebar.text_input("Username", key="login_username")
    password = st.sidebar.text_input("Password", type="password", key="login_password")

    if st.sidebar.button("Login"):
        user = login(username, password)
        if user:
            st.session_state.user = user
            st.sidebar.success(f"✅ Logged in as: {user['Username']} (Role: {user['Role']})")
        else:
            st.sidebar.error("❌ Invalid username or password.")
else:
    st.sidebar.write(f"✅ Logged in as: {st.session_state.user['Username']} (Role: {st.session_state.user['Role']})")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.sidebar.success("You have been logged out.")

    if choice == "User Management":
        show_user_management()
    elif choice == "Import Data":
        show_import_data()
    elif choice == "Form":
        show_form()
    elif choice == "Reports":
        show_reports()
    elif choice == "Charts":
        show_charts()
