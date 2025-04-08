
import streamlit as st
import pandas as pd

def show_admin_edit_orders():
    st.title("Admin: Edit Orders")

    # Przykładowe dane – zamień na dane z bazy
    sample_data = pd.DataFrame({
        "Order ID": [1, 2, 3],
        "Product": ["Widget A", "Widget B", "Widget C"],
        "Quantity": [10, 5, 20],
        "Status": ["New", "In Progress", "Completed"]
    })

    edited_data = st.data_editor(sample_data, num_rows="dynamic", use_container_width=True)

    if st.button("Save Changes"):
        # Tutaj można dodać zapis zmian do bazy danych
        st.success("Changes saved (not really, just demo for now).")
