import bcrypt

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
