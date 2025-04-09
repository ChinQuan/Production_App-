import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

def show_edit_orders():
    st.title("✏️ Edit Orders")

    # Sprawdź, czy dane są dostępne
    if "orders" not in st.session_state or not st.session_state.orders:
        st.warning("No orders to edit.")
        return

    # Załaduj dane do DataFrame
    df = pd.DataFrame(st.session_state.orders)

    # Konfiguracja edytowalnych kolumn
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=True, filter=True, sortable=True)
    gb.configure_grid_options(domLayout='normal')
    gb.configure_selection(selection_mode="single", use_checkbox=True)

    grid_options = gb.build()

    # Wyświetlenie edytowalnej tabeli
    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        editable=True,
        fit_columns_on_grid_load=True,
        height=400,
        theme="dark",
    )

    updated_df = grid_response["data"]
    selected_rows = grid_response["selected_rows"]

    # Zapis zmian
    if st.button("💾 Save Changes"):
        st.session_state.orders = updated_df.to_dict("records")
        st.success("Changes saved.")

    # Usuwanie wybranego wiersza
    if selected_rows:
        if st.button("🗑 Delete Selected Row"):
            selected_index = df.index[df["id"] == selected_rows[0]["id"]].tolist()[0]
            updated_df = updated_df.drop(index=selected_index).reset_index(drop=True)
            st.session_state.orders = updated_df.to_dict("records")
            st.success("Selected row deleted.")
