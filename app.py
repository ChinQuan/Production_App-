import streamlit as st  # Musi być pierwsze

st.set_page_config(page_title="Production Manager App", layout="wide")  # Musi być zaraz po imporcie

# Następnie importujesz swoje moduły
from modules.user_management import show_user_management
from modules.import_data import show_import_data
from modules.form import show_form
from modules.reports import show_reports
from modules.charts import show_charts
from modules.admin_management import show_admin_creation


if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.user_role = None

menu = ["Home", "Form", "Reports", "Charts", "User Management", "Import Data", "Admin Panel"]
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
        if user:
            st.session_state.user = user[0]
            st.session_state.user_role = user[2]  # Zakładamy, że rola jest na trzeciej pozycji
            st.success(f"✅ Witaj, {username}!")
        else:
            st.error("❌ Niepoprawne dane logowania.")
        conn.close()

if st.session_state.user:
    if choice == "Home":
        st.title("🏠 Strona główna")
        st.write("Witaj w aplikacji Production Manager App!")
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
    elif choice == "Admin Panel":
        if st.session_state.user_role == 'Admin':
            show_admin_creation()
        else:
            st.error("🚫 Tylko administratorzy mają dostęp do tego panelu!")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.user_role = None
        st.experimental_rerun()
