import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

def show_edit_orders():
    st.title("✏️ Edit Orders")

    if "orders" not in st.session_state or not st.session_state.orders:
        st.warning("No orders to edit.")
        return

    df = pd.DataFrame(st.session_state.orders)

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=True)
    grid_options = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        update_mode='MANUAL',
        editable=True,
        height=300,
    )

    updated_df = grid_response["data"]

    if st.button("💾 Save Changes"):
        st.session_state.orders = updated_df.to_dict("records")
        st.success("Changes saved.")
# Placeholder for edit_orders.py
