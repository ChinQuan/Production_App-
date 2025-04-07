# Updated Production Manager Application Code

# 1. Wprowadzenie lepszego bezpieczeństwa w module 'database.py'.
# 2. Optymalizacja wydajności w modułach 'charts.py' i 'import_data.py'.
# 3. Uspójnienie logowania w całej aplikacji.
# 4. Ulepszenie walidacji i responsywności formularzy w 'form.py'.
# 5. Dodanie funkcjonalności eksportu raportów do różnych formatów.


import logging
import logging.config
import pandas as pd
import streamlit as st
import psycopg2

# Konfiguracja logowania
logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


# Wprowadzenie jednolitego systemu logowania w całej aplikacji

class LogManager:
    @staticmethod
    def get_logger(name: str):
        return logging.getLogger(name)


# Przykład użycia w różnych modułach
logger = LogManager.get_logger('database')
logger.info('Logowanie z modułu database działa poprawnie.')


# Zaktualizowany moduł 'database.py'

def get_connection():
    try:
        conn = psycopg2.connect(
            host=st.secrets["postgres"]["host"],
            database=st.secrets["postgres"]["database"],
            user=st.secrets["postgres"]["user"],
            password=st.secrets["postgres"]["password"],
            port=st.secrets["postgres"]["port"]
        )
        logger.info("Połączenie z bazą danych zostało nawiązane pomyślnie.")
        return conn
    except psycopg2.OperationalError as e:
        logger.error(f"Błąd operacyjny podczas łączenia się z bazą danych: {e}")
        st.error(f"Błąd operacyjny podczas łączenia się z bazą danych: {e}")
    except Exception as e:
        logger.error(f"Niespodziewany błąd podczas łączenia się z bazą danych: {e}")
        st.error(f"Niespodziewany błąd podczas łączenia się z bazą danych: {e}")
    return None


# Wprowadzone zmiany:
# - Dodanie szczegółowego logowania błędów.
# - Wyświetlanie komunikatów błędów w interfejsie Streamlit.
# - Poprawiona obsługa wyjątków dla dokładniejszej diagnostyki problemów.


# Kontynuować z testowaniem aplikacji na Streamlit Cloud.
