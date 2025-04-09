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
            value=pd.to_datetime(selected_order.get("date", datetime.today())).date()
        )
        company = st.text_input("Company", value=selected_order.get("company", ""))
        operator = st.text_input("Operator", value=selected_order.get("operator", ""))
        profile = st.text_input("Profile", value=selected_order.get("profile", ""))
        product = st.text_input("Product", value=selected_order.get("product", ""))
        comments = st.text_area("Comments", value=selected_order.get("comments", ""))

        submitted = st.form_submit_button("Save Changes")
        if submitted:
            updated_order = {
                "date": date,
                "company": company,
                "operator": operator,
                "profile": profile,
                "product": product,
                "comments": comments,
            }
            update_order(selected_index, updated_order)
            st.success("Order updated successfully!")
