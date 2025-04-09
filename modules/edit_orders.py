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

    if filtered_by_date.empty:
        st.warning("No orders on selected date.")
        return

    selected_operator = st.selectbox("Select Operator", filtered_by_date['operator'].unique())
    filtered_operator_df = filtered_by_date[filtered_by_date['operator'] == selected_operator]

    if filtered_operator_df.empty:
        st.warning("No orders for selected operator.")
        return

    order = filtered_operator_df.iloc[0]

    with st.form("edit_order_form"):
        st.write("Edit the fields below:")

        date = st.date_input("Date", value=order.get('date', pd.to_datetime('today')).date())
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
            st.write("🔁 Implement DB update logic here")
            st.json(updated_order)
