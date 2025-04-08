import streamlit as st

# 🔑 Page configuration - MUST be the very first Streamlit command!
st.set_page_config(page_title="Production Manager App", layout="wide")

import bcrypt
from modules.user_management import show_user_management
from modules.import_data import show_import_data
from modules.form import show_form
from modules.reports import show_reports
from modules.charts import show_charts
from modules.database import execute_query
import psycopg2


# ✅ Funkcja do nawiązywania połączenia z bazą danych
def get_connection():
    return psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        database=st.secrets["postgres"]["database"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"],
        port=st.secrets["postgres"]["port"],
        sslmode=st.secrets["postgres"]["sslmode"]
    )

# ✅ Funkcja logowania
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
        st.error(f"Błąd połączenia z bazą danych: {e}")
        return None

# Inicjalizacja stanu sesji
if 'user' not in st.session_state:
    st.session_state.user = None

# 🌟 Interfejs logowania
if st.session_state.user is None:
    st.sidebar.title("🔑 Logowanie")
    username = st.sidebar.text_input("Nazwa użytkownika", key="login_username")
    password = st.sidebar.text_input("Hasło", type="password", key="login_password")

    if st.sidebar.button("Zaloguj"):
        user = login(username, password)
        if user:
            st.session_state.user = user
            st.sidebar.success(f"✅ Zalogowano jako: {user['Username']} (Rola: {user['Role']})")
        else:
            st.sidebar.error("❌ Niepoprawna nazwa użytkownika lub hasło.")
else:
    st.sidebar.write(f"✅ Zalogowany jako: {st.session_state.user['Username']} (Rola: {st.session_state.user['Role']})")

    if st.sidebar.button("Wyloguj"):
        st.session_state.user = None
        st.sidebar.success("Zostałeś wylogowany.")

    # 📌 Użycie zakładek zamiast selectbox
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Home", "Formularz", "Raporty", "Wykresy", "Zarządzanie użytkownikami"])

    with tab1:
        st.header("📋 Home")
        show_form()  # Wyświetla formularz po lewej i listę zleceń po środku

    with tab2:
        st.header("📑 Formularz")
        show_form()

    with tab3:
        st.header("📊 Raporty")
        show_reports()

    with tab4:
        st.header("📈 Wykresy")
        show_charts()

    with tab5:
        st.header("👥 Zarządzanie użytkownikami")
        show_user_management()
