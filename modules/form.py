import streamlit as st

def show_form():
    st.title("📝 Add New Production Order")

    if "orders" not in st.session_state:
        st.session_state.orders = []

    with st.form("order_form"):
        company = st.text_input("Company Name")
        operator = st.text_input("Operator Name")
        seals = st.number_input("Number of Seals", min_value=1)
        time = st.number_input("Production Time (min)", min_value=1)
        submitted = st.form_submit_button("✅ Submit Order")

        if submitted:
            new_order = {
                "Order ID": len(st.session_state.orders) + 1,
                "Company": company,
                "Operator": operator,
                "Seals": seals,
                "Time (min)": time
            }
            st.session_state.orders.append(new_order)
            st.success(f"Order for **{company}** submitted successfully.")
# Placeholder for form.py
