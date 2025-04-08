import streamlit as st
st.set_page_config(page_title="Production Manager App", layout="wide")
import pandas as pd
from modules.user_management import authenticate_user, show_user_management
from modules.import_data import show_import_data
from modules.reports import show_reports
from modules.charts import show_charts
from modules.production_analysis import calculate_average_time
from modules.database import get_connection
from modules.form import show_form, show_home



def main():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.role = None

    if not st.session_state.authenticated:
        st.title("🔐 Login")

        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type="password")
        login_button = st.button("Login")

        if login_button:
            username, role, authenticated = authenticate_user(username_input, password_input)
            if authenticated:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.role = role
                st.experimental_rerun()
            else:
                st.error("❌ Authentication failed. Please try again.")
        return

    # User is authenticated
    username = st.session_state.username
    role = st.session_state.role

    st.sidebar.markdown(f"## 👤 Logged in as {role}: `{username}`")

    if st.sidebar.button("🚪 Logout"):
        for key in ["authenticated", "username", "role"]:
            if key in st.session_state:
                del st.session_state[key]
        st.experimental_rerun()

    menu = ["Add Order", "Reports", "Charts"]
    if role == "Admin":
        menu.extend(["User Management", "Edit Orders"])

    tab = st.sidebar.radio("📂 Navigation", menu)

    if tab == "Add Order":
        show_form()
        show_home()
    elif tab == "Reports":
        show_reports()
    elif tab == "Charts":
        show_charts()
        calculate_average_time()
    elif tab == "User Management" and role == "Admin":
        show_user_management(role)
    elif tab == "Edit Orders" and role == "Admin":
        show_edit_orders()

def show_edit_orders():
    st.title('📋 Edit Orders')

    conn = get_connection()
    df = pd.read_sql("SELECT * FROM orders", conn)
    conn.close()

    if df.empty:
        st.warning("No data available for editing.")
        return

    st.dataframe(df)

    selected_order_id = st.selectbox("Select Order ID to Delete", df['id'])

    if st.button("Delete Order"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orders WHERE id = %s", (selected_order_id,))
        conn.commit()
        conn.close()
        st.success("✅ Order deleted successfully.")
        st.experimental_rerun()

if __name__ == '__main__':
    main()
