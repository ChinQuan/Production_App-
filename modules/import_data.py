import streamlit as st
import pandas as pd
from modules.database import get_connection


def show_import_data():
    st.header("📂 Import Data")
    st.write("Upload your Excel file with the new production data.")

    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

    if uploaded_file is not None:
        try:
            # Read the Excel file
            df = pd.read_excel(uploaded_file, sheet_name=0)

            if 'date' not in df.columns or 'company' not in df.columns or 'operator' not in df.columns or 'seal_type' not in df.columns:
                st.error("The Excel file must contain columns: date, company, operator, seal_type, profile, seal_count, production_time, downtime, downtime_reason")
                return

            conn = get_connection()
            cursor = conn.cursor()

            inserted_rows = 0
            skipped_rows = 0

            for index, row in df.iterrows():
                date = pd.to_datetime(row['date']).date()
                company = row['company'] if pd.notna(row['company']) else "Unknown"  # Zamiana NaN na "Unknown"
                operator = row['operator']
                seal_type = row['seal_type']
                profile = row.get('profile', '')
                seal_count = row.get('seal_count', 0)
                production_time = row.get('production_time', 0)
                downtime = row.get('downtime', 0)
                downtime_reason = row.get('downtime_reason', '')

                # 🔍 Checking for duplicate entries
                cursor.execute(
                    "SELECT COUNT(*) FROM orders WHERE date = %s AND operator = %s AND seal_type = %s AND company = %s",
                    (date, operator, seal_type, company)
                )
                result = cursor.fetchone()

                if result[0] == 0:
                    # Insert new record if no duplicate is found
                    cursor.execute(
                        "INSERT INTO orders (date, company, operator, seal_type, profile, seal_count, production_time, downtime, downtime_reason) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (date, company, operator, seal_type, profile, seal_count, production_time, downtime, downtime_reason)
                    )
                    conn.commit()
                    inserted_rows += 1
                else:
                    # Skip if duplicate is found
                    skipped_rows += 1

            st.success(f"✅ Import completed. Inserted rows: {inserted_rows}, Skipped duplicates: {skipped_rows}")

            cursor.close()
            conn.close()

        except Exception as e:
            st.error(f"❌ Error occurred while uploading the file: {e}")
