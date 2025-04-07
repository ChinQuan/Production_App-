import streamlit as st
from modules.database import get_connection

def show_form(tab_name):  # Dodano parametr tab_name, aby generować unikalne klucze
    st.sidebar.subheader("📋 Dodaj nowe zlecenie")

    conn = get_connection()
    cursor = conn.cursor()

    # Generowanie unikalnych kluczy na podstawie tab_name oraz unikalnych identyfikatorów
    date_key = f"{tab_name}_date_input_{id(st.session_state)}"
    company_key = f"{tab_name}_company_input_{id(st.session_state)}"
    operator_key = f"{tab_name}_operator_input_{id(st.session_state)}"
    seal_type_key = f"{tab_name}_seal_type_input_{id(st.session_state)}"
    profile_key = f"{tab_name}_profile_input_{id(st.session_state)}"
    seal_count_key = f"{tab_name}_seal_count_input_{id(st.session_state)}"
    production_time_key = f"{tab_name}_production_time_input_{id(st.session_state)}"
    downtime_key = f"{tab_name}_downtime_input_{id(st.session_state)}"
    downtime_reason_key = f"{tab_name}_downtime_reason_input_{id(st.session_state)}"
    submit_button_key = f"{tab_name}_submit_button_{id(st.session_state)}"

    date = st.sidebar.date_input("Data", key=date_key)
    company = st.sidebar.text_input("Firma", key=company_key)
    operator = st.sidebar.text_input("Operator", key=operator_key)
    seal_type = st.sidebar.text_input("Rodzaj uszczelki", key=seal_type_key)
    profile = st.sidebar.text_input("Profil", key=profile_key)
    seal_count = st.sidebar.number_input("Ilość uszczelek", min_value=1, step=1, key=seal_count_key)
    production_time = st.sidebar.number_input("Czas produkcji (h)", min_value=0.0, key=production_time_key)
    downtime = st.sidebar.number_input("Przestój (h)", min_value=0.0, key=downtime_key)
    downtime_reason = st.sidebar.text_input("Powód przestoju", key=downtime_reason_key)
    
    if st.sidebar.button("Dodaj zlecenie", key=submit_button_key):
        if company and operator and seal_type and profile and seal_count > 0:
            try:
                cursor.execute(
                    "INSERT INTO orders (date, company, operator, seal_type, profile, seal_count, production_time, downtime, downtime_reason) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (date, company, operator, seal_type, profile, seal_count, production_time, downtime, downtime_reason)
                )
                conn.commit()
                st.sidebar.success("✅ Zlecenie zostało pomyślnie dodane.")
            except Exception as e:
                st.sidebar.error(f"❌ Wystąpił błąd podczas dodawania zlecenia: {e}")
        else:
            st.sidebar.error("❌ Wszystkie pola muszą być wypełnione.")
    
    cursor.close()
    conn.close()
