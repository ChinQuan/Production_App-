import streamlit as st
import psycopg2
import bcrypt

def get_connection():
    return psycopg2.connect(
        host=st.secrets['postgres']['host'],
        database=st.secrets['postgres']['database'],
        user=st.secrets['postgres']['user'],
        password=st.secrets['postgres']['password'],
        port=st.secrets['postgres']['port']
    )

def authenticate_user():
    st.sidebar.subheader('🔐 Logowanie')
    username = st.sidebar.text_input('Nazwa użytkownika')
    password = st.sidebar.text_input('Hasło', type='password')

    if st.sidebar.button('Zaloguj'):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT username, password, role FROM users WHERE username = %s', (username,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()

            if result:
                db_username, hashed_password, role = result
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    return username, role, True
                else:
                    st.sidebar.error("❌ Nieprawidłowe hasło.")
            else:
                st.sidebar.error("❌ Użytkownik nie istnieje.")
        except Exception as e:
            st.sidebar.error(f"❌ Błąd logowania: {e}")

        return None, None, False

    return None, None, False


def show_user_management(role):
    if role != 'Admin':
        st.error('❌ Brak uprawnień do zarządzania użytkownikami.')
        return

    st.subheader('👤 Zarządzanie użytkownikami')

    conn = get_connection()
    cursor = conn.cursor()

    # Wyświetlenie wszystkich użytkowników
    cursor.execute('SELECT username, role FROM users')
    users = cursor.fetchall()
    st.write('### Lista użytkowników')
    st.dataframe(users, use_container_width=True)

    # Dodawanie nowego użytkownika
    st.sidebar.header('Dodaj nowego użytkownika')
    new_username = st.sidebar.text_input('Nazwa użytkownika (nowy)')
    new_password = st.sidebar.text_input('Hasło (nowe)', type='password')
    new_role = st.sidebar.selectbox('Rola', ['Admin', 'Operator'])

    if st.sidebar.button('Dodaj użytkownika'):
        try:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute('INSERT INTO users (username, password, role) VALUES (%s, %s, %s)', (new_username, hashed_password, new_role))
            conn.commit()
            st.success(f'✅ Użytkownik {new_username} dodany pomyślnie!')
        except Exception as e:
            st.error(f'❌ Wystąpił błąd podczas dodawania użytkownika: {e}')

    cursor.close()
    conn.close()
