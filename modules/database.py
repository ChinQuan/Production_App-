
import psycopg2
import streamlit as st
import logging

def get_connection():
    try:
        conn = psycopg2.connect(
            host=st.secrets["postgres"]["host"],
            database=st.secrets["postgres"]["database"],
            user=st.secrets["postgres"]["user"],
            password=st.secrets["postgres"]["password"],
            port=st.secrets["postgres"]["port"]
        )
        return conn
    except psycopg2.Error as e:
        logging.error(f"Database connection error: {e}")
        st.error("Database connection failed. Contact administrator.")
        return None

def execute_query(query, params=None, fetch=False):
    conn = get_connection()
    if conn is None:
        return None
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if fetch:
                    return cursor.fetchall()
    except psycopg2.Error as e:
        logging.error(f"Query execution error: {e}")
        st.error("An error occurred during database operation. Contact administrator.")
