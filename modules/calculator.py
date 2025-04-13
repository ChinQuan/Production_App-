import streamlit as st
import pandas as pd
import datetime

def add_work_minutes(start_datetime, work_minutes, seal_type, max_days=365):
    """
    Calculates the end date based on working minutes and seal type.
    Takes into account different working day lengths depending on the day of the week and seal type.
    """
    total_minutes = 0
    days_processed = 0

    # Input validation
    if not isinstance(start_datetime, datetime.datetime):
        st.error("❌ Invalid start date. Make sure it's a datetime object.")
        return None
    if not isinstance(work_minutes, int) or work_minutes <= 0:
        st.error("❌ Working minutes must be a positive integer.")
        return None
    if seal_type not in ['Standard Hard', 'Standard Soft', 'Express']:
        st.error("❌ Unknown seal type.")
        return None

    while work_minutes > 0:
        if days_processed > max_days:
            st.error("⚠️ Maximum day limit (365) exceeded. Check your input.")
            return None

        weekday = start_datetime.weekday()  # 0 = Monday

        # Determine working minutes for the given day and seal type
        if weekday < 4:  # Mon - Thu
            if seal_type in ['Standard Hard', 'Standard Soft'] and weekday in [0, 1, 2]:
                work_day_minutes = 960
            else:
                work_day_minutes = 510
        elif weekday == 4:  # Friday
            if seal_type in ['Standard Hard', 'Standard Soft']:
                work_day_minutes = 450
            else:
                work_day_minutes = 0
        else:  # Weekend
            start_datetime += datetime.timedelta(days=1)
            days_processed += 1
            continue

        # Deduct minutes from the current day
        if work_minutes <= work_day_minutes:
            total_minutes += work_minutes
            start_datetime += datetime.timedelta(minutes=work_minutes)
            break
        else:
            work_minutes -= work_day_minutes
            start_datetime += datetime.timedelta(days=1)
            days_processed += 1

    return start_datetime

def show_calculator():
    st.title("🧮 Production Time Calculator")

    st.markdown("Add multiple production orders:")

    if "orders" not in st.session_state:
        st.session_state.orders = []

    with st.form("add_order_form"):
        company = st.text_input("Company name")
        seal_type = st.selectbox("Seal type", ['Standard Hard', 'Standard Soft', 'Express'], key="seal_type")
        quantity = st.number_input("Quantity", min_value=1, step=1, key="quantity")
        start_date = st.date_input("Start date", datetime.date.today(), key="start_date")
        start_time = st.time_input("Start time", datetime.time(8, 0), key="start_time")
        submitted = st.form_submit_button("Add order")

    if submitted:
        start_datetime = datetime.datetime.combine(start_date, start_time)
        st.session_state.orders.append({
            "company": company,
            "seal_type": seal_type,
            "quantity": quantity,
            "start_datetime": start_datetime
        })
        st.success("Order added!")

    if st.session_state.orders:
        st.subheader("📦 Orders")
        df_orders = pd.DataFrame(st.session_state.orders)
        st.dataframe(df_orders)

        if st.button("Calculate End Dates"):
            results = []
            for order in st.session_state.orders:
                total_minutes = order["quantity"] * 5  # example: 5 minutes per unit
                end_date = add_work_minutes(order["start_datetime"], total_minutes, order["seal_type"])
                results.append({
                    "Company": order["company"],
                    "Seal Type": order["seal_type"],
                    "Quantity": order["quantity"],
                    "Start": order["start_datetime"],
                    "Estimated End": end_date
                })
            st.subheader("📅 Estimated Completion Dates")
            st.dataframe(pd.DataFrame(results))
