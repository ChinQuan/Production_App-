import streamlit as st
import pandas as pd

def show_form():
    st.title("📝 Add New Production Order")

    with st.form("order_form"):
        company = st.text_input("Company Name")
        operator = st.text_input("Operator Name")
        seals = st.number_input("Number of Seals", min_value=0)
        time = st.number_input("Production Time (min)", min_value=0)
        submitted = st.form_submit_button("✅ Submit Order")

        if submitted:
            st.success(f"Order for **{company}** submitted successfully (Operator: {operator}, Seals: {seals}, Time: {time} min)")
# Placeholder for form.py
