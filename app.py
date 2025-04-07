import streamlit as st
import bcrypt
from modules.user_management import show_user_management
from modules.import_data import show_import_data
from modules.form import show_form
from modules.reports import show_reports
from modules.charts import show_charts
from modules.database import execute_query
import psycopg2

# 🔑 Konfiguracja strony - MUSI być na samym początku!
st.set_page_config(page_title="Production Manager App", layout="wide")

# Niestandardowy styl CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 30px;
        font-weight: bold;
        color: #2E86C1;
    }
    .sidebar-title {
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 10px;
        color: #1ABC9C;
    }
    .sidebar-text {
        font-size: 16px;
        color: #34495E;
    }
    .stButton>button {
        background-color: #1ABC9C;
        color: white;
        border-radius: 10px;
    }
    .stButton>button:hover {
        background-color: #16A085;
    }
    </style>
""", unsafe_allow_html=True)

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

# ✅ Funkcja logowania - poprawiona do współpracy z bcrypt
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

menu = ["🏠 Home", "📄 Formularz", "📊 Raporty", "📈 Wykresy", "👥 Zarządzanie użytkownikami", "📥 Import danych"]
choice = st.sidebar.selectbox("📋 Wybierz menu", menu)

# 🌟 Interfejs logowania
if st.session_state.user is None:
    st.sidebar.markdown("<div class='sidebar-title'>🔑 Logowanie</div>", unsafe_allow_html=True)
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
    st.sidebar.markdown(f"<div class='sidebar-title'>✅ Zalogowany jako: {st.session_state.user['Username']} (Rola: {st.session_state.user['Role']})</div>", unsafe_allow_html=True)

    if st.sidebar.button("Wyloguj"):
        st.session_state.user = None
        st.sidebar.success("Zostałeś wylogowany.")

    st.markdown("<div class='main-header'>Production Manager App</div>", unsafe_allow_html=True)

    if choice == "👥 Zarządzanie użytkownikami":
        show_user_management()
    elif choice == "📥 Import danych":
        show_import_data()
    elif choice == "📄 Formularz":
        show_form()
    elif choice == "📊 Raporty":
        show_reports()
    elif choice == "📈 Wykresy":
        show_charts()
