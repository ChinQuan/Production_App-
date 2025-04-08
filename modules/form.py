import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from modules.database import get_connection


def format_time(seconds):
    if seconds < 60:
        return f"{int(seconds)} seconds"
    else:
        minutes = int(seconds // 60)
        remaining_seconds = int(seconds % 60)
        return f"{minutes} minute{'s' if minutes > 1 else ''} {remaining_seconds} seconds"


def calculate_average_time():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM orders", conn)
    conn.close()

    if df.empty:
        st.write("No data available to calculate average production time.")
        return

    df['date'] = pd.to_datetime(df['date'])

    daily_avg = df.groupby('date')['seal_count'].mean().reset_index()

    st.write("### Average Seal Count Per Day")
    st.line_chart(daily_avg)


def show_form():
    st.title("📋 Form Module")

    st.header("⏳ Advanced Production Analysis")
    calculate_average_time()

    st.success("✅ Form module loaded successfully!")
