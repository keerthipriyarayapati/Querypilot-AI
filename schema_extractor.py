import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()


def get_database_schema():

    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

    cursor = conn.cursor()

    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public';
    """)

    tables = cursor.fetchall()

    schema = ""

    for table in tables:

        table_name = table[0]

        schema += f"\nTable: {table_name}\n"

        cursor.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = %s;
        """, (table_name,))

        columns = cursor.fetchall()

        for column in columns:
            schema += f"  - {column[0]} ({column[1]})\n"

    cursor.close()
    conn.close()

    return schema