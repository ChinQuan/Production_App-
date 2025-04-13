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

    with st.form("production_calc"):
        st.markdown("Enter production time data:")

        start_date = st.date_input("Start date", datetime.date.today())
        start_time = st.time_input("Start time", datetime.time(8, 0))
        seal_type = st.selectbox("Seal type", ['Standard Hard', 'Standard Soft', 'Express'])
        work_minutes = st.number_input("Working time [minutes]", min_value=1, max_value=50000, value=480)

        submitted = st.form_submit_button("Calculate end date")

    if submitted:
        try:
            start_datetime = datetime.datetime.combine(start_date, start_time)
            result = add_work_minutes(start_datetime, int(work_minutes), seal_type)

            if result:
                st.success(f"✅ Estimated end date: **{result.strftime('%Y-%m-%d %H:%M')}**")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
