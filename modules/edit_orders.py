import streamlit as st
import pandas as pd

def show_edit_orders(df):
    st.header("✏️ Edit Orders")

    if df.empty:
        st.warning("No data available for editing.")
        return

    # Display the full orders table
    st.subheader("📋 All Orders")
    st.dataframe(df)

    # Check if 'id' column exists
    if 'id' not in df.columns:
        st.error("The 'id' column was not found in the data.")
        return

    # Select an order by ID
    st.subheader("🔍 Select Order to Edit")
    selected_id = st.selectbox("Select Order ID", df['id'].tolist())

    selected_order = df[df['id'] == selected_id]

    if selected_order.empty:
        st.warning("No order found for the selected ID.")
        return

    order = selected_order.iloc[0]

    # Edit form
    with st.form("edit_order_form"):
        company = st.text_input("Company", value=order["company"])
        operator = st.text_input("Operator", value=order["operator"])
        seal_type = st.text_input("Seal Type", value=order["seal_type"])
        profile = st.text_input("Profile", value=order["profile"])
        seal_count = st.number_input("Seal Count", value=int(order["seal_count"]))
        production_time = st.number_input("Production Time (minutes)", value=float(order["production_time"]))
        downtime = st.number_input("Downtime (minutes)", value=float(order["downtime"]))
        downtime_reason = st.text_input("Downtime Reason", value=order["downtime_reason"])

        submitted = st.form_submit_button("💾 Save Changes")

        if submitted:
            df.loc[df['id'] == selected_id, 'company'] = company
            df.loc[df['id'] == selected_id, 'operator'] = operator
            df.loc[df['id'] == selected_id, 'seal_type'] = seal_type
            df.loc[df['id'] == selected_id, 'profile'] = profile
            df.loc[df['id'] == selected_id, 'seal_count'] = seal_count
            df.loc[df['id'] == selected_id, 'production_time'] = production_time
            df.loc[df['id'] == selected_id, 'downtime'] = downtime
            df.loc[df['id'] == selected_id, 'downtime_reason'] = downtime_reason

            st.success(f"✅ Order with ID {selected_id} has been updated.")
