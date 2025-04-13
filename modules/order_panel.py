import streamlit as st
import pandas as pd
from datetime import datetime
from modules.database import insert_order, get_orders_df

def show_order_panel():
    st.title("📥 Order Panel")

    st.subheader("➕ Add New Completed Order")

    with st.form("order_panel_form"):
        date = st.date_input("📅 Production Date", value=datetime.today())
        company = st.text_input("🏢 Company Name")
        operator = st.text_input("👷 Operator")
        seal_type = st.selectbox("🧷 Seal Type", [
            "Standard Hard", "Standard Soft", "Custom",
            "Custom Soft", "Custom Hard", "V-Rings"
        ])
        profile = st.text_input("📄 Enter Seal Profile (optional)")
        seal_count = st.number_input("🔢 Ordered Quantity", min_value=1, step=1)

        is_stack = st.checkbox("🧱 This is a stack (one order = multiple items)")
        stack_size = 1
        if is_stack:
            stack_size = st.number_input("🔢 Items per Stack", min_value=1, step=1, value=1)

        production_time = st.number_input("⏱️ Production Time (Minutes)", min_value=0.0, step=1.0)
        notes = st.text_area("📝 Additional Notes (optional)")

        submitted = st.form_submit_button("✅ Submit Order")

        if submitted:
            errors = []
            if not company:
                errors.append("❗ Company name is required.")
            if not operator:
                errors.append("❗ Operator name is required.")
            if seal_count <= 0:
                errors.append("❗ Seal count must be greater than zero.")
            if production_time <= 0:
                st.warning("⚠️ Production time is zero.")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                physical_count = seal_count * stack_size
                new_order = {
                    "date": date,
                    "company": company,
                    "operator": operator,
                    "seal_type": seal_type,
                    "profile": profile,
                    "seal_count": physical_count,
                    "production_time": production_time,
                    "notes": notes
                }

                try:
                    insert_order(new_order)
                    st.success("✅ Order added successfully!")
                except Exception as e:
                    st.error(f"❌ Failed to save order: {e}")

    # ---------------------------
    # 📋 Recently Added Orders
    # ---------------------------
    st.subheader("📋 Recently Added Orders")
    try:
        df = get_orders_df()
        df['date'] = pd.to_datetime(df['date']).dt.date
        if not df.empty:
            df["date"] = pd.to_datetime(df["date"])
            latest_orders = df.sort_values("date", ascending=False).head(10)
            st.dataframe(latest_orders, use_container_width=True)
        else:
            st.info("No orders available.")
    except Exception as e:
        st.error(f"Failed to load recent orders: {e}")
