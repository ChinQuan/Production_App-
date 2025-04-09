import streamlit as st
import psycopg2
import pandas as pd
from psycopg2.extras import RealDictCursor

# 📥 Fetch orders data from the database
def get_orders_df():
    config = st.secrets["postgres"]

    try:
        conn = psycopg2.connect(
            host=config["host"],
            database=config["database"],
            user=config["user"],
            password=config["password"],
            port=config["port"],
            sslmode=config["sslmode"]
        )
        query = "SELECT * FROM orders"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Failed to load orders from database:\n\n{e}")
        return pd.DataFrame()

# 📤 Insert a new order into the database
def insert_order(order_data):
    config = st.secrets["postgres"]

    try:
        conn = psycopg2.connect(
            host=config["host"],
            database=config["database"],
            user=config["user"],
            password=config["password"],
            port=config["port"],
            sslmode=config["sslmode"]
        )
        cursor = conn.cursor()

        query = """
            INSERT INTO orders (date, company, operator, seal_type, seal_count, production_time)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            order_data["date"],
            order_data["company"],
            order_data["operator"],
            order_data["seal_type"],
            order_data["seal_count"],
            order_data["production_time"]
        )

        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"❌ Failed to insert order:\n\n{e}")
        return False
