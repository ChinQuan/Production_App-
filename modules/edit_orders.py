import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

def show_edit_orders():
    st.title("🧩 Edit Production Orders")

    # Dane testowe – symulacja zamówień
    df = pd.DataFrame({
        "ID": [1, 2, 3],
        "Company": ["Alpha", "Beta", "Gamma"],
        "Operator": ["John", "Anna", "Tom"],
        "Seals": [120, 150, 130],
        "Time (min)": [60, 90, 75],
    })

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

    edited_df = grid_response['data']

    if st.button("💾 Save Changes"):
        st.success("Changes saved (simulated)")
        st.write(edited_df)
# Placeholder for edit_orders.py
