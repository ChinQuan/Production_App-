import streamlit as st
import pandas as pd
from modules.database import get_orders_df, update_order
from datetime import datetime

def show_edit_orders(df):
    st.header("✏️ Edit Orders (Excel-style)")

    if df.empty:
        st.warning("No orders available to edit.")
        return

    st.subheader("📋 Editable Orders Table")

    # Konwersja kolumny 'date' do datetime, jeśli nie jest
    if not pd.api.types.is_datetime64_any_dtype(df['date']):
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
        key="orders_editor"
    )

    st.markdown("---")
    if st.button("💾 Save Changes"):
        changes = edited_df.compare(df)
        if not changes.empty:
            for index in changes.index.levels[0]:
                row = edited_df.loc[index]
                updated_order = {
                    "date": row["date"],
                    "company": row["company"],
                    "operator": row["operator"],
                    "seal_type": row["seal_type"],
                    "seal_count": row["seal_count"],
                    "production_time": row["production_time"],
                }
                try:
                    update_order(int(row["id"]), updated_order)
                    st.success(f"Order ID {int(row['id'])} updated successfully!")
                except Exception as e:
                    st.error(f"❌ Failed to update Order ID {int(row['id'])}:\n{e}")
        else:
            st.info("No changes detected.")
