import streamlit as st
from modules.user_management import show_user_management
from modules.import_data import show_import_data
from modules.form import show_form
from modules.reports import show_reports
from modules.charts import show_charts

# Ustawienia aplikacji
st.set_page_config(page_title="Production Manager App", layout="wide")

if 'user' not in st.session_state:
    st.session_state.user = None

menu = ["Home", "Form", "Reports", "Charts", "User Management", "Import Data"]
choice = st.sidebar.selectbox("Select Menu", menu)

if st.session_state.user is None:
    st.sidebar.title("🔑 Login")
    username = st.sidebar.text_input("Username", key="login_username")
    password = st.sidebar.text_input("Password", type="password", key="login_password")

    if st.sidebar.button("Login"):
        from modules.database import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s",
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()
        
        if user:
            st.session_state.user = {"Username": user[1], "Role": user[3]}
            st.sidebar.success(f"Logged in as {user[1]} with role {user[3]}")
        else:
            st.sidebar.error("Invalid username or password")

else:
    st.sidebar.write(f"✅ Logged in as {st.session_state.user['Username']} ({st.session_state.user['Role']})")
    
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.experimental_rerun()
    
    if choice == "Home":
        st.title("🏠 Production Manager App - Home")
    
    elif choice == "Form":
        show_form()

    elif choice == "Reports":
        show_reports()

    elif choice == "Charts":
        show_charts()

    elif choice == "User Management":
        show_user_management()
    
    elif choice == "Import Data":
        show_import_data()
