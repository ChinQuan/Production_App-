import streamlit as st
import bcrypt
from modules.user_management import show_user_management, authenticate_user
from modules.import_data import show_import_data
from modules.form import show_form
from modules.reports import show_reports
from modules.charts import show_charts
from modules.production_analysis import calculate_average_time  # Nowy moduł
from modules.database import execute_query, get_connection
import pandas as pd

st.set_page_config(page_title="Production Manager App", layout="wide")

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
    daily_average = df.groupby(df['date'].dt.date)['seal_count'].sum().mean()

    st.subheader("📈 Average Daily Production")
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

        tabs = st.tabs(["Home", "Formularz", "Raporty", "Wykresy", "Użytkownicy", "Import danych", "Analiza Produkcji"])

        with tabs[0]:
            show_home()
        with tabs[1]:
            show_form("form_tab")  
        with tabs[2]:
            show_reports()
        with tabs[3]:
            show_charts()
        with tabs[4]:
            show_user_management()
        with tabs[5]:
            show_import_data()
        with tabs[6]:
            calculate_average_time()


if __name__ == "__main__":
    main()
