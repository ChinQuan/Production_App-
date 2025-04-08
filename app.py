# app.py

import streamlit as st
st.set_page_config(page_title="Production Manager App", layout="wide")
import pandas as pd
from modules.user_management import authenticate_user, show_user_management
from modules.import_data import show_import_data
from modules.reports import show_reports
from modules.charts import show_charts
from modules.production_analysis import calculate_average_time
from modules.database import get_connection



def main():
    username, role, authenticated = authenticate_user()

    if username is None or role is None:
        st.error("❌ Błąd uwierzytelniania: brak danych użytkownika.")
        return

    if not authenticated:
        st.warning("Proszę się zalogować.")
        return

    st.sidebar.markdown(f"## 👤 Zalogowano jako {role}: `{username}`")
    menu = ["Dodaj zlecenie", "Raporty", "Wykresy"]
    if role == "Admin":
        menu.append("Zarządzanie użytkownikami")
        menu.append("Edycja zleceń")

    tab = st.sidebar.radio("📂 Nawigacja", menu)

    if tab == "Dodaj zlecenie":
        show_form()
        show_home()

    elif tab == "Raporty":
        show_reports()

    elif tab == "Wykresy":
        show_charts()
        calculate_average_time()

    elif tab == "Zarządzanie użytkownikami" and role == "Admin":
        show_user_management(role)

    elif tab == "Edycja zleceń" and role == "Admin":
        show_edit_orders()

def show_edit_orders():
    st.title('📋 Edycja zleceń')

    conn = get_connection()
    df = pd.read_sql("SELECT * FROM orders", conn)
    conn.close()

    if df.empty:
        st.warning("Brak danych do edycji.")
        return

    st.dataframe(df)

    selected_order_id = st.selectbox("Wybierz ID zlecenia do edycji", df['id'])

    if st.button("Usuń zlecenie"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orders WHERE id = %s", (selected_order_id,))
        conn.commit()
        conn.close()
        st.success("✅ Zlecenie zostało usunięte.")
        st.experimental_rerun()

if __name__ == '__main__':
    main()
