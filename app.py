
# app.py

import streamlit as st
import pandas as pd
from modules.user_management import authenticate_user, show_user_management
from modules.import_data import show_import_data
from modules.reports import show_reports
from modules.charts import show_charts
from modules.production_analysis import calculate_average_time
from modules.database import get_connection


def main():
    st.set_page_config(page_title="Production Manager App", layout="wide")

    # Logowanie użytkownika
    username, role, authenticated = authenticate_user()

    if not authenticated:
        st.warning("Proszę się zalogować.")
        return

    if role == 'Admin':
        st.sidebar.success(f"👑 Zalogowano jako Admin: {username}")
        show_user_management(role)
        show_import_data()
        show_reports()
        show_charts()
        calculate_average_time()
        show_edit_orders()

    elif role == 'Operator':
        st.sidebar.success(f"🔧 Zalogowano jako Operator: {username}")
        show_form()
        show_home()


def show_edit_orders():
    st.title('📋 Edycja zleceń')

    conn = get_connection()
    df = pd.read_sql("SELECT * FROM orders", conn)
    conn.close()

    if df.empty:
        st.warning("Brak danych do edycji.")
        return

    st.write("### Aktualne zlecenia")
    st.write(df)

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
