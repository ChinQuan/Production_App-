import streamlit as st
import pandas as pd
import bcrypt
from modules.user_management import show_user_management
from modules.import_data import show_import_data
from modules.database import execute_query
import psycopg2
from datetime import datetime, timedelta

# 🔑 Page configuration
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

# ✅ Login function
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

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None

tabs = st.tabs(["Home", "Production Statistics", "User Management", "Import Data"])

with tabs[0]:  # Home
    st.header("📋 Home")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Dodaj nowe zlecenie")
        task = st.text_input("Nazwa zadania")
        date = st.date_input("Data dodania")
        amount = st.number_input("Ilość uszczelek", min_value=0)
        
        if st.button("Dodaj zlecenie"):
            if task and amount > 0:
                # Save task to database
                execute_query("INSERT INTO orders (task_name, date, amount) VALUES (%s, %s, %s)", (task, date, amount))
                st.success("✅ Zlecenie zostało dodane.")
            else:
                st.error("❌ Wprowadź poprawne dane.")

    with col2:
        st.subheader("Lista zleceń")
        query = "SELECT task_name, date, amount FROM orders ORDER BY date DESC"
        orders = execute_query(query, fetch=True)
        
        if orders:
            df = pd.DataFrame(orders, columns=["Nazwa zadania", "Data", "Ilość uszczelek"])
            st.dataframe(df, use_container_width=True)
        else:
            st.write("Brak zleceń do wyświetlenia.")

with tabs[1]:  # Production Statistics
    st.header("📊 Production Statistics")
    st.write("Średnia dzienna ilość uszczelek (tylko dni robocze)")

    query = "SELECT date, amount FROM orders"
    orders = execute_query(query, fetch=True)
    
    if orders:
        df = pd.DataFrame(orders, columns=["Date", "Amount"])
        
        # Filtrujemy tylko dni robocze (poniedziałek - piątek)
        df["Date"] = pd.to_datetime(df["Date"])
        df = df[df["Date"].dt.weekday < 5]
        
        # Obliczamy liczbę dni roboczych
        working_days = len(df["Date"].unique())
        
        if working_days > 0:
            # Obliczamy średnią ilość uszczelek na dzień roboczy
            average_daily = df["Amount"].sum() / working_days
            st.metric(label="Średnia dzienna ilość uszczelek", value=round(average_daily, 2))
        else:
            st.write("Brak danych dla dni roboczych.")
    else:
        st.write("Brak danych o produkcji.")

with tabs[2]:  # User Management
    st.header("👥 Zarządzanie użytkownikami")
    show_user_management()

with tabs[3]:  # Import Data
    st.header("📥 Import danych")
    show_import_data()
