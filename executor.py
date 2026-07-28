import pandas as pd

from database import engine


def execute_query(sql_query):
    """
    Executes a SQL query on PostgreSQL and
    returns the result as a Pandas DataFrame.
    """

    try:
        result = pd.read_sql(sql_query, engine)
        return result

    except Exception as e:
        print(f"Error executing query: {e}")
        return None