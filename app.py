import streamlit as st

# Ustawienie konfiguracji strony MUSI być pierwszą komendą Streamlit
st.set_page_config(page_title="Production Manager App", layout="wide")

import bcrypt
from modules.user_management import show_user_management, authenticate_user
from modules.import_data import show_import_data
from modules.reports import show_reports
from modules.charts import show_charts
from modules.production_analysis import calculate_average_time  # Nowy moduł
from modules.database import execute_query, get_connection
import pandas as pd

def show_form():
    st.sidebar.subheader("📋 Dodaj nowe zlecenie")

    conn = get_connection()
    cursor = conn.cursor()

    date = st.sidebar.date_input("Data")
    company = st.sidebar.text_input("Firma")
    operator = st.sidebar.text_input("Operator")
    seal_type = st.sidebar.text_input("Rodzaj uszczelki")
    profile = st.sidebar.text_input("Profil")
    seal_count = st.sidebar.number_input("Ilość uszczelek", min_value=1, step=1)
    production_time = st.sidebar.number_input("Czas produkcji (minuty)", min_value=0, step=1)
    downtime = st.sidebar.number_input("Przestój (minuty)", min_value=0, step=1)
    downtime_reason = st.sidebar.text_input("Powód przestoju")

    if st.sidebar.button("Dodaj zlecenie"):
        if company and operator and seal_type and profile and seal_count > 0:
            try:
                production_time_hours = production_time / 60
                downtime_hours = downtime / 60

                cursor.execute(
                    "INSERT INTO orders (date, company, operator, seal_type, profile, seal_count, production_time, downtime, downtime_reason) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (date, company, operator, seal_type, profile, seal_count, production_time_hours, downtime_hours, downtime_reason)
                )
                conn.commit()
                st.sidebar.success("✅ Zlecenie zostało pomyślnie dodane.")
            except Exception as e:
                st.sidebar.error(f"❌ Wystąpił błąd podczas dodawania zlecenia: {e}")
        else:
            st.sidebar.error("❌ Wszystkie pola muszą być wypełnione.")

    cursor.close()
    conn.close()

def show_home():
    st.title("🏠 Home")
    conn = get_connection()
    if conn is None:
        st.error("Database connection failed. Contact administrator.")
        return

    df = pd.read_sql("SELECT * FROM orders", conn)
    conn.close()

    if df.empty:
        st.warning("No data available to display.")
        return

    st.subheader("All Orders")
    st.dataframe(df)

    df['date'] = pd.to_datetime(df['date'])
    working_days_df = df[df['date'].dt.dayofweek < 5]
    daily_average = working_days_df.groupby(working_days_df['date'].dt.date)['seal_count'].sum().mean()

    st.subheader("📈 Average Daily Production (Weekdays Only)")
    st.metric(label="Average Daily Production", value=f"{daily_average:.2f} seals/day")

def main():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None

    if not st.session_state.authenticated:
        username, authenticated = authenticate_user()
        if authenticated:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.sidebar.success("✅ Zalogowano pomyślnie.")
        else:
            st.sidebar.error("❌ Błędne dane logowania. Spróbuj ponownie.")
    else:
        st.sidebar.success(f"✅ Zalogowany jako: {st.session_state.username}")

        show_form()  # Formularz jest dostępny na każdej stronie w pasku bocznym

        tabs = st.tabs(["Home", "Raporty", "Wykresy", "Użytkownicy", "Import danych", "Analiza Produkcji"])

        with tabs[0]:
            show_home()
        with tabs[1]:
            show_reports()
        with tabs[2]:
            show_charts()
        with tabs[3]:
            show_user_management()
        with tabs[4]:
            show_import_data()
        with tabs[5]:
            calculate_average_time()


if __name__ == "__main__":
    main()
