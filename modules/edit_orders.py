import streamlit as st
import pandas as pd
from modules.database import get_orders_df, update_order, delete_order
from datetime import datetime

def show_edit_orders(df):
    st.title("✏️ Edit or Delete Orders")

    if df.empty:
        st.warning("No orders available.")
        return

    df["date"] = pd.to_datetime(df["date"]).dt.date

    # ---------------------------
    # 🔍 Filters
    # ---------------------------
    st.sidebar.header("🔍 Filter Orders")
    unique_dates = sorted(df["date"].unique())
    selected_date = st.sidebar.selectbox("Select Date", ["All"] + [str(d) for d in unique_dates])
    selected_company = st.sidebar.selectbox("Select Company", ["All"] + sorted(df["company"].dropna().unique().tolist()))
    selected_operator = st.sidebar.selectbox("Select Operator", ["All"] + sorted(df["operator"].dropna().unique().tolist()))

    filtered_df = df.copy()
    if selected_date != "All":
        filtered_df = filtered_df[filtered_df["date"] == pd.to_datetime(selected_date).date()]
    if selected_company != "All":
        filtered_df = filtered_df[filtered_df["company"] == selected_company]
    if selected_operator != "All":
        filtered_df = filtered_df[filtered_df["operator"] == selected_operator]

    if filtered_df.empty:
        st.warning("No matching records found.")
        return

    st.subheader("📋 Filtered Orders")
    st.dataframe(filtered_df.drop(columns=["id"]), use_container_width=True)

    selected_index = st.selectbox("Select Row Index to Edit/Delete", filtered_df.index.tolist())

    try:
        selected_order = filtered_df.loc[selected_index]
        order_id = int(selected_order["id"])  # for updates and deletes
    except KeyError:
        st.error("Selected index not found.")
        return

    # ---------------------------
    # ✏️ Edit Form
    # ---------------------------
    with st.form("edit_order_form"):
        st.markdown("### 📝 Edit Selected Order")

        date = st.date_input("Date", value=selected_order["date"])
        company = st.text_input("Company", value=selected_order["company"])
        operator = st.text_input("Operator", value=selected_order["operator"])
        seal_type = st.text_input("Seal Type", value=selected_order["seal_type"])
        seal_count = st.number_input("Seal Count", value=int(selected_order["seal_count"]), step=1)
        production_time = st.text_input("Production Time", value=str(selected_order["production_time"]))

        submitted = st.form_submit_button("💾 Save Changes")
        if submitted:
            updated_order = {
                "date": date,
                "company": company,
                "operator": operator,
                "seal_type": seal_type,
                "seal_count": seal_count,
                "production_time": production_time
            }
            success = update_order(order_id, updated_order)
            if success:
                st.success("✅ Order updated successfully.")
            else:
                st.error("❌ Failed to update order.")

    # ---------------------------
    # 🗑️ Delete Button
    # ---------------------------
    st.markdown("---")
    st.markdown("### 🗑️ Delete This Order")
    if st.button("Delete Order"):
        confirm = st.checkbox("I confirm to delete this order permanently.")
        if confirm:
            deleted = delete_order(order_id)
            if deleted:
                st.success("✅ Order deleted successfully.")
            else:
                st.error("❌ Failed to delete order.")
