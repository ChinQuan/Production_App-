import streamlit as st
from modules.database import get_connection

def show_form(tab_name):  # Dodano parametr tab_name, aby generować unikalne klucze
    st.sidebar.subheader("📋 Dodaj nowe zlecenie")

    conn = get_connection()
    cursor = conn.cursor()

    # Generowanie unikalnych kluczy na podstawie nazwy zakładki
    date = st.sidebar.date_input("Data", key=f"{tab_name}_date_input")
    company = st.sidebar.text_input("Firma", key=f"{tab_name}_company_input")
    operator = st.sidebar.text_input("Operator", key=f"{tab_name}_operator_input")
    seal_type = st.sidebar.text_input("Rodzaj uszczelki", key=f"{tab_name}_seal_type_input")
    profile = st.sidebar.text_input("Profil", key=f"{tab_name}_profile_input")
    seal_count = st.sidebar.number_input("Ilość uszczelek", min_value=1, step=1, key=f"{tab_name}_seal_count_input")
    production_time = st.sidebar.number_input("Czas produkcji (h)", min_value=0.0, key=f"{tab_name}_production_time_input")
    downtime = st.sidebar.number_input("Przestój (h)", min_value=0.0, key=f"{tab_name}_downtime_input")
    downtime_reason = st.sidebar.text_input("Powód przestoju", key=f"{tab_name}_downtime_reason_input")
    
    if st.sidebar.button("Dodaj zlecenie", key=f"{tab_name}_submit_button"):
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
