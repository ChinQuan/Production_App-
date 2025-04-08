import streamlit as st
import pandas as pd
from modules.database import get_connection
from datetime import datetime

def show_form():
    st.title("➕ Dodaj nowe zlecenie")

    with st.form("form_add_order"):
        data = st.date_input("Data", value=datetime.today())
        firma = st.text_input("Firma")
        operator = st.text_input("Operator")
        rodzaj_uszczelki = st.text_input("Rodzaj uszczelki")
        profil = st.text_input("Profil")
        ilosc_uszczelek = st.number_input("Ilość uszczelek", min_value=1)
        czas_produkcji = st.number_input("Czas produkcji (minuty)", min_value=0)
        przestoj = st.number_input("Czas przestoju (minuty)", min_value=0)
        powod_przestoju = st.text_input("Powód przestoju", value="-")

        submitted = st.form_submit_button("Zapisz zlecenie")

        if submitted:
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO orders (data, firma, operator, rodzaj_uszczelki, profil, ilosc_uszczelek, czas_produkcji, przestoj, powod_przestoju)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (data, firma, operator, rodzaj_uszczelki, profil, ilosc_uszczelek, czas_produkcji, przestoj, powod_przestoju))
                conn.commit()
                cursor.close()
                conn.close()
                st.success("✅ Zlecenie zostało zapisane.")
            except Exception as e:
                st.error(f"❌ Błąd podczas zapisywania: {e}")

def show_home():
    st.title("📋 Lista zleceń")

    try:
        conn = get_connection()
        df = pd.read_sql("SELECT * FROM orders ORDER BY data DESC", conn)
        conn.close()

        if df.empty:
            st.info("Brak zleceń w bazie.")
        else:
            st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"❌ Błąd podczas ładowania danych: {e}")

