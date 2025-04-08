import streamlit as st
from modules.database import get_connection

def show_form(tab_name):
    st.sidebar.subheader("📋 Dodaj nowe zlecenie")

    try:
        conn = get_connection()
        if conn is None:
            st.sidebar.error("❌ Błąd połączenia z bazą danych. Upewnij się, że konfiguracja jest poprawna.")
            return
        cursor = conn.cursor()
    except Exception as e:
        st.sidebar.error(f"❌ Wystąpił błąd podczas nawiązywania połączenia: {e}")
        return

    # Generowanie unikalnych kluczy na podstawie tab_name
    date_key = f"{tab_name}_date_input"
    company_key = f"{tab_name}_company_input"
    operator_key = f"{tab_name}_operator_input"
    seal_type_key = f"{tab_name}_seal_type_input"
    profile_key = f"{tab_name}_profile_input"
    seal_count_key = f"{tab_name}_seal_count_input"
    production_time_key = f"{tab_name}_production_time_input"
    downtime_key = f"{tab_name}_downtime_input"
    downtime_reason_key = f"{tab_name}_downtime_reason_input"
    submit_button_key = f"{tab_name}_submit_button"

    date = st.sidebar.date_input("Data", key=date_key)
    company = st.sidebar.text_input("Firma", key=company_key)
    operator = st.sidebar.text_input("Operator", key=operator_key)
    seal_type = st.sidebar.text_input("Rodzaj uszczelki", key=seal_type_key)
    profile = st.sidebar.text_input("Profil", key=profile_key)
    seal_count = st.sidebar.number_input("Ilość uszczelek", min_value=1, step=1, key=seal_count_key)
    
    # ⏳ Teraz wprowadzamy minuty zamiast godzin
    production_time = st.sidebar.number_input("Czas produkcji (minuty)", min_value=0, step=1, key=production_time_key)
    downtime = st.sidebar.number_input("Przestój (minuty)", min_value=0, step=1, key=downtime_key)
    downtime_reason = st.sidebar.text_input("Powód przestoju", key=downtime_reason_key)

    if st.sidebar.button("Dodaj zlecenie", key=submit_button_key):
        if company and operator and seal_type and profile and seal_count > 0:
            try:
                # Konwersja minut na godziny do zapisu w bazie danych
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
