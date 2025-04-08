import streamlit as st
import psycopg2
import bcrypt

def get_connection():
    conn = psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        database=st.secrets["postgres"]["database"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"],
        port=st.secrets["postgres"]["port"]
    )
    return conn


def authenticate_user():
    st.sidebar.subheader("🔑 Logowanie")
    username = st.sidebar.text_input("Nazwa użytkownika")
    password = st.sidebar.text_input("Hasło", type="password")
    
    if st.sidebar.button("Zaloguj"):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT username, password FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()

            if result:
                db_username, hashed_password = result
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    return username, True
                else:
                    st.sidebar.error("❌ Nieprawidłowe hasło.")
            else:
                st.sidebar.error("❌ Użytkownik nie istnieje.")

            cursor.close()
            conn.close()
        except Exception as e:
            st.sidebar.error(f"❌ Wystąpił błąd podczas logowania: {e}")

    return None, False


def show_user_management():
    st.subheader("User Management")

    # Dodawanie nowego użytkownika
    st.sidebar.header("Add New User")
    new_username = st.sidebar.text_input("Nazwa użytkownika (nowy)")
    new_password = st.sidebar.text_input("Hasło (nowe)", type="password")

    if st.sidebar.button("Dodaj użytkownika"):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (new_username, hashed_password))
            conn.commit()

            st.sidebar.success(f"✅ Użytkownik {new_username} został dodany.")

            cursor.close()
            conn.close()
        except Exception as e:
            st.sidebar.error(f"❌ Wystąpił błąd podczas dodawania użytkownika: {e}")
