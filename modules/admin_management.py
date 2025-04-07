import streamlit as st
import psycopg2

# Funkcja połączenia z bazą danych PostgreSQL
def get_connection():
    conn = psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        database=st.secrets["postgres"]["database"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"],
        port=st.secrets["postgres"]["port"]
    )
    return conn

# Funkcja do dodawania nowego admina
def add_admin(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
        (username, password, 'Admin')
    )
    conn.commit()
    conn.close()
    st.success(f"✅ Admin {username} dodany pomyślnie!")

# Wyświetlenie interfejsu do tworzenia admina
def show_admin_creation():
    st.title("Admin Management")

    st.sidebar.header("Add New Admin")
    new_username = st.sidebar.text_input("Username")
    new_password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Add Admin"):
        if new_username and new_password:
            add_admin(new_username, new_password)
        else:
            st.error("❌ Wprowadź nazwę użytkownika i hasło")
