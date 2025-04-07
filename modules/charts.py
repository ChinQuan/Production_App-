import streamlit as st
import pandas as pd
import plotly.express as px
from modules.database import get_connection  # Importujemy połączenie z pliku database.py

def show_charts():
    st.title("📈 Production Charts")

    conn = get_connection()
    df = pd.read_sql("SELECT * FROM orders", conn)
    conn.close()

    if df.empty:
        st.warning("No data available to generate charts.")
        return

    # Konwersja kolumny 'date' do formatu datetime
    df['date'] = pd.to_datetime(df['date'])

    # Wykres trendu dziennej produkcji
    daily_production = df.groupby('date')['seal_count'].sum().reset_index()
    fig = px.line(daily_production, x='date', y='seal_count', title='Daily Production Trend')
    st.plotly_chart(fig)

    # Wykres produkcji na podstawie operatora
    operator_production = df.groupby('operator')['seal_count'].sum().reset_index()
    fig = px.bar(operator_production, x='operator', y='seal_count', title='Production by Operator')
    st.plotly_chart(fig)

    # Wykres produkcji na podstawie firmy
    company_production = df.groupby('company')['seal_count'].sum().reset_index()
    fig = px.pie(company_production, names='company', values='seal_count', title='Production by Company')
    st.plotly_chart(fig)
