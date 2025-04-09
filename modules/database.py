# modules/database.py
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st

def get_connection():
    creds = st.secrets["postgres"]
    return psycopg2.connect(
        host=creds["host"],
        database=creds["database"],
        user=creds["user"],
        password=creds["password"],
        port=creds["port"],
        sslmode=creds["sslmode"]
    )

def get_orders_df():
    try:
        conn = get_connection()
        query = """
            SELECT id, date AS "Date", company AS "Company", operator AS "Operator",
                   seal_type AS "Seal Type", seal_profile AS "Seal Profile",
                   seal_count AS "Seal Count", production_time AS "Production Time",
                   downtime AS "Downtime", downtime_reason AS "Downtime Reason"
            FROM orders
            ORDER BY id;
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Failed to fetch orders: {e}")
        return pd.DataFrame()

def insert_order(data):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO orders (date, company, operator, seal_type, seal_profile,
                               seal_count, production_time, downtime, downtime_reason)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(query, (
            data["date"],
            data["company"],
            data["operator"],
            data["seal_type"],
            data["seal_profile"],
            data["seal_count"],
            data["production_time"],
            data["downtime"],
            data["downtime_reason"]
        ))
        conn.commit()
        cursor.close()
        conn.close()
        st.success("✅ Order saved to database.")
    except Exception as e:
        st.error(f"❌ Failed to insert order: {e}")

def get_users():
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT username, password, role FROM users;")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users
    except Exception as e:
        st.error(f"❌ Failed to fetch users: {e}")
        return []
