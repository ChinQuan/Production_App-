import streamlit as st
import pandas as pd

def show_edit_orders(df):
    st.header("✏️ Edit Orders")

    if df.empty:
        st.warning("No data available for editing.")
        return

    # Display all orders
    st.subheader("📋 All Orders")
    st.dataframe(df)

    # Reset index for selection
    df = df.reset_index(drop=True)

    # Select by index
    st.subheader("🔍 Select Order to Edit or Delete")
    selected_index = st.selectbox("Select order by index", df.index.tolist())

    try:
        selected_order = df.loc[selected_index]
    except KeyError:
        st.error(f"Invalid index selected: {selected_index}")
        return

    # Convert date column to datetime if not already
    if not pd.api.types.is_datetime64_any_dtype(df["date"]):
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Edit form
    with st.form("edit_order_form"):
        date = st.date_input("Date", value=selected_order["date"].date() if pd.notna(selected_order["date"]) else pd.to_datetime("today").date())
        company = st.text_input("Company", value=selected_order.get("company", ""))
        operator = st.text_input("Operator", value=selected_order.get("operator", ""))
        seal_type = st.text_input("Seal Type", value=selected_order.get("seal_type", ""))
        profile = st.text_input("Profile", value=selected_order.get("profile", ""))
        seal_count = st.number_input("Seal Count", value=int(selected_order.get("seal_count", 0)))
        production_time = st.number_input("Production Time (min)", value=float(selected_order.get("production_time", 0)))
        downtime = st.number_input("Downtime (min)", value=float(selected_order.get("downtime", 0)))
        downtime_reason = st.text_input("Downtime Reason", value=selected_order.get("downtime_reason", ""))

        submitted = st.form_submit_button("💾 Save Changes")

        if submitted:
            df.at[selected_index, "date"] = pd.to_datetime(date)
            df.at[selected_index, "company"] = company
            df.at[selected_index, "operator"] = operator
            df.at[selected_index, "seal_type"] = seal_type
            df.at[selected_index, "profile"] = profile
            df.at[selected_index, "seal_count"] = seal_count
            df.at[selected_index, "production_time"] = production_time
            df.at[selected_index, "downtime"] = downtime
            df.at[selected_index, "downtime_reason"] = downtime_reason

            st.success(f"✅ Order at index {selected_index} has been updated.")

    # Delete functionality
    st.markdown("---")
    if st.button("🗑 Delete Selected Order"):
        df.drop(index=selected_index, inplace=True)
        df.reset_index(drop=True, inplace=True)
        st.success(f"🗑 Order at index {selected_index} has been deleted.")
        st.experimental_rerun()
