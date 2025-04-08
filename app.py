import streamlit as st
import psycopg2
import bcrypt
from modules.database import get_connection
from modules.user_management import authenticate_user, show_user_management

def main():
    # Logowanie
    username, role, authenticated = authenticate_user()
    if authenticated:
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.role = role
        
        # Tworzenie menu
        menu = ["Home", "Add Order", "Reports", "Charts", "User Management"]
        tab = st.sidebar.selectbox("Select a tab", menu)

        # Logika nawigacji
        if tab == "Home":
            st.title("Welcome to the Production Manager App!")
        elif tab == "Add Order":
            show_add_order()
        elif tab == "Reports":
            show_reports()
        elif tab == "Charts":
            show_charts()
        elif tab == "User Management" and role == "Admin":
            show_user_management(role)
        else:
            st.warning("You don't have permission to access this page.")
    else:
        st.warning("Please log in.")

def show_add_order():
    st.title("📦 Add New Order")
    
    # Formularz do dodawania nowego zlecenia
    company = st.text_input("Company")
    operator = st.text_input("Operator")
    seal_type = st.text_input("Seal Type")
    seal_count = st.number_input("Seal Count", min_value=0)
    production = st.number_input("Production", min_value=0)
    downtime = st.number_input("Downtime", min_value=0)

    if st.button("Add Order"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO orders (company, operator, seal_type, seal_count, production, downtime)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (company, operator, seal_type, seal_count, production, downtime))
        conn.commit()
        conn.close()
        st.success("✅ Order added successfully.")
        st.experimental_rerun()

def show_reports():
    st.title("📊 Reports")
    # Implementacja raportów
    st.write("Reports feature coming soon!")

def show_charts():
    st.title("📈 Charts")
    # Implementacja wykresów
    st.write("Charts feature coming soon!")

def show_orders():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, company, operator, seal_type, seal_count, production, downtime FROM orders")
    orders = cursor.fetchall()
    conn.close()

    st.subheader("📝 Orders Management")
    for order in orders:
        with st.expander(f"Edit Order {order[0]}"):
            new_company = st.text_input(f"Company for Order {order[0]}", value=order[1])
            new_operator = st.text_input(f"Operator for Order {order[0]}", value=order[2])
            new_seal_type = st.text_input(f"Seal Type for Order {order[0]}", value=order[3])
            new_seal_count = st.number_input(f"Seal Count for Order {order[0]}", value=order[4])
            new_production = st.number_input(f"Production for Order {order[0]}", value=order[5])
            new_downtime = st.number_input(f"Downtime for Order {order[0]}", value=order[6])

            if st.button(f"Save Changes for Order {order[0]}"):
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE orders 
                    SET company = %s, operator = %s, seal_type = %s, seal_count = %s, production = %s, downtime = %s
                    WHERE id = %s
                """, (new_company, new_operator, new_seal_type, new_seal_count, new_production, new_downtime, order[0]))
                conn.commit()
                conn.close()
                st.success(f"✅ Order {order[0]} updated successfully.")
                st.experimental_rerun()

def show_user_management(role):
    st.title("👥 User Management")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, role FROM users")
    users = cursor.fetchall()
    conn.close()

    st.subheader("📋 Existing Users")
    for user in users:
        st.write(f"👤 {user[0]} - {user[1]}")

    st.subheader("➕ Add New User")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    new_role = st.selectbox("Role", ["Admin", "Operator"])

    if st.button("Create User"):
        hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                       (new_username, hashed_password, new_role))
        conn.commit()
        conn.close()
        st.success("✅ User created successfully.")
        st.experimental_memo.clear()  # Clear any cached data and force refresh of components
        show_user_management(role)

    st.subheader("🗑️ Delete User")
    user_to_delete = st.text_input("Enter username to delete")
    if st.button("Delete"):
        if user_to_delete != "admin":
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE username = %s", (user_to_delete,))
            conn.commit()
            conn.close()
            st.success("✅ User deleted.")
            show_user_management(role)
        else:
            st.warning("⚠️ Cannot delete the main admin user.")

if __name__ == "__main__":
    main()
