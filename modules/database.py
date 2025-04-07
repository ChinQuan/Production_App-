import streamlit as st
import psycopg2
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        pass

    def get_connection(self):
        try:
            conn = psycopg2.connect(
                host=st.secrets['postgres']['host'],
                database=st.secrets['postgres']['database'],
                user=st.secrets['postgres']['user'],
                password=st.secrets['postgres']['password'],
                port=st.secrets['postgres']['port']
            )
            logger.info('Połączenie z bazą danych zostało nawiązane pomyślnie.')
            return conn
        except psycopg2.OperationalError as e:
            logger.error(f'Błąd operacyjny podczas łączenia się z bazą danych: {e}')
            st.error(f'Błąd operacyjny podczas łączenia się z bazą danych: {e}')
        except Exception as e:
            logger.error(f'Niespodziewany błąd podczas łączenia się z bazą danych: {e}')
            st.error(f'Niespodziewany błąd podczas łączenia się z bazą danych: {e}')
        return None

    def execute_query(self, query, params=()):
        conn = self.get_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    conn.commit()
                    result = cursor.fetchall()
                    return result
            except Exception as e:
                logger.error(f'Błąd podczas wykonywania zapytania: {e}')
            finally:
                conn.close()
