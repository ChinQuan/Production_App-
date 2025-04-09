import streamlit as st
import pandas as pd

def show_edit_orders(df):
    st.title("✏️ Edit Orders")

    if df.empty:
        st.warning("No orders available.")
        return

    # Wyświetl ramkę z wszystkimi zleceniami
    st.subheader("📋 All Orders")
    st.dataframe(df)

    # Wybór zlecenia po ID
    st.subheader("🔍 Select Order by ID")
    selected_id = st.selectbox("Select Order ID", df['id'].unique())

    # Znajdź rekord
    order = df[df['id'] == selected_id].iloc[0]

    with st.form("edit_order_form"):
        st.write(f"📝 Editing Order ID: {selected_id}")

        date = st.date_input("Date", value=pd.to_datetime(order.get('date')))
        company = st.text_input("Company", value=order.get('company', ''))
        operator = st.text_input("Operator", value=order.get('operator', ''))
        seal_type = st.text_input("Seal Type", value=order.get('seal_type', ''))
        profile = st.text_input("Profile", value=order.get('profile', ''))
        seal_count = st.number_input("Seal Count", min_value=0, value=int(order.get('seal_count', 0)))
        production_time = st.number_input("Production Time (min)", min_value=0.0, value=float(order.get('production_time', 0.0)))
        downtime = st.number_input("Downtime (min)", min_value=0.0, value=float(order.get('downtime', 0.0)))
        downtime_reason = st.text_input("Downtime Reason", value=order.get('downtime_reason', ''))

        submitted = st.form_submit_button("Save Changes")

        if submitted:
            updated_order = {
                "id": selected_id,
                "date": date,
                "company": company,
                "operator": operator,
                "seal_type": seal_type,
                "profile": profile,
                "seal_count": seal_count,
                "production_time": production_time,
                "downtime": downtime,
                "downtime_reason": downtime_reason,
            }

            st.success("✅ Order updated successfully!")
            st.write("🛠 Now update the database or file with this data:")
            st.json(updated_order)

