import streamlit as st
import pandas as pd
import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        database=st.secrets["postgres"]["database"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"],
        port=st.secrets["postgres"]["port"]
    )
    return conn

def save_to_db(df):
    conn = get_connection()
    cursor = conn.cursor()
    
    for index, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO orders (date, company, operator, seal_type, profile, seal_count, production_time, downtime, downtime_reason)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (row['date'], row['company'], row['operator'], row['seal_type'], row['profile'],
             row['seal_count'], row['production_time'], row['downtime'], row['downtime_reason'])
        )
    conn.commit()
    conn.close()
    st.success("Data imported successfully!")

def show_import_data():
    st.subheader("📥 Import Data")
    
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])
    
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.write("Preview of Uploaded Data:", df.head())
        
        if st.button("Save Data to Database"):
            save_to_db(df)
