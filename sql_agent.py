import os
import sqlite3

from dotenv import load_dotenv
from google import genai


# Load API key
load_dotenv()

api_key = os.getenv("AIzaSyBfWIq2C6QJm5oQMhmqra9G-gVLPD0Hco8")

client = genai.Client(api_key=api_key)
client = genai.client()

# Database connection
DATABASE = "enterprise.db"


def generate_sql(question):

    prompt = f"""
You are an SQL assistant.

You are working with a SQLite database.

The database has these tables:

employees:
- id
- name
- department
- salary

products:
- id
- product_name
- category
- price

sales:
- id
- product_id
- employee_id
- quantity
- sale_amount
- sale_date

Convert the user's question into ONE SQLite SELECT query.

IMPORTANT:
- Only generate SELECT queries.
- Do not generate INSERT.
- Do not generate UPDATE.
- Do not generate DELETE.
- Do not generate DROP.
- Do not generate ALTER.
- Do not generate CREATE.
- Return ONLY the SQL query.
- Do not use markdown code blocks.

User question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    sql = response.text.strip()

    # Remove markdown if Gemini accidentally adds it
    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    return sql


def is_safe_sql(sql):

    sql_upper = sql.upper().strip()

    # Only SELECT is allowed
    if not sql_upper.startswith("SELECT"):
        return False

    forbidden_words = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "CREATE",
        "REPLACE",
        "TRUNCATE"
    ]

    for word in forbidden_words:

        if word in sql_upper:
            return False

    return True


def execute_sql(sql):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(sql)

    results = cursor.fetchall()

    columns = [
        description[0]
        for description in cursor.description
    ]

    connection.close()

    return columns, results


def answer_question(question):

    # Generate SQL
    sql = generate_sql(question)

    # Security check
    if not is_safe_sql(sql):

        return "I cannot execute this type of database query.", sql

    try:

        columns, results = execute_sql(sql)

        # Convert database result into readable text
        database_result = ""

        for row in results:
            database_result += str(row) + "\n"

        prompt = f"""
You are an Enterprise AI Assistant.

Answer the user's question using the database result.

User question:
{question}

SQL query:
{sql}

Database result:
{database_result}

Give a simple, professional answer.

Do not mention internal technical details unless necessary.
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text, sql

    except Exception as error:

        return f"Database error: {error}", sql
