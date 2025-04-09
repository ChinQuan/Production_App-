import streamlit as st
import pandas as pd
from modules.database import load_data, update_order, delete_order
from datetime import datetime

def show_edit_orders(df):
    st.header("✏️ Edit Orders")

    if df.empty:
        st.warning("No orders available to edit.")
        return

    st.subheader("📋 All Orders")
    st.dataframe(df, use_container_width=True)

    index_options = df.index.tolist()
    selected_index = st.selectbox("Select Row Index to Edit", index_options)

    try:
        selected_order = df.loc[selected_index]
    except KeyError:
        st.error("Selected index not found.")
        return

    with st.form("edit_order_form"):
        date = st.date_input(
            "Date",
            value=pd.to_datetime(selected_order["date"]).date()
            if pd.notna(selected_order["date"])
            else datetime.today().date(),
        )
        company = st.text_input("Company", value=selected_order["company"])
        operator = st.text_input("Operator", value=selected_order["operator"])
        seal_type = st.text_input("Seal Type", value=selected_order["seal_type"])
        profile = st.text_input("Profile", value=selected_order["profile"])
        seal_count = st.number_input(
            "Seal Count", value=int(selected_order["seal_count"]), min_value=0
        )
        production_time = st.number_input(
            "Production Time (minutes)",
            value=float(selected_order["production_time"]),
            min_value=0.0,
        )
        downtime = st.number_input(
            "Downtime (minutes)",
            value=float(selected_order["downtime"]),
            min_value=0.0,
        )
        downtime_reason = st.text_input("Downtime Reason", value=selected_order["downtime_reason"])

        submitted = st.form_submit_button("Update Order")

        if submitted:
            update_order(
                order_id=selected_order["id"],
                date=date,
                company=company,
                operator=operator,
                seal_type=seal_type,
                profile=profile,
                seal_count=seal_count,
                production_time=production_time,
                downtime=downtime,
                downtime_reason=downtime_reason,
            )
            st.success("Order updated successfully!")

    if st.button("🗑 Delete This Order"):
        delete_order(selected_order["id"])
        st.success("Order deleted.")
