import streamlit as st
import pandas as pd
from modules.database import get_orders_df, update_order, delete_order
from datetime import datetime

def show_edit_orders(df):
    st.header("✏️ Edit Orders")

    if df.empty:
        st.warning("No orders available to edit.")
        return

    st.subheader("📋 All Orders")
    st.dataframe(df.drop(columns=["id"]), use_container_width=True)

    index_options = df.index.tolist()
    selected_index = st.selectbox("Select Row Index to Edit", index_options)

    try:
        selected_order = df.loc[selected_index]
        order_id = int(selected_order["id"])  # używamy ID do aktualizacji/usuwania
    except KeyError:
        st.error("Selected index not found.")
        return

    with st.form("edit_order_form"):
        date = st.date_input(
            "Date",
            value=pd.to_datetime(selected_order.get("date", datetime.today())).date()
        )
        company = st.text_input("Company", value=selected_order.get("company", ""))
        operator = st.text_input("Operator", value=selected_order.get("operator", ""))
        seal_type = st.text_input("Seal Type", value=selected_order.get("seal_type", ""))
        seal_count = st.number_input("Seal Count", value=selected_order.get("seal_count", 0), step=1)
        production_time = st.text_input("Production Time", value=selected_order.get("production_time", ""))

        submitted = st.form_submit_button("Save Changes")
        if submitted:
            updated_order = {
                "date": date,
                "company": company,
                "operator": operator,
                "seal_type": seal_type,
                "seal_count": seal_count,
                "production_time": production_time,
            }
            try:
                update_order(order_id, updated_order)
                st.success("Order updated successfully!")
            except Exception as e:
                st.error(f"❌ Failed to update order:\n{e}")

    st.markdown("---")
    if st.button("🗑️ Delete This Order"):
        try:
            delete_order(order_id)
            st.success("Order deleted successfully!")
        except Exception as e:
            st.error(f"❌ Failed to delete order:\n{e}")
