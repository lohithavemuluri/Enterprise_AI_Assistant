import os
import sqlite3
import streamlit as st
from dotenv import load_dotenv
from google import genai


# =====================================================
# LOAD API KEY
# =====================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


# =====================================================
# DATABASE
# =====================================================

DB_PATH = "enterprise.db"


# =====================================================
# GENERATE REPORT
# =====================================================

def generate_report():

    st.header("📑 AI Report Generator")

    st.write(
        "Generate an intelligent business report "
        "using data from the enterprise database."
    )

    # ---------------------------------------------
    # CONNECT TO DATABASE
    # ---------------------------------------------

    try:

        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()

        # -----------------------------------------
        # GET TABLES
        # -----------------------------------------

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
        """)

        tables = [
            row[0]
            for row in cursor.fetchall()
        ]

        # -----------------------------------------
        # GET BASIC DATABASE INFORMATION
        # -----------------------------------------

        database_info = ""

        for table in tables:

            cursor.execute(
                f'SELECT * FROM "{table}"'
            )

            rows = cursor.fetchall()

            database_info += f"\n\nTABLE: {table}\n"

            database_info += str(rows)

        conn.close()

        # -----------------------------------------
        # GENERATE REPORT BUTTON
        # -----------------------------------------

        if st.button("📄 Generate AI Report"):

            with st.spinner(
                "Generating intelligent report..."
            ):

                prompt = f"""
You are an Enterprise Business Analyst.

Analyze the following enterprise database information
and generate a professional business report.

DATABASE INFORMATION:

{database_info}

The report should contain:

1. Executive Summary
2. Sales Overview
3. Product Performance
4. Employee/Department Insights
5. Key Business Insights
6. Recommendations

Do not invent information.

Use only the data provided above.

Write the report in clear, professional language.
"""

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                # ---------------------------------
                # DISPLAY REPORT
                # ---------------------------------

                st.subheader("📋 Generated Business Report")

                st.write(response.text)

                # ---------------------------------
                # DOWNLOAD REPORT
                # ---------------------------------

                st.download_button(
                    label="⬇️ Download Report",
                    data=response.text,
                    file_name="enterprise_business_report.txt",
                    mime="text/plain"
                )

    except Exception as e:

        st.error(
            "Unable to generate the report."
        )

        with st.expander("Technical Details"):

            st.code(str(e))