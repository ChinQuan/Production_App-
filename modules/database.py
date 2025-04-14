import streamlit as st
import psycopg2
import pandas as pd
from psycopg2.extras import RealDictCursor
import bcrypt

# 📥 Fetch orders data from the database
def get_orders_df():
    config = st.secrets["postgres"]

    try:
        conn = psycopg2.connect(**config)
        query = """
            SELECT id, date, company, operator, seal_type, seal_count, production_time
            FROM orders
            ORDER BY id
        """
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
        conn = psycopg2.connect(**config)
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

# ✏️ Update an existing order
def update_order(order_id, updated_data):
    config = st.secrets["postgres"]

    try:
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()

        query = """
            UPDATE orders
            SET date = %s,
                company = %s,
                operator = %s,
                seal_type = %s,
                seal_count = %s,
                production_time = %s
            WHERE id = %s
        """
        values = (
            updated_data["date"],
            updated_data["company"],
            updated_data["operator"],
            updated_data["seal_type"],
            updated_data["seal_count"],
            updated_data["production_time"],
            order_id
        )

        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"❌ Failed to update order:\n\n{e}")
        return False

# ❌ Delete an order by ID
def delete_order(order_id):
    config = st.secrets["postgres"]

    try:
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()

        query = "DELETE FROM orders WHERE id = %s"
        cursor.execute(query, (order_id,))
        conn.commit()

        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"❌ Failed to delete order:\n\n{e}")
        return False

# 🔐 Get user details by username
def get_user_by_username(username):
    config = st.secrets["postgres"]

    try:
        conn = psycopg2.connect(**config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    except Exception as e:
        st.error(f"❌ Failed to fetch user:\n\n{e}")
        return None

# 👥 Get all users
def get_all_users():
    config = st.secrets["postgres"]
    try:
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role FROM users ORDER BY id")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users
    except Exception as e:
        st.error(f"❌ Failed to fetch users:\n\n{e}")
        return []

# 🔄 Update a user
def update_user(user_id, new_role, new_password=None):
    config = st.secrets["postgres"]
    try:
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        if new_password:
            hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            cursor.execute("UPDATE users SET role = %s, password = %s WHERE id = %s", (new_role, hashed_pw, user_id))
        else:
            cursor.execute("UPDATE users SET role = %s WHERE id = %s", (new_role, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"❌ Failed to update user:\n\n{e}")
        return False

# 🗑️ Delete a user
def delete_user(user_id):
    config = st.secrets["postgres"]
    try:
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"❌ Failed to delete user:\n\n{e}")
        return False

# ➕ Create a new user
def create_user(username, password, role):
    config = st.secrets["postgres"]
    try:
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, hashed_pw, role))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"❌ Failed to create user:\n\n{e}")
        return False
