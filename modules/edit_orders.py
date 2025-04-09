import streamlit as st
import pandas as pd

def show_edit_orders(df):
    st.title("✏️ Edit Orders")

    if df.empty:
        st.warning("No orders available to edit.")
        return

    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    st.subheader("🔍 Select Order to Edit")
    selected_date = st.selectbox("Select Date", df['date'].dt.date.unique())
    filtered_by_date = df[df['date'].dt.date == selected_date]

    selected_operator = st.selectbox("Select Operator", filtered_by_date['operator'].unique())
    order_to_edit = filtered_by_date[filtered_by_date['operator'] == selected_operator]

    if order_to_edit.empty:
        st.info("No order found for the selected criteria.")
        return

    order = order_to_edit.iloc[0]  # assuming one record per date + operator

    with st.form("edit_order_form"):
        st.write("Edit the fields below:")

        date = st.date_input("Date", value=order['date'].date())
        company = st.text_input("Company", value=order['company'])
        operator = st.text_input("Operator", value=order['operator'])
        seal_type = st.text_input("Seal Type", value=order['seal_type'])
        profile = st.text_input("Profile", value=order['profile'])
        seal_count = st.number_input("Seal Count", min_value=0, value=int(order['seal_count']))
        production_time = st.number_input("Production Time (min)", min_value=0.0, value=float(order['production_time']))
        downtime = st.number_input("Downtime (min)", min_value=0.0, value=float(order['downtime']))
        downtime_reason = st.text_input("Downtime Reason", value=order['downtime_reason'])

        submitted = st.form_submit_button("Save Changes")

        if submitted:
            # Tu powinieneś podmienić dane w bazie danych lub w CSV
            st.success("✅ Order updated successfully!")
            st.write("🔁 To save to a real database, implement update logic here.")

            # Pokazanie zmodyfikowanego zamówienia
            updated_order = {
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
            st.json(updated_order)
