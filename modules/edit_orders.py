import streamlit as st
import pandas as pd
from datetime import datetime
from modules.database import get_orders_df, update_order, delete_order

def show_edit_orders(df):
    st.header("📝 Edit Orders")

    if df.empty:
        st.warning("No orders available.")
        return

    # Display full table
    st.subheader("📋 Current Orders")
    st.dataframe(df)

    # Select row by index
    indices = df.index.tolist()
    selected_index = st.selectbox("Select Order Index", indices)

    selected_order = df.loc[selected_index]

    with st.form("edit_order_form"):
        # Safely parse the date
        raw_date = selected_order.get("date")
        try:
            parsed_date = pd.to_datetime(raw_date).date()
        except Exception:
            parsed_date = datetime.today().date()

        date = st.date_input("Date", value=parsed_date)
        company = st.text_input("Company", value=selected_order.get("company", ""))
        operator = st.text_input("Operator", value=selected_order.get("operator", ""))
        profile = st.text_input("Profile", value=selected_order.get("profile", ""))
        seal_type = st.text_input("Seal Type", value=selected_order.get("seal_type", ""))
        seal_count = st.number_input("Seal Count", value=int(selected_order.get("seal_count", 0)), min_value=0)
        production_time = st.number_input("Production Time (min)", value=float(selected_order.get("production_time", 0)), min_value=0.0)
        downtime = st.number_input("Downtime (min)", value=float(selected_order.get("downtime", 0)), min_value=0.0)
        downtime_reason = st.text_input("Downtime Reason", value=selected_order.get("downtime_reason", ""))

        submitted = st.form_submit_button("💾 Save Changes")
        delete = st.form_submit_button("🗑 Delete Order")

        if submitted:
            df.at[selected_index, "date"] = pd.to_datetime(date)
            df.at[selected_index, "company"] = company
            df.at[selected_index, "operator"] = operator
            df.at[selected_index, "profile"] = profile
            df.at[selected_index, "seal_type"] = seal_type
            df.at[selected_index, "seal_count"] = seal_count
            df.at[selected_index, "production_time"] = production_time
            df.at[selected_index, "downtime"] = downtime
            df.at[selected_index, "downtime_reason"] = downtime_reason

            save_data(df)
            st.success("Order updated successfully.")

        elif delete:
            df = df.drop(index=selected_index)
            save_data(df)
            st.success("Order deleted successfully.")
            st.experimental_rerun()

