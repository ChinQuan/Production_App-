import streamlit as st
from modules.database import get_connection

def show_form():
    st.sidebar.subheader("📋 Dodaj nowe zlecenie")

    conn = get_connection()
    cursor = conn.cursor()

    # Dodanie unikalnych kluczy do każdego komponentu, aby uniknąć błędu StreamlitDuplicateElementId
    date = st.sidebar.date_input("Data", key="date_input_form")
    company = st.sidebar.text_input("Firma", key="company_input_form")
    operator = st.sidebar.text_input("Operator", key="operator_input_form")
    seal_type = st.sidebar.text_input("Rodzaj uszczelki", key="seal_type_input_form")
    profile = st.sidebar.text_input("Profil", key="profile_input_form")
    seal_count = st.sidebar.number_input("Ilość uszczelek", min_value=1, step=1, key="seal_count_input_form")
    production_time = st.sidebar.number_input("Czas produkcji (h)", min_value=0.0, key="production_time_input_form")
    downtime = st.sidebar.number_input("Przestój (h)", min_value=0.0, key="downtime_input_form")
    downtime_reason = st.sidebar.text_input("Powód przestoju", key="downtime_reason_input_form")
    
    if st.sidebar.button("Dodaj zlecenie", key="submit_button_form"):
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
