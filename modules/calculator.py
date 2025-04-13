import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import psycopg2

# Updated list of valid seal types with production time per unit (minutes)
SEAL_PRODUCTION_TIMES = {
    'Standard Hard': 6,
    'Standard Soft': 5,
    'Custom': 10,
    'Custom Soft': 9,
    'Custom Hard': 11,
    'V-Rings': 4
}

VALID_SEAL_TYPES = list(SEAL_PRODUCTION_TIMES.keys())

def load_average_times_from_db():
    """Fetch average production time per unit from PostgreSQL."""
    avg_times = {}
    try:
        dbname = st.secrets["postgres"].get("dbname", st.secrets["postgres"].get("database"))
        conn = psycopg2.connect(
            host=st.secrets["postgres"]["host"],
            port=st.secrets["postgres"]["port"],
            dbname=dbname,
            user=st.secrets["postgres"]["user"],
            password=st.secrets["postgres"]["password"]
        )
        cursor = conn.cursor()
        query = """
            SELECT company, seal_type,
                   AVG(production_time::float / NULLIF(seal_count, 0)) AS avg_time_per_unit
              FROM orders
             WHERE seal_count > 0 AND production_time IS NOT NULL
             GROUP BY company, seal_type;
        """
        cursor.execute(query)
        for row in cursor.fetchall():
            key = (row[0], row[1])
            avg_times[key] = float(row[2])
        cursor.close()
        conn.close()
    except Exception as e:
        st.warning(f"⚠️ Could not load dynamic production times from DB: {e}")
    return avg_times

def get_company_list_from_db():
    """Fetch distinct company names from the orders table."""
    companies = []
    try:
        dbname = st.secrets["postgres"].get("dbname", st.secrets["postgres"].get("database"))
        conn = psycopg2.connect(
            host=st.secrets["postgres"]["host"],
            port=st.secrets["postgres"]["port"],
            dbname=dbname,
            user=st.secrets["postgres"]["user"],
            password=st.secrets["postgres"]["password"]
        )
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT company FROM orders WHERE company IS NOT NULL ORDER BY company;")
        companies = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
    except Exception as e:
        st.warning(f"⚠️ Could not fetch company list from DB: {e}")
    return companies

def format_duration(duration_hours):
    if duration_hours < 1:
        return f"{int(duration_hours * 60)} min"
    return f"{duration_hours:.2f} h"

def add_work_minutes(start_datetime, work_minutes, seal_type, max_days=365):
    total_minutes = 0
    days_processed = 0
    while work_minutes > 0:
        if days_processed > max_days:
            return None
        weekday = start_datetime.weekday()
        if weekday < 4:
            if seal_type in ['Standard Hard', 'Standard Soft'] and weekday in [0, 1, 2]:
                work_day_minutes = 960
            else:
                work_day_minutes = 510
        elif weekday == 4:
            if seal_type in ['Standard Hard', 'Standard Soft']:
                work_day_minutes = 450
            else:
                work_day_minutes = 0
        else:
            start_datetime += datetime.timedelta(days=1)
            days_processed += 1
            continue
        if work_minutes <= work_day_minutes:
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

    avg_times = load_average_times_from_db()
    company_list = get_company_list_from_db()

    if "orders" not in st.session_state:
        st.session_state.orders = []

    with st.form("add_order_form"):
        input_text = st.text_input("Type company name (at least 2 letters)")
        filtered_companies = [c for c in company_list if input_text.lower() in c.lower()] if input_text else company_list
        if filtered_companies:
            company = st.selectbox("Select company", filtered_companies)
        else:
            company = st.text_input("Enter new company name")

        seal_type = st.selectbox("Seal type", VALID_SEAL_TYPES)
        quantity = st.number_input("Quantity", min_value=1, step=1)
        start_date = st.date_input("Start date", datetime.date.today())
        start_time = st.time_input("Start time", datetime.time(8, 0))
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
        for i, order in enumerate(st.session_state.orders):
            col1, col2 = st.columns([5, 1])
            with col1:
                st.write(f"{i+1}. {order['company']} | {order['seal_type']} | Qty: {order['quantity']} | Start: {order['start_datetime']}")
            with col2:
                if st.button(f"❌", key=f"remove_{i}"):
                    st.session_state.orders.pop(i)
                    st.experimental_rerun()

        if st.button("Clear all orders"):
            st.session_state.orders = []
            st.success("All orders have been cleared.")

        if st.button("Calculate End Dates"):
            results = []
            for order in st.session_state.orders:
                key = (order["company"], order["seal_type"])
                unit_time = avg_times.get(key, SEAL_PRODUCTION_TIMES.get(order["seal_type"], 5))
                total_minutes = int(order["quantity"] * unit_time)
                end_date = add_work_minutes(order["start_datetime"], total_minutes, order["seal_type"])
                duration_hr = total_minutes / 60
                results.append({
                    "Company": order["company"],
                    "Seal Type": order["seal_type"],
                    "Quantity": order["quantity"],
                    "Start": order["start_datetime"],
                    "Estimated End": end_date,
                    "Duration": format_duration(duration_hr)
                })

            df_results = pd.DataFrame(results)
            st.subheader("📅 Estimated Completion Dates")
            st.dataframe(df_results)

            st.subheader("📊 Gantt Chart")
            gantt_df = df_results.copy()
            gantt_df["Start"] = pd.to_datetime(gantt_df["Start"])
            gantt_df["Estimated End"] = pd.to_datetime(gantt_df["Estimated End"])
            fig = px.timeline(gantt_df, x_start="Start", x_end="Estimated End", y="Company", color="Seal Type")
            fig.update_yaxes(autorange="reversed")
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("📈 Summary Statistics")
            st.markdown(f"**Total Orders:** {len(df_results)}")
            st.markdown(f"**Total Quantity:** {df_results['Quantity'].sum()} units")
