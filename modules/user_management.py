import streamlit as st
import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        database=st.secrets["postgres"]["database"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"],
        port=st.secrets["postgres"]["port"]
    )
    return conn

def show_user_management():
    st.subheader("User Management")

    # Dodawanie nowego użytkownika
    st.sidebar.header("Add New User")
    new_username = st.sidebar.text_input("Username", key="new_username_input")
    new_password = st.sidebar.text_input("Password", type="password", key="new_password_input")
    new_role = st.sidebar.selectbox("Role", ["Admin", "Operator", "User"], key="new_role_select")

    if st.sidebar.button("Add User", key="add_user_button"):
        if new_username and new_password:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                (new_username, new_password, new_role)
            )
            conn.commit()
            conn.close()
            st.sidebar.success(f"User '{new_username}' added successfully!")
        else:
            st.sidebar.error("Provide a username and password.")

    # Wyświetlanie listy użytkowników
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()

    if users:
        st.write("### Users List")
        for user in users:
            st.write(f"Username: {user[1]}, Role: {user[3]}")
