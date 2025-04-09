import streamlit as st
import pandas as pd
from modules.database import insert_order
from datetime import datetime

def show_form():
    st.markdown("<h1 style='color:#1abc9c;'>➕ ADD NEW ORDER</h1>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📋 Fill Form", "📈 Preview"])

    with tab1:
        col1, col2 = st.columns([2, 3])

        with col1:
            st.subheader("📝 Order Details")
            with st.form("order_form"):
                date = st.date_input("📅 Date", value=datetime.today())
                company = st.text_input("🏢 Company")
                operator = st.text_input("👷 Operator")
                seal_type = st.selectbox("🔧 Seal Type", ["Standard Hard", "Standard Soft", "Custom"])
                seal_count = st.number_input("🔢 Seal Count", min_value=0, step=1)
                production_time = st.number_input("⏱️ Production Time (min)", min_value=0, step=1)

                submitted = st.form_submit_button("🚀 Submit Order")
                if submitted:
                    new_order = {
                        "date": date,
                        "company": company,
                        "operator": operator,
                        "seal_type": seal_type,
                        "seal_count": seal_count,
                        "production_time": production_time
                    }
                    try:
                        insert_order(new_order)
                        st.success("✅ Order added successfully!")
                    except Exception as e:
                        st.error(f"❌ Failed to add order:\n{e}")

        with col2:
            st.subheader("🧾 Preview Panel")
            st.info("This section can be used for live preview, validation, or analytics.")

    with tab2:
        st.write("📄 This tab will show a preview of all recent orders (planned).")
