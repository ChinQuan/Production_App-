# modules/database.py

import streamlit as st
import psycopg2
import pandas as pd
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        database=st.secrets["postgres"]["database"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"],
        port=st.secrets["postgres"]["port"],
        sslmode=st.secrets["postgres"]["sslmode"]
    )

def get_users_df():
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM users;")
        rows = cursor.fetchall()
        return pd.DataFrame(rows)
    except Exception as e:
        st.error(f"❌ Error loading users: {e}")
        return pd.DataFrame()

def get_orders_df():
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM orders;")
        rows = cursor.fetchall()
        return pd.DataFrame(rows)
    except Exception as e:
        st.error(f"❌ Error loading orders: {e}")
        return pd.DataFrame()

