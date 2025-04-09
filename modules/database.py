import pandas as pd
import streamlit as st

def get_orders_df():
    if "orders" not in st.session_state or not st.session_state.orders:
        return pd.DataFrame()

    return pd.DataFrame(st.session_state.orders)
# Placeholder for database.py
