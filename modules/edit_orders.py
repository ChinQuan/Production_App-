import streamlit as st
import pandas as pd

def show_edit_orders(df):
    st.header("✏️ Edit Orders")

    if df.empty:
        st.warning("No data available for editing.")
        return

    # Show the full DataFrame
    st.subheader("📋 All Orders")
    st.dataframe(df)

    # Make sure the index is named for clarity
    df = df.reset_index(drop=False)

    # Select based on DataFrame index
    st.subheader("🔍 Select Order to Edit (by index)")
    selected_index = st.selectbox("Select DataFrame Index", df.index.tolist())

    selected_order = df.loc[selected_index]

    # Edit form
    with st.form("edit_order_form"):
        company = st.text_input("Company", value=selected_order["company"])
        operator = st.text_input("Operator", value=selected_order["operator"])
        seal_type = st.text_input("Seal Type", value=selected_order["seal_type"])
        profile = st.text_input("Profile", value=selected_order["profile"])
        seal_count = st.number_input("Seal Count", value=int(selected_order["seal_count"]))
        production_time = st.number_input("Production Time (minutes)", value=float(selected_order["production_time"]))
        downtime = st.number_input("Downtime (minutes)", value=float(selected_order["downtime"]))
        downtime_reason = st.text_input("Downtime Reason", value=selected_order["downtime_reason"])

        submitted = st.form_submit_button("💾 Save Changes")

        if submitted:
            df.at[selected_index, 'company'] = company
            df.at[selected_index, 'operator'] = operator
            df.at[selected_index, 'seal_type'] = seal_type
            df.at[selected_index, 'profile'] = profile
            df.at[selected_index, 'seal_count'] = seal_count
            df.at[selected_index, 'production_time'] = production_time
            df.at[selected_index, 'downtime'] = downtime
            df.at[selected_index, 'downtime_reason'] = downtime_reason

            st.success(f"✅ Order at index {selected_index} has been updated.")
