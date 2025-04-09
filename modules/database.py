import streamlit as st
import psycopg2
import pandas as pd
from psycopg2.extras import RealDictCursor

def get_connection():
    config = st.secrets["postgres"]
    return psycopg2.connect(
        host=config["host"],
        database=config["database"],
        user=config["user"],
        password=config["password"],
        port=config["port"],
        sslmode=config["sslmode"]
    )

# Load all data from orders table
def load_data():
    try:
        conn = get_connection()
        query = "SELECT * FROM orders"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Failed to load data:\n\n{e}")
        return pd.DataFrame()

# Overwrite the entire orders table with a new DataFrame
def save_data(df):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orders")

        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO orders (date, company, operator, seal_type, profile, seal_count, production_time, downtime, downtime_reason)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row["date"],
                row["company"],
                row["operator"],
                row["seal_type"],
                row["profile"],
                row["seal_count"],
                row["production_time"],
                row["downtime"],
                row["downtime_reason"]
            ))

        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"❌ Failed to save data:\n\n{e}")

# Delete one order by DataFrame index
def delete_order(index):
    try:
        df = load_data()
        df = df.drop(index)
        save_data(df.reset_index(drop=True))
    except Exception as e:
        st.error(f"❌ Failed to delete order:\n\n{e}")

# Update one order by DataFrame index
def update_order(index, updated_order):
    try:
        df = load_data()
        for key in updated_order:
            df.at[index, key] = updated_order[key]
        save_data(df)
    except Exception as e:
        st.error(f"❌ Failed to update order:\n\n{e}")

